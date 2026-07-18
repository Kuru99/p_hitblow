from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import asyncio
import websockets

app = FastAPI()

# GUI を返す
@app.get("/")
def gui():
    return FileResponse("src/hitblow/web/static/index.html")


# WebSocket サーバー（既存コードを流用）
async def handler(websocket):
    while True:
        msg = await websocket.recv()
        await websocket.send(f"受信: {msg}")


async def start_ws():
    # Render が割り当てるポートを使う（絶対にこれ）
    PORT = int(os.environ.get("PORT", 8765))
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()


# FastAPI と WebSocket を同時起動
import threading
threading.Thread(target=lambda: asyncio.run(start_ws()), daemon=True).start()
