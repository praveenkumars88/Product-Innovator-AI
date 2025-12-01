# MAPIS Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation Steps

### 1. Install Dependencies

```bash
# Install all required packages
pip3 install -r requirements.txt
```

**Note**: If `google-adk` is not available via pip, you may need to:
- Install it from a specific source (if provided by Google)
- Or use an alternative LLM agent framework

### 2. Install Google ADK (if needed)

The Google ADK package might need to be installed separately. Check if you have access to:
- Google's internal package repository
- Or use an alternative like `langchain` or `openai` agents

If Google ADK is not available, you can modify the agents to use:
- OpenAI API
- Anthropic Claude API
- Or other LLM providers

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env and add your Google API key
```

### 4. Run MAPIS

#### Interactive Mode
```bash
python3 main.py
```

#### With Direct Input
```bash
# New app idea
python3 main.py "Give me a new idea in the EdTech domain"

# Feature extension
python3 main.py "Add a voice ordering feature for Swiggy"
```

#### Run Examples
```bash
python3 example_usage.py
```

## Troubleshooting

### ModuleNotFoundError: No module named 'google'

If you get this error, the Google ADK package is not installed. Options:

1. **Install Google ADK** (if available):
   ```bash
   pip3 install google-adk
   ```

2. **Use Alternative Framework**:
   - Modify agents to use `langchain` or `openai`
   - Update imports in agent files

3. **Mock for Testing**:
   - Create a mock Agent class for testing
   - Implement actual integration later

### Other Common Issues

- **Import errors**: Make sure you're in the project root directory
- **MCP connection errors**: MCP tools are placeholders - implement actual connections
- **Memory issues**: Check Python version compatibility

## Quick Test

After installation, test with:
```bash
python3 -c "from my_agent.orchestrator import MAPISOrchestrator; print('Import successful!')"
```

If this works, you can run the full system.

