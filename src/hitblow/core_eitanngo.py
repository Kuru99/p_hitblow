"""英単語版 Hit & Blow の中心ロジック"""

import random

# 出題する単語（すべて3文字）
WORDS = [
    "cat",
    "dog",
    "sun",
    "map",
    "pen",
    "hat",
    "box",
    "cup",
    "car",
    "bus",
]


def judge_eitanngo(secret, guess):
    """secret と guess を比べて (hit, blow) を返す。"""
    hits = sum(s == g for s, g in zip(secret, guess))
    common = sum(min(secret.count(c), guess.count(c)) for c in set(guess))
    return hits, common - hits


def make_secret_eitanngo():
    """ランダムに英単語を1つ選ぶ。"""
    return random.choice(WORDS)