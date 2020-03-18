import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("connected")


@sio.event
def disconnect():
    print("disconnected")


@sio.event
def my_response(data):
    print(data)


if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    sio.wait()
