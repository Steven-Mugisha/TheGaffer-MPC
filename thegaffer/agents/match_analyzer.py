"""
Match Analyzer Agent - Specializes in analyzing specific matches and providing tactical insights.
"""

import logging
from typing import Optional

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from ..core.config import Config

logger = logging.getLogger(__name__)


class MatchAnalyzer:
    """Agent specializing in match analysis and tactical insights."""

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

    async def analyze_match(self, match_data: str, teams: str = "", focus_areas: str = "") -> str:
        """Analyze a specific match and provide tactical insights."""

        prompt = f"""You are TheGaffer, an expert soccer match analyst with decades of experience. Provide comprehensive tactical analysis of this match.

MATCH DATA: {match_data}
TEAMS: {teams or 'Not specified'}
FOCUS AREAS: {focus_areas or 'General analysis'}

Provide a detailed match analysis including:

1. MATCH OVERVIEW:
   - Key moments and turning points
   - Scoreline and performance summary
   - Overall tactical approach of both teams

2. FORMATION ANALYSIS:
   - Starting formations and adjustments
   - How formations influenced the game
   - Tactical changes during the match

3. KEY TACTICAL BATTLE:
   - Main tactical contest (e.g., midfield battle, wide play)
   - How each team tried to impose their style
   - Tactical advantages and disadvantages

4. PLAYER PERFORMANCE:
   - Standout individual performances
   - Key tactical roles and execution
   - Substitutions and their impact

5. TACTICAL INSIGHTS:
   - What worked and what didn't
   - Tactical innovations or interesting approaches
   - Lessons for future matches

6. COACHING PERSPECTIVE:
   - What each coach got right/wrong
   - Tactical decisions that influenced the outcome
   - Alternative approaches that could have worked

7. FUTURE IMPLICATIONS:
   - How this match might influence future tactics
   - Tactical trends or patterns to watch
   - Recommendations for similar situations

8. SPECIFIC FOCUS AREAS (if requested):
   - Detailed analysis of requested aspects
   - Tactical breakdown of specific moments
   - Technical and tactical lessons

Be specific, analytical, and include tactical diagrams where relevant. Use your expertise to provide actionable insights for coaches and players."""

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
            logger.error(f"Error in match analysis: {e}")
            return f"Sorry, I encountered an error while analyzing the match: {str(e)}"

    async def analyze_period(self, period_data: str, context: str = "") -> str:
        """Analyze a specific period of a match (first half, second half, extra time)."""

        prompt = f"""You are TheGaffer, an expert soccer analyst. Provide detailed analysis of this specific match period.

PERIOD DATA: {period_data}
CONTEXT: {context or 'General period analysis'}

Provide a comprehensive period analysis including:

1. PERIOD OVERVIEW:
   - Key events and momentum shifts
   - Tactical approach during this period
   - Performance comparison between teams

2. TACTICAL ADJUSTMENTS:
   - Changes made during this period
   - How teams adapted to the situation
   - Tactical responses to key events

3. KEY MOMENTS:
   - Critical tactical decisions
   - Turning points and their causes
   - Tactical execution of key plays

4. PLAYER ROLES:
   - How player roles evolved during this period
   - Tactical responsibilities and execution
   - Individual contributions to team tactics

5. TACTICAL LESSONS:
   - What worked and what didn't
   - Tactical principles demonstrated
   - Coaching insights from this period

6. FUTURE APPLICATIONS:
   - How to apply these lessons
   - Tactical patterns to replicate or avoid
   - Training focus areas based on this period

Be specific, analytical, and provide actionable tactical insights."""

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
            logger.error(f"Error in period analysis: {e}")
            return f"Sorry, I encountered an error while analyzing the period: {str(e)}"

    async def compare_matches(self, match1_data: str, match2_data: str, comparison_focus: str = "") -> str:
        """Compare two matches and identify tactical patterns and differences."""

        prompt = f"""You are TheGaffer, an expert soccer analyst. Compare these two matches and identify tactical patterns and insights.

MATCH 1: {match1_data}
MATCH 2: {match2_data}
COMPARISON FOCUS: {comparison_focus or 'General comparison'}

Provide a comprehensive comparison including:

1. OVERALL COMPARISON:
   - Similarities and differences in approach
   - Tactical evolution or consistency
   - Performance patterns across matches

2. FORMATION ANALYSIS:
   - Formation choices and their effectiveness
   - Tactical flexibility and adaptation
   - Formation-specific patterns

3. TACTICAL PATTERNS:
   - Recurring tactical approaches
   - Successful and unsuccessful patterns
   - Tactical learning and adaptation

4. PLAYER PERFORMANCE:
   - Consistent vs. variable performances
   - Role evolution across matches
   - Tactical role effectiveness

5. COACHING INSIGHTS:
   - Tactical decision-making patterns
   - Adaptation and learning curves
   - Strategic consistency vs. flexibility

6. FUTURE IMPLICATIONS:
   - Tactical trends to watch
   - Areas for improvement
   - Strategic recommendations

7. SPECIFIC FOCUS (if requested):
   - Detailed comparison of requested aspects
   - Tactical breakdown of specific elements
   - Targeted insights for the focus area

Be analytical, comparative, and provide actionable insights for tactical development."""

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
            logger.error(f"Error in match comparison: {e}")
            return f"Sorry, I encountered an error while comparing the matches: {str(e)}"
