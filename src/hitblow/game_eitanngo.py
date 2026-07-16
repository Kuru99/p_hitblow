"""英単語版 Hit & Blow"""

from .core_eitanngo import judge_eitanngo, make_secret_eitanngo


def play_eitanngo():
    secret = make_secret_eitanngo()

    print("Hit & Blow（英単語モード・3文字）")
    #print("使れる単語一覧")
    #print(", ".join(WORDS))

    tries = 0

    while True:
        guess = input("予想 > ").strip().lower()

        if len(guess) != 3 or not guess.isalpha():
            print("3文字の英単語を入力してください")
            continue

        #if guess not in WORDS:
            #print("一覧にある単語を入力してください")
            #continue

        tries += 1

        hit, blow = judge_eitanngo(secret, guess)

        print(f"  Hit={hit}  Blow={blow}")

        if hit == 3:
            print(f"正解！ {tries} 回で当たり（答え {secret}）")
            break