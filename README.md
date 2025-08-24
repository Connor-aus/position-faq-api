# Position-FAQ-API

An LLM workflow built with FastAPI that processes questions about job positions and companies.

## Overview

Position-FAQ-API is an LLM-powered workflow that provides the following capabilities:
- Identify whether an input is a question
- Determine if the question is about a job position or a company
- Return relevant information about positions or companies

## Architecture

- **Framework**: FastAPI
- **AI/ML**: Anthropic Claude models for text processing
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
   LLM_MODEL_ID=claude-3-5-sonnet-latest
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

Send a POST request to the `/workflow` endpoint:

```bash
curl -X POST http://localhost:8000/workflow \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the responsibilities of a Software Engineer position?"}'
```

## Project Structure

- `src/`: Source code
  - `main.py`: Entry point for the application
  - `api/`: API endpoints and validation
  - `handlers/`: Request handlers
  - `llms/`: Language model configurations
  - `workflow/`: Workflow logic and processing
  - `utils/`: Utility functions
- `tests/`: Unit and integration tests

## License

This project is provided for public viewing. All rights are reserved by Connor McSweeney. No part of this repository may be copied, modified, or redistributed without explicit written permission.

© Connor McSweeney 2025. All rights reserved.