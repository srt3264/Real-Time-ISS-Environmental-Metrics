from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI()

# Configure CORS
allow_origins=[
    "http://localhost:3000",
    "https://curly-space-orbit-9rw97jj7j54cx7q-3000.app.github.dev" # <--- ENSURE THIS IS PRESENT AND EXACT
],

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins, # Use the defined origins list
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
    expose_headers=["*"]
)

@app.get("/")
async def read_root():
    return {"message": "Hello from Simple FastAPI!", "server_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

@app.websocket("/ws/echo")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected!")

    import asyncio
    async def send_heartbeat():
        while True:
            await websocket.send_text(f"Server Heartbeat: {datetime.datetime.now().strftime('%H:%M:%S')}")
            await asyncio.sleep(3)

    heartbeat_task = asyncio.create_task(send_heartbeat())

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("WebSocket disconnected!")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        heartbeat_task.cancel()
        print("WebSocket cleanup complete.")