"""
Tactical Advisor Agent - Provides general tactical advice and analysis.
"""

import logging
from typing import Optional

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from ..core.config import Config

logger = logging.getLogger(__name__)


class TacticalAdvisor:
    """Agent for providing tactical advice and analysis."""

    def __init__(self, config: Config):
        self.config = config
        self._setup_llm()

    def _setup_llm(self):
        """Setup LLM client based on configuration."""
        if self.config.llm.provider == "openai":
            self.client = AsyncOpenAI(api_key=self.config.llm.api_key)
        elif self.config.llm.provider == "anthropic":
            self.client = AsyncAnthropic(api_key=self.config.llm.api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.config.llm.provider}")

    async def analyze(
        self, query: str, formation: Optional[str] = None, context: str = ""
    ) -> str:
        """Analyze tactical query and provide advice."""

        # Build the prompt based on the query type
        if "high press" in query.lower():
            prompt = self._build_high_press_prompt(query, formation, context)
        elif "counter" in query.lower() or "beat" in query.lower():
            prompt = self._build_counter_prompt(query, formation, context)
        elif "formation" in query.lower():
            prompt = self._build_formation_prompt(query, formation, context)
        else:
            prompt = self._build_general_prompt(query, formation, context)

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
            logger.error(f"Error in tactical analysis: {e}")
            return f"Sorry, I encountered an error while analyzing your tactical query: {str(e)}"

    def _build_high_press_prompt(
        self, query: str, formation: Optional[str], context: str
    ) -> str:
        """Build prompt for high press analysis."""
        return f"""You are TheGaffer, an expert soccer tactical advisor. Analyze this high press scenario and provide detailed tactical advice.

Query: {query}
Formation: {formation or 'Not specified'}
Context: {context}

Provide a comprehensive analysis including:
1. How to break down the high press
2. Key principles for playing out from the back
3. Player positioning and movement patterns
4. Specific tactical adjustments for the formation
5. Common mistakes to avoid
6. Training drills to practice

Be specific, practical, and include tactical diagrams in your explanation."""

    def _build_counter_prompt(
        self, query: str, formation: Optional[str], context: str
    ) -> str:
        """Build prompt for counter-attacking analysis."""
        return f"""You are TheGaffer, an expert soccer tactical advisor. Analyze this counter-attacking scenario and provide detailed tactical advice.

Query: {query}
Formation: {formation or 'Not specified'}
Context: {context}

Provide a comprehensive analysis including:
1. How to effectively counter the opponent's approach
2. Transition moments and triggers
3. Player roles and responsibilities
4. Formation adjustments if needed
5. Key principles for success
6. Common tactical mistakes to avoid

Be specific, practical, and include tactical insights."""

    def _build_formation_prompt(
        self, query: str, formation: Optional[str], context: str
    ) -> str:
        """Build prompt for formation analysis."""
        return f"""You are TheGaffer, an expert soccer tactical advisor. Analyze this formation scenario and provide detailed tactical advice.

Query: {query}
Formation: {formation or 'Not specified'}
Context: {context}

Provide a comprehensive analysis including:
1. Formation strengths and weaknesses
2. Key tactical principles
3. Player requirements for each position
4. Attacking and defending patterns
5. How to adapt to different opponents
6. Training focus areas

Be specific, practical, and include tactical insights."""

    def _build_general_prompt(
        self, query: str, formation: Optional[str], context: str
    ) -> str:
        """Build prompt for general tactical analysis."""
        return f"""You are TheGaffer, an expert soccer tactical advisor with decades of experience. Provide detailed tactical analysis and advice.

Query: {query}
Formation: {formation or 'Not specified'}
Context: {context}

Provide a comprehensive analysis including:
1. Tactical principles and concepts
2. Practical implementation strategies
3. Player roles and responsibilities
4. Key success factors
5. Common challenges and solutions
6. Training recommendations

Be specific, practical, and include tactical insights. Use your expertise to provide actionable advice."""
