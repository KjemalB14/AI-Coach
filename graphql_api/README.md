# AI Coach GraphQL API

A FastAPI-based GraphQL API that serves as the backend for AI Coach, allowing video uploads and GraphQL queries.

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
uvicorn app:app --reload
```

4. Access the API:
   - GraphQL playground: http://127.0.0.1:8000/graphql
   - API documentation: http://127.0.0.1:8000/docs

## GraphQL Examples

### Query Hello World

```graphql
{
  hello
}
```

### Query Video List

```graphql
{
  videoList {
    filename
    uploadTime
  }
}
```

### Check Video Upload Status

```graphql
mutation {
  uploadVideoStatus(filename: "your-filename-here.mp4") {
    success
    message
    filename
  }
}
```

## REST API Endpoints

- `POST /upload-video`: Upload a video file (supports multipart form data)
- `GET /`: Welcome page with API information

## Project Structure

- `app.py`: Main application file with FastAPI and GraphQL setup
- `requirements.txt`: Python dependencies
- `schema.graphql`: GraphQL schema definition
- `uploads/`: Directory where uploaded videos are stored
- `test.py`: Unit tests for the API

## Testing

Run the tests with:

```bash
python -m unittest test.py
```

## Notes

- This project uses FastAPI with Ariadne for GraphQL integration
- Videos are stored in the `uploads` directory with metadata tracked in `uploads/video_metadata.json`
- Supported video formats: MP4, MOV, AVI, etc. (15-30 second clips)
