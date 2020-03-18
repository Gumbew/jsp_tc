import eventlet.wsgi
import socketio

sio = socketio.Server(async_mode='eventlet')

app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print("Connect ", sid)
    sio.emit("my_response", "Hi from coffee machine! :)")


@sio.event
def disconnect(sid):
    print('Disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)
