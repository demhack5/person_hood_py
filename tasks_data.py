import sqlite3 as sql

# TODO: remove

def init_tasks_table():
    conn = sql.connect('../tasks.db')

    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
            id INT PRIMARY KEY,
            text           TEXT);""")

    # HARDCODE
    cur.execute("INSERT INTO tasks VALUES(?, ?)", (0, "Подпишитесь на https://t.me/roskomsvoboda"))
    cur.execute("INSERT INTO tasks VALUES(?, ?)", (1, "Подпишите петицию https://www.change.org/p/%D1%82%D1%80%D0%B5%D0%B1%D1%83%D0%B5%D0%BC-%D0%B7%D0%B0%D0%BA%D0%BE%D0%BD-%D0%BE-%D0%B7%D0%B0%D1%89%D0%B8%D1%82%D0%B5-%D0%BC%D0%B5%D0%B4%D0%B8%D1%86%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D1%85-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BD%D0%B8%D0%BA%D0%BE%D0%B2-%D0%BE%D1%82-%D0%BD%D0%B0%D1%81%D0%B8%D0%BB%D0%B8%D1%8F?source_location=petitions_browse"))
    cur.execute("INSERT INTO tasks VALUES(?, ?)", (2, "Отправьте 100р на https://donate.roskomsvoboda.org/"))
    
    conn.commit()
    return

def n_available_actions():

    # TODO: path
    conn = sql.connect('../tasks.db')
    cur  = conn.cursor()

    data = cur.execute("SELECT * FROM tasks").fetchall()

    conn.commit()
    return len(data)

def get_action_text(n_action):
    
    conn = sql.connect('../tasks.db')
    cur  = conn.cursor()

    data = cur.execute("SELECT text FROM tasks where id=%d" % n_action).fetchall()[0][0]
    conn.commit()

    return data

