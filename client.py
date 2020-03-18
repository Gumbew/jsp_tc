import socketio

sio = socketio.Client()


class CoffeeMachineNamespace(socketio.ClientNamespace):
    def on_connect(self):
        print("connected")

    def on_disconnect(self):
        print("disconnected")

    def on_my_response(self, data):
        print(data)


class CoffeeMachineManager:
    namespace = '/coffee'

    @staticmethod
    def make_coffee(data):
        sio.emit("make_coffee", data, namespace=CoffeeMachineManager.namespace)

    @staticmethod
    def show_orders():
        sio.emit("show_orders", namespace=CoffeeMachineManager.namespace)

    @staticmethod
    def show_goods():
        sio.emit("show_goods", namespace=CoffeeMachineManager.namespace)


if __name__ == "__main__":
    sio.register_namespace(CoffeeMachineNamespace('/coffee'))
    sio.connect("http://localhost:5000", namespaces=['/coffee'])

    orders = [{"drink": "Latte", "add": "sugar"}, {"drink": "Latte"}, {"drink": "Latte", "add": "ABRA"},
              {"drink": "ABRA", "add": "sugar"}]

    CoffeeMachineManager.show_goods()

    for order in orders:
        CoffeeMachineManager.make_coffee(order)
        CoffeeMachineManager.show_goods()

    CoffeeMachineManager.show_orders()


