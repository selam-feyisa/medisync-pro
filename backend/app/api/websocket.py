from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from uuid import UUID
from app.core.security import get_current_user_ws
from app.websocket.manager import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
):
    """WebSocket endpoint for real-time notifications."""
    try:
        # Authenticate user from token
        user = await get_current_user_ws(token)
        
        # Connect to manager
        await manager.connect(user.id, websocket)
        
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "message": "WebSocket connected successfully",
            "user_id": str(user.id)
        })
        
        try:
            # Keep connection alive and listen for messages
            while True:
                data = await websocket.receive_text()
                # Echo back or handle client messages
                await websocket.send_json({
                    "type": "echo",
                    "message": f"Received: {data}"
                })
        except WebSocketDisconnect:
            manager.disconnect(user.id, websocket)
            
    except Exception as e:
        await websocket.close(code=4000, reason=str(e))
