# Echobot Backend

A simple FastAPI backend for the Echobot chat application.

## Features

- RESTful API with FastAPI
- Input validation using Pydantic
- Comprehensive error handling
- Logging configuration
- CORS support
- Health check endpoint
- API documentation (Swagger UI and ReDoc)
- Test suite

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /chat
Echoes back the user's message.

Request:
```json
{
    "message": "Hello"
}
```

Response:
```json
{
    "reply": "You said: Hello"
}
```

### GET /
Health check endpoint.

Response:
```json
{
    "status": "healthy",
    "message": "Echobot API is running"
}
```

## Development

### Code Style

The project uses several tools to maintain code quality:

- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

To run all code quality checks:
```bash
black .
isort .
flake8 .
mypy .
```

### Testing

Run the test suite:
```bash
pytest
```

## Deployment

This backend can be deployed to various platforms:

1. **Render**:
   - Create a new Web Service
   - Connect your GitHub repository
   - Set the build command: `pip install -r requirements.txt`
   - Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Railway**:
   - Create a new project
   - Connect your GitHub repository
   - Add the same build and start commands as Render

3. **Replit**:
   - Create a new Python repl
   - Upload the files
   - Set the run command to: `uvicorn main:app --host 0.0.0.0 --port 8080`

## CORS Configuration

The API is configured to accept requests from any origin (`*`). In production, you should update the `allow_origins` list in `main.py` to include only your frontend's domain.

## Error Handling

The API includes comprehensive error handling:
- Input validation errors (422)
- Internal server errors (500)
- Global exception handler for unhandled exceptions

## Logging

The application uses Python's built-in logging module with the following configuration:
- Log level: INFO
- Format: timestamp - logger name - level - message
- All errors are logged with full stack traces 