#!/bin/bash
# Start MDOP Platform

set -e

echo "=========================================="
echo "Starting MDOP Platform"
echo "=========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "Creating .env file from template..."
    cp backend/.env.example backend/.env
    echo "Please edit backend/.env with your configuration"
fi

# Start services
echo "Starting Docker containers..."
docker-compose up -d

# Wait for services to be healthy
echo "Waiting for services to be ready..."
sleep 20

# Check service health
echo ""
echo "Checking service health..."
docker-compose ps

echo ""
echo "=========================================="
echo "MDOP Platform started successfully!"
echo "=========================================="
echo ""
echo "Available services:"
echo "  - Backend API:       http://localhost:8000"
echo "  - API Docs:          http://localhost:8000/docs"
echo "  - Neo4j Browser:     http://localhost:7474"
echo "  - Elasticsearch:     http://localhost:9200"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop:      ./scripts/stop.sh"
echo "=========================================="
