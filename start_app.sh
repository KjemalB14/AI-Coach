#!/bin/bash

# Start AI Coach Application - Frontend and Backend
echo "Starting AI Coach Application..."

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to check if Python dependencies are installed
check_python_deps() {
  echo "Checking Python dependencies..."
  cd graphql_api
  if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
  fi
  
  # Activate virtual environment
  source venv/bin/activate
  
  # Install dependencies
  echo "Installing Python dependencies..."
  pip install -r requirements.txt
  
  # Deactivate virtual environment
  deactivate
  cd ..
}

# Function to check if Node dependencies are installed
check_node_deps() {
  echo "Checking Node dependencies..."
  cd ai-coach-app
  if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
  fi
  cd ..
}

# Check if necessary commands exist
if ! command_exists python3; then
  echo "Error: python3 is not installed. Please install Python 3."
  exit 1
fi

if ! command_exists npm; then
  echo "Error: npm is not installed. Please install Node.js and npm."
  exit 1
fi

# Check and install dependencies
check_python_deps
check_node_deps

# Start backend in background
echo "Starting backend server..."
cd graphql_api
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 3

# Start frontend in background
echo "Starting frontend server..."
cd ai-coach-app
npm start &
FRONTEND_PID=$!
cd ..

# Function to handle script termination
cleanup() {
  echo "Stopping servers..."
  kill $FRONTEND_PID
  kill $BACKEND_PID
  exit 0
}

# Register cleanup function for when script is terminated
trap cleanup SIGINT SIGTERM

echo "AI Coach Application is running!"
echo "- Frontend: http://localhost:4200"
echo "- Backend: http://localhost:8000"
echo "- GraphQL: http://localhost:8000/graphql"
echo "Press Ctrl+C to stop both servers."

# Keep script running
wait
