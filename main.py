from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

template = Jinja2Templates(directory='templates')


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return template.TemplateResponse('index.html', {'request': request})


@app.websocket_route('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        for i in range(1, 1000):
            await websocket.send_json(
                [str(i), await websocket.receive_text()]
            )
