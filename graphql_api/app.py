import os
import shutil
import json
import datetime
from typing import Optional, List, Dict
from fastapi import FastAPI, Request, Response, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync, snake_case_fallback_resolvers
from ariadne.explorer import ExplorerGraphiQL
from ariadne import ObjectType, MutationType
from ariadne.asgi import GraphQL
import uuid

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create a simple in-memory database for video metadata
VIDEO_DB_FILE = os.path.join(UPLOAD_DIR, "video_metadata.json")


def get_video_db() -> List[Dict]:
    if os.path.exists(VIDEO_DB_FILE):
        with open(VIDEO_DB_FILE, 'r') as f:
            return json.load(f)
    return []


def save_video_db(videos: List[Dict]):
    with open(VIDEO_DB_FILE, 'w') as f:
        json.dump(videos, f)


def add_video_to_db(filename: str):
    videos = get_video_db()
    videos.append({
        "filename": filename,
        "uploadTime": datetime.datetime.now().isoformat()
    })
    save_video_db(videos)


# Define types and resolvers
query = ObjectType("Query")
mutation = MutationType()


@query.field("hello")
def resolve_hello(*_):
    return "Hello, World!"


@query.field("videoList")
def resolve_video_list(*_):
    return get_video_db()


@mutation.field("uploadVideoStatus")
def resolve_upload_video_status(_, info, filename):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return {
            "success": True,
            "message": "Video exists in the system",
            "filename": filename
        }
    else:
        return {
            "success": False,
            "message": f"No video found with filename {filename}",
            "filename": None
        }


# Load schema from file
type_defs = load_schema_from_path("schema.graphql")

schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    snake_case_fallback_resolvers
)

# Create FastAPI app
app = FastAPI(title="AI Coach API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount GraphQL app
graphql_app = GraphQL(
    schema=schema,
    explorer=ExplorerGraphiQL(),
    debug=True
)
app.mount("/graphql", graphql_app)


@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    """
    Upload a small video file (15-30 seconds)
    """
    # Validate file
    if not file.content_type.startswith("video/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a video file."
        )

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save metadata
    add_video_to_db(unique_filename)

    return {
        "status": "success",
        "message": "Video received successfully",
        "filename": unique_filename
    }


@app.get("/")
async def root():
    return {"message": "Welcome to AI Coach API. Use /graphql for GraphQL API or /upload-video to upload videos."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
