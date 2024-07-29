import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jinja2 import Environment, FileSystemLoader

router = APIRouter()

env = Environment(loader=FileSystemLoader("templates"))


connections: list[WebSocket] = []


async def broadcast(message: str):
    template = env.get_template("chat/message.html")
    html = template.render(message=message)
    for websocket in connections:
        await websocket.send_text(html)


async def clear_input(websocket: WebSocket):
    template = env.get_template("chat/input.html")
    html = template.render()
    await websocket.send_text(html)


@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            name = json_data["name"]
            message = json_data["message"]
            await broadcast(f"{name}: {message}")
            await clear_input(websocket)
    except WebSocketDisconnect:
        connections.remove(websocket)
