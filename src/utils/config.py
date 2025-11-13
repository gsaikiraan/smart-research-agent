"""Configuration management for the research agent."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration loader and validator."""

    def __init__(self):
        """Initialize configuration from environment variables."""
        load_dotenv()

        # AI Provider
        self.ai_provider = os.getenv("AI_PROVIDER", "perplexity")

        # API Keys
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")

        # Models
        self.anthropic_model = os.getenv(
            "ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"
        )
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        self.perplexity_model = os.getenv(
            "PERPLEXITY_MODEL", "llama-3.1-sonar-large-128k-online"
        )

        # Search
        self.search_engine = os.getenv("SEARCH_ENGINE", "duckduckgo")
        self.max_search_results = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
        self.max_sources_to_analyze = int(os.getenv("MAX_SOURCES_TO_ANALYZE", "5"))

        # Storage
        self.database_path = Path(os.getenv("DATABASE_PATH", "data/research.db"))
        self.cache_dir = Path(os.getenv("CACHE_DIR", "data/cache"))
        self.report_output_dir = Path(
            os.getenv("REPORT_OUTPUT_DIR", "data/reports")
        )

        # Vector Store
        self.enable_vector_store = (
            os.getenv("ENABLE_VECTOR_STORE", "false").lower() == "true"
        )
        self.vector_store_type = os.getenv("VECTOR_STORE_TYPE", "chromadb")
        self.vector_store_path = Path(
            os.getenv("VECTOR_STORE_PATH", "data/vector_store")
        )

        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "logs/research_agent.log")

    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate configuration.

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check API key based on provider
        if self.ai_provider == "anthropic" and not self.anthropic_api_key:
            return False, "ANTHROPIC_API_KEY is required when using anthropic provider"

        if self.ai_provider == "openai" and not self.openai_api_key:
            return False, "OPENAI_API_KEY is required when using openai provider"

        if self.ai_provider == "perplexity" and not self.perplexity_api_key:
            return False, "PERPLEXITY_API_KEY is required when using perplexity provider"

        # Create necessary directories
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.report_output_dir.mkdir(parents=True, exist_ok=True)

        if self.enable_vector_store:
            self.vector_store_path.mkdir(parents=True, exist_ok=True)

        return True, None

    def get_api_key(self) -> Optional[str]:
        """Get the API key for the configured provider."""
        if self.ai_provider == "anthropic":
            return self.anthropic_api_key
        elif self.ai_provider == "openai":
            return self.openai_api_key
        elif self.ai_provider == "perplexity":
            return self.perplexity_api_key
        return None

    def get_model(self) -> str:
        """Get the model name for the configured provider."""
        if self.ai_provider == "anthropic":
            return self.anthropic_model
        elif self.ai_provider == "openai":
            return self.openai_model
        elif self.ai_provider == "perplexity":
            return self.perplexity_model
        return ""
