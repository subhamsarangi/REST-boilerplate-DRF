import asyncio
import websockets
import json

async def send_message():
    uri = "ws://localhost:8000/ws/sockette/"
    print(f"Connecting to WebSocket at {uri}")

    try:
        async with websockets.connect(uri) as websocket:
            print("Connection established")

            message = "Hello from backend!"
            print(f"Sending message: {message}")
            await websocket.send(json.dumps({'message': message}))
            
            print("Message sent, waiting for response...")
            response = await websocket.recv()
            print(f"Received: {response}")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket connection closed with error: {e}")
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"Invalid status code received: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.get_event_loop().run_until_complete(send_message())
