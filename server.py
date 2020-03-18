import eventlet.wsgi
import socketio
import datetime

sio = socketio.Server(async_mode='eventlet')

app = socketio.WSGIApp(sio)


class CoffeeMachine:
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

    @staticmethod
    def make_order(sid, data):
        order = {"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "order description": data}

        if sid not in CoffeeMachine.orders:
            CoffeeMachine.orders[sid] = [order]
        else:
            CoffeeMachine.orders[sid].append(order)

    @staticmethod
    def make_coffee(sid, data):
        response = CoffeeMachine.validate(data)

        if "OK" in response:
            if 'add' in data:
                CoffeeMachine.goods['adds'][data['add']] -= 1

            CoffeeMachine.goods['drinks'][data['drink']] -= 1
            CoffeeMachine.make_order(sid, data)

        return response

    @staticmethod
    def validate(data):
        if 'drink' not in data:
            return {"Error": 400, "Description": "Bad request. You didn't mention 'drink' in your request"}
        elif data['drink'] not in CoffeeMachine.goods['drinks']:
            return {"Error": 404, "Description": "Not found. You want to order unknown 'drink'"}
        elif CoffeeMachine.goods['drinks'][data['drink']] == 0:
            return {"Error": 403, "Description": "Forbidden. Out of stock!"}

        elif 'add' in data:
            if data['add'] not in CoffeeMachine.goods['adds']:
                return {"Error": 404, "Description": "Not found. You want to order unknown 'add'"}
            elif CoffeeMachine.goods['adds'][data['add']] == 0:
                return {"Error": 403, "Description": "Forbidden. Out of stock!"}

            return {"OK": 201, "Description": f"{data['drink']} with {data['add']} is created!"}

        return {"OK": 201, "Description": f"{data['drink']} is created!"}


class CoffeeMachineNamespace(socketio.Namespace):
    namespace = '/coffee'
    def on_connect(self, sid, environ):
        print("Connect ", sid)
        sio.emit("my_response", "Hi from coffee machine! :)", namespace=self.namespace)

    def on_disconnect(self, sid):
        print('Disconnect ', sid)

    def on_show_goods(self, sid):
        sio.emit('my_response', {"OK": 200, "Goods": CoffeeMachine.goods}, namespace=self.namespace)

    def on_show_orders(self, sid):
        sio.emit('my_response', {"OK": 200, "Orders": CoffeeMachine.orders}, namespace=self.namespace)

    def on_make_coffee(self, sid, data):
        sio.emit('my_response', CoffeeMachine.make_coffee(sid, data), namespace=self.namespace)


if __name__ == '__main__':
    sio.register_namespace(CoffeeMachineNamespace('/coffee'))
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)
