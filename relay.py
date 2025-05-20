import asyncio
import os
from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
import uvicorn
from typing import Set

app = FastAPI()
connected_clients: Set[WebSocket] = set()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/connections")
async def get_connections():
    return {
        "total_connections": len(connected_clients),
        "connection_ids": [id(client) for client in connected_clients]
    }

@app.websocket("/ws")
async def relay(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            # Broadcast to all clients except sender
            await asyncio.gather(*[
                client.send_text(message)
                for client in connected_clients
                if client != websocket
            ])
    except Exception:
        pass
    finally:
        connected_clients.remove(websocket)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8888))
    uvicorn.run(app, host="0.0.0.0", port=port)