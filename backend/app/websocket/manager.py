from typing import Dict, Set
from fastapi import WebSocket
import json
import uuid


class ConnectionManager:
    """WebSocket connection manager for real-time notifications."""
    
    def __init__(self):
        # user_id -> set of WebSocket connections
        self.active_connections: Dict[uuid.UUID, Set[WebSocket]] = {}
    
    async def connect(self, user_id: uuid.UUID, websocket: WebSocket):
        """Accept and store WebSocket connection."""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
    
    def disconnect(self, user_id: uuid.UUID, websocket: WebSocket):
        """Remove WebSocket connection."""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            
            # Clean up empty sets
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    async def send_personal_message(self, user_id: uuid.UUID, message: dict):
        """Send message to specific user's all connections."""
        if user_id in self.active_connections:
            disconnected = set()
            
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.add(connection)
            
            # Remove failed connections
            for conn in disconnected:
                self.disconnect(user_id, conn)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected users."""
        for user_id in list(self.active_connections.keys()):
            await self.send_personal_message(user_id, message)


manager = ConnectionManager()
