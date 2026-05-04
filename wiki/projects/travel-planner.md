---
title: Travel-Planner
domain: projects
tags: [multi-agent-systems, llm-agents, streamlit, fastapi, adk]
sources: [https://github.com/HarshTomar1234/Travel-Planner]
last_updated: 2026-04-07
confidence: 0.8
links: [[genai-agents]], [[reasoning-llms]], [[vlmverse]]
---

## Project Overview

The Travel-Planner is a travel planning application utilizing Google's Agent Development Kit (ADK) to orchestrate a multi-agent system. It generates comprehensive travel recommendations by leveraging OpenAI's GPT-4o model via LiteLLM, responding to user-defined destinations, dates, and budget constraints.

## Key Features

*   **Multi-Agent Architecture**: Dedicated agents manage specific planning domains.
    *   **Host Agent**: Coordinates overall trip planning.
    *   **Flight Agent**: Suggests flight options, including airline, times, and prices.
    *   **Stay Agent**: Recommends accommodations with location, pricing, and amenities.
    *   **Activities Agent**: Provides activity suggestions, descriptions, pricing, and duration.
*   **Interactive Streamlit UI**: User interface for input and recommendation display.
*   **Budget-Aware Planning**: All recommendations adhere to specified budget parameters.
*   **Realistic Suggestions**: Generates plausible travel itineraries.

## System Architecture

The system employs an Agent-to-Agent (A2A) communication model for distributed processing.

### Component Organization

*   `agents/`
    *   `host_agent/`: Orchestrates planning.
    *   `flight_agent/`: Manages flight searches.
    *   `stay_agent/`: Manages accommodation searches.
    *   `activities_agent/`: Manages activity suggestions.
*   `common/`: Shared utilities, including `a2a_client.py` and `a2a_server.py`.
*   `travel_trip.py`: Streamlit UI implementation.

### Agent Communication Architecture

1.  **User Interface (Streamlit)**: Gathers user travel preferences.
2.  **Host Agent (Port 8000)**: Receives initial request, dispatches sub-tasks.
3.  **Specialized Agents**:
    *   **Flight Agent (Port 8001)**: Processes flight search parameters.
    *   **Stay Agent (Port 8002)**: Processes accommodation search parameters.
    *   **Activities Agent (Port 8003)**: Processes activity search parameters.
4.  **Result Aggregation**: Host Agent collects and synthesizes results from specialized agents.
5.  **Output Presentation**: Host Agent returns the comprehensive travel plan to the Streamlit UI.

## Technology Stack

*   **Google ADK**: Agent development framework.
*   **LiteLLM**: LLM abstraction for OpenAI GPT-4o.
*   **FastAPI**: Backend API for inter-agent communication.
*   **Streamlit**: Frontend user interface framework.
*   **Uvicorn**: ASGI server.
*   **HTTPX**: Asynchronous HTTP client.
*   **Python-dotenv**: Environment variable management.

## Installation and Setup

### Prerequisites

*   Python 3.9+
*   OpenAI API Key

### Procedure

1.  Clone the repository:
    `git clone https://github.com/HarshTomar1234/Travel-Planner.git`
    `cd Travel-Planner`
2.  Install dependencies:
    `pip install -r requirements.txt`
3.  Configure environment variables: Create a `.env` file in the root directory with `OPENAI_API_KEY=your_openai_api_key_here`.

## Operational Procedure

### Start Agent Services

Launch each agent in a separate terminal:

*   Flight Agent: `python -m agents.flight_agent` (Port 8001)
*   Stay Agent: `python -m agents.stay_agent` (Port 8002)
*   Activities Agent: `python -m agents.activities_agent` (Port 8003)
*   Host Agent: `python -m agents.host_agent` (Port 8000)

### Launch Streamlit UI

In an additional terminal, run:

*   `streamlit run travel_trip.py` (accessible via `http://localhost:8501`)

### Plan Generation

Input travel parameters (origin, destination, dates, budget) into the UI and initiate the planning process.

## Recommendation Output

The system generates detailed recommendations covering:

*   **Flights**: Airline, departure/return times, price, direct/connecting status.
*   **Accommodation**: Hotel/stay name, location, price per night, amenities.
*   **Activities**: Activity name, description, estimated price, duration, practical tips.

## Troubleshooting Guide

*   **API Key Issues**: Verify `OPENAI_API_KEY` in `.env` file.
*   **Agent Connection Errors**: Confirm all agent services are running on designated ports.
*   **No Results**: Consider increasing the specified budget.

## Future Development

*   Integration with live travel APIs for real-time booking.
*   User authentication and saved trip functionality.
*   Offline mode for cached plans.
*   Mobile application development.

## Related

- [[genai-agents]] — multi-agent orchestration patterns used in this project
- [[reasoning-llms]] — GPT-4o reasoning capabilities powering the agents
- [[vlmverse]] — broader LLM ecosystem context