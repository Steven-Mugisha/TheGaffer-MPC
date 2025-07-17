"""
Formation Expert Agent - Specializes in formation analysis and counter-formations.
"""

import logging
from typing import Optional

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from ..core.config import Config

logger = logging.getLogger(__name__)


class FormationExpert:
    """Agent specializing in formation analysis and counter-formations."""

    def __init__(self, config: Config):
        self.config = config
        self._setup_llm()

        # Formation knowledge base
        self.formation_characteristics = {
            "4-3-3": {
                "strengths": [
                    "Attacking width",
                    "High press capability",
                    "Midfield control",
                ],
                "weaknesses": [
                    "Vulnerable to counter-attacks",
                    "Can be outnumbered in midfield",
                ],
                "key_positions": ["Wingers", "Holding midfielder", "Full-backs"],
            },
            "3-5-2": {
                "strengths": [
                    "Midfield dominance",
                    "Flexible attacking",
                    "Solid defensive base",
                ],
                "weaknesses": ["Limited width", "Can be exposed on flanks"],
                "key_positions": ["Wing-backs", "Central midfielders", "Strikers"],
            },
            "4-4-2": {
                "strengths": [
                    "Balanced",
                    "Simple to implement",
                    "Good defensive structure",
                ],
                "weaknesses": ["Can be predictable", "Limited creativity in midfield"],
                "key_positions": ["Central midfielders", "Strikers", "Full-backs"],
            },
            "4-2-3-1": {
                "strengths": [
                    "Attacking midfield creativity",
                    "Flexible transitions",
                    "Good defensive cover",
                ],
                "weaknesses": [
                    "Can leave striker isolated",
                    "Requires specific player types",
                ],
                "key_positions": [
                    "Attacking midfielder",
                    "Holding midfielders",
                    "Striker",
                ],
            },
        }

    def _setup_llm(self):
        """Setup LLM client based on configuration."""
        if self.config.llm.provider == "openai":
            self.client = AsyncOpenAI(api_key=self.config.llm.api_key)
        elif self.config.llm.provider == "anthropic":
            self.client = AsyncAnthropic(api_key=self.config.llm.api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.config.llm.provider}")

    async def suggest_counter(self, opponent_formation: str, your_strengths: str = "", match_context: str = "") -> str:
        """Suggest formations and tactics to counter a specific formation."""

        # Get formation characteristics
        formation_info = self.formation_characteristics.get(opponent_formation, {})

        prompt = f"""You are TheGaffer, an expert soccer formation specialist. Provide detailed counter-formation advice.

OPPONENT FORMATION: {opponent_formation}

Formation Characteristics:
- Strengths: {', '.join(formation_info.get('strengths', ['Unknown']))}
- Weaknesses: {', '.join(formation_info.get('weaknesses', ['Unknown']))}
- Key Positions: {', '.join(formation_info.get('key_positions', ['Unknown']))}

YOUR TEAM STRENGTHS: {your_strengths or 'Not specified'}
MATCH CONTEXT: {match_context or 'Not specified'}

Provide a comprehensive counter-strategy including:

1. RECOMMENDED FORMATIONS (ranked by effectiveness):
   - Primary counter-formation with detailed explanation
   - Alternative formations with pros/cons
   - Formation adjustments during the match

2. TACTICAL APPROACH:
   - How to exploit the opponent's weaknesses
   - Key tactical principles to follow
   - Player positioning and movement patterns

3. SPECIFIC STRATEGIES:
   - Attacking approach
   - Defensive organization
   - Transition moments
   - Set-piece strategies

4. PLAYER REQUIREMENTS:
   - Key player types needed
   - Position-specific instructions
   - Substitution strategies

5. MATCH PHASES:
   - Opening 15 minutes approach
   - Mid-game adjustments
   - Closing stages tactics

6. COMMON MISTAKES TO AVOID:
   - Tactical errors when countering this formation
   - Player positioning mistakes
   - Timing issues

Be specific, practical, and include tactical diagrams in your explanation. Consider the match context and your team's strengths."""

        try:
            if self.config.llm.provider == "openai":
                response = await self.client.chat.completions.create(
                    model=self.config.llm.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config.llm.temperature,
                    max_tokens=self.config.llm.max_tokens,
                )
                return response.choices[0].message.content
            elif self.config.llm.provider == "anthropic":
                response = await self.client.messages.create(
                    model=self.config.llm.model,
                    max_tokens=self.config.llm.max_tokens,
                    temperature=self.config.llm.temperature,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.content[0].text
        except Exception as e:
            logger.error(f"Error in formation analysis: {e}")
            return f"Sorry, I encountered an error while analyzing the formation: {str(e)}"

    async def analyze_formation(self, formation: str, context: str = "") -> str:
        """Analyze a specific formation in detail."""

        formation_info = self.formation_characteristics.get(formation, {})

        prompt = f"""You are TheGaffer, an expert soccer formation specialist. Provide detailed analysis of this formation.

FORMATION: {formation}

Formation Characteristics:
- Strengths: {', '.join(formation_info.get('strengths', ['Unknown']))}
- Weaknesses: {', '.join(formation_info.get('weaknesses', ['Unknown']))}
- Key Positions: {', '.join(formation_info.get('key_positions', ['Unknown']))}

CONTEXT: {context or 'General analysis'}

Provide a comprehensive formation analysis including:

1. FORMATION OVERVIEW:
   - Basic structure and philosophy
   - Historical context and evolution
   - Modern interpretations

2. TACTICAL PRINCIPLES:
   - Attacking principles
   - Defensive organization
   - Transition moments
   - Pressing strategies

3. PLAYER REQUIREMENTS:
   - Position-specific requirements
   - Key attributes for each role
   - Player combinations that work well

4. IMPLEMENTATION:
   - Training focus areas
   - Common challenges
   - Adaptation strategies
   - Progression from basic to advanced

5. MATCH SCENARIOS:
   - When to use this formation
   - How to adapt during matches
   - Substitution strategies
   - Set-piece organization

6. COUNTERING THIS FORMATION:
   - How opponents might try to counter
   - Vulnerabilities to be aware of
   - Adjustment strategies

Be specific, practical, and include tactical insights. Use your expertise to provide actionable advice."""

        try:
            if self.config.llm.provider == "openai":
                response = await self.client.chat.completions.create(
                    model=self.config.llm.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config.llm.temperature,
                    max_tokens=self.config.llm.max_tokens,
                )
                return response.choices[0].message.content
            elif self.config.llm.provider == "anthropic":
                response = await self.client.messages.create(
                    model=self.config.llm.model,
                    max_tokens=self.config.llm.max_tokens,
                    temperature=self.config.llm.temperature,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.content[0].text
        except Exception as e:
            logger.error(f"Error in formation analysis: {e}")
            return f"Sorry, I encountered an error while analyzing the formation: {str(e)}"
