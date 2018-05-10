
from dblite import create

CREATE_SCRIPT = '''CREATE TABLE company(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME VARCHAR2(400))'''


def insert_table_company(id,name):
    connection = create()
    c = connection.cursor()
    c.execute('insert into company (ID,NAME) values (?,?)', (id,name))
    last_id = c.lastrowid
    c.close()
    connection.close()
    return last_id


def update_table_company(id, **kwargs):
    connection = create()
    c = connection.cursor()
    sql = ''
    sql += 'update company set'
    sql += (',').join(k + ' = ?' for k,v in kwargs.iteritems())
    sql +='\twhere id = ?'
    params = list(v for k,v in kwargs.iteritems()).append(id)
    c.execute(sql,params)
    c.close()
    connection.close()
