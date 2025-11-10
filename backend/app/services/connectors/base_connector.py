"""
Base Data Connector
Abstract base class for all data connector implementations
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Iterator
from dataclasses import dataclass
from enum import Enum
import time

from app.core.logging import logger


class ConnectorStatus(Enum):
    """Connector status enumeration"""
    IDLE = "idle"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    SYNCING = "syncing"
    ERROR = "error"
    DISCONNECTED = "disconnected"


@dataclass
class SyncResult:
    """Data sync result"""
    success: bool
    records_processed: int
    records_failed: int
    duration_seconds: float
    error_message: Optional[str] = None


class BaseConnector(ABC):
    """
    Abstract base class for data connectors
    
    All data connector implementations must inherit from this class
    and implement the required abstract methods.
    """
    
    def __init__(self, connector_id: str, config: Dict[str, Any], mapping: Dict[str, Any]):
        """
        Initialize connector
        
        Args:
            connector_id: Unique connector identifier
            config: Connector configuration (connection details, credentials, etc.)
            mapping: Schema mapping from source to ontology
        """
        self.connector_id = connector_id
        self.config = config
        self.mapping = mapping
        self.status = ConnectorStatus.IDLE
        self._connection = None
    
    @abstractmethod
    async def connect(self) -> bool:
        """
        Establish connection to data source
        
        Returns:
            True if connection successful
        """
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """
        Close connection to data source
        
        Returns:
            True if disconnection successful
        """
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """
        Test connectivity to data source
        
        Returns:
            True if connection can be established
        """
        pass
    
    @abstractmethod
    async def detect_schema(self) -> Dict[str, Any]:
        """
        Automatically detect schema from data source
        
        Returns:
            Detected schema structure
        """
        pass
    
    @abstractmethod
    async def fetch_data(
        self, 
        full_sync: bool = False, 
        batch_size: int = 1000
    ) -> Iterator[List[Dict[str, Any]]]:
        """
        Fetch data from source
        
        Args:
            full_sync: If True, fetch all data. If False, fetch only changed data (CDC)
            batch_size: Number of records per batch
            
        Yields:
            Batches of records
        """
        pass
    
    async def sync(self, full_sync: bool = False) -> SyncResult:
        """
        Execute data synchronization
        
        Args:
            full_sync: If True, perform full sync. If False, incremental sync (CDC)
            
        Returns:
            Sync result with statistics
        """
        start_time = time.time()
        records_processed = 0
        records_failed = 0
        
        try:
            self.status = ConnectorStatus.SYNCING
            logger.info(f"Starting {'full' if full_sync else 'incremental'} sync for connector {self.connector_id}")
            
            # Connect if not connected
            if self.status != ConnectorStatus.CONNECTED:
                await self.connect()
            
            # Fetch and process data in batches
            async for batch in self.fetch_data(full_sync=full_sync):
                try:
                    # Transform data according to mapping
                    transformed_batch = self._transform_batch(batch)
                    
                    # Load data into graph
                    loaded = await self._load_to_graph(transformed_batch)
                    
                    records_processed += loaded
                    logger.debug(f"Processed batch of {loaded} records")
                    
                except Exception as e:
                    records_failed += len(batch)
                    logger.error(f"Failed to process batch: {e}")
            
            duration = time.time() - start_time
            self.status = ConnectorStatus.CONNECTED
            
            logger.info(f"Sync completed: {records_processed} processed, {records_failed} failed in {duration:.2f}s")
            
            return SyncResult(
                success=True,
                records_processed=records_processed,
                records_failed=records_failed,
                duration_seconds=duration
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.status = ConnectorStatus.ERROR
            logger.error(f"Sync failed: {e}")
            
            return SyncResult(
                success=False,
                records_processed=records_processed,
                records_failed=records_failed,
                duration_seconds=duration,
                error_message=str(e)
            )
    
    def _transform_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform data batch according to mapping
        
        Args:
            batch: Raw data records
            
        Returns:
            Transformed records
        """
        transformed = []
        
        for record in batch:
            try:
                transformed_record = self._transform_record(record)
                transformed.append(transformed_record)
            except Exception as e:
                logger.warning(f"Failed to transform record: {e}")
        
        return transformed
    
    def _transform_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform single record according to mapping
        
        Args:
            record: Raw record
            
        Returns:
            Transformed record
        """
        # Extract entity type from mapping
        entity_type = self.mapping.get("entity_type")
        
        # Extract field mappings
        field_mappings = self.mapping.get("field_mappings", {})
        
        # Transform fields
        properties = {}
        for target_field, source_field in field_mappings.items():
            if source_field in record:
                properties[target_field] = record[source_field]
        
        return {
            "type": entity_type,
            "properties": properties
        }
    
    async def _load_to_graph(self, records: List[Dict[str, Any]]) -> int:
        """
        Load transformed records into Neo4j graph
        
        Args:
            records: Transformed records
            
        Returns:
            Number of records loaded
        """
        from app.db.neo4j_client import neo4j_client
        
        loaded = 0
        
        for record in records:
            try:
                entity_type = record["type"]
                properties = record["properties"]
                
                query = f"""
                CREATE (n:{entity_type} $properties)
                SET n.id = toString(id(n))
                SET n.created_at = datetime()
                RETURN n
                """
                
                neo4j_client.execute_write(query, {"properties": properties})
                loaded += 1
                
            except Exception as e:
                logger.error(f"Failed to load record to graph: {e}")
        
        return loaded
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get connector status
        
        Returns:
            Status information
        """
        return {
            "connector_id": self.connector_id,
            "status": self.status.value,
            "config": {k: "***" if "password" in k.lower() or "secret" in k.lower() else v 
                      for k, v in self.config.items()}
        }
