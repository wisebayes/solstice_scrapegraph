# Solstice ScrapeGraph

A comprehensive web scraping and AI-powered data extraction library that combines the power of large language models with advanced web scraping capabilities.

## Features

🚀 **AI-Powered Extraction**: Leverage OpenAI, Mistral, and other LLMs for intelligent data extraction  
🌐 **Multi-format Support**: Handle HTML, JSON, XML, CSV, and PDF documents  
🎯 **Smart Scraping**: Intelligent content parsing and structure recognition  
📷 **Visual Intelligence**: Image-to-text conversion and screenshot analysis  
🔄 **Multi-graph Architecture**: Support for complex data processing workflows  
⚡ **Async Support**: High-performance concurrent processing  
🛡️ **Robot-friendly**: Respects robots.txt and rate limiting  

## Installation

```bash
pip install solstice-scrapegraph
```

### Development Installation

```bash
git clone https://github.com/yourusername/solstice_scrapegraph.git
cd solstice_scrapegraph
pip install -e .[dev]
```

## Quick Start

```python
from scrapegraphai.graphs import SmartScraperGraph

# Configure your LLM
llm_config = {
    "llm_model": "gpt-3.5-turbo",
    "api_key": "your_openai_api_key"
}

# Create a scraper instance
scraper = SmartScraperGraph(
    prompt="Extract all product names and prices",
    source="https://example-ecommerce.com",
    config=llm_config
)

# Run the scraper
result = scraper.run()
print(result)
```

## Available Graphs

- **SmartScraperGraph**: Basic AI-powered web scraping
- **JSONScraperGraph**: Specialized for JSON data extraction
- **XMLScraperGraph**: XML document processing
- **CSVScraperGraph**: CSV file analysis
- **DocumentScraperGraph**: PDF and document processing
- **OmniScraperGraph**: Multi-modal scraping with image analysis
- **SearchGraph**: Web search and result extraction
- **CodeGeneratorGraph**: Generate scraping code automatically

## Supported LLM Providers

- OpenAI (GPT-3.5, GPT-4)
- Mistral AI
- AWS Bedrock
- Ollama (local models)
- Azure OpenAI

## Key Components

### Nodes
- **FetchNode**: Web page retrieval and loading
- **ParseNode**: HTML/content parsing and cleaning
- **GenerateAnswerNode**: LLM-powered data extraction
- **ImageToTextNode**: Visual content analysis
- **MergeAnswersNode**: Result consolidation

### Utilities
- **Output Parsers**: Structured data extraction
- **Screenshot Tools**: Visual page capture
- **Token Management**: Cost optimization
- **HTML Cleanup**: Content sanitization

## Examples

### Extract Structured Data

```python
from scrapegraphai.graphs import SmartScraperGraph
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    rating: float

scraper = SmartScraperGraph(
    prompt="Extract product information",
    source="https://shop.example.com",
    config={
        "llm_model": "gpt-4",
        "api_key": "your_key",
        "schema": Product
    }
)

products = scraper.run()
```

### Multi-page Scraping

```python
from scrapegraphai.graphs import SmartScraperMultiGraph

urls = [
    "https://news.example.com/page1",
    "https://news.example.com/page2",
    "https://news.example.com/page3"
]

scraper = SmartScraperMultiGraph(
    prompt="Extract article titles and summaries",
    source=urls,
    config=llm_config
)

results = scraper.run()
```

### Document Processing

```python
from scrapegraphai.graphs import DocumentScraperGraph

scraper = DocumentScraperGraph(
    prompt="Extract key financial metrics",
    source="path/to/financial_report.pdf",
    config=llm_config
)

metrics = scraper.run()
```

## Configuration

### Basic Configuration

```python
config = {
    "llm_model": "gpt-3.5-turbo",
    "api_key": "your_openai_api_key",
    "verbose": True,
    "headless": True,
    "max_results": 10
}
```

### Advanced Configuration

```python
config = {
    "llm_model": "gpt-4",
    "api_key": "your_key",
    "temperature": 0.1,
    "max_tokens": 2000,
    "rate_limiter": {
        "requests_per_second": 1,
        "burst_size": 5
    },
    "browser_config": {
        "headless": True,
        "timeout": 30000,
        "user_agent": "custom_agent"
    }
}
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/solstice_scrapegraph.git
cd solstice_scrapegraph

# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Format code
black .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: contact@solstice.dev
- 💬 Issues: [GitHub Issues](https://github.com/yourusername/solstice_scrapegraph/issues)
- 📖 Documentation: [Coming Soon]

## Acknowledgments

Built with ❤️ by the Solstice Team, powered by:
- [LangChain](https://langchain.com/) for LLM integration
- [Playwright](https://playwright.dev/) for browser automation
- [Pydantic](https://pydantic.dev/) for data validation 