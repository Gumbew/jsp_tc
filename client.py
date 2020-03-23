import socketio
import time

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
    def make_coffee():
        data = {}
        drink = input("Which coffee do you want? \n")
        data['drink'] = drink
        add = input("Enter an add or press Enter key to continue")

        if add:
            data['add'] = add

        print(f"You have ordered a/an {drink}, please wait")
        sio.emit("make_coffee", data, namespace=CoffeeMachineManager.namespace)

    @staticmethod
    def show_orders():
        sio.emit("show_orders", namespace=CoffeeMachineManager.namespace)

    @staticmethod
    def show_goods():
        sio.emit("show_goods", namespace=CoffeeMachineManager.namespace)


def menu():
    try:
        user_choice = int(input("""
        Please choose one of the options below:
        1: Order a drink
        2: Show goods
        3: Show order history
        4: Quit
        """))
    except ValueError:
        print("Wrong input! Try again")
    else:
        return user_choice


if __name__ == "__main__":
    sio.register_namespace(CoffeeMachineNamespace('/coffee'))
    sio.connect("http://localhost:5000", namespaces=['/coffee'])

    while True:
        user_choice = menu()

        if user_choice:
            if user_choice == 1:
                CoffeeMachineManager.make_coffee()
            elif user_choice == 2:
                CoffeeMachineManager.show_goods()
            elif user_choice == 3:
                CoffeeMachineManager.show_orders()
            elif user_choice == 4:
                print("You left the menu")
                break
            else:
                print("Wrong number!")

        time.sleep(1)
