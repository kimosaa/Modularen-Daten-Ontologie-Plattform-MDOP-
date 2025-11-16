"""
Neo4j Graph Database Client
Manages connections to Neo4j graph database
"""
from typing import Dict, List, Any, Optional
from neo4j import GraphDatabase, Driver, Session
from app.core.config import settings
from app.core.logging import logger


class Neo4jClient:
    """Neo4j Database Client"""
    
    def __init__(self):
        self.driver: Optional[Driver] = None
        self.uri = settings.NEO4J_URI
        self.user = settings.NEO4J_USER
        self.password = settings.NEO4J_PASSWORD
        self.database = settings.NEO4J_DATABASE
    
    def connect(self):
        """Establish connection to Neo4j"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Verify connectivity
            self.driver.verify_connectivity()
            logger.info(f"Connected to Neo4j at {self.uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")
    
    def execute_query(
        self, 
        query: str, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute Cypher query
        
        Args:
            query: Cypher query string
            parameters: Query parameters
            
        Returns:
            List of result records as dictionaries
        """
        with self.driver.session(database=self.database) as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]
    
    def execute_write(
        self, 
        query: str, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute write transaction
        
        Args:
            query: Cypher query string
            parameters: Query parameters
            
        Returns:
            List of result records as dictionaries
        """
        def _execute(tx):
            result = tx.run(query, parameters or {})
            return [dict(record) for record in result]
        
        with self.driver.session(database=self.database) as session:
            return session.execute_write(_execute)
    
    def execute_read(
        self, 
        query: str, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute read transaction
        
        Args:
            query: Cypher query string
            parameters: Query parameters
            
        Returns:
            List of result records as dictionaries
        """
        def _execute(tx):
            result = tx.run(query, parameters or {})
            return [dict(record) for record in result]
        
        with self.driver.session(database=self.database) as session:
            return session.execute_read(_execute)
    
    def create_indexes(self):
        """Create necessary indexes for performance"""
        indexes = [
            "CREATE INDEX entity_type_idx IF NOT EXISTS FOR (n:Entity) ON (n.type)",
            "CREATE INDEX entity_id_idx IF NOT EXISTS FOR (n:Entity) ON (n.id)",
            "CREATE INDEX relationship_type_idx IF NOT EXISTS FOR ()-[r:RELATES_TO]-() ON (r.type)",
        ]
        
        for index_query in indexes:
            try:
                self.execute_write(index_query)
                logger.info(f"Created index: {index_query[:50]}...")
            except Exception as e:
                logger.warning(f"Index creation failed: {e}")
    
    def health_check(self) -> bool:
        """Check Neo4j connection health"""
        try:
            result = self.execute_read("RETURN 1 as health")
            return len(result) > 0 and result[0].get("health") == 1
        except Exception as e:
            logger.error(f"Neo4j health check failed: {e}")
            return False


# Global Neo4j client instance
neo4j_client = Neo4jClient()
