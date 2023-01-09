from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = """
<!DOCTYPE html>
<html>
    <head>
        <title>Relabs</title>
        <style>
            form {
                margin: 20px;
            }
            button:checked{
                background-color: green;
            }
        </style>
    </head>
    <body>
        <form action='' onsubmit='sendMessage(event)'>
            <input type='text' id="text"/>
            <button type='submit'>Send</button>
        </form>
        <ol id='messages'>
        </ol>
        <script>
            var websocket = new WebSocket('ws://localhost:8000/ws');
            websocket.onmessage = function(event){
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById('text')
                websocket.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(HTML)


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_text(
            {await websocket.receive_text()}
        )
