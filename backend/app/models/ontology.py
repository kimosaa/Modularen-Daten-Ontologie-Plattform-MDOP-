"""
Ontology Models
Defines the core ontology data structures
"""
from sqlalchemy import Column, String, Integer, JSON, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.postgres_client import Base


class EntityType(Base):
    """
    Entity Type Definition
    Represents a class of entities in the ontology (e.g., Person, Company, Location)
    """
    __tablename__ = "entity_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    label = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    color = Column(String(20), nullable=True)
    properties = Column(JSON, nullable=False, default=dict)  # JSON schema for properties
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    relationships_from = relationship("RelationshipType", foreign_keys="RelationshipType.from_entity_type_id", back_populates="from_entity")
    relationships_to = relationship("RelationshipType", foreign_keys="RelationshipType.to_entity_type_id", back_populates="to_entity")


class RelationshipType(Base):
    """
    Relationship Type Definition
    Defines how two entity types can be related (e.g., WORKS_AT, LOCATED_IN)
    """
    __tablename__ = "relationship_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    label = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    from_entity_type_id = Column(Integer, ForeignKey("entity_types.id"), nullable=False)
    to_entity_type_id = Column(Integer, ForeignKey("entity_types.id"), nullable=False)
    properties = Column(JSON, nullable=False, default=dict)  # Relationship properties schema
    is_directed = Column(Boolean, default=True)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    from_entity = relationship("EntityType", foreign_keys=[from_entity_type_id], back_populates="relationships_from")
    to_entity = relationship("EntityType", foreign_keys=[to_entity_type_id], back_populates="relationships_to")


class OntologyVersion(Base):
    """
    Ontology Version Tracking
    Maintains version history of ontology changes
    """
    __tablename__ = "ontology_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    schema_snapshot = Column(JSON, nullable=False)  # Complete ontology schema at this version
    created_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DataConnector(Base):
    """
    Data Connector Configuration
    Stores configuration for data source connectors
    """
    __tablename__ = "data_connectors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    type = Column(String(50), nullable=False)  # postgresql, mongodb, rest, csv, etc.
    config = Column(JSON, nullable=False)  # Connection configuration
    mapping = Column(JSON, nullable=False)  # Schema mapping to ontology
    is_active = Column(Boolean, default=True)
    last_sync_at = Column(DateTime(timezone=True), nullable=True)
    sync_status = Column(String(50), default="pending")  # pending, running, success, error
    sync_error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
