from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import asyncio
import json
import random

from hitblow.core import make_secret, judge
from hitblow.net.protocol import (
    msg_game_start,
    msg_your_turn,
    msg_result,
    msg_win,
    msg_game_over,
    msg_server_status,
    msg_room_created,
    msg_room_joined,
    msg_room_error,
    msg_player_ready
)

app = FastAPI()

class Player:
    def __init__(self, ws: WebSocket):
        self.ws = ws
        self.room_id = None
        self.is_ready = False
        self.player_idx = -1  # 0 or 1 in a room

class Room:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.players: list[Player] = []
        self.state = "waiting" # waiting, ready, playing, finished
        self.mode = "digits"
        self.digits = 3
        self.max_turns = 15
        
        # Game state
        self.secret = ""
        self.turn = 0
        self.turn_count = 0
        self.player_tries = [0, 0]

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[Player] = []
        self.rooms: dict[str, Room] = {}

    async def connect(self, player: Player):
        await player.ws.accept()
        self.active_connections.append(player)
        await self.broadcast_status()

    async def disconnect(self, player: Player):
        if player in self.active_connections:
            self.active_connections.remove(player)
        
        # If in a room, handle disconnect
        if player.room_id and player.room_id in self.rooms:
            room = self.rooms[player.room_id]
            if player in room.players:
                room.players.remove(player)
                # Notify remaining player
                for p in room.players:
                    try:
                        await p.ws.send_text(json.dumps(msg_room_error("Opponent disconnected. Room closed.")))
                    except:
                        pass
            del self.rooms[player.room_id]
        
        await self.broadcast_status()

    async def broadcast_status(self):
        msg = json.dumps(msg_server_status(len(self.active_connections)))
        for p in self.active_connections:
            try:
                await p.ws.send_text(msg)
            except:
                pass

manager = ConnectionManager()

@app.get("/")
def gui():
    return FileResponse("src/hitblow/web/static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    player = Player(websocket)
    await manager.connect(player)
    
    try:
        while True:
            msg = await websocket.receive_text()
            data = json.loads(msg)
            msg_type = data.get("type")
            
            if msg_type == "create_room":
                # Create a room
                room_id = str(random.randint(1000, 9999))
                room = Room(room_id)
                room.mode = data.get("mode", "digits")
                room.digits = data.get("digits", 3)
                room.players.append(player)
                player.room_id = room_id
                player.player_idx = 0
                manager.rooms[room_id] = room
                await websocket.send_text(json.dumps(msg_room_created(room_id)))
                await websocket.send_text(json.dumps(msg_room_joined(room_id, 0)))

            elif msg_type == "join_room":
                room_id = data.get("room_id")
                if room_id in manager.rooms:
                    room = manager.rooms[room_id]
                    if len(room.players) < 2:
                        room.players.append(player)
                        player.room_id = room_id
                        player.player_idx = 1
                        await websocket.send_text(json.dumps(msg_room_joined(room_id, 1)))
                    else:
                        await websocket.send_text(json.dumps(msg_room_error("Room is full.")))
                else:
                    await websocket.send_text(json.dumps(msg_room_error("Room not found.")))

            elif msg_type == "ready":
                if player.room_id and player.room_id in manager.rooms:
                    room = manager.rooms[player.room_id]
                    player.is_ready = True
                    # Notify both players
                    for p in room.players:
                        await p.ws.send_text(json.dumps(msg_player_ready(player.player_idx)))
                    
                    # If both ready, start game
                    if len(room.players) == 2 and all(p.is_ready for p in room.players):
                        room.state = "playing"
                        room.secret = make_secret(room.digits, room.mode)
                        print(f"Room {room.room_id} started. Secret: {room.secret}")
                        
                        start_msg = msg_game_start(room.mode, room.digits, room.max_turns)
                        for p in room.players:
                            await p.ws.send_text(json.dumps(start_msg))
                        
                        # Send turn 1 to player 0
                        room.turn_count = 1
                        await room.players[0].ws.send_text(json.dumps(msg_your_turn(0, 1)))
            
            elif msg_type == "guess":
                if player.room_id and player.room_id in manager.rooms:
                    room = manager.rooms[player.room_id]
                    if room.state != "playing":
                        continue
                    
                    if player.player_idx != room.turn:
                        # Not this player's turn
                        continue
                    
                    guess = data.get("value", "")
                    hit, blow = judge(room.secret, guess)
                    room.player_tries[player.player_idx] += 1
                    
                    # Broadcast result
                    res_msg = msg_result(player.player_idx, guess, hit, blow)
                    for p in room.players:
                        await p.ws.send_text(json.dumps(res_msg))
                    
                    # Check win
                    if hit == room.digits:
                        win_msg = msg_win(player.player_idx, room.secret, room.player_tries[player.player_idx])
                        for p in room.players:
                            await p.ws.send_text(json.dumps(win_msg))
                        room.state = "finished"
                        continue
                    
                    # Next turn
                    room.turn = 1 - room.turn
                    if room.turn == 0:
                        room.turn_count += 1
                    
                    if room.turn_count > room.max_turns:
                        over_msg = msg_game_over()
                        for p in room.players:
                            await p.ws.send_text(json.dumps(over_msg))
                        room.state = "finished"
                        continue
                        
                    # Notify next player
                    next_player = room.players[room.turn]
                    await next_player.ws.send_text(json.dumps(msg_your_turn(room.turn, room.turn_count)))

    except WebSocketDisconnect:
        await manager.disconnect(player)
