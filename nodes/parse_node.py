"""
ParseNode Module
"""

import re
from typing import List, Optional, Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from langchain_community.document_transformers import Html2TextTransformer
from langchain_core.documents import Document

from ..helpers import default_filters
from ..utils.split_text_into_chunks import split_text_into_chunks
from .base_node import BaseNode


class ParseNode(BaseNode):
    """
    A node responsible for parsing HTML content from a document.
    The parsed content is split into chunks for further processing.

    This node enhances the scraping workflow by allowing for targeted extraction of
    content, thereby optimizing the processing of large HTML documents.

    Attributes:
        verbose (bool): A flag indicating whether to show print statements during execution.

    Args:
        input (str): Boolean expression defining the input keys needed from the state.
        output (List[str]): List of output keys to be updated in the state.
        node_config (dict): Additional configuration for the node.
        node_name (str): The unique identifier name for the node, defaulting to "Parse".
    """

    url_pattern = re.compile(
        r"[http[s]?:\/\/]?(www\.)?([-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)"
    )
    relative_url_pattern = re.compile(r"[\(](/[^\(\)\s]*)")

    def __init__(
        self,
        input: str,
        output: List[str],
        node_config: Optional[dict] = None,
        node_name: str = "ParseNode",
    ):
        super().__init__(node_name, "node", input, output, 1, node_config)

        self.verbose = (
            False if node_config is None else node_config.get("verbose", False)
        )
        self.parse_html = (
            True if node_config is None else node_config.get("parse_html", True)
        )
        self.parse_urls = (
            False if node_config is None else node_config.get("parse_urls", False)
        )

        self.llm_model = node_config.get("llm_model")
        self.chunk_size = node_config.get("chunk_size")

    def execute(self, state: dict) -> dict:
        """
        Executes the node's logic to parse the HTML document content and split it into chunks.

        Args:
            state (dict): The current state of the graph. The input keys will be used to fetch the
                            correct data from the state.

        Returns:
            dict: The updated state with the output key containing the parsed content chunks.

        Raises:
            KeyError: If the input keys are not found in the state, indicating that the
                        necessary information for parsing the content is missing.
        """

        self.logger.info(f"--- Executing {self.node_name} Node ---")

        input_keys = self.get_input_keys(state)
        input_data = [state[key] for key in input_keys]
        docs_transformed = input_data[0]
        source = input_data[1] if self.parse_urls else None

        if self.parse_html:
            # ----------------------------------------
            # 1.  Run URL extraction on *raw HTML* to keep <img> tags intact.
            #     html2text can strip/remove image elements, which prevents us
            #     from ever seeing those URLs later.  Using the untouched HTML
            #     guarantees every <img>/<a> reference is available.
            # ----------------------------------------
            raw_docs = input_data[0]
            # Handle both single-Document and list-of-Document cases
            if isinstance(raw_docs, list):
                raw_html = "\n".join(doc.page_content for doc in raw_docs)
            else:
                raw_html = raw_docs.page_content

            link_urls, img_urls = self._extract_urls(raw_html, source)

            # ----------------------------------------
            # 2.  Convert HTML → markdown/plain-text for chunking so that the
            #     LLM gets cleaner text, *after* we've harvested URLs.
            # ----------------------------------------
            docs_transformed = Html2TextTransformer(ignore_links=False).transform_documents(raw_docs)
            if isinstance(docs_transformed, list):
                docs_transformed = docs_transformed[0]

            chunks = split_text_into_chunks(
                text=docs_transformed.page_content,
                chunk_size=self.chunk_size - 250,
            )
        else:
            docs_transformed = docs_transformed[0]

            try:
                link_urls, img_urls = self._extract_urls(
                    docs_transformed.page_content, source
                )
            except Exception:
                link_urls, img_urls = "", ""

            chunk_size = self.chunk_size
            chunk_size = min(chunk_size - 500, int(chunk_size * 0.8))

            if isinstance(docs_transformed, Document):
                chunks = split_text_into_chunks(
                    text=docs_transformed.page_content,
                    chunk_size=chunk_size,
                )
            else:
                chunks = split_text_into_chunks(
                    text=docs_transformed, chunk_size=chunk_size
                )

        state.update({self.output[0]: chunks})
        state.update({"parsed_doc": chunks})
        state.update({"content": chunks})

        if self.parse_urls:
            state.update({self.output[1]: link_urls})
            state.update({self.output[2]: img_urls})

        return state

    def _extract_urls(self, text: str, source: str) -> Tuple[List[str], List[str]]:
        """Return (links, images) detected in *text*.

        The strategy is:
        1.  Parse the string as HTML with BeautifulSoup – this reliably finds
            <a>, <img>, <source>, etc. and their *href* / *src* / *data-src*.
        2.  Run a regex pass to catch any http(s) links that are present in
            markdown or plain text.
        3.  Run a regex pass for the markdown relative-link syntax `](path)` so
            we don't miss images that were converted to markdown by html2text.
        4.  Normalise every URL – convert relative paths to absolute using the
            original *source* page, strip whitespace, drop empty and hash-only
            anchors, and split off query-strings when checking the extension.
        """

        if not self.parse_urls:
            return [], []

        image_exts = default_filters.filter_dict["img_exts"]

        links: set[str] = set()
        images: set[str] = set()

        def _categorise(url: str):
            url = url.strip()
            if not url or url in {"#", "/"}:
                return

            # Make absolute if needed
            if not urlparse(url).scheme:
                url_abs = urljoin(source, url)
            else:
                url_abs = url

            # Decide image vs link
            url_no_query = url_abs.split("?", 1)[0].split("#", 1)[0]
            if any(url_no_query.lower().endswith(ext) for ext in image_exts):
                images.add(url_abs)
            else:
                links.add(url_abs)

        # 1. BeautifulSoup on HTML content (may gracefully handle plain text)
        try:
            soup = BeautifulSoup(text, "html.parser")

            # <a href>
            for a in soup.find_all("a", href=True):
                _categorise(a["href"])

            # <img src> + common lazy-loading attributes
            for tag in soup.find_all(["img", "source"]):
                for attr in ("src", "data-src", "data-srcset", "srcset"):
                    if tag.has_attr(attr):
                        raw = tag[attr]
                        # srcset can hold multiple URLs
                        parts = [p.split()[0] for p in raw.split(",")] if attr.endswith("set") else [raw]
                        for part in parts:
                            _categorise(part)
        except Exception as e:
            if self.verbose:
                self.logger.warning(f"BeautifulSoup parsing failed in _extract_urls: {e}")

        # 2. Regex pass for absolute http(s) URLs in markdown/plain-text
        abs_url_re = re.compile(r"https?://[^\s)\"'<>]+", re.I)
        for match in abs_url_re.findall(text):
            _categorise(match)

        # 3. Regex pass for markdown relative links/images: ![alt](path) or [txt](path)
        md_rel_re = re.compile(r"\]\(([^)]+)\)")
        for match in md_rel_re.findall(text):
            # Ignore titles inside the same parens – take only the first token
            _categorise(match.split()[0])

        # Remove duplicates and ensure deterministic order for reproducibility
        final_links = sorted(links - images)
        final_images = sorted(images)

        if self.verbose:
            self.logger.info(
                f"Extracted {len(final_links)} links and {len(final_images)} images from page"
            )

        return final_links, final_images

    def _clean_urls(self, urls: List[str]) -> List[str]:
        """
        Cleans the URLs extracted from the text.

        Args:
            urls (List[str]): The list of URLs to clean.

        Returns:
            List[str]: The cleaned URLs.
        """
        cleaned_urls = []
        for url in urls:
            if not ParseNode._is_valid_url(url):
                url = re.sub(r".*?\]\(", "", url)
                url = re.sub(r".*?\[\(", "", url)
                url = re.sub(r".*?\[\)", "", url)
                url = re.sub(r".*?\]\)", "", url)
                url = re.sub(r".*?\)\[", "", url)
                url = re.sub(r".*?\)\[", "", url)
                url = re.sub(r".*?\(\]", "", url)
                url = re.sub(r".*?\)\]", "", url)
            url = url.rstrip(").-")
            if len(url) > 0:
                cleaned_urls.append(url)

        return cleaned_urls

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """
        CHecks if the URL format is valid.

        Args:
            url (str): The URL to check.

        Returns:
            bool: True if the URL format is valid, False otherwise
        """
        if re.fullmatch(ParseNode.url_pattern, url) is not None:
            return True
        return False
