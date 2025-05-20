import asyncio
import websockets

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
    async with websockets.serve(relay, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())