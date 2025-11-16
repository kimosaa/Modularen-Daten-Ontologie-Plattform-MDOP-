#!/bin/bash
# Stop MDOP Platform

echo "=========================================="
echo "Stopping MDOP Platform"
echo "=========================================="

docker-compose down

echo ""
echo "MDOP Platform stopped."
echo "To start again: ./scripts/start.sh"
echo "=========================================="
