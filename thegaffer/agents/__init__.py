"""
TheGaffer Agents Package

Specialized agents for different aspects of tactical analysis.
"""

from .formation_expert import FormationExpert
from .match_analyzer import MatchAnalyzer
from .tactical_advisor import TacticalAdvisor

__all__ = ["TacticalAdvisor", "FormationExpert", "MatchAnalyzer"]
