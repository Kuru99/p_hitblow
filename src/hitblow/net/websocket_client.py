import asyncio
import websockets
import json

from hitblow.net.protocol import msg_guess


async def run_client(host: str):
    """WebSocket サーバーに接続してゲームをプレイする"""
    # Render等の本番環境は wss、ローカルは ws を使う
    scheme = "wss" if not host.startswith("localhost") and not host.startswith("127.0.0.1") else "ws"
    url = f"{scheme}://{host}/ws"
    print(f"Connecting to {url} ...")

    async with websockets.connect(url) as ws:
        print("Connected to server.")

        async for msg in ws:
            data = json.loads(msg)
            msg_type = data.get("type")

            if msg_type == "your_turn":
                player = data["player"]
                print(f"あなたのターンです（Player{player}）")
                guess = input("予想を入力してください > ").strip()
                await ws.send(json.dumps(msg_guess(guess)))

            elif msg_type == "result":
                player = data["player"]
                guess = data["guess"]
                hit = data["hit"]
                blow = data["blow"]
                print(f"Player{player} の予想 {guess} → Hit={hit} Blow={blow}")

            elif msg_type == "win":
                winner = data["winner"]
                answer = data["answer"]
                print(f"Player{winner} の勝ち！")
                print(f"答えは {answer} でした。")
                break


def main():
    host = input("サーバーのホスト名（例: p-hitblow.onrender.com）> ").strip()
    asyncio.run(run_client(host))


if __name__ == "__main__":
    main()
