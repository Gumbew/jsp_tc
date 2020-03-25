import sqlite3

conn = sqlite3.connect('coffee_machine.db')
c = conn.cursor()


def make_coffee(drink, addition=None):
    try:
        c.execute("""UPDATE drinks set qty = qty-1 where name = ? """, [drink])
        if addition:
            c.execute("""UPDATE additions set qty = qty-1 where name = ? """, [addition])
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        conn.commit()


def make_order(time, sid, drink, addition=None):
    try:
        c.execute("""INSERT INTO orders VALUES (NULL,?,?,?,?)""", [time, sid, drink, addition])
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        conn.commit()


def get_drinks():
    try:
        c.execute("""SELECT name, qty FROM drinks""")
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        return [{'name': i[0], 'qty': i[1]} for i in c.fetchall()]


def get_additions():
    try:
        c.execute("""SELECT name,qty FROM additions""")
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        return [{'name': i[0], 'qty': i[1]} for i in c.fetchall()]


def get_orders(sid):
    try:
        c.execute("""SELECT * FROM orders WHERE sid=?""", [sid])
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        return c.fetchall()
