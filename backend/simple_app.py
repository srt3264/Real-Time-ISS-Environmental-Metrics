from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import datetime
from backend.db_manager import get_historical_data
from typing import Optional
from datetime import datetime, timezone


app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000", # Old React local
    "https://curly-space-orbit-9rw97jj7j54cx7q-3000.app.github.dev", # Old React Codespace
    "http://localhost:8080", # New Vue local (or 5173 if using Vite)
    "https://curly-space-orbit-9rw97jj7j54cx7q-8080.app.github.dev" # <--- ADD YOUR NEW VUE APP'S CODESPACE URL HERE (adjust port if needed)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
     return {"message": "Hello from Simple FastAPI!", "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}



@app.get("/api/data/{table_name}")
async def api_get_data(
    table_name: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    limit: Optional[int] = None
):
    def parse(dt_str):
        return datetime.fromisoformat(dt_str).astimezone(timezone.utc)

    start_dt = parse(start_time) if start_time else None
    end_dt = parse(end_time) if end_time else None

    try:
        df = get_historical_data(table_name, start_dt=start_dt, end_dt=end_dt, limit=limit)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

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