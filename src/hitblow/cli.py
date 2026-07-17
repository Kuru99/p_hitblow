"""コマンドの入口。ここでモードを選んでから、対応するゲームを呼ぶ。"""

from .game import play
from .game_eitanngo import play_eitanngo
from .game_battle import play_battle
from .net.websocket_client import run_client   # ★ 追加

def main():
    print("=== Hit & Blow ===")
    print("1: 1人プレイ")
    print("2: 対戦モード（ローカル）")
    print("3: 通信対戦（WebSocket）")   # ★ 追加

    while True:
        play_mode = input("プレイ人数を選んでください（1 / 2 / 3） > ").strip()

        if play_mode == "1":
            choose_solo_mode()
            break

        elif play_mode == "2":
            play_battle()
            break

        elif play_mode == "3":
            host = input("サーバーURLを入力してください（例: hitblow-ws.onrender.com） > ").strip()
            run_client(host)
            break

        else:
            print("1, 2, 3 のいずれかを入力してね")


def choose_solo_mode():
    print("1: 数字当てモード")
    print("2: 英単語当てモード")

    while True:
        mode = input("モードを選んでください（1 or 2） > ").strip()
        if mode == "1":
            play()
            break
        elif mode == "2":
            play_eitanngo()
            break
        else:
            print("1か2を入力してね")
