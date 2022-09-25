import sqlite3 as sql
from tasks_data import *

N_STAGES = 3
DATA_BASE_NAME = 'users_data'
DATABASE_PATH  = '../'

def init_table():
    conn = sql.connect('%s/%s.db' % (DATABASE_PATH, DATA_BASE_NAME))

    cur = conn.cursor()
    table_init_str = """CREATE TABLE IF NOT EXISTS %s(
            user_id INT PRIMARY KEY,
            cur_stage     INT,""" % (DATA_BASE_NAME)

    for n_stage in range(N_STAGES - 1):
        table_init_str += "stage%d INT, " % (n_stage)

    table_init_str += "stage%d INT" % (N_STAGES - 1)
    table_init_str += ");"
    
    cur.execute(table_init_str)
    conn.commit()

    return

def get_cur_stage(user_id):

    conn = sql.connect('%s/%s.db' % (DATABASE_PATH, DATA_BASE_NAME))
    cur  = conn.cursor()

    cur_stage = cur.execute("SELECT cur_stage FROM %s WHERE user_id = %d" % (DATA_BASE_NAME, user_id)).fetchall()

    conn.commit()
    
    return cur_stage[0][0]

def get_cur_actions(user_id):
    conn = sql.connect('%s/%s.db' % (DATABASE_PATH, DATA_BASE_NAME))
    cur  = conn.cursor()

   # TODO: optimize

    cur_actions = []
    cur_stage = get_cur_stage(user_id)

    for n_action in range(cur_stage + 1):
        cur_actions.append(cur.execute("SELECT stage%d FROM %s WHERE user_id = %d" % (n_action, DATA_BASE_NAME, user_id)).fetchall()[0][0])
    
    conn.commit()

    return cur_actions

def check_user_in_database(user_id):
    
    conn = sql.connect('%s/%s.db' % (DATABASE_PATH, DATA_BASE_NAME))
    cur  = conn.cursor()

    user_data = cur.execute("SELECT * FROM %s WHERE user_id = %d" % (DATA_BASE_NAME, user_id)).fetchall()
    conn.commit()

    if(len(user_data) > 0):
        return
    
    cmd_str = "INSERT INTO %s VALUES(" % (DATA_BASE_NAME) + str(user_id) + ", -1, "

    for n_stage in range(N_STAGES - 1):
        cmd_str += "0, "
    cmd_str += '0)'

    cur.execute(cmd_str)
    conn.commit()

    return

def add_action_to_user(user_id, n_action, stage):
    conn = sql.connect('%s/%s.db' % (DATABASE_PATH, DATA_BASE_NAME))
    cur  = conn.cursor()

    print()
    cur.execute("UPDATE %s SET stage%d=%d WHERE user_id=%d" % (DATA_BASE_NAME, stage, n_action, user_id))
    cur.execute("UPDATE %s SET cur_stage=%d WHERE user_id=%d" % (DATA_BASE_NAME, stage, user_id))

    conn.commit()

    return

def get_next_action_text(user_id):
   
    cur_stage   = get_cur_stage(user_id)
    cur_actions = get_cur_actions(user_id)

    for n_action in range(n_available_actions()):
        if not (n_action in cur_actions):
            add_action_to_user(user_id, n_action, cur_stage + 1)
            return get_action_text(n_action)
    # TODO: remove
    return "you have done all available actions"

def validate_last_action(user_id):
    
    # TODO: !!!
    return True
