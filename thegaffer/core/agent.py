"""
TheGaffer MCP Agent - Main tactical advisor agent.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp import Server, StdioServerParameters
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    EmbeddedResource,
    EmbeddedResourceReference,
    Image,
    ImageContent,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    LoggingLevel,
    ReadResourceRequest,
    ReadResourceResult,
    Resource,
    Text,
    TextContent,
    Tool,
)

from ..agents.formation_expert import FormationExpert
from ..agents.match_analyzer import MatchAnalyzer
from ..agents.tactical_advisor import TacticalAdvisor
from ..tools.retriever import TacticalRetriever
from ..tools.summarizer import MatchSummarizer
from .config import Config

logger = logging.getLogger(__name__)


class TheGafferAgent:
    """Main MCP agent for soccer tactical advice."""

    def __init__(self, config: Config):
        self.config = config
        self.server = Server("thegaffer")

        # Initialize specialized agents
        self.tactical_advisor = TacticalAdvisor(config)
        self.match_analyzer = MatchAnalyzer(config)
        self.formation_expert = FormationExpert(config)

        # Initialize tools
        self.retriever = TacticalRetriever()
        self.summarizer = MatchSummarizer(config)

        # Register MCP handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register all MCP protocol handlers."""

        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """List available tools."""
            tools = [
                Tool(
                    name="analyze_tactics",
                    description="Analyze soccer tactics and provide advice",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Tactical question or scenario",
                            },
                            "formation": {
                                "type": "string",
                                "description": "Optional formation to analyze (e.g., '4-3-3', '3-5-2')",
                            },
                            "context": {
                                "type": "string",
                                "description": "Additional context about the situation",
                            },
                        },
                        "required": ["query"],
                    },
                ),
                Tool(
                    name="counter_formation",
                    description="Suggest formations and tactics to counter a specific formation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "opponent_formation": {
                                "type": "string",
                                "description": "Opponent's formation (e.g., '4-3-3', '3-5-2')",
                            },
                            "your_strengths": {
                                "type": "string",
                                "description": "Your team's strengths and available players",
                            },
                            "match_context": {
                                "type": "string",
                                "description": "Match context (home/away, importance, etc.)",
                            },
                        },
                        "required": ["opponent_formation"],
                    },
                ),
                Tool(
                    name="analyze_match",
                    description="Analyze a specific match and provide tactical insights",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "match_data": {
                                "type": "string",
                                "description": "Match data or description to analyze",
                            },
                            "teams": {
                                "type": "string",
                                "description": "Teams involved in the match",
                            },
                            "focus_areas": {
                                "type": "string",
                                "description": "Specific areas to focus analysis on",
                            },
                        },
                        "required": ["match_data"],
                    },
                ),
                Tool(
                    name="get_tactical_knowledge",
                    description="Retrieve tactical knowledge and historical data",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Tactical topic to search for",
                            },
                            "era": {
                                "type": "string",
                                "description": "Era or time period to focus on",
                            },
                            "coach": {
                                "type": "string",
                                "description": "Specific coach or team to focus on",
                            },
                        },
                        "required": ["topic"],
                    },
                ),
            ]
            return ListToolsResult(tools=tools)

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls and route to appropriate agents."""
            try:
                if name == "analyze_tactics":
                    result = await self.tactical_advisor.analyze(
                        query=arguments["query"],
                        formation=arguments.get("formation"),
                        context=arguments.get("context", ""),
                    )
                    return CallToolResult(content=[TextContent(type="text", text=result)])

                elif name == "counter_formation":
                    result = await self.formation_expert.suggest_counter(
                        opponent_formation=arguments["opponent_formation"],
                        your_strengths=arguments.get("your_strengths", ""),
                        match_context=arguments.get("match_context", ""),
                    )
                    return CallToolResult(content=[TextContent(type="text", text=result)])

                elif name == "analyze_match":
                    result = await self.match_analyzer.analyze_match(
                        match_data=arguments["match_data"],
                        teams=arguments.get("teams", ""),
                        focus_areas=arguments.get("focus_areas", ""),
                    )
                    return CallToolResult(content=[TextContent(type="text", text=result)])

                elif name == "get_tactical_knowledge":
                    result = await self.retriever.retrieve(
                        topic=arguments["topic"],
                        era=arguments.get("era"),
                        coach=arguments.get("coach"),
                    )
                    return CallToolResult(content=[TextContent(type="text", text=result)])

                else:
                    raise ValueError(f"Unknown tool: {name}")

            except Exception as e:
                logger.error(f"Error in tool call {name}: {e}")
                return CallToolResult(content=[TextContent(type="text", text=f"Error: {str(e)}")])

    async def run(self):
        """Run the MCP server."""
        params = StdioServerParameters()
        async with self.server.run_stdio(params) as stream:
            await stream.run()

    async def run_http(self):
        """Run the MCP server over HTTP."""
        import uvicorn
        from fastapi import FastAPI

        app = FastAPI(title="TheGaffer MCP", version=self.config.mcp.version)

        # Add MCP endpoints
        @app.post("/mcp/tools")
        async def list_tools():
            result = await self.server.list_tools()()
            return result

        @app.post("/mcp/call")
        async def call_tool(name: str, arguments: Dict[str, Any]):
            result = await self.server.call_tool()(name, arguments)
            return result

        uvicorn.run(
            app,
            host=self.config.mcp.host,
            port=self.config.mcp.port,
            log_level=self.config.log_level.lower(),
        )
