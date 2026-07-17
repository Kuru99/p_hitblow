# src/hitblow/net/protocol.py

def msg_your_turn(player: int):
    """サーバー → クライアント：ターン通知"""
    return {
        "type": "your_turn",
        "player": player
    }

def msg_guess(value: str):
    """クライアント → サーバー：予想送信"""
    return {
        "type": "guess",
        "value": value
    }

def msg_result(player: int, guess: str, hit: int, blow: int):
    """サーバー → 全クライアント：判定結果"""
    return {
        "type": "result",
        "player": player,
        "guess": guess,
        "hit": hit,
        "blow": blow
    }

def msg_win(winner: int, answer: str):
    """サーバー → 全クライアント：勝利通知"""
    return {
        "type": "win",
        "winner": winner,
        "answer": answer
    }

