# Quick Start Guide

Get up and running with Smart Research Agent in 5 minutes!

## Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Configure API Key

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your Perplexity API key
# You can get one from: https://www.perplexity.ai/settings/api
```

Your `.env` should look like:
```
AI_PROVIDER=perplexity
PERPLEXITY_API_KEY=pplx-your-actual-key-here
```

## Step 3: Verify Setup

```bash
python main.py setup
```

You should see green checkmarks if everything is configured correctly.

## Step 4: Run Your First Research

```bash
python main.py research "artificial intelligence trends 2024"
```

The agent will:
- Generate research questions
- Search multiple sources
- Analyze content with AI
- Generate a comprehensive report

Reports are saved to `data/reports/`

## Common Commands

```bash
# Quick research (3 sources)
python main.py research "topic" --depth quick

# Deep research (10+ sources)
python main.py research "topic" --depth deep --max-sources 10

# Quick web search
python main.py search "latest news on AI"

# List previous research
python main.py list-reports

# Get help
python main.py --help
```

## Troubleshooting

**Problem**: ImportError or ModuleNotFoundError
```bash
# Solution: Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Problem**: "PERPLEXITY_API_KEY is required"
```bash
# Solution: Check your .env file exists and has your API key
cat .env
# Should show: PERPLEXITY_API_KEY=pplx-...
```

**Problem**: "No search results found"
```bash
# Solution: Try a more specific query or check internet connection
python main.py search "test query"
```

## Next Steps

- Explore the generated reports in `data/reports/`
- Check research history with `python main.py list-reports`
- Customize configuration in `.env`
- Read the full README.md for advanced features

Happy researching!
