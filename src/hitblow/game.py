"""ゲームの進行（入力・表示・ループ）。

★ チームで足す機能は **自分の担当の場所**に書く（1機能=1ファイル）。
   下の「ここに足す」場所は3か所（① 開始時 ② 入力コマンド ③ 勝利時）。
   ペアごとに**別の場所**を直すので、並行作業でも衝突しない。
   import も自分の場所の近くに書くこと（ファイル先頭にまとめない＝衝突回避）。
"""

from .core import judge, make_secret


def play(digits=3, mode="digits"):
    secret = make_secret(digits, mode)
    mode_name = "英字" if mode == "letters" else "数字"
    print(f"Hit & Blow（{digits} 桁・{mode_name}・重複なし）")

    # ===== ① 開始時に足す（難易度・あいさつ など）: ここに書く =====

    tries = 0
    while True:
        guess = input("予想 > ").strip()
        if mode == "letters":
            guess = guess.upper()

        # ===== ② 入力コマンドに足す（ヒント など）: ここに書く（import もここに） =====
        # 例:  from .hint import hint
        #      if guess == "h":
        #          print(hint(secret)); continue

        valid = guess.isalpha() if mode == "letters" else guess.isdigit()
        if len(guess) != digits or not valid:
            print(f"{digits} 桁の{mode_name}で入力してね")
            continue
        tries += 1
        hit, blow = judge(secret, guess)
        print(f"  Hit={hit}  Blow={blow}")
        if hit == digits:

            # ===== ③ 勝利時に足す（スコア・履歴 など）: ここに書く =====

            print(f"正解！ {tries} 回で当たり（答え {secret}）")
            break
