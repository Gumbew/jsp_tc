import eventlet.wsgi
import socketio
import datetime

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

orders = {}


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


@sio.event
def show_orders(sid):
    sio.emit('my_response', {"OK": 200, "Orders": orders})


@sio.event
def make_coffee(sid, data):
    response = validate(data)
    if "OK" in response:
        if 'add' in data:
            goods['adds'][data['add']] -= 1
        goods['drinks'][data['drink']] -= 1
        make_order(sid, data)
    sio.emit('my_response', response)


def make_order(sid, data):
    order = {"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "order description": data}

    if sid not in orders:
        orders[sid] = [order]
    else:
        orders[sid].append(order)


def validate(data):
    if 'drink' not in data:
        return {"Error": 400, "Description": "Bad request. You didn't mention 'drink' in your request"}
    elif data['drink'] not in goods['drinks']:
        return {"Error": 404, "Description": "Not found. You want to order unknown 'drink'"}
    elif goods['drinks'][data['drink']] == 0:
        return {"Error": 403, "Description": "Forbidden. Out of stock!"}

    elif 'add' in data:
        if data['add'] not in goods['adds']:
            return {"Error": 404, "Description": "Not found. You want to order unknown 'add'"}
        elif goods['adds'][data['add']] == 0:
            return {"Error": 403, "Description": "Forbidden. Out of stock!"}

    return {"OK": 201, "Description": "Coffee created!"}


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)
