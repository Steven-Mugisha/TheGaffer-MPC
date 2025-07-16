# TheGaffer - Soccer Tactical Chat MCP

Like a coach on the bench giving live tactical advice with AI

## Overview

TheGaffer is a sophisticated MCP (Model Context Protocol) agent that provides expert soccer tactical advice and analysis. It acts as your personal tactical advisor, helping you understand formations, counter-strategies, match analysis, and tactical concepts.

## Features

### 🏟️ Tactical Analysis

- **Formation Analysis**: Deep insights into various formations (4-3-3, 3-5-2, 4-4-2, etc.)
- **Counter-Formations**: Expert advice on how to counter specific formations
- **High Press Strategies**: How to beat high-pressing teams
- **Tactical Concepts**: Understanding pressing, possession, counter-attacking, etc.

### 📊 Match Analysis

- **Match Summaries**: Comprehensive analysis of specific matches
- **Tactical Insights**: Extract key tactical lessons from games
- **Performance Analysis**: Player roles and tactical execution
- **Historical Context**: Tactical evolution and trends

### 🧠 Knowledge Base

- **Tactical Knowledge**: Historical data and tactical principles
- **Coach Profiles**: Analysis of famous coaches and their styles
- **Era Analysis**: Tactical approaches from different periods
- **Training Recommendations**: Practical training guidance

## Quick Start

### Prerequisites

- Python 3.11+
- `uv` package manager (recommended)
- OpenAI API key or Anthropic API key

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd TheGaffer-MPC
   ```

2. **Install dependencies with uv**:

   ```bash
   export PATH="$HOME/.local/bin:$PATH"  # Add uv to PATH
   uv sync
   ```

3. **Set up environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the agent**:
   ```bash
   uv run python main.py
   ```

## Configuration

Create a `.env` file with your configuration:

```env
# LLM Configuration
LLM_PROVIDER=openai  # or anthropic
LLM_API_KEY=your_api_key_here
LLM_MODEL=gpt-4o  # or claude-3-5-sonnet
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# MCP Configuration
MCP_HOST=localhost
MCP_PORT=8000
MCP_NAME=thegaffer
MCP_VERSION=0.1.0

# Debug Configuration
DEBUG=false
LOG_LEVEL=INFO
```

## Usage Examples

### Basic Tactical Queries

```python
# Ask about formations
"How do I beat a high press with a 4-3-3?"

# Counter-formations
"What formation counters a 3-5-2?"

# Tactical concepts
"Explain the principles of gegenpressing"
```

### Match Analysis

```python
# Analyze a specific match
"Summarize today's Euro match and suggest tactical insights"

# Compare matches
"Compare Liverpool vs Manchester City and Real Madrid vs Barcelona"
```

### Knowledge Retrieval

```python
# Get tactical knowledge
"Tell me about Pep Guardiola's tactical philosophy"

# Historical context
"What were the key tactical innovations of the 1970s?"
```

## Architecture

### Core Components

- **TheGafferAgent**: Main MCP agent that handles requests
- **TacticalAdvisor**: General tactical advice and analysis
- **FormationExpert**: Specialized formation analysis
- **MatchAnalyzer**: Match-specific analysis and insights

### Tools

- **TacticalRetriever**: Retrieves tactical knowledge and historical data
- **MatchSummarizer**: Summarizes matches and extracts insights

### Configuration

- **Config**: Centralized configuration management
- **LLMConfig**: LLM provider configuration
- **MCPConfig**: MCP server configuration

## Development

### Project Structure

```
TheGaffer-MPC/
├── thegaffer/
│   ├── core/
│   │   ├── agent.py          # Main MCP agent
│   │   └── config.py         # Configuration management
│   ├── agents/
│   │   ├── tactical_advisor.py
│   │   ├── formation_expert.py
│   │   └── match_analyzer.py
│   ├── tools/
│   │   ├── retriever.py      # Knowledge retrieval
│   │   └── summarizer.py     # Match summarization
│   ├── data/                 # Tactical data and knowledge base
│   ├── utils/                # Utility functions
│   └── tests/                # Test suite
├── main.py                   # Entry point
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

### Development Setup

1. **Install development dependencies**:

   ```bash
   uv sync --extra dev
   ```

2. **Run tests**:

   ```bash
   uv run pytest
   ```

3. **Format code**:

   ```bash
   uv run black .
   uv run isort .
   ```

4. **Type checking**:
   ```bash
   uv run mypy thegaffer/
   ```

### Adding New Features

1. **New Agents**: Add to `thegaffer/agents/`
2. **New Tools**: Add to `thegaffer/tools/`
3. **Configuration**: Update `thegaffer/core/config.py`
4. **Tests**: Add corresponding tests in `thegaffer/tests/`

## Why Use `uv`?

`uv` is a modern Python package manager that offers several advantages:

### Speed

- **10-100x faster** than pip for package installation
- **Parallel downloads** and optimized dependency resolution
- **Caching** for faster subsequent installations

### Reliability

- **Better dependency resolution** with fewer conflicts
- **Lockfile support** for reproducible builds
- **Virtual environment management** built-in

### Modern Features

- **Built with Rust** for performance and reliability
- **Compatible** with existing Python workflows
- **Active development** with regular updates

### Commands

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Run commands in virtual environment
uv run python main.py
uv run pytest
uv run black .

# Create new project
uv init --python 3.11
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Inspired by the tactical genius of coaches like Pep Guardiola, Jurgen Klopp, and Carlo Ancelotti
- Built with modern Python tooling and best practices
- Powered by state-of-the-art language models

---

**TheGaffer** - Your AI tactical advisor on the bench! ⚽️
