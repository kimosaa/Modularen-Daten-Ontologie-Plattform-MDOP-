"""
WebSocket Manager
Manages WebSocket connections for real-time updates
"""
from typing import Dict, Set
from fastapi import WebSocket
import json
import asyncio
from app.core.logging import logger


class WebSocketManager:
    """Manages WebSocket connections and broadcasts"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.connection_channels: Dict[WebSocket, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, channel: str = "default"):
        """
        Accept and register a new WebSocket connection
        
        Args:
            websocket: WebSocket connection
            channel: Channel name for targeted broadcasts
        """
        await websocket.accept()
        
        if channel not in self.active_connections:
            self.active_connections[channel] = set()
        
        self.active_connections[channel].add(websocket)
        
        if websocket not in self.connection_channels:
            self.connection_channels[websocket] = set()
        
        self.connection_channels[websocket].add(channel)
        
        logger.info(f"WebSocket connected to channel '{channel}'. Total connections: {self.get_connection_count()}")
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection
        
        Args:
            websocket: WebSocket connection to remove
        """
        if websocket in self.connection_channels:
            channels = self.connection_channels[websocket].copy()
            for channel in channels:
                if channel in self.active_connections:
                    self.active_connections[channel].discard(websocket)
                    if not self.active_connections[channel]:
                        del self.active_connections[channel]
            
            del self.connection_channels[websocket]
        
        logger.info(f"WebSocket disconnected. Total connections: {self.get_connection_count()}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        Send message to a specific connection
        
        Args:
            message: Message data
            websocket: Target WebSocket connection
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: dict, channel: str = "default"):
        """
        Broadcast message to all connections in a channel
        
        Args:
            message: Message data
            channel: Target channel
        """
        if channel not in self.active_connections:
            return
        
        disconnected = []
        
        for connection in self.active_connections[channel]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
    
    async def broadcast_entity_created(self, entity_type: str, entity_data: dict):
        """Broadcast entity creation event"""
        await self.broadcast({
            "event": "entity_created",
            "entity_type": entity_type,
            "data": entity_data
        }, channel="graph_updates")
    
    async def broadcast_entity_updated(self, entity_type: str, entity_id: str, entity_data: dict):
        """Broadcast entity update event"""
        await self.broadcast({
            "event": "entity_updated",
            "entity_type": entity_type,
            "entity_id": entity_id,
            "data": entity_data
        }, channel="graph_updates")
    
    async def broadcast_relationship_created(self, rel_data: dict):
        """Broadcast relationship creation event"""
        await self.broadcast({
            "event": "relationship_created",
            "data": rel_data
        }, channel="graph_updates")
    
    def get_connection_count(self) -> int:
        """Get total number of active connections"""
        return sum(len(connections) for connections in self.active_connections.values())


# Global WebSocket manager instance
ws_manager = WebSocketManager()
