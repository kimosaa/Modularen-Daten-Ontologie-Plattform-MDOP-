/**
 * Ontology Type Definitions
 * Matches backend API schemas
 */

export interface EntityType {
  id: number;
  name: string;
  label: string;
  description?: string;
  icon?: string;
  color?: string;
  properties: Record<string, PropertySchema>;
  version: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface PropertySchema {
  type: 'string' | 'integer' | 'float' | 'boolean' | 'date' | 'datetime';
  required?: boolean;
  default?: any;
  description?: string;
}

export interface RelationshipType {
  id: number;
  name: string;
  label: string;
  description?: string;
  from_entity_type_id: number;
  to_entity_type_id: number;
  properties: Record<string, PropertySchema>;
  is_directed: boolean;
  version: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface Entity {
  id: string;
  type: string;
  properties: Record<string, any>;
}

export interface Relationship {
  id: string;
  type: string;
  from_entity_id: string;
  to_entity_id: string;
  properties: Record<string, any>;
}

export interface GraphNode {
  id: string;
  type: string;
  label: string;
  properties: Record<string, any>;
  x?: number;
  y?: number;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  label: string;
  properties: Record<string, any>;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}
