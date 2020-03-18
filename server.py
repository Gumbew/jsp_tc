import eventlet.wsgi
import socketio

sio = socketio.Server(async_mode='eventlet')

app = socketio.WSGIApp(sio)

goods = {
    "drinks": {
        "Americano": 20,
        "Latte": 20,
        "Cappuccino": 15,
        "Espresso": 20,
        "Irish Coffee": 7,
    },
    "adds": {
        "milk": 8,
        "sugar": 8,
        "whiskey": 7
    }
}


@sio.event
def connect(sid, environ):
    print("Connect ", sid)
    sio.emit("my_response", "Hi from coffee machine! :)")


@sio.event
def disconnect(sid):
    print('Disconnect ', sid)


@sio.event
def show_goods(sid):
    sio.emit('my_response', {"OK": 200, "Goods": goods})


def validate(data):
    if 'drink' not in data:
        return {"Error": 400, "Description": "Bad request. You didn't mention 'drink' in your request"}
    elif data['drink'] not in goods['drinks']:
        return {"Error": 404, "Description": "Not found. You want to order unknown 'drink'"}
    elif goods['drinks'][data['drink']] == 0:
        return {"Error": 403, "Description": "Forbidden. Out of stock!"}
    else:
        return {"OK": 201, "Description": "Coffee created!"}


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)
