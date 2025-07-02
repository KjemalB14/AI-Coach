#!/bin/bash

# Terminal colors for better visibility
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Start AI Coach Application - Frontend and Backend
echo -e "${BLUE}╔════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      STARTING AI COACH APP        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════╝${NC}"

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to check if Python dependencies are installed
check_python_deps() {
  echo -e "\n${YELLOW}⟹ Checking Python dependencies...${NC}"
  cd graphql_api
  if [ ! -d "venv" ]; then
    echo -e "${GREEN}  ↳ Creating Python virtual environment...${NC}"
    python3 -m venv venv
  fi
  
  # Activate virtual environment
  source venv/bin/activate
  
  # Install dependencies
  echo -e "${GREEN}  ↳ Installing Python dependencies...${NC}"
  pip install -r requirements.txt
  
  # Deactivate virtual environment
  deactivate
  cd ..
}

# Function to check if Node dependencies are installed
check_node_deps() {
  echo -e "\n${YELLOW}⟹ Checking Node dependencies...${NC}"
  cd ai-coach-app
  if [ ! -d "node_modules" ]; then
    echo -e "${GREEN}  ↳ Installing Node dependencies...${NC}"
    npm install
  fi
  cd ..
}

# Check if necessary commands exist
if ! command_exists python3; then
  echo -e "${RED}✖ Error: python3 is not installed. Please install Python 3.${NC}"
  exit 1
fi

if ! command_exists npm; then
  echo -e "${RED}✖ Error: npm is not installed. Please install Node.js and npm.${NC}"
  exit 1
fi

# Check and install dependencies
check_python_deps
check_node_deps

# Start backend in background
echo -e "\n${YELLOW}⟹ Starting backend server...${NC}"
cd graphql_api
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo -e "${YELLOW}  ↳ Waiting for backend to initialize...${NC}"
sleep 3

# Start frontend in background
echo -e "\n${YELLOW}⟹ Starting frontend server...${NC}"
cd ai-coach-app
npm start &
FRONTEND_PID=$!
cd ..

# Function to handle script termination
cleanup() {
  echo -e "\n${YELLOW}⟹ Stopping servers...${NC}"
  echo -e "${GREEN}  ↳ Terminating frontend (PID: $FRONTEND_PID)${NC}"
  kill $FRONTEND_PID
  echo -e "${GREEN}  ↳ Terminating backend (PID: $BACKEND_PID)${NC}"
  kill $BACKEND_PID
  echo -e "\n${BLUE}✓ AI Coach Application stopped successfully.${NC}"
  exit 0
}

# Register cleanup function for when script is terminated
trap cleanup SIGINT SIGTERM

# Display success message with service URLs
echo -e "\n${BLUE}╔════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   AI COACH APPLICATION RUNNING    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════╝${NC}"
echo -e "${GREEN}✓ Frontend:${NC} http://localhost:4200"
echo -e "${GREEN}✓ Backend:${NC}  http://localhost:8000"
echo -e "${GREEN}✓ GraphQL:${NC}  http://localhost:8000/graphql"
echo -e "\n${YELLOW}Press Ctrl+C to stop both servers.${NC}"

# Keep script running
wait
