"""
Configuration management for the Smart Research Agent.
Handles environment variables and application settings.
"""

import os 
from typing import Optional
from dotenv import load_dotenv


# load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class."""

    # API Configuration
    GROQ_API_KEY: str = os.getenv('GROQ_API_KEY','')
    GROQ_MODEL: str = os.getenv('GROQ_MODEL', 'llama3-8b-8192')

    # Search Configuration
    SEARCH_API_KEY: str = os.getenv('SEARCH_API_KEY','')
    MAX_SEARCH_RESULTS: int = int(os.getenv('MAX_SEARCH_RESULTS','5'))
    
    BRAVE_API_KEY: str = os.getenv("BRAVE_API_KEY","")
    BRAVE_SEARCH_ENDPOINT: str = "https://api.search.brave.com/res/v1/web/search"


    # Agent Configuration
    REPORT_OUTPUT_DIR: str = os.getenv('REPORT_OUTPUT_DIR','./reports')
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS",'1000'))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", '0.7'))

    @classmethod
    def validate(cls) -> bool:
        """Validate theat required configuration is present."""
        if not cls.GROQ_API_KEY:
            print("Error: GROQ_API_KEY not found in environment")
            print(" Make sure to check your API key to the .env file")
            return False
        
        if not cls.GROQ_API_KEY.startswith('gsk_'):
            print("Error: Invalid GROQ_API_KEY format")
            print("Your API key should start with 'gsk_'")
            return False
        
        if not cls.BRAVE_API_KEY:
            print("Error: BRAVE_API_KEY not found in environment")
            print(" Make sure you've added your Brave Search API key to the .env file")

            return False
        return True
    
        
        
    
    @classmethod
    def display_config(cls):
        """Display current configuration (safely)."""
        print("Current Configuration: ")
        print(f" Model: {cls.GROQ_MODEL}")
        print(f" Max Tokens: {cls.MAX_TOKENS}")
        print(f" Temperature: {cls.TEMPERATURE}")
        print(f" Output Directory : {cls.REPORT_OUTPUT_DIR}")
        print(f" API Key: {'Set' if cls.GROQ_API_KEY else  'Missing'}")