# MAPIS Architecture Document

## System Overview

The Multi-Agent Product Innovation System (MAPIS) is built using Google ADK (Agent Development Kit) with a multi-agent architecture pattern. The system orchestrates 10 specialized agents to generate comprehensive product innovation outputs.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      User Input                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Intent Classification Agent                     │
│         (Determines: new_app_idea | feature_extension)      │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                              │
        ▼                              ▼
┌──────────────────┐        ┌──────────────────────┐
│  New App Idea    │        │  Feature Extension   │
│     Flow         │        │       Flow           │
└────────┬─────────┘        └──────────┬───────────┘
         │                              │
         ├─ Domain Understanding        ├─ Feature Design
         ├─ Idea Breakdown              ├─ Concept Paper
         ├─ Competitor Analysis         ├─ Competitor Analysis
         ├─ Market Size                 ├─ Wireframe Generation
         ├─ Architecture                ├─ Architecture
         ├─ Wireframe Generation        │
         └─ Pitch Creation              │
                       │                              │
                       └──────────────┬───────────────┘
                                      ▼
                       ┌──────────────────────────┐
                       │  Final Output Aggregator │
                       │      (Orchestrator)      │
                       └──────────┬───────────────┘
                                  ▼
                       ┌──────────────────────────┐
                       │      Final Output        │
                       └──────────────────────────┘
```

## Component Details

### 1. Intent Classification Agent
- **Purpose**: Classify user intent
- **Input**: User text
- **Output**: JSON with intent, domain, keywords
- **Model**: Gemini 2.5 Flash

### 2. Domain Understanding Agent
- **Purpose**: Analyze domain for opportunities
- **Tools**: Google Search MCP
- **Output**: Pain points, user segments, trends, market gaps
- **Model**: Gemini 2.5 Flash

### 3. Idea Breakdown Agent
- **Purpose**: Structure rough ideas
- **Output**: Problem statement, value prop, personas, features
- **Model**: Gemini 2.5 Flash

### 4. Feature Design Agent
- **Purpose**: Design features for existing apps
- **Output**: Epics, user stories, acceptance criteria
- **Model**: Gemini 2.5 Flash

### 5. Competitor Analysis Agent
- **Purpose**: Research competitors
- **Tools**: Google Search MCP
- **Output**: Competitor list, feature comparison, gaps
- **Model**: Gemini 2.5 Flash

### 6. Architecture Suggestion Agent
- **Purpose**: Generate technical blueprints
- **Output**: Services, databases, APIs, tech stack
- **Model**: Gemini 2.5 Flash

### 7. Market Size Agent
- **Purpose**: Calculate TAM/SAM/SOM
- **Tools**: Google Search MCP
- **Output**: Market size estimates with methodology
- **Model**: Gemini 2.5 Flash

### 8. Wireframe Generator Agent
- **Purpose**: Create ASCII wireframes
- **Tools**: Code Execution MCP
- **Output**: ASCII wireframes for screens
- **Model**: Gemini 2.5 Flash

### 9. Concept Paper Writer Agent
- **Purpose**: Write enterprise concept papers
- **Output**: Full concept paper with all sections
- **Model**: Gemini 2.5 Flash

### 10. Pitch Creator Agent
- **Purpose**: Create startup pitches
- **Output**: Pitch summary with all sections
- **Model**: Gemini 2.5 Flash

### 11. Orchestrator (Final Output Aggregator)
- **Purpose**: Coordinate all agents
- **Features**: 
  - Sequential and parallel execution
  - Memory management
  - Error handling
  - Result aggregation

## Data Flow

### New App Idea Flow
1. Intent Classification → Intent: "new_app_idea"
2. Domain Understanding (parallel with Idea Breakdown prep)
3. Idea Breakdown
4. Competitor Analysis (parallel with Market Size)
5. Market Size Calculation
6. Architecture Suggestion
7. Wireframe Generation
8. Pitch Creation
9. Output Aggregation

### Feature Extension Flow
1. Intent Classification → Intent: "feature_extension"
2. Feature Design
3. Concept Paper (parallel with Competitor Analysis)
4. Competitor Analysis
5. Wireframe Generation
6. Architecture Suggestion
7. Output Aggregation

## Memory Management

- **InMemorySessionService**: Maintains conversation context
- **Session Storage**: 
  - Context (key-value pairs)
  - History (agent interactions)
  - Preferences (user preferences)
  - Previous ideas/features

## Tool Integration

### Google Search MCP
- Competitor research
- Market trends
- Market size data

### Code Execution MCP
- Wireframe generation
- ASCII art creation

## Observability

- **Logging**: Structured logging with structlog
- **Metrics**: Agent execution times
- **Tracing**: Agent dependency tracking
- **Error Handling**: Graceful fallbacks

## Scalability Considerations

- Pluggable agent system
- Parallel execution where possible
- Session-based memory (can be extended to persistent storage)
- Modular tool integration

## Security

- Input sanitization
- No personal data storage
- Safe code execution (sandboxed)
- Session isolation

## Future Enhancements

- Persistent memory (database)
- PDF report generation
- Web UI
- API endpoints
- Cost calculator agent
- User preference learning

