"""Web Search Tool - Handles web searches using Brave Search API.
Provides clean, structured search results for the research agent.

"""

import requests
import time
from typing import List, Dict, Optional 
from src.utils.config import Config

class WebSearchTool:
    """ Tool for performing web searches and retrieving results."""

    def __init__(self):
        """Initialize the web search tool."""
        self.config =Config()
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding':'gzip',
            'X-Subscription-Token':self.config.BRAVE_API_KEY
        }

    def search(self, query : str, max_results: int = None) -> List[Dict]:
        """
        Perform a web search and return structured results.
        
        """