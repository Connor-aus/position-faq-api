# Position-FAQ-API

An LLM workflow built with FastAPI that processes questions about job positions and companies.

## Overview

Position-FAQ-API is an LLM-powered workflow that provides the following capabilities:
- Identify whether an input is a question
- Determine if the question is about a job position or a company
- Return relevant information about positions or companies
- Update relevant information to reflect questions asked

## Architecture

- **Framework**: FastAPI
- **AI/ML**: Anthropic Claude models via LangChain
- **Runtime**: Python 3.11

## Prerequisites

- Python 3.11+
- Anthropic API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/position-faq-api.git
   cd position-faq-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in a `.env` file:
   ```
   LLM_MODEL_ID=claude-3-haiku-20240307
   ANTHROPIC_API_KEY=your-anthropic-api-key
   MAX_INPUT_LENGTH=4000
   LOGGING_LEVEL=INFO
   ```

## Local Development

Run the API locally with:
```bash
cd src
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Usage

### Chat Request

Send a POST request to the `/v1/chatRequest` endpoint:

```bash
curl -X POST http://localhost:8000/v1/chatRequest \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the responsibilities of this position?", "positionId": 1001}'
```

### Get Company Positions

Get all positions for a specific company:

```bash
curl -X GET http://localhost:8000/v1/company/2001/positions
```

### Get Position Versions

Get all versions of a specific position:

```bash
curl -X GET http://localhost:8000/v1/position/1001/versions
```

### Update Position Details

Update details for a specific position (creates a new version):

```bash
curl -X PUT http://localhost:8000/v1/position/1001/details \
  -H "Content-Type: application/json" \
  -d '{
    "position": {
      "id": 1001,
      "companyId": 2001,
      "positionTitle": "Updated Position Title",
      "positionDescription": "Updated description"
    },
    "positionFAQs": [
      {
        "id": 50001,
        "positionId": 1001,
        "question": "Is this role hybrid?",
        "response": "Yes, 2 days in office per week"
      }
    ],
    "positionInfo": [
      {
        "id": 60001,
        "positionId": 1001,
        "subject": "Team size",
        "answer": "8 engineers + 1 EM + 1 PM"
      }
    ]
  }'
```

## Data Structure

### Position Data

Each position contains:
- Basic position details (id, title, description)
- Position FAQs (questions and answers)
- Position Info (key information about the role)

Example:
```json
{
  "position": {
    "id": 1001,
    "companyId": 2001,
    "positionTitle": "Senior Full Stack Engineer (Payments)",
    "positionDescription": "Senior Full Stack Engineer (Payments). Brisbane (Hybrid).",
    "version": 1,
    "timestamp": "2025-08-24T15:05:00+10:00"
  },
  "positionFAQs": [
    {
      "id": 50001,
      "positionId": 1001,
      "question": "Is this role hybrid or fully on-site?",
      "response": "Hybrid: 2 days in-office (Tue/Thu), flexible start 7-10am."
    }
  ],
  "positionInfo": [
    {
      "id": 60001,
      "positionId": 1001,
      "subject": "Team size",
      "answer": "8 engineers + 1 EM + 1 PM."
    }
  ]
}
```

## Project Structure

- `src/`: Source code
  - `main.py`: Entry point for the application
  - `api/`: API endpoints and validation
  - `handlers/`: Request handlers
  - `llms/`: Language model configurations using LangChain
  - `workflow/`: Workflow logic and processing
  - `utils/`: Utility functions
  - `database/`: Data storage and retrieval
  - `staticFiles/`: Example data files
- `tests/`: Unit and integration tests

## Dependencies

- anthropic: 0.54.0
- fastapi: 0.115.12
- langchain: 0.3.25
- langchain-anthropic: 0.3.15
- langchain-core: 0.3.65
- langgraph: 0.3.1
- pydantic: 2.11.5
- python-dotenv: 1.1.0
- uvicorn: 0.34.3
- structlog: 23.1.0

## License

This project is provided for public viewing. All rights are reserved by Connor McSweeney. No part of this repository may be copied, modified, or redistributed without explicit written permission.

© Connor McSweeney 2025. All rights reserved.