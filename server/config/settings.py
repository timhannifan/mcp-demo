"""Configuration module using Pydantic BaseSettings."""

from pathlib import Path

from config.logging_config import get_logger
from pydantic import Field
from pydantic_settings import BaseSettings

logger = get_logger(__name__)


class AppConfig(BaseSettings):
    """Application configuration using Pydantic BaseSettings."""

    # MCP Server Configuration
    mcp_host: str = Field(
        default="0.0.0.0", description="Host to bind the MCP server to"
    )  # noqa: S104
    mcp_port: int = Field(default=8765, description="Port for the MCP server")

    # Corpus Configuration
    corpus_dir: str = Field(
        default="data/corpus", description="Directory containing corpus documents"
    )

    # Application Settings
    app_name: str = Field(
        default="scholarlens", description="Name of the MCP application"
    )
    app_instructions: str = Field(
        default="Academic retrieval + text analytics demo",
        description="Application description",
    )

    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string",
    )

    # Health Check Configuration
    health_check_enabled: bool = Field(
        default=True, description="Enable health check endpoint"
    )

    # Text Analysis Settings
    max_answer_words: int = Field(
        default=120, description="Maximum words in synthesized answers"
    )
    max_snippet_words: int = Field(
        default=60, description="Maximum words in source snippets"
    )
    top_sources_count: int = Field(
        default=5, description="Maximum number of sources to return"
    )

    # TF-IDF Vectorizer Settings
    tfidf_max_df: float = Field(
        default=0.9, description="Maximum document frequency for TF-IDF"
    )
    tfidf_min_df: int = Field(
        default=1, description="Minimum document frequency for TF-IDF"
    )
    tfidf_ngram_range: tuple[int, int] = Field(
        default=(1, 2), description="N-gram range for TF-IDF"
    )

    model_config = {
        "case_sensitive": False,
        "extra": "ignore",
        "validate_default": True,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    def get_mcp_config(self) -> dict:
        """Get MCP server configuration."""
        return {
            "host": self.mcp_host,
            "port": self.mcp_port,
            "name": self.app_name,
            "instructions": self.app_instructions,
        }

    def get_corpus_path(self) -> str:
        """Get the full path to the corpus directory."""
        return Path(self.corpus_dir)

    def get_logging_config(self) -> dict:
        """Get logging configuration."""
        return {
            "level": self.log_level,
            "format": self.log_format,
        }


try:
    config = AppConfig()
except Exception as e:
    logger.error("Error loading config: %s", e)
    config = AppConfig.model_validate({})
