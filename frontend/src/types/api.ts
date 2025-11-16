/**
 * API Type Definitions
 */

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface HealthStatus {
  status: 'healthy' | 'unhealthy';
  version: string;
  services: {
    neo4j: boolean;
    postgres: boolean;
    redis: boolean;
  };
}

export interface QueryRequest {
  query: string;
  parameters?: Record<string, any>;
}

export interface QueryResponse {
  results: any[];
  count: number;
  execution_time_ms: number;
}
