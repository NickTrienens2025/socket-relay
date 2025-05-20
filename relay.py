import asyncio
import websockets
import os
from aiohttp import web

connected_clients = set()

async def health_check(request):
    return web.Response(status=200)

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
    port = int(os.getenv("PORT", 80))
    
    # Create HTTP app for health check
    app = web.Application()
    app.router.add_get('/health', health_check)
    
    # Start HTTP server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    # Start WebSocket server
    async with websockets.serve(relay, "0.0.0.0", port + 1):
        print(f"WebSocket relay server started on port {port + 1}")
        print(f"Health check endpoint available at http://0.0.0.0:{port}/health")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())