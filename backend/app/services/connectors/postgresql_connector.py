"""
PostgreSQL Data Connector
Connector implementation for PostgreSQL databases
"""
import psycopg2
import psycopg2.extras
from typing import Dict, Any, List, Iterator
from app.services.connectors.base_connector import BaseConnector, ConnectorStatus
from app.core.logging import logger


class PostgreSQLConnector(BaseConnector):
    """
    PostgreSQL Database Connector
    
    Connects to PostgreSQL databases and syncs data to the graph
    """
    
    def __init__(self, connector_id: str, config: Dict[str, Any], mapping: Dict[str, Any]):
        super().__init__(connector_id, config, mapping)
        self._connection = None
        self._cursor = None
    
    async def connect(self) -> bool:
        """Establish connection to PostgreSQL"""
        try:
            self.status = ConnectorStatus.CONNECTING
            
            self._connection = psycopg2.connect(
                host=self.config.get("host"),
                port=self.config.get("port", 5432),
                database=self.config.get("database"),
                user=self.config.get("user"),
                password=self.config.get("password")
            )
            
            self._cursor = self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            self.status = ConnectorStatus.CONNECTED
            
            logger.info(f"Connected to PostgreSQL: {self.config.get('host')}/{self.config.get('database')}")
            return True
            
        except Exception as e:
            self.status = ConnectorStatus.ERROR
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            return False
    
    async def disconnect(self) -> bool:
        """Close PostgreSQL connection"""
        try:
            if self._cursor:
                self._cursor.close()
            if self._connection:
                self._connection.close()
            
            self.status = ConnectorStatus.DISCONNECTED
            logger.info("Disconnected from PostgreSQL")
            return True
            
        except Exception as e:
            logger.error(f"Error disconnecting from PostgreSQL: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """Test PostgreSQL connectivity"""
        try:
            conn = psycopg2.connect(
                host=self.config.get("host"),
                port=self.config.get("port", 5432),
                database=self.config.get("database"),
                user=self.config.get("user"),
                password=self.config.get("password")
            )
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    async def detect_schema(self) -> Dict[str, Any]:
        """
        Detect schema from PostgreSQL table
        
        Returns:
            Schema information including columns and data types
        """
        table_name = self.mapping.get("source_table")
        
        if not table_name:
            raise ValueError("source_table not specified in mapping")
        
        if not self._cursor:
            await self.connect()
        
        # Query table schema
        query = """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position
        """
        
        self._cursor.execute(query, (table_name,))
        columns = self._cursor.fetchall()
        
        schema = {
            "table": table_name,
            "columns": []
        }
        
        for col in columns:
            schema["columns"].append({
                "name": col["column_name"],
                "type": col["data_type"],
                "nullable": col["is_nullable"] == "YES"
            })
        
        logger.info(f"Detected schema for {table_name}: {len(schema['columns'])} columns")
        return schema
    
    async def fetch_data(
        self,
        full_sync: bool = False,
        batch_size: int = 1000
    ) -> Iterator[List[Dict[str, Any]]]:
        """
        Fetch data from PostgreSQL table
        
        Args:
            full_sync: If True, fetch all data. If False, fetch only changed data
            batch_size: Number of records per batch
            
        Yields:
            Batches of records
        """
        table_name = self.mapping.get("source_table")
        
        if not table_name:
            raise ValueError("source_table not specified in mapping")
        
        if not self._cursor:
            await self.connect()
        
        # Build query
        if full_sync:
            query = f"SELECT * FROM {table_name}"
        else:
            # For incremental sync, use timestamp column if specified
            timestamp_column = self.mapping.get("timestamp_column")
            if timestamp_column:
                # TODO: Implement incremental sync based on last sync timestamp
                query = f"SELECT * FROM {table_name}"
            else:
                query = f"SELECT * FROM {table_name}"
        
        # Execute query with server-side cursor for large datasets
        cursor_name = f"{self.connector_id}_cursor"
        self._cursor = self._connection.cursor(cursor_name, cursor_factory=psycopg2.extras.RealDictCursor)
        self._cursor.execute(query)
        
        # Fetch in batches
        while True:
            batch = self._cursor.fetchmany(batch_size)
            if not batch:
                break
            
            # Convert to list of dicts
            yield [dict(record) for record in batch]
        
        self._cursor.close()
        self._cursor = self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
