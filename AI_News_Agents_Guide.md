# AI News Agents - Complete Usage Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
3. [Basic Usage](#basic-usage)
4. [Customization Options](#customization-options)
5. [Advanced Features](#advanced-features)
6. [Future Development Ideas](#future-development-ideas)
7. [Development Workflow](#development-workflow)
8. [Troubleshooting](#troubleshooting)
9. [Resources](#resources)

## Project Overview

Your AI_NEWS_AGENTS project is a fully functional CrewAI-based system that automatically:
- Searches for news on specified topics using web search
- Scrapes relevant websites for detailed information
- Generates comprehensive news reports in markdown format

### Project Structure
```
AI_NEWS_AGENTS/
├── .env                          # Your API keys (KEEP SECURE!)
├── pyproject.toml               # Project configuration
├── uv.lock                      # Dependency lock file
├── README.md                    # Project documentation
├── report.md                    # Generated reports
├── knowledge/
│   └── user_preference.txt
├── src/
│   └── ai_news_agents/
│       ├── __init__.py
│       ├── main.py              # Main entry point
│       └── crew.py              # Crew definition (3 agents)
└── news/                        # Generated news articles
```

## Getting Started

### Prerequisites
- Python 3.10 or higher
- UV package manager
- API Keys:
  - SERPER_API_KEY (from https://serper.dev/)
  - OPENAI_API_KEY (from https://openai.com/)

### Installation
1. Navigate to your project directory:
   ```bash
   cd C:\Users\nobel\AI_NEWS_AGENTS
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

## Basic Usage

### Running the News Agent
```bash
# Method 1: Using CrewAI command
crewai run

# Method 2: Using UV directly
uv run run_crew

# Method 3: Using Python module
uv run python -m ai_news_agents.main
```

### Default Behavior
- **Topic**: AI LLMs (Large Language Models)
- **Output**: report.md file with comprehensive news analysis
- **Process**: Sequential execution of 3 agents

## Customization Options

### 1. Changing News Topics

Edit `src/ai_news_agents/main.py`:

```python
inputs = {
    'topic': 'Your Topic Here',  # Examples:
    # 'Quantum Computing'
    # 'Cryptocurrency'
    # 'Climate Change Technology'
    # 'Space Exploration'
    # 'Cybersecurity'
    'date': datetime.now().strftime('%Y-%m-%d')
}
```

### 2. Modifying Agent Behavior

Edit `src/ai_news_agents/crew.py`:

#### News Agent Customization:
```python
@agent
def news_agent(self) -> Agent:
    return Agent(
        role='{topic} News Retriever',
        goal='Find the most recent and relevant {topic} news',
        backstory="Customize the agent's background and expertise",
        tools=[SerperDevTool()],
        verbose=True
    )
```

#### Web Scraper Agent Customization:
```python
@agent
def webscrapper_agent(self) -> Agent:
    return Agent(
        role='Content Analyzer',
        goal='Extract key insights from news sources',
        backstory="Expert at analyzing and summarizing web content",
        tools=[ScrapeWebsiteTool()],
        verbose=True
    )
```

#### File Generator Customization:
```python
@agent
def filegenerate_analyst(self) -> Agent:
    return Agent(
        role='Report Writer',
        goal='Create professional news reports',
        backstory="Skilled journalist and technical writer",
        tools=[FileWriterTool()],
        verbose=True
    )
```

### 3. Modifying Task Outputs

Customize what each task produces:

```python
@task
def generate_news_task(self) -> Task:
    return Task(
        description='Search for recent {topic} developments',
        expected_output='Top 5 most relevant news sources with URLs and brief descriptions',
        agent=self.news_agent()
    )

@task
def webscraping_task(self) -> Task:
    return Task(
        description='Analyze and extract key information from news sources',
        expected_output='Detailed analysis with key points, quotes, and data',
        agent=self.webscrapper_agent(),
        output_file='detailed_analysis.md'
    )

@task
def filegenerate_task(self) -> Task:
    return Task(
        description='Create a comprehensive news report',
        expected_output='Professional report with executive summary, key findings, and recommendations',
        agent=self.filegenerate_analyst(),
        output_file='final_report.md'
    )
```

## Advanced Features

### 1. Adding More Tools

Available CrewAI tools you can add:

```python
from crewai_tools import (
    YoutubeVideoSearchTool,
    TwitterSearchTool,
    WebsiteSearchTool,
    PDFSearchTool,
    CSVSearchTool,
    JSONSearchTool
)

# Add to any agent:
tools=[SerperDevTool(), YoutubeVideoSearchTool(), TwitterSearchTool()]
```

### 2. Multiple Crew Processes

Change how agents work together:

```python
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.parallel,  # or Process.hierarchical
        verbose=True,
        max_execution_time=600  # 10 minutes timeout
    )
```

### 3. Different LLM Models

Change the model in `.env`:

```env
# High-quality options:
MODEL=gpt-4o
MODEL=gpt-4-turbo

# Cost-effective options:
MODEL=gpt-3.5-turbo
MODEL=gpt-4o-mini

# Alternative providers:
MODEL=claude-3-sonnet
MODEL=claude-3-haiku
```

### 4. Custom Output Formats

Modify file outputs:

```python
@task
def filegenerate_task(self) -> Task:
    return Task(
        description='Generate news in specific format',
        expected_output='News report in JSON format with structured data',
        agent=self.filegenerate_analyst(),
        output_file=f'news/{datetime.now().strftime("%Y-%m-%d")}_news.json'
    )
```

## Future Development Ideas

### 1. Automated Scheduling
Create a daily news service:

**Windows Task Scheduler:**
- Program: `cmd.exe`
- Arguments: `/c cd C:\Users\nobel\AI_NEWS_AGENTS && crewai run`
- Schedule: Daily at desired time

**Python Scheduler:**
```python
import schedule
import time

def run_news_agent():
    # Your crew execution code here
    pass

schedule.every().day.at("09:00").do(run_news_agent)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 2. Multi-Topic News Service

Create different configurations:

```
AI_NEWS_AGENTS/
├── configs/
│   ├── ai_news_config.py
│   ├── crypto_config.py
│   ├── tech_config.py
│   └── science_config.py
└── run_all_topics.py
```

### 3. Web Dashboard

Create a Flask web interface:

```python
from flask import Flask, render_template, request
from your_crew import AiNewsAgents

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/run_news', methods=['POST'])
def run_news():
    topic = request.form['topic']
    # Run your crew with custom topic
    return render_template('results.html', results=results)
```

### 4. Email/Slack Integration

Add notification agents:

```python
from crewai_tools import EmailTool, SlackTool

@agent
def notification_agent(self) -> Agent:
    return Agent(
        role='News Broadcaster',
        goal='Share news reports with stakeholders',
        tools=[EmailTool(), SlackTool()],
        verbose=True
    )
```

### 5. Advanced Analytics

Add analysis capabilities:

```python
@task
def sentiment_analysis_task(self) -> Task:
    return Task(
        description='Analyze sentiment and trends in news',
        expected_output='Sentiment scores and trend analysis',
        agent=self.analysis_agent()
    )
```

### 6. Database Integration

Store news data:

```python
import sqlite3
from crewai_tools import DatabaseTool

# Create database agent
@agent
def database_agent(self) -> Agent:
    return Agent(
        role='Data Manager',
        goal='Store and retrieve news data',
        tools=[DatabaseTool()],
        verbose=True
    )
```

## Development Workflow

### Making Changes
1. **Edit Configuration**: Modify `crew.py` for agent/task changes
2. **Test Changes**: Run `crewai run` to test
3. **Check Output**: Review generated reports in `report.md`
4. **Iterate**: Refine based on results

### Adding Dependencies
```bash
# Add new packages
uv add package_name

# Update existing packages
uv sync --upgrade

# Install development dependencies
uv add --dev pytest black flake8
```

### Version Control Setup
```bash
# Initialize git repository
git init

# Create .gitignore
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".venv/" >> .gitignore
echo "report.md" >> .gitignore

# First commit
git add .
git commit -m "Initial AI News Agents setup"
```

### Environment Management

**Development Environment:**
```env
MODEL=gpt-4o-mini  # Cost-effective for testing
OPENAI_API_KEY=your_dev_key
SERPER_API_KEY=your_serper_key
DEBUG=true
```

**Production Environment:**
```env
MODEL=gpt-4o  # Higher quality for production
OPENAI_API_KEY=your_prod_key
SERPER_API_KEY=your_serper_key
DEBUG=false
```

## Troubleshooting

### Common Issues

**1. Import Errors:**
```bash
# Reinstall dependencies
uv sync --reinstall
```

**2. API Key Issues:**
```bash
# Check .env file exists and has correct keys
cat .env
```

**3. Build Errors:**
```bash
# Clean and rebuild
uv clean
uv sync
```

**4. Permission Errors:**
```bash
# Run as administrator or check file permissions
```

### Debug Mode

Add debug logging to `main.py`:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

def run():
    try:
        print("Debug: Starting crew...")
        # Your code here
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
```

### Performance Optimization

**1. Reduce API Calls:**
```python
# Limit search results
tools=[SerperDevTool(search_results=5)]  # Default is 10
```

**2. Set Timeouts:**
```python
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        max_execution_time=300,  # 5 minutes
        verbose=True
    )
```

**3. Use Cheaper Models for Testing:**
```env
MODEL=gpt-3.5-turbo  # Much cheaper than GPT-4
```

## Resources

### Documentation
- **CrewAI Official Docs**: https://docs.crewai.com/
- **CrewAI Tools**: https://docs.crewai.com/tools/
- **Pydantic Documentation**: https://docs.pydantic.dev/

### API Documentation
- **OpenAI API**: https://platform.openai.com/docs
- **Serper API**: https://serper.dev/docs

### Community
- **CrewAI GitHub**: https://github.com/joaomdmoura/crewai
- **CrewAI Discord**: https://discord.gg/X4JWnZnxPb

### Learning Resources
- **CrewAI Tutorials**: https://docs.crewai.com/tutorials/
- **Multi-Agent Systems**: Learn about agent coordination and task distribution
- **LangChain Integration**: CrewAI builds on LangChain concepts

### Cost Management
- **OpenAI Pricing**: https://openai.com/pricing
- **Serper Pricing**: https://serper.dev/pricing
- **Monitor Usage**: Check your API dashboards regularly

## Best Practices

### 1. Security
- Never commit `.env` files to version control
- Use environment-specific API keys
- Rotate API keys regularly
- Monitor API usage for unusual activity

### 2. Code Organization
- Keep agents focused on single responsibilities
- Use descriptive names for agents and tasks
- Comment complex configurations
- Maintain consistent formatting

### 3. Testing
- Test with different topics regularly
- Verify output quality
- Monitor execution times
- Check API costs

### 4. Monitoring
- Log important events
- Track successful vs failed runs
- Monitor output quality
- Set up alerts for failures

---

## Quick Reference Commands

```bash
# Run the news agent
crewai run

# Install new dependency
uv add package_name

# Update all dependencies
uv sync --upgrade

# Check project status
uv lock --check

# Run with debug output
uv run run_crew --verbose

# Check Python environment
uv run python --version
```

---

**Created**: July 20, 2025
**Version**: 1.0
**Author**: AI Assistant
**Project**: AI_NEWS_AGENTS CrewAI Implementation
