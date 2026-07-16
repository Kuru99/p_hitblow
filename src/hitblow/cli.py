"""コマンドの入口。第3回で `hitblow` コマンドがここ（main）を呼ぶ。"""

"""コマンドの入口。ここでモードを選んでから、対応するゲームを呼ぶ。"""

from .game import play
from .game_eitanngo import play_eitanngo


def main():
    print("=== Hit & Blow ===")
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