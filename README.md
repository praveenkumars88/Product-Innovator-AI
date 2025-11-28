# Multi-Agent Product Innovation System (MAPIS)

## Overview
MAPIS is an AI-powered solution designed to generate domain-specific product ideas, feature enhancements, and full product concept documents using a multi-agent architecture.

## Architecture

### Core Agents
1. **Intent Classification Agent** - Determines if user wants new app idea or feature extension
2. **Domain Understanding Agent** - Analyzes domain, pain points, trends
3. **Idea Breakdown Agent** - Breaks rough ideas into structured components
4. **Feature Design Agent** - Designs features for existing apps
5. **Concept Paper Writer Agent** - Generates enterprise-style concept papers
6. **Competitor Analysis Agent** - Researches competitors and differentiation
7. **Architecture Suggestion Agent** - Generates technical blueprints
8. **Market Size Agent** - Calculates TAM/SAM/SOM
9. **Wireframe Generator Agent** - Creates ASCII wireframes
10. **Pitch Creator Agent** - Produces startup-style pitch summaries
11. **Final Output Aggregator** - Combines all outputs

### System Flow

#### New App Ideas Flow:
```
User → Intent Agent → Domain Agent → Idea Breakdown → Competitor Agent →
Market Size → Architecture Agent → Wireframe Agent → Pitch Creator → Output
```

#### Feature Extension Flow:
```
User → Intent Agent → Feature Design Agent → Concept Paper Agent →
Competitor Agent → Wireframe Agent → Architecture Agent → Output
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (if needed):
```bash
cp .env.example .env
```

3. Run the system:
```bash
python main.py
```

## Features
- Multi-agent orchestration (sequential + parallel)
- MCP tool integration (Google Search, Code Execution)
- Memory management (InMemorySessionService)
- Observability and logging
- Long-running operations support

## Project Structure
```
Capstone/
├── my_agent/
│   ├── agents/                    # Individual agent implementations
│   │   ├── intent_classification_agent.py
│   │   ├── domain_understanding_agent.py
│   │   ├── idea_breakdown_agent.py
│   │   ├── feature_design_agent.py
│   │   ├── competitor_analysis_agent.py
│   │   ├── architecture_suggestion_agent.py
│   │   ├── market_size_agent.py
│   │   ├── wireframe_generator_agent.py
│   │   ├── concept_paper_writer_agent.py
│   │   └── pitch_creator_agent.py
│   ├── orchestrator.py            # Agent orchestration logic
│   ├── memory.py                  # Memory management
│   ├── tools/                     # MCP tool integrations
│   │   ├── google_search.py
│   │   └── code_execution.py
│   └── utils/                     # Utilities and helpers
│       └── logger.py
├── main.py                        # Entry point
├── example_usage.py               # Example usage scripts
├── requirements.txt               # Dependencies
├── README.md                      # This file
└── ARCHITECTURE.md                # Architecture documentation
```

## Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment (optional)
cp .env.example .env
# Edit .env with your configuration
```

### Basic Usage

#### Command Line
```bash
# Interactive mode
python main.py

# Direct input
python main.py "Give me a new idea in the EdTech domain"
```

#### Programmatic Usage
```python
import asyncio
from my_agent.orchestrator import MAPISOrchestrator

async def main():
    orchestrator = MAPISOrchestrator()
    result = await orchestrator.process(
        "Add a voice ordering feature for Swiggy",
        session_id="my_session"
    )
    print(result)

asyncio.run(main())
```

### Example Usage
```bash
python example_usage.py
```

## Agent Workflows

### New App Idea Workflow
1. **Intent Classification** → Determines intent is "new_app_idea"
2. **Domain Understanding** → Analyzes domain (EdTech, FinTech, etc.)
3. **Idea Breakdown** → Structures the idea
4. **Competitor Analysis** → Researches competitors
5. **Market Size** → Calculates TAM/SAM/SOM
6. **Architecture** → Suggests technical architecture
7. **Wireframes** → Generates UI wireframes
8. **Pitch** → Creates startup pitch

### Feature Extension Workflow
1. **Intent Classification** → Determines intent is "feature_extension"
2. **Feature Design** → Designs the feature
3. **Concept Paper** → Writes enterprise concept paper
4. **Competitor Analysis** → Analyzes competitive landscape
5. **Wireframes** → Generates feature wireframes
6. **Architecture** → Suggests integration architecture

## Output Structure

### New App Idea Output
- Intent classification
- Domain analysis
- Idea breakdown (problem, value prop, personas, features)
- Competitor analysis
- Market size (TAM/SAM/SOM)
- Architecture suggestion
- Wireframes
- Pitch summary

### Feature Extension Output
- Intent classification
- Feature design (epics, user stories, acceptance criteria)
- Concept paper (full enterprise document)
- Competitor analysis
- Wireframes
- Architecture suggestion

## Configuration

See `.env.example` for configuration options:
- Google API keys
- MCP server URLs
- Logging levels

## Development

### Adding a New Agent
1. Create agent file in `my_agent/agents/`
2. Inherit from base agent pattern
3. Add to orchestrator imports
4. Integrate into workflow

### Extending Tools
1. Add tool implementation in `my_agent/tools/`
2. Integrate with MCP server
3. Use in relevant agents

## Testing

Run examples to test the system:
```bash
python example_usage.py
```

## Troubleshooting

### Common Issues
1. **Import errors**: Ensure all dependencies are installed
2. **MCP connection errors**: Check MCP server configuration
3. **Memory issues**: Check session management

## License

[Add your license here]

## Contributors

- Praveenkumar S
- Aravind V

