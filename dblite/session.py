import uuid

# from . import *
from dblite import create

CREATE_SCRIPT = '''
CREATE TABLE session(ID VARCHAR2(50) PRIMARY KEY,
                     USER_ID INTEGER)
'''


def create_session(user_id):
    sid = str(uuid.uuid4())
    insert_table_session(sid, user_id)
    return sid

def get_user_id(sid):
    sql = '''select * from session where ID = ?'''
    connection = create()
    c = connection.cursor()
    print sid, sql
    res = c.execute(sql, [sid])
    rows = res.fetchall()
    return None if len(rows) == 0 else rows[0][1]


def insert_table_session(id, user_id):
    connection = create()
    c = connection.cursor()
    c.execute('insert into session (ID, USER_ID) values (?,?)', (id, user_id))
    last_id = c.lastrowid
    c.close()
    connection.commit()
    connection.close()