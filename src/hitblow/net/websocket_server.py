# src/hitblow/net/websocket_server.py

import asyncio
import websockets
import json
import os

from hitblow.core import make_secret, judge
from hitblow.net.protocol import (
    msg_your_turn,
    msg_guess,
    msg_result,
    msg_win
)

# Render が割り当てるポート番号
PORT = int(os.environ.get("PORT", 8765))

# 接続中のクライアントを保持
connected = []


async def handler(ws):
    """クライアント接続時に呼ばれる"""
    connected.append(ws)
    print("Client connected")

    # 2人揃ったらゲーム開始
    if len(connected) == 2:
        asyncio.create_task(game_loop())

    try:
        # クライアントからのメッセージは game_loop 側で処理するのでここでは何もしない
        async for _ in ws:
            pass
    finally:
        connected.remove(ws)


async def game_loop():
    """ゲーム進行のメインループ"""
    secret = make_secret(3)
    print(f"Secret: {secret}")

    turn = 0  # 0: Player1, 1: Player2

    while True:
        # ターン通知
        await connected[turn].send(json.dumps(msg_your_turn(turn)))

        # 入力待ち
        msg = await connected[turn].recv()
        data = json.loads(msg)
        guess = data["value"]

        # 判定
        hit, blow = judge(secret, guess)

        # 全員に結果通知
        for ws in connected:
            await ws.send(json.dumps(
                msg_result(turn, guess, hit, blow)
            ))

        # 勝利判定
        if hit == 3:
            for ws in connected:
                await ws.send(json.dumps(
                    msg_win(turn, secret)
                ))
            break

        # ターン交代
        turn = 1 - turn


async def main():
    """Render で起動されるエントリポイント"""
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"Server started on port {PORT}")
        await asyncio.Future()  # 永久に待つ


def run():
    """コマンドラインエントリポイント用の同期ラッパー"""
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())

