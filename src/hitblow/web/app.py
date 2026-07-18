from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import asyncio
import json

from hitblow.core import make_secret, judge
from hitblow.net.protocol import (
    msg_game_start,
    msg_your_turn,
    msg_result,
    msg_win,
    msg_game_over,
)

app = FastAPI()

# ゲーム状態
class GameState:
    def __init__(self):
        self.connected: list[WebSocket] = []
        self.game_task: asyncio.Task | None = None
        self.mode: str = "digits"  # "digits" or "letters"
        self.digits: int = 3
        self.max_turns: int = 15
        self.game_active: bool = False

game_state = GameState()


# GUI を返す
@app.get("/")
def gui():
    return FileResponse("src/hitblow/web/static/index.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    game_state.connected.append(websocket)
    print(f"Client connected. Total: {len(game_state.connected)}")

    try:
        # クライアントからのメッセージを処理
        while True:
            msg = await websocket.receive_text()
            data = json.loads(msg)
            msg_type = data.get("type")

            # ゲーム設定（モード・難易度選択）
            if msg_type == "game_config":
                game_state.mode = data.get("mode", "digits")
                game_state.digits = data.get("digits", 3)
                game_state.max_turns = data.get("max_turns", 15)
                print(f"Game config: mode={game_state.mode}, digits={game_state.digits}, max_turns={game_state.max_turns}")

                # 2人揃ったらゲーム開始
                if len(game_state.connected) == 2 and game_state.game_task is None:
                    game_state.game_active = True
                    game_state.game_task = asyncio.create_task(game_loop())

    except WebSocketDisconnect:
        print("Client disconnected")
        if websocket in game_state.connected:
            game_state.connected.remove(websocket)
        game_state.game_active = False
        game_state.game_task = None


async def game_loop():
    """ゲーム進行のメインループ"""
    try:
        # ゲーム開始通知
        start_msg = msg_game_start(game_state.mode, game_state.digits, game_state.max_turns)
        for ws in game_state.connected:
            await ws.send_text(json.dumps(start_msg))

        # 秘密の数字を生成
        secret = make_secret(game_state.digits, game_state.mode)
        print(f"Secret: {secret}")

        turn = 0  # 0: Player1, 1: Player2
        turn_count = 0
        player_tries = [0, 0]

        while turn_count < game_state.max_turns:
            # 接続が2人揃っていなければ終了
            if len(game_state.connected) < 2:
                print("Player disconnected. Ending game.")
                break

            # ターン通知
            turn_count += 1
            await game_state.connected[turn].send_text(json.dumps(msg_your_turn(turn, turn_count)))

            # 入力待ち
            msg = await game_state.connected[turn].receive_text()
            data = json.loads(msg)
            guess = data["value"]

            # 判定
            hit, blow = judge(secret, guess)
            player_tries[turn] += 1

            # 全員に結果通知
            for ws in game_state.connected:
                await ws.send_text(json.dumps(
                    msg_result(turn, guess, hit, blow)
                ))

            # 勝利判定
            if hit == game_state.digits:
                for ws in game_state.connected:
                    await ws.send_text(json.dumps(
                        msg_win(turn, secret, player_tries[turn])
                    ))
                break

            # ターン交代
            turn = 1 - turn

        # 最大ターン達成でゲームオーバー
        if turn_count >= game_state.max_turns and hit < game_state.digits:
            for ws in game_state.connected:
                await ws.send_text(json.dumps(msg_game_over()))

    except Exception as e:
        print(f"Game loop error: {e}")
    finally:
        game_state.game_task = None
        game_state.game_active = False
