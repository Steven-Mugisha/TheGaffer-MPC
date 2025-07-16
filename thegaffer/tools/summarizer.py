"""
Match Summarizer Tool - Summarizes matches and extracts tactical insights.
"""

import logging
from typing import Dict, List, Optional

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from ..core.config import Config

logger = logging.getLogger(__name__)


class MatchSummarizer:
    """Tool for summarizing matches and extracting tactical insights."""

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

    async def summarize_match(
        self, match_data: str, focus_areas: Optional[List[str]] = None
    ) -> str:
        """Summarize a match and extract key tactical insights."""

        focus_text = (
            ", ".join(focus_areas) if focus_areas else "general tactical analysis"
        )

        prompt = f"""You are TheGaffer, an expert soccer analyst. Provide a comprehensive match summary with tactical insights.

MATCH DATA: {match_data}
FOCUS AREAS: {focus_text}

Provide a structured summary including:

1. MATCH SUMMARY:
   - Final score and key statistics
   - Overall flow of the match
   - Key moments and turning points

2. TACTICAL ANALYSIS:
   - Starting formations and adjustments
   - Main tactical battles
   - How each team tried to impose their style

3. KEY INSIGHTS:
   - What worked and what didn't
   - Tactical innovations or interesting approaches
   - Player performances and tactical roles

4. COACHING PERSPECTIVE:
   - Tactical decisions that influenced the outcome
   - What each coach got right/wrong
   - Alternative approaches that could have worked

5. FUTURE IMPLICATIONS:
   - How this match might influence future tactics
   - Tactical trends or patterns to watch
   - Lessons for similar situations

6. SPECIFIC FOCUS (if requested):
   - Detailed analysis of requested aspects
   - Tactical breakdown of specific moments
   - Technical and tactical lessons

Be concise but comprehensive. Focus on actionable tactical insights for coaches and players."""

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
            logger.error(f"Error in match summarization: {e}")
            return (
                f"Sorry, I encountered an error while summarizing the match: {str(e)}"
            )

    async def extract_tactical_insights(self, match_data: str) -> Dict[str, str]:
        """Extract specific tactical insights from match data."""

        prompt = f"""You are TheGaffer, an expert soccer analyst. Extract specific tactical insights from this match data.

MATCH DATA: {match_data}

Extract and categorize the following tactical insights:

1. FORMATION INSIGHTS:
   - How formations influenced the game
   - Tactical adjustments made during the match
   - Formation effectiveness

2. PRESSING INSIGHTS:
   - Pressing intensity and effectiveness
   - Pressing triggers and coordination
   - How teams dealt with pressing

3. TRANSITION INSIGHTS:
   - Counter-attacking effectiveness
   - Transition moments and triggers
   - Defensive transitions

4. SET-PIECE INSIGHTS:
   - Set-piece strategies and execution
   - Defensive set-piece organization
   - Key set-piece moments

5. PLAYER ROLE INSIGHTS:
   - Key tactical roles and execution
   - Position-specific performances
   - Tactical substitutions and their impact

6. COACHING INSIGHTS:
   - Tactical decisions and their impact
   - In-game adjustments
   - Strategic planning and execution

Provide each insight as a concise, actionable statement."""

        try:
            if self.config.llm.provider == "openai":
                response = await self.client.chat.completions.create(
                    model=self.config.llm.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config.llm.temperature,
                    max_tokens=self.config.llm.max_tokens,
                )
                content = response.choices[0].message.content
            elif self.config.llm.provider == "anthropic":
                response = await self.client.messages.create(
                    model=self.config.llm.model,
                    max_tokens=self.config.llm.max_tokens,
                    temperature=self.config.llm.temperature,
                    messages=[{"role": "user", "content": prompt}],
                )
                content = response.content[0].text

            # Parse the response into structured insights
            insights = self._parse_insights(content)
            return insights

        except Exception as e:
            logger.error(f"Error extracting tactical insights: {e}")
            return {"error": f"Failed to extract insights: {str(e)}"}

    def _parse_insights(self, content: str) -> Dict[str, str]:
        """Parse the LLM response into structured insights."""
        insights = {}

        # Simple parsing - in a real implementation, you might use more sophisticated parsing
        sections = content.split("\n\n")

        for section in sections:
            if section.strip():
                lines = section.strip().split("\n")
                if lines:
                    category = lines[0].replace(":", "").strip()
                    if len(lines) > 1:
                        insights[category] = "\n".join(lines[1:]).strip()
                    else:
                        insights[category] = ""

        return insights

    async def compare_matches(self, match1_data: str, match2_data: str) -> str:
        """Compare two matches and identify tactical patterns."""

        prompt = f"""You are TheGaffer, an expert soccer analyst. Compare these two matches and identify tactical patterns and differences.

MATCH 1: {match1_data}
MATCH 2: {match2_data}

Provide a comprehensive comparison including:

1. OVERALL COMPARISON:
   - Similarities and differences in approach
   - Tactical evolution or consistency
   - Performance patterns across matches

2. FORMATION COMPARISON:
   - Formation choices and their effectiveness
   - Tactical flexibility and adaptation
   - Formation-specific patterns

3. TACTICAL PATTERNS:
   - Recurring tactical approaches
   - Successful and unsuccessful patterns
   - Tactical learning and adaptation

4. PLAYER PERFORMANCE COMPARISON:
   - Consistent vs. variable performances
   - Role evolution across matches
   - Tactical role effectiveness

5. COACHING COMPARISON:
   - Tactical decision-making patterns
   - Adaptation and learning curves
   - Strategic consistency vs. flexibility

6. FUTURE IMPLICATIONS:
   - Tactical trends to watch
   - Areas for improvement
   - Strategic recommendations

Be analytical and provide actionable insights for tactical development."""

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
            logger.error(f"Error comparing matches: {e}")
            return (
                f"Sorry, I encountered an error while comparing the matches: {str(e)}"
            )

    async def generate_training_recommendations(self, match_data: str) -> str:
        """Generate training recommendations based on match analysis."""

        prompt = f"""You are TheGaffer, an expert soccer coach. Based on this match analysis, provide specific training recommendations.

MATCH DATA: {match_data}

Provide training recommendations including:

1. TECHNICAL FOCUS:
   - Specific technical skills to improve
   - Drills and exercises to address weaknesses
   - Technical patterns to practice

2. TACTICAL FOCUS:
   - Tactical concepts to reinforce
   - Position-specific training
   - Team tactical patterns to practice

3. PHYSICAL FOCUS:
   - Conditioning requirements
   - Movement patterns to improve
   - Physical demands to address

4. MENTAL FOCUS:
   - Decision-making scenarios
   - Game understanding
   - Mental preparation

5. SPECIFIC DRILLS:
   - Recommended training exercises
   - Progression from basic to advanced
   - Integration of multiple aspects

6. MEASUREMENT:
   - How to measure improvement
   - Key performance indicators
   - Assessment methods

Be specific, practical, and provide actionable training guidance."""

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
            logger.error(f"Error generating training recommendations: {e}")
            return f"Sorry, I encountered an error while generating training recommendations: {str(e)}"
