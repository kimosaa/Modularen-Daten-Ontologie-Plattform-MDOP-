/**
 * Ontology Service
 * API calls for ontology management
 */
import { api } from './api';
import { EntityType, RelationshipType, Entity, Relationship } from '@types/ontology';

export const ontologyService = {
  // Entity Types
  async getEntityTypes(): Promise<EntityType[]> {
    return api.get<EntityType[]>('/ontology/entity-types');
  },

  async getEntityType(id: number): Promise<EntityType> {
    return api.get<EntityType>(`/ontology/entity-types/${id}`);
  },

  async createEntityType(data: Partial<EntityType>): Promise<EntityType> {
    return api.post<EntityType>('/ontology/entity-types', data);
  },

  async updateEntityType(id: number, data: Partial<EntityType>): Promise<EntityType> {
    return api.put<EntityType>(`/ontology/entity-types/${id}`, data);
  },

  async deleteEntityType(id: number): Promise<void> {
    return api.delete<void>(`/ontology/entity-types/${id}`);
  },

  // Relationship Types
  async getRelationshipTypes(): Promise<RelationshipType[]> {
    return api.get<RelationshipType[]>('/ontology/relationship-types');
  },

  async createRelationshipType(data: Partial<RelationshipType>): Promise<RelationshipType> {
    return api.post<RelationshipType>('/ontology/relationship-types', data);
  },

  // Entities
  async getEntities(type: string, params?: any): Promise<Entity[]> {
    return api.get<Entity[]>('/ontology/entities', { params: { entity_type: type, ...params } });
  },

  async getEntity(id: string): Promise<Entity> {
    return api.get<Entity>(`/ontology/entities/${id}`);
  },

  async createEntity(data: Partial<Entity>): Promise<Entity> {
    return api.post<Entity>('/ontology/entities', data);
  },

  // Relationships
  async createRelationship(data: Partial<Relationship>): Promise<Relationship> {
    return api.post<Relationship>('/ontology/relationships', data);
  },

  // Graph Queries
  async executeQuery(query: string, parameters?: Record<string, any>): Promise<any> {
    return api.post('/query/cypher', { query, parameters });
  },
};
