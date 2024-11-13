## Getting Started

This instructions are always using the `backend` directory as working directory.
```bash
cd backend
```

First, add your API keys to a new `.env` file:

```
OPENAI_API_KEY=sk-xxx
LANGSMITH_API_KEY=ls-xxx
LANGCHAIN_ENDPOINT=https://eu.api.smith.langchain.com
IMAGE_NAME=fuel-prices-agent-backend
```

### Dependencies
Please ensure you have installed:
- python 3.11
- docker
- langgraph cli

### Installing langgraph CLI
```bash
pip install -U langgraph-cli
```

### Building and Running the server

#### Build the image
```bash
langgraph build -t fuel-prices-agent-backend
```

#### Run the server with Langgraph CLI
Run the development server with langgraph CLI.
```bash
langgraph up
```

#### Run the server with Docker
Alternatively, you can run the development server with docker.
```bash
docker compose up
```

### Running Tests
Open the browser with:
- http://localhost:8123/ok to see if the server is running fine.
- http://localhost:8123/docs to see the API documentation.