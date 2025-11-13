# Smart Research Agent

An AI-powered command-line tool that helps you quickly analyze and organize knowledge. The agent accepts a topic as input, automatically searches the internet for relevant information, analyzes and synthesizes the findings, and generates a structured report. All results are stored for future reference, making it a useful tool for research, learning, and knowledge management.

## Features

- 🤖 **AI-Powered Analysis**: Uses Perplexity, Claude, or GPT for intelligent research
- 🔍 **Automated Web Search**: Searches and extracts content from multiple sources
- 📊 **Structured Reports**: Generates comprehensive, well-organized research reports
- 💾 **Data Persistence**: Stores all research sessions, sources, and findings in SQLite
- 🎯 **Flexible Depth Levels**: Choose between quick, standard, or deep research
- 📝 **Multiple Export Formats**: Save reports in Markdown format

## Prerequisites

- Python 3.8 or higher
- API key from one of:
  - [Perplexity](https://www.perplexity.ai/settings/api) (recommended)
  - [Anthropic](https://console.anthropic.com/)
  - [OpenAI](https://platform.openai.com/api-keys)

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/smart-research-agent.git
cd smart-research-agent
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
```

5. **Edit `.env` and add your API key:**
```bash
# For Perplexity (recommended)
AI_PROVIDER=perplexity
PERPLEXITY_API_KEY=your_actual_api_key_here

# OR for Claude
# AI_PROVIDER=anthropic
# ANTHROPIC_API_KEY=your_actual_api_key_here

# OR for OpenAI
# AI_PROVIDER=openai
# OPENAI_API_KEY=your_actual_api_key_here
```

6. **Run setup check:**
```bash
python main.py setup
```

## Usage

### Basic Research

Research a topic with default settings:
```bash
python main.py research "artificial intelligence in healthcare"
```

### Custom Research Depth

Choose research depth (quick, standard, deep):
```bash
python main.py research "climate change solutions" --depth deep
```

### Specify Maximum Sources

Control the number of sources to analyze:
```bash
python main.py research "quantum computing" --max-sources 10
```

### Custom Output Location

Save report to a specific location:
```bash
python main.py research "blockchain technology" --output ./my-reports/blockchain.md
```

### List Previous Reports

View your research history:
```bash
python main.py list-reports --limit 20
```

### Quick Web Search

Perform a quick web search without full analysis:
```bash
python main.py search "latest AI developments"
```

## Project Structure

```
smart-research-agent/
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── src/
│   ├── agent/            # Research agent logic
│   │   ├── research_agent.py
│   │   └── llm_client.py
│   ├── search/           # Web search modules
│   │   └── web_search.py
│   ├── storage/          # Database and storage
│   │   └── database.py
│   └── utils/            # Utilities
│       └── config.py
├── data/
│   ├── reports/          # Generated reports
│   ├── cache/            # Cached data
│   └── research.db       # SQLite database
└── tests/                # Test suite
```

## How It Works

1. **Research Questions**: The agent generates focused research questions based on your topic
2. **Web Search**: Searches multiple sources using your configured search engine
3. **Content Extraction**: Extracts and cleans content from relevant web pages
4. **AI Analysis**: Uses AI to analyze sources and extract key findings
5. **Report Generation**: Synthesizes findings into a comprehensive, structured report
6. **Storage**: Saves all data to SQLite for future reference

## Configuration

All configuration is done via the `.env` file. Key options:

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_PROVIDER` | AI provider (perplexity/anthropic/openai) | perplexity |
| `SEARCH_ENGINE` | Search engine (duckduckgo/serper/serpapi) | duckduckgo |
| `MAX_SEARCH_RESULTS` | Maximum search results per query | 10 |
| `MAX_SOURCES_TO_ANALYZE` | Maximum sources to analyze | 5 |
| `REPORT_OUTPUT_DIR` | Directory for reports | data/reports |

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/ tests/
```

### Linting

```bash
pylint src/
```

## Troubleshooting

**Issue**: "API key not found" error
- **Solution**: Make sure you've copied `.env.example` to `.env` and added your API key

**Issue**: "No search results found"
- **Solution**: Try a more specific search query or check your internet connection

**Issue**: Import errors
- **Solution**: Make sure you've activated your virtual environment and installed all dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for any purpose.

## Acknowledgments

- Built with [Perplexity AI](https://www.perplexity.ai/)
- Powered by [LangChain](https://www.langchain.com/)
- Search via [DuckDuckGo](https://duckduckgo.com/)
