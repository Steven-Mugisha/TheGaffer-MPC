"""
Configuration management for TheGaffer MCP agent.
"""

import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class LLMConfig(BaseModel):
    """Configuration for LLM providers."""

    provider: str = Field(
        default="openai", description="LLM provider (openai, anthropic)"
    )
    api_key: Optional[str] = Field(
        default=None, description="API key for the LLM provider"
    )
    model: str = Field(
        default="gpt-4o", description="Model to use for tactical analysis"
    )
    temperature: float = Field(default=0.7, description="Temperature for LLM responses")
    max_tokens: int = Field(default=2000, description="Maximum tokens for responses")


class MCPConfig(BaseModel):
    """Configuration for MCP server."""

    host: str = Field(default="localhost", description="MCP server host")
    port: int = Field(default=8000, description="MCP server port")
    name: str = Field(default="thegaffer", description="MCP server name")
    version: str = Field(default="0.1.0", description="MCP server version")


class Config(BaseModel):
    """Main configuration for TheGaffer."""

    llm: LLMConfig = Field(default_factory=LLMConfig)
    mcp: MCPConfig = Field(default_factory=MCPConfig)
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls(
            llm=LLMConfig(
                provider=os.getenv("LLM_PROVIDER", "openai"),
                api_key=os.getenv("LLM_API_KEY"),
                model=os.getenv("LLM_MODEL", "gpt-4o"),
                temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
                max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
            ),
            mcp=MCPConfig(
                host=os.getenv("MCP_HOST", "localhost"),
                port=int(os.getenv("MCP_PORT", "8000")),
                name=os.getenv("MCP_NAME", "thegaffer"),
                version=os.getenv("MCP_VERSION", "0.1.0"),
            ),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
