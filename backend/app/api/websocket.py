"""
WebSocket API Endpoints
Real-time communication endpoints
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import ws_manager
from app.core.logging import logger


router = APIRouter(prefix="/ws", tags=["WebSocket"])


@router.websocket("/graph")
async def websocket_graph_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time graph updates
    
    Clients can subscribe to graph changes and receive real-time updates
    when entities or relationships are created/updated/deleted.
    """
    await ws_manager.connect(websocket, channel="graph_updates")
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_json()
            
            # Handle different message types
            message_type = data.get("type")
            
            if message_type == "ping":
                await ws_manager.send_personal_message({"type": "pong"}, websocket)
            
            elif message_type == "subscribe":
                # Handle channel subscription
                channel = data.get("channel", "default")
                await ws_manager.connect(websocket, channel)
                await ws_manager.send_personal_message({
                    "type": "subscribed",
                    "channel": channel
                }, websocket)
            
            else:
                logger.warning(f"Unknown WebSocket message type: {message_type}")
    
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)


@router.websocket("/notifications")
async def websocket_notifications_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for system notifications
    
    Clients receive general system notifications, alerts, and status updates.
    """
    await ws_manager.connect(websocket, channel="notifications")
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "ping":
                await ws_manager.send_personal_message({"type": "pong"}, websocket)
    
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    
    except Exception as e:
        logger.error(f"WebSocket notifications error: {e}")
        ws_manager.disconnect(websocket)
