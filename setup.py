#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scrapegraphai",
    version="1.51.0",
    author="Solstice Team",
    author_email="contact@solstice.dev",
    description="A comprehensive web scraping and AI-powered data extraction library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/solstice_scrapegraph",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "langchain-community>=0.0.20",
        "langchain-core>=0.1.0",
        "langchain-openai>=0.0.5",
        "langchain-mistralai>=0.0.1",
        "langchain-aws>=0.1.0",
        "pydantic>=2.0.0",
        "requests>=2.25.0",
        "tqdm>=4.60.0",
        "playwright>=1.30.0",
        "html2text>=2020.1.16",
        "html-to-markdown>=0.1.0",
        "pypdf>=3.0.0",
        "beautifulsoup4>=4.9.0",
        "lxml>=4.6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.910",
            "pre-commit>=2.15.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "myst-parser>=0.15",
        ],
    },
    entry_points={
        "console_scripts": [
            "scrapegraph=scrapegraphai.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 
