"""数字版 Hit & Blow（対戦モード）"""

from .core import judge, make_secret


def play_battle(digits=3):
    secret = make_secret(digits)
    print(f"Hit & Blow 対戦モード（{digits} 桁・重複なし）")
    print("3文字の数字を入力してください。")
    # ===== ① 開始時に足す =====

    players = ["ユーザー1", "ユーザー2"]
    tries = [0, 0]
    turn = 0

    while True:
        player = players[turn]
        guess = input(f"{player} の予想 > ").strip()

        # ===== ② 入力コマンドに足す =====

        if len(guess) != digits or not guess.isdigit():
            print(f"{digits} 桁の数字で入力してね")
            continue

        tries[turn] += 1

        hit, blow = judge(secret, guess)
        print(f"  Hit={hit}  Blow={blow}")

        if hit == digits:

            # ===== ③ 勝利時に足す =====

            print(f"正解！ 答えは {secret}")
            print(f"{player} の勝ち！")
            print(f"{player} は {tries[turn]} 回で当てました。")
            break

        # プレイヤー交代
        turn = 1 - turn