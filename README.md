# TheGaffer - Soccer Tactical Chat MCP

An AI-powered soccer tactical advisor providing expert analysis through the Model Context Protocol (MCP).

## 🚀 Quick Start

```bash
git clone <repository-url>
cd TheGaffer-MPC
uv sync
cp env.example .env  # Add your API keys
uv run python main.py
```

## 🏗️ Architecture

- **TheGafferAgent** - Main MCP agent with request routing
- **TacticalAdvisor** - General tactical analysis and advice
- **FormationExpert** - Specialized formation and counter-strategy analysis
- **MatchAnalyzer** - Match-specific insights and tactical breakdowns
- **TacticalRetriever** - Knowledge base and historical data retrieval
- **MatchSummarizer** - Match summarization and insight extraction

## 🎯 Usage Examples

```python
# Tactical analysis
"How do I beat a high press with a 4-3-3?"
"What formation counters a 3-5-2?"

# Match analysis
Summarize today's Euro match and suggest tactical insights"

# Knowledge retrieval
Tellme about Pep Guardiola's tactical philosophy"
```

## ⚙️ Configuration

```env
LLM_PROVIDER=openai  # or anthropic
LLM_API_KEY=your_api_key_here
LLM_MODEL=gpt-4o
MCP_HOST=localhost
MCP_PORT=8000
```

## 🛠️ Development

```bash
uv sync --extra dev
uv run pytest
uv run black .
uv run mypy thegaffer/
```

## 📁 Project Structure

```
TheGaffer-MPC/
├── thegaffer/
│   ├── core/          # Agent & config
│   ├── agents/        # Analysis agents
│   ├── tools/         # Data processing
│   └── tests/         # Test suite
├── main.py            # Entry point
└── pyproject.toml     # Dependencies
```

---

**TheGaffer** - Your AI tactical advisor ⚽️
