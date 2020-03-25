import eventlet.wsgi
import socketio
import datetime
import coffee_machine_sql_manager as cm_sql

sio = socketio.Server(async_mode='eventlet')

app = socketio.WSGIApp(sio)


class CoffeeMachine:

    @staticmethod
    def make_order(sid, data):
        order_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if 'add' in data:
            cm_sql.make_order(order_time, sid, data['drink'], data['add'])
        else:
            cm_sql.make_order(order_time, sid, data['drink'])

    @staticmethod
    def make_coffee(sid, data):
        response = CoffeeMachine.validate(data)

        if "OK" in response:
            if 'add' in data:
                cm_sql.make_coffee(data['drink'], data['add'])
            else:
                cm_sql.make_coffee(data['drink'])

            CoffeeMachine.make_order(sid, data)

        return response

    @staticmethod
    def get_drink_names():
        drinks = cm_sql.get_drinks()
        return {i['name'] for i in drinks}

    @staticmethod
    def get_add_names():
        adds = cm_sql.get_additions()
        return {i['name'] for i in adds}

    @staticmethod
    def get_qty(name, good_type):
        if type == 'drink':
            drinks = cm_sql.get_drinks()
            for i in drinks:
                if i['name'] == name:
                    return i['qty']
        else:
            additions = cm_sql.get_additions()
            for i in additions:
                if i['name'] == name:
                    return i['qty']

    @staticmethod
    def show_goods():
        drinks = cm_sql.get_drinks()
        additions = cm_sql.get_additions()
        result = {
            'drinks': drinks,
            'additions': additions
        }

        return result

    @staticmethod
    def show_orders(sid):
        orders = cm_sql.get_orders(sid)
        result = []
        for i in orders:
            result.append({'data': i[1],
                           'drink_name': i[3],
                           'addition': i[4]
                           })

        return result

    @staticmethod
    def validate(data):
        if 'drink' not in data:
            return {"Error": 400, "Description": "Bad request. You didn't mention 'drink' in your request"}
        elif data['drink'] not in CoffeeMachine.get_drink_names():
            return {"Error": 404, "Description": "Not found. You want to order unknown 'drink'"}
        elif CoffeeMachine.get_qty(data['drink'], 'drink') == 0:
            return {"Error": 403, "Description": "Forbidden. Out of stock!"}

        elif 'add' in data:
            if data['add'] not in CoffeeMachine.get_add_names():
                return {"Error": 404, "Description": "Not found. You want to order unknown 'add'"}
            elif CoffeeMachine.get_qty(data['add'], 'add') == 0:
                return {"Error": 403, "Description": "Forbidden. Out of stock!"}

            return {"OK": 201, "Description": f"{data['drink']} with {data['add']} is created!"}

        return {"OK": 201, "Description": f"{data['drink']} is created!"}


class CoffeeMachineNamespace(socketio.Namespace):
    namespace = '/coffee'

    def on_connect(self, sid, environ):
        print("Connect ", sid)

    def on_disconnect(self, sid):
        print('Disconnect ', sid)

    def on_show_goods(self, sid):
        sio.emit('my_response', {"OK": 200, "Goods": CoffeeMachine.show_goods()}, namespace=self.namespace)

    def on_show_orders(self, sid):
        sio.emit('my_response', {"OK": 200, "Orders": CoffeeMachine.show_orders(sid)}, namespace=self.namespace)

    def on_make_coffee(self, sid, data):
        sio.emit('my_response', CoffeeMachine.make_coffee(sid, data), namespace=self.namespace)


if __name__ == '__main__':
    sio.register_namespace(CoffeeMachineNamespace('/coffee'))
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)
