"""
Ontology Schemas
Pydantic models for API request/response validation
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


# Entity Type Schemas
class EntityTypeBase(BaseModel):
    """Base schema for Entity Type"""
    name: str = Field(..., min_length=1, max_length=255, description="Unique entity type name")
    label: str = Field(..., min_length=1, max_length=255, description="Display label")
    description: Optional[str] = Field(None, description="Entity type description")
    icon: Optional[str] = Field(None, max_length=50, description="Icon identifier")
    color: Optional[str] = Field(None, max_length=20, description="Color code")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Property definitions")


class EntityTypeCreate(EntityTypeBase):
    """Schema for creating an entity type"""
    pass


class EntityTypeUpdate(BaseModel):
    """Schema for updating an entity type"""
    label: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None


class EntityTypeResponse(EntityTypeBase):
    """Schema for entity type response"""
    id: int
    version: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Relationship Type Schemas
class RelationshipTypeBase(BaseModel):
    """Base schema for Relationship Type"""
    name: str = Field(..., min_length=1, max_length=255, description="Unique relationship name")
    label: str = Field(..., min_length=1, max_length=255, description="Display label")
    description: Optional[str] = Field(None, description="Relationship description")
    from_entity_type_id: int = Field(..., description="Source entity type ID")
    to_entity_type_id: int = Field(..., description="Target entity type ID")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Relationship properties")
    is_directed: bool = Field(True, description="Whether relationship is directed")


class RelationshipTypeCreate(RelationshipTypeBase):
    """Schema for creating a relationship type"""
    pass


class RelationshipTypeUpdate(BaseModel):
    """Schema for updating a relationship type"""
    label: Optional[str] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    is_directed: Optional[bool] = None


class RelationshipTypeResponse(RelationshipTypeBase):
    """Schema for relationship type response"""
    id: int
    version: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Entity Instance Schemas (for actual graph nodes)
class EntityCreate(BaseModel):
    """Schema for creating an entity instance"""
    type: str = Field(..., description="Entity type name")
    properties: Dict[str, Any] = Field(..., description="Entity properties")


class EntityResponse(BaseModel):
    """Schema for entity instance response"""
    id: str = Field(..., description="Neo4j node ID")
    type: str
    properties: Dict[str, Any]


# Relationship Instance Schemas
class RelationshipCreate(BaseModel):
    """Schema for creating a relationship instance"""
    type: str = Field(..., description="Relationship type name")
    from_entity_id: str = Field(..., description="Source entity ID")
    to_entity_id: str = Field(..., description="Target entity ID")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Relationship properties")


class RelationshipResponse(BaseModel):
    """Schema for relationship instance response"""
    id: str = Field(..., description="Neo4j relationship ID")
    type: str
    from_entity_id: str
    to_entity_id: str
    properties: Dict[str, Any]


# Ontology Version Schemas
class OntologyVersionResponse(BaseModel):
    """Schema for ontology version response"""
    id: int
    version: int
    description: Optional[str]
    created_by: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Graph Query Schemas
class GraphQueryRequest(BaseModel):
    """Schema for graph query request"""
    query: str = Field(..., description="Cypher query string")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Query parameters")


class GraphQueryResponse(BaseModel):
    """Schema for graph query response"""
    results: List[Dict[str, Any]]
    count: int
    execution_time_ms: float
