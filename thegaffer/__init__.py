"""
TheGaffer - Soccer Tactical Chat MCP

A sophisticated MCP agent that provides tactical advice and analysis for soccer.
"""

__version__ = "0.1.0"
__author__ = "TheGaffer Team"
__email__ = "tactics@thegaffer.com"

from .core.agent import TheGafferAgent
from .core.config import Config

__all__ = ["TheGafferAgent", "Config"]
