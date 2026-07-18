from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import asyncio
import json

from hitblow.core import make_secret, judge
from hitblow.net.protocol import (
    msg_your_turn,
    msg_result,
    msg_win,
)

app = FastAPI()

# 接続中のクライアントを保持
connected: list[WebSocket] = []
game_task: asyncio.Task | None = None


# GUI を返す
@app.get("/")
def gui():
    return FileResponse("src/hitblow/web/static/index.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global game_task

    await websocket.accept()
    connected.append(websocket)
    print(f"Client connected. Total: {len(connected)}")

    # 2人揃ったらゲーム開始
    if len(connected) == 2 and game_task is None:
        game_task = asyncio.create_task(game_loop())

    try:
        # クライアントからのメッセージは game_loop 側で処理する
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("Client disconnected")
        if websocket in connected:
            connected.remove(websocket)
        game_task = None


async def game_loop():
    """ゲーム進行のメインループ"""
    global game_task

    secret = make_secret(3)
    print(f"Secret: {secret}")

    turn = 0  # 0: Player1, 1: Player2

    try:
        while True:
            # 接続が2人揃っていなければ終了
            if len(connected) < 2:
                print("Player disconnected. Ending game.")
                break

            # ターン通知
            await connected[turn].send_text(json.dumps(msg_your_turn(turn)))

            # 入力待ち
            msg = await connected[turn].receive_text()
            data = json.loads(msg)
            guess = data["value"]

            # 判定
            hit, blow = judge(secret, guess)

            # 全員に結果通知
            for ws in connected:
                await ws.send_text(json.dumps(
                    msg_result(turn, guess, hit, blow)
                ))

            # 勝利判定
            if hit == 3:
                for ws in connected:
                    await ws.send_text(json.dumps(
                        msg_win(turn, secret)
                    ))
                break

            # ターン交代
            turn = 1 - turn
    finally:
        game_task = None