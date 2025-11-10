"""
Main API Router
Aggregates all API routes
"""
from fastapi import APIRouter
from app.api import ontology


api_router = APIRouter()

# Include all sub-routers
api_router.include_router(ontology.router)

# Add more routers as they are implemented
# api_router.include_router(connectors.router)
# api_router.include_router(query.router)
# api_router.include_router(security.router)
