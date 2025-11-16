"""
Ontology Service
Core business logic for ontology management
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
import time

from app.models.ontology import EntityType, RelationshipType, OntologyVersion
from app.schemas.ontology import (
    EntityTypeCreate, EntityTypeUpdate,
    RelationshipTypeCreate, RelationshipTypeUpdate,
    EntityCreate, RelationshipCreate
)
from app.db.neo4j_client import neo4j_client
from app.db.redis_client import redis_client
from app.core.logging import logger


class OntologyService:
    """Service for managing ontology definitions and instances"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ========== Entity Type Management ==========
    
    def create_entity_type(self, entity_type_data: EntityTypeCreate) -> EntityType:
        """
        Create a new entity type definition
        
        Args:
            entity_type_data: Entity type creation data
            
        Returns:
            Created EntityType
        """
        # Check if entity type already exists
        existing = self.db.query(EntityType).filter(EntityType.name == entity_type_data.name).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Entity type '{entity_type_data.name}' already exists")
        
        # Create entity type
        entity_type = EntityType(**entity_type_data.model_dump())
        self.db.add(entity_type)
        self.db.commit()
        self.db.refresh(entity_type)
        
        # Create Neo4j constraint for this entity type
        self._create_neo4j_entity_constraint(entity_type.name)
        
        # Invalidate cache
        redis_client.delete("ontology:entity_types")
        
        logger.info(f"Created entity type: {entity_type.name}")
        return entity_type
    
    def get_entity_types(self, skip: int = 0, limit: int = 100) -> List[EntityType]:
        """Get all entity types"""
        # Try cache first
        cache_key = f"ontology:entity_types:{skip}:{limit}"
        cached = redis_client.get(cache_key)
        if cached:
            return cached
        
        entity_types = self.db.query(EntityType).filter(EntityType.is_active == True).offset(skip).limit(limit).all()
        
        # Cache for 5 minutes
        redis_client.set(cache_key, entity_types, expire=300)
        
        return entity_types
    
    def get_entity_type(self, entity_type_id: int) -> EntityType:
        """Get entity type by ID"""
        entity_type = self.db.query(EntityType).filter(EntityType.id == entity_type_id).first()
        if not entity_type:
            raise HTTPException(status_code=404, detail="Entity type not found")
        return entity_type
    
    def update_entity_type(self, entity_type_id: int, update_data: EntityTypeUpdate) -> EntityType:
        """Update entity type"""
        entity_type = self.get_entity_type(entity_type_id)
        
        # Update fields
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(entity_type, field, value)
        
        entity_type.version += 1
        self.db.commit()
        self.db.refresh(entity_type)
        
        # Invalidate cache
        redis_client.delete("ontology:entity_types")
        
        logger.info(f"Updated entity type: {entity_type.name}")
        return entity_type
    
    def delete_entity_type(self, entity_type_id: int) -> bool:
        """Soft delete entity type"""
        entity_type = self.get_entity_type(entity_type_id)
        entity_type.is_active = False
        self.db.commit()
        
        # Invalidate cache
        redis_client.delete("ontology:entity_types")
        
        logger.info(f"Deleted entity type: {entity_type.name}")
        return True
    
    # ========== Relationship Type Management ==========
    
    def create_relationship_type(self, rel_type_data: RelationshipTypeCreate) -> RelationshipType:
        """Create a new relationship type definition"""
        # Verify entity types exist
        from_entity = self.get_entity_type(rel_type_data.from_entity_type_id)
        to_entity = self.get_entity_type(rel_type_data.to_entity_type_id)
        
        # Check if relationship type already exists
        existing = self.db.query(RelationshipType).filter(RelationshipType.name == rel_type_data.name).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Relationship type '{rel_type_data.name}' already exists")
        
        # Create relationship type
        rel_type = RelationshipType(**rel_type_data.model_dump())
        self.db.add(rel_type)
        self.db.commit()
        self.db.refresh(rel_type)
        
        logger.info(f"Created relationship type: {rel_type.name}")
        return rel_type
    
    def get_relationship_types(self, skip: int = 0, limit: int = 100) -> List[RelationshipType]:
        """Get all relationship types"""
        return self.db.query(RelationshipType).filter(RelationshipType.is_active == True).offset(skip).limit(limit).all()
    
    # ========== Entity Instance Management ==========
    
    def create_entity(self, entity_data: EntityCreate) -> Dict[str, Any]:
        """
        Create an entity instance in Neo4j graph
        
        Args:
            entity_data: Entity creation data
            
        Returns:
            Created entity with ID
        """
        # Verify entity type exists
        entity_type = self.db.query(EntityType).filter(EntityType.name == entity_data.type).first()
        if not entity_type:
            raise HTTPException(status_code=404, detail=f"Entity type '{entity_data.type}' not found")
        
        # Validate properties against schema
        # TODO: Implement JSON schema validation
        
        # Create node in Neo4j
        query = f"""
        CREATE (n:{entity_data.type} $properties)
        SET n.id = toString(id(n))
        SET n.created_at = datetime()
        RETURN n
        """
        
        result = neo4j_client.execute_write(query, {"properties": entity_data.properties})
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create entity")
        
        node = result[0]["n"]
        
        logger.info(f"Created entity of type {entity_data.type} with ID {node['id']}")
        
        return {
            "id": node["id"],
            "type": entity_data.type,
            "properties": dict(node)
        }
    
    def get_entity(self, entity_id: str) -> Dict[str, Any]:
        """Get entity by ID"""
        query = """
        MATCH (n)
        WHERE n.id = $entity_id
        RETURN n, labels(n) as labels
        """
        
        result = neo4j_client.execute_read(query, {"entity_id": entity_id})
        
        if not result:
            raise HTTPException(status_code=404, detail="Entity not found")
        
        node = result[0]["n"]
        labels = result[0]["labels"]
        
        return {
            "id": node["id"],
            "type": labels[0] if labels else "Unknown",
            "properties": dict(node)
        }
    
    def search_entities(self, entity_type: str, filters: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Search entities by type and filters"""
        # Build WHERE clause from filters
        where_clauses = []
        parameters = {"skip": skip, "limit": limit}
        
        for key, value in filters.items():
            where_clauses.append(f"n.{key} = ${key}")
            parameters[key] = value
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
        MATCH (n:{entity_type})
        WHERE {where_clause}
        RETURN n
        SKIP $skip
        LIMIT $limit
        """
        
        result = neo4j_client.execute_read(query, parameters)
        
        return [
            {
                "id": record["n"]["id"],
                "type": entity_type,
                "properties": dict(record["n"])
            }
            for record in result
        ]
    
    # ========== Relationship Instance Management ==========
    
    def create_relationship(self, rel_data: RelationshipCreate) -> Dict[str, Any]:
        """Create a relationship instance in Neo4j"""
        # Verify relationship type exists
        rel_type = self.db.query(RelationshipType).filter(RelationshipType.name == rel_data.type).first()
        if not rel_type:
            raise HTTPException(status_code=404, detail=f"Relationship type '{rel_data.type}' not found")
        
        # Create relationship in Neo4j
        query = f"""
        MATCH (from), (to)
        WHERE from.id = $from_id AND to.id = $to_id
        CREATE (from)-[r:{rel_data.type} $properties]->(to)
        SET r.id = toString(id(r))
        SET r.created_at = datetime()
        RETURN r, from.id as from_id, to.id as to_id
        """
        
        result = neo4j_client.execute_write(query, {
            "from_id": rel_data.from_entity_id,
            "to_id": rel_data.to_entity_id,
            "properties": rel_data.properties
        })
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create relationship")
        
        rel = result[0]["r"]
        
        logger.info(f"Created relationship {rel_data.type} from {rel_data.from_entity_id} to {rel_data.to_entity_id}")
        
        return {
            "id": rel["id"],
            "type": rel_data.type,
            "from_entity_id": rel_data.from_entity_id,
            "to_entity_id": rel_data.to_entity_id,
            "properties": dict(rel)
        }
    
    # ========== Helper Methods ==========
    
    def _create_neo4j_entity_constraint(self, entity_type_name: str):
        """Create Neo4j uniqueness constraint for entity type"""
        try:
            query = f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:{entity_type_name}) REQUIRE n.id IS UNIQUE"
            neo4j_client.execute_write(query)
        except Exception as e:
            logger.warning(f"Failed to create constraint for {entity_type_name}: {e}")
