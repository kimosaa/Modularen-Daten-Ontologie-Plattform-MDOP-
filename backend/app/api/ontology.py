"""
Ontology API Endpoints
REST API for ontology management
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.postgres_client import get_db
from app.services.ontology.ontology_service import OntologyService
from app.schemas.ontology import (
    EntityTypeCreate, EntityTypeUpdate, EntityTypeResponse,
    RelationshipTypeCreate, RelationshipTypeUpdate, RelationshipTypeResponse,
    EntityCreate, EntityResponse,
    RelationshipCreate, RelationshipResponse
)


router = APIRouter(prefix="/ontology", tags=["Ontology"])


def get_ontology_service(db: Session = Depends(get_db)) -> OntologyService:
    """Dependency to get OntologyService instance"""
    return OntologyService(db)


# ========== Entity Type Endpoints ==========

@router.post("/entity-types", response_model=EntityTypeResponse, status_code=201)
async def create_entity_type(
    entity_type: EntityTypeCreate,
    service: OntologyService = Depends(get_ontology_service)
):
    """
    Create a new entity type definition
    
    - **name**: Unique identifier for the entity type (e.g., "Person", "Company")
    - **label**: Human-readable display name
    - **description**: Description of the entity type
    - **properties**: JSON schema defining entity properties
    """
    return service.create_entity_type(entity_type)


@router.get("/entity-types", response_model=List[EntityTypeResponse])
async def list_entity_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: OntologyService = Depends(get_ontology_service)
):
    """
    List all entity types
    
    Returns paginated list of entity type definitions
    """
    return service.get_entity_types(skip=skip, limit=limit)


@router.get("/entity-types/{entity_type_id}", response_model=EntityTypeResponse)
async def get_entity_type(
    entity_type_id: int,
    service: OntologyService = Depends(get_ontology_service)
):
    """Get a specific entity type by ID"""
    return service.get_entity_type(entity_type_id)


@router.put("/entity-types/{entity_type_id}", response_model=EntityTypeResponse)
async def update_entity_type(
    entity_type_id: int,
    entity_type: EntityTypeUpdate,
    service: OntologyService = Depends(get_ontology_service)
):
    """Update an existing entity type"""
    return service.update_entity_type(entity_type_id, entity_type)


@router.delete("/entity-types/{entity_type_id}", status_code=204)
async def delete_entity_type(
    entity_type_id: int,
    service: OntologyService = Depends(get_ontology_service)
):
    """Delete (deactivate) an entity type"""
    service.delete_entity_type(entity_type_id)
    return None


# ========== Relationship Type Endpoints ==========

@router.post("/relationship-types", response_model=RelationshipTypeResponse, status_code=201)
async def create_relationship_type(
    relationship_type: RelationshipTypeCreate,
    service: OntologyService = Depends(get_ontology_service)
):
    """
    Create a new relationship type definition
    
    Defines how two entity types can be related
    """
    return service.create_relationship_type(relationship_type)


@router.get("/relationship-types", response_model=List[RelationshipTypeResponse])
async def list_relationship_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: OntologyService = Depends(get_ontology_service)
):
    """List all relationship types"""
    return service.get_relationship_types(skip=skip, limit=limit)


# ========== Entity Instance Endpoints ==========

@router.post("/entities", response_model=EntityResponse, status_code=201)
async def create_entity(
    entity: EntityCreate,
    service: OntologyService = Depends(get_ontology_service)
):
    """
    Create a new entity instance in the graph
    
    - **type**: Entity type name
    - **properties**: Entity property values
    """
    return service.create_entity(entity)


@router.get("/entities/{entity_id}", response_model=EntityResponse)
async def get_entity(
    entity_id: str,
    service: OntologyService = Depends(get_ontology_service)
):
    """Get an entity instance by ID"""
    return service.get_entity(entity_id)


@router.get("/entities", response_model=List[EntityResponse])
async def search_entities(
    entity_type: str = Query(..., description="Entity type to search"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: OntologyService = Depends(get_ontology_service)
):
    """
    Search entities by type and optional filters
    
    Query parameters can be used as filters
    """
    # Note: Advanced filtering would be implemented here
    return service.search_entities(entity_type, {}, skip=skip, limit=limit)


# ========== Relationship Instance Endpoints ==========

@router.post("/relationships", response_model=RelationshipResponse, status_code=201)
async def create_relationship(
    relationship: RelationshipCreate,
    service: OntologyService = Depends(get_ontology_service)
):
    """
    Create a new relationship instance in the graph
    
    Connects two existing entities
    """
    return service.create_relationship(relationship)
