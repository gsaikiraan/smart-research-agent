"""Web search functionality."""

from typing import List, Dict, Any
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup


class WebSearcher:
    """Web search and content extraction."""

    def __init__(self, engine: str = "duckduckgo"):
        """
        Initialize web searcher.

        Args:
            engine: Search engine to use (duckduckgo, serper, serpapi)
        """
        self.engine = engine

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search the web for a query.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of search results with title, url, and snippet
        """
        if self.engine == "duckduckgo":
            return self._search_duckduckgo(query, max_results)
        else:
            raise NotImplementedError(f"Search engine {self.engine} not yet implemented")

    def _search_duckduckgo(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search using DuckDuckGo."""
        try:
            with DDGS() as ddgs:
                results = []
                for result in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", ""),
                    })
                return results
        except Exception as e:
            print(f"Error searching with DuckDuckGo: {e}")
            return []

    def extract_content(self, url: str) -> str:
        """
        Extract main content from a URL.

        Args:
            url: URL to extract content from

        Returns:
            Extracted text content
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = " ".join(chunk for chunk in chunks if chunk)

            return text[:10000]  # Limit to first 10k characters

        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return ""
