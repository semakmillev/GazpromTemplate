import uuid

# from . import *
from dblite import create

CREATE_SCRIPT = '''
CREATE TABLE session(ID VARCHAR2(50) PRIMARY KEY,
                     USER_ID INTEGER)
'''


def create_session(user_id):
    sid = uuid.uuid4()
    insert_table_session(sid, user_id)


def get_user_id(sid):
    sql = '''select * from session where ID = ?'''
    connection = create()
    c = connection.cursor()
    print sid, sql
    res = c.execute(sql, [sid])
    return None if len(res.fetchall()) == 0 else res.fetchall()[0]['USER_ID']


def insert_table_session(id, user_id):
    connection = create()
    c = connection.cursor()
    c.execute('insert into session (ID,USER_ID) values (?,?)', (id, user_id))
    last_id = c.lastrowid
    c.close()
    connection.close()


def update_table_session(id, **kwargs):
    connection = create()
    c = connection.cursor()
    sql = ''
    sql += 'update session set'
    sql += (',').join(k + ' = ?' for k, v in kwargs.iteritems())
    sql += '\twhere id = ?'
    params = list(v for k, v in kwargs.iteritems()).append(id)
    c.execute(sql, params)
    c.close()
    connection.close()
