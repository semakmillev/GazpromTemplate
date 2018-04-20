import sqlite3

import os

def create():
    try:
        already_exists = os.path.exists("logging.db")
        conn = sqlite3.connect("logging.db")
        if already_exists:
            return  conn

        c = conn.cursor()
        c.execute(
            '''CREATE TABLE user (_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  create_date  DATETIME DEFAULT current_timestamp ,
                                  email varchar2(200),
                                  user_name varchar2(200),
                                  company varchar2(200),
                                  default_lang varchar2(200) default 'RUS',
                                  event_source varchar2(200),

                                  ''')

        c.execute('''CREATE INDEX i_event_date_request ON request (event_date, event_source)''')

        c.execute(
            '''CREATE TABLE db_state_opened (_id INTEGER PRIMARY KEY ,
                                       event_date  DATETIME DEFAULT current_timestamp ,
                                       opened INTEGER)''')
        c.execute(
            '''CREATE TABLE db_state_busy (_id INTEGER PRIMARY KEY ,
                                       event_date  DATETIME DEFAULT current_timestamp ,
                                       busy INTEGER)''')

        c.execute('''CREATE INDEX i_db_state_opened_d ON db_state_opened (event_date)''')
        c.execute('''CREATE INDEX i_db_state_busy_d_d ON db_state_busy (event_date)''')
        c.close()
        return conn
    except Exception as ex:
        print '%s'%ex
        raise