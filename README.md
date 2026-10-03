# 🤖 AI Service Desk Operations Platform

An AI-powered IT Service Desk assistant designed to help Tier 1 support analysts analyze incidents, identify possible causes, recommend troubleshooting steps, and determine when escalation may be appropriate.

The application runs a local LLM using Ollama and stores analyzed tickets in a persistent SQLite database.

## Features

- AI-powered IT incident analysis
- Automatic issue categorization
- Priority assessment
- Possible cause identification
- Tier 1 troubleshooting recommendations
- Resolution and escalation guidance
- Persistent ticket history
- Local LLM processing

## Technologies

- Python
- Streamlit
- Ollama
- Llama 3.2
- SQLite
- REST API
- Git & GitHub

## How It Works

1. A Service Desk analyst enters an IT support issue.
2. The application sends the ticket to a locally hosted Llama model through the Ollama API.
3. The AI analyzes the incident and generates troubleshooting guidance.
4. The application displays the analysis to the analyst.
5. The ticket and AI response are stored in SQLite for ticket history.

## Example Use Cases

The application can assist with incidents involving:

- VPN connectivity
- Microsoft 365
- Authentication and password issues
- Network connectivity
- Software problems
- Hardware issues
- General Tier 1 troubleshooting

## Privacy

The current version uses a locally hosted LLM through Ollama. Ticket content is processed locally rather than being sent to a third-party cloud AI API.

## Project Status

Active portfolio project focused on AI-enabled IT support and Service Desk operations.