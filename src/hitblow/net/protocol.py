# src/hitblow/net/protocol.py

def msg_game_start(mode: str, digits: int, max_turns: int):
    """サーバー → クライアント：ゲーム開始通知"""
    return {
        "type": "game_start",
        "mode": mode,  # "digits" or "letters"
        "digits": digits,
        "max_turns": max_turns
    }

def msg_your_turn(player: int, turn_count: int):
    """サーバー → クライアント：ターン通知"""
    return {
        "type": "your_turn",
        "player": player,
        "turn": turn_count
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

def msg_win(winner: int, answer: str, tries: int):
    """サーバー → 全クライアント：勝利通知"""
    return {
        "type": "win",
        "winner": winner,
        "answer": answer,
        "tries": tries
    }

def msg_game_over():
    """サーバー → 全クライアント：ゲームオーバー（最大ターン達成）"""
    return {
        "type": "game_over",
        "message": "Max turns reached. Game over!"
    }


