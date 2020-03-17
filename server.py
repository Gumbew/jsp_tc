import socketio
from aiohttp import web

sio = socketio.AsyncServer(async_mode='aiohttp')

app = web.Application()
sio.attach(app)


@sio.event
def connect(sid, environ):
    print("Connect ", sid)


@sio.event
def disconnect(sid):
    print('Disconnect ', sid)


if __name__ == '__main__':
    web.run_app(app, host="localhost", port=5000)
