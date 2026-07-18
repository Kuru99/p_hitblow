"""数字版 Hit & Blow（対戦モード）"""

from .core import judge, make_secret


def play_battle(digits=3, mode="digits"):
    secret = make_secret(digits, mode)
    mode_name = "英字" if mode == "letters" else "数字"
    print(f"Hit & Blow 対戦モード（{digits} 桁・{mode_name}・重複なし）")
    print(f"{digits}文字の{mode_name}を入力してください。")
    # ===== ① 開始時に足す =====

    players = ["ユーザー1", "ユーザー2"]
    tries = [0, 0]
    turn = 0
    while True:
        player = players[turn]
        guess = input(f"{player} の予想 > ").strip()
        if mode == "letters":
            guess = guess.upper()

        # ===== ② 入力コマンドに足す =====

        valid = guess.isalpha() if mode == "letters" else guess.isdigit()
        if len(guess) != digits or not valid:
            print(f"{digits} 桁の{mode_name}で入力してね")
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