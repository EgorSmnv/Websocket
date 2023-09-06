from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <style>
            ol {
            list-style-type: none;
            }
        </style>
    </head>
    <body>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ol id='messages'>
        </ol>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var data_mes = JSON.parse(event.data)
                var text = data_mes.index + '. ' + data_mes.text
                message.innerHTML = text
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    i = 1
    while True:
        try:
            data = await websocket.receive_text()
            resp = {'index': i, 'text': data}
            i += 1
            await websocket.send_json(resp)
        except Exception as e:
            print('error:', e)
            break
