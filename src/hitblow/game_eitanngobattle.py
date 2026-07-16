"""英単語版 Hit & Blow（対戦モード）"""

from .core_eitanngo import judge, make_secret


def play_eitanngo_battle():
    secret = make_secret()

    print("=== 英単語 Hit & Blow 対戦モード ===")
    print("3文字の英単語を入力してください。")
    

    players = ["ユーザー1", "ユーザー2"]
    tries = [0, 0]
    turn = 0

    while True:
        player = players[turn]

        guess = input(f"{player} の予想 > ").strip().lower()

        if len(guess) != 3 or not guess.isalpha():
            print("3文字の英単語を入力してください")
            continue

        tries[turn] += 1

        hit, blow = judge(secret, guess)

        print(f"  Hit={hit}  Blow={blow}")

        if hit == 3:
            print()
            print(f"🎉 {player} の勝ち！")
            print(f"答えは {secret} でした。")
            print(f"{player} は {tries[turn]} 回で正解しました。")
            break

        # 次のプレイヤーへ交代
        turn = 1 - turn