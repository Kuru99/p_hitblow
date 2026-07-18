"""コマンドの入口。ここでモードを選んでから、対応するゲームを呼ぶ。"""

from .game import play
from .game_eitanngo import play_eitanngo
from .game_battle import play_battle

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
            choose_battle_mode()
            break

        elif play_mode == "3":
            print("ブラウザで通信対戦ページを開きます...")
            import webbrowser
            webbrowser.open("https://p-hitblow.onrender.com")
            break

        else:
            print("1, 2, 3 のいずれかを入力してね")


def choose_solo_mode():
    print("1: 数字当てモード")
    print("2: 英単語当てモード")
    print("3: 英語(ランダム)当てモード")

    while True:
        mode = input("モードを選んでください（1, 2, 3） > ").strip()
        if mode == "1":
            play(mode="digits")
            break
        elif mode == "2":
            play_eitanngo()
            break
        elif mode == "3":
            play(mode="letters")
            break
        else:
            print("1, 2, 3 のいずれかを入力してね")

def choose_battle_mode():
    print("1: 数字当てモード")
    print("2: 英語(ランダム)当てモード")

    while True:
        mode = input("モードを選んでください（1 or 2） > ").strip()
        if mode == "1":
            play_battle(mode="digits")
            break
        elif mode == "2":
            play_battle(mode="letters")
            break
        else:
            print("1か2を入力してね")
