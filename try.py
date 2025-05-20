# test_client.py
import asyncio
import websockets

async def listen():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello from client!")
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")

asyncio.run(listen())