import asyncio
import websockets
import json

async def send_message():
    uri = "ws://yourdomain/ws/some_path/"
    async with websockets.connect(uri) as websocket:
        message = "Hello from backend!"
        await websocket.send(json.dumps({'message': message}))
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.get_event_loop().run_until_complete(send_message())
