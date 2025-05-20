import asyncio
import websockets
import os

connected_clients = set()

async def relay(websocket, path):
    # Register client
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast to all clients except sender
            await asyncio.gather(*[
                client.send(message)
                for client in connected_clients
                if client != websocket
            ])
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)

async def main():
    port = int(os.getenv("PORT", 8080))
    async with websockets.serve(relay, "0.0.0.0", port):
        print(f"WebSocket relay server started on port {port}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())