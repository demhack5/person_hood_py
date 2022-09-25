import sqlite3 as sql
from tasks_data import *

N_STAGES = 3

class users_data(object):

    def __init__(self, db_path):

        self.path  = db_path + '/users_data.db'
        self.tasks = tasks_data(db_path)

        onlyfiles = [f for f in listdir(db_path) if isfile(join(db_path, f))]
    
        if not 'tasks' in onlyfiles:
            conn = sql.connect(self.path)

            cur = conn.cursor()
            table_init_str = """CREATE TABLE IF NOT EXISTS users_data(
                    user_id INT PRIMARY KEY,
                    cur_stage     INT,"""

            for n_stage in range(N_STAGES - 1):
                table_init_str += "stage%d INT, " % (n_stage)

            table_init_str += "stage%d INT" % (N_STAGES - 1)
            table_init_str += ");"
            
            cur.execute(table_init_str)
            conn.commit()

    def get_cur_stage(self, user_id):

        conn = sql.connect(self.path)
        cur  = conn.cursor()

        cur_stage = cur.execute("SELECT cur_stage FROM users_data WHERE user_id = %d" % (user_id)).fetchall()

        conn.commit()
        
        return cur_stage[0][0]

    def get_cur_actions(self, user_id):
        conn = sql.connect(self.path)
        cur  = conn.cursor()

    # TODO: optimize

        cur_actions = []
        cur_stage = self.get_cur_stage(user_id)

        for n_action in range(cur_stage + 1):
            cur_actions.append(cur.execute("SELECT stage%d FROM users_data WHERE user_id = %d" % (n_action, user_id)).fetchall()[0][0])
        
        conn.commit()

        return cur_actions

    def check_user_in_database(self, user_id):
        
        conn = sql.connect(self.path)
        cur  = conn.cursor()

        user_data = cur.execute("SELECT * FROM users_data WHERE user_id = %d" % (user_id)).fetchall()
        conn.commit()

        if(len(user_data) > 0):
            return
        
        cmd_str = "INSERT INTO users_data VALUES(" + str(user_id) + ", -1, "

        for n_stage in range(N_STAGES - 1):
            cmd_str += "0, "
        cmd_str += '0)'

        cur.execute(cmd_str)
        conn.commit()

        return

    def add_action_to_user(self, user_id, n_action, stage):
        conn = sql.connect(self.path)
        cur  = conn.cursor()

        cur.execute("UPDATE users_data SET stage%d=%d WHERE user_id=%d" % (stage, n_action, user_id))
        cur.execute("UPDATE users_data SET cur_stage=%d WHERE user_id=%d" % (stage, user_id))

        conn.commit()

        return

    def get_next_action_text(self, user_id):
    
        cur_stage   = self.get_cur_stage(user_id)
        cur_actions = self.get_cur_actions(user_id)

        for n_action in range(self.tasks.n_available_actions()):
            if not (n_action in cur_actions):
                self.add_action_to_user(user_id, n_action, cur_stage + 1)
                return self.tasks.get_action_text(n_action)
        # TODO: remove
        return "you have done all available actions"

    def validate_last_action(self, user_id):
        
        # TODO: !!!
        return True
        
    def get_registration_link(self, user_id):
        return "https:://registrate"
