#!/usr/bin/env python3
"""
TheGaffer MCP - Soccer Tactical Chat Agent
A sophisticated MCP agent that provides tactical advice and analysis for soccer.
"""

import asyncio
import logging
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from thegaffer.core.agent import TheGafferAgent
from thegaffer.core.config import Config

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


async def main():
    try:
        config = Config.from_env()

        agent = TheGafferAgent(config)

        logger.info("Starting TheGaffer MCP agent...")
        logger.info(f"Configuration: {config.mcp.name} v{config.mcp.version}")
        logger.info(f"LLM Provider: {config.llm.provider}")
        logger.info(f"Model: {config.llm.model}")

        await agent.run()

    except KeyboardInterrupt:
        logger.info("Shutting down TheGaffer MCP agent...")
    except Exception as e:
        logger.error(f"Error running TheGaffer MCP agent: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
