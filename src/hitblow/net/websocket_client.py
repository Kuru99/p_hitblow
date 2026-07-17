# src/hitblow/net/websocket_client.py

import asyncio
import websockets
import json

from hitblow.net.protocol import (
    msg_guess
)

async def run_client(host: str):
    """WebSocket サーバーに接続してゲームをプレイする"""
    url = f"ws://{host}"
    print(f"Connecting to {url} ...")

    async with websockets.connect(url) as ws:
        print("Connected to server.")

        async for msg in ws:
            data = json.loads(msg)

            msg_type = data.get("type")

            # --- ターン通知 ---
            if msg_type == "your_turn":
                player = data["player"]
                print(f"あなたのターンです（Player{player}）")

                guess = input("予想を入力してください > ").strip()
                await ws.send(json.dumps(msg_guess(guess)))

            # --- 結果通知 ---
            elif msg_type == "result":
                player = data["player"]
                guess = data["guess"]
                hit = data["hit"]
                blow = data["blow"]

                print(f"Player{player} の予想 {guess} → Hit={hit} Blow={blow}")

            # --- 勝利通知 ---
            elif msg_type == "win":
                winner = data["winner"]
                answer = data["answer"]

                print(f"Player{winner} の勝ち！")
                print(f"答えは {answer} でした。")
                break


def main():
    host = input("サーバーのホスト名（例: hitblow-ws.onrender.com）> ").strip()
    asyncio.run(run_client(host))


if __name__ == "__main__":
    main()

