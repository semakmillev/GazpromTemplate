from dblite import create

CREATE_SCRIPT = '''CREATE TABLE brand(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
	NAME VARCHAR2(400),
	COMPANY_ID INTEGER)'''


def insert_table_brand(id, name, company_id):
    connection = create()
    c = connection.cursor()
    c.execute('insert into brand (ID,NAME,COMPANY_ID) values (?,?,?)', (id, name, company_id))
    last_id = c.lastrowid
    c.close()
    connection.close()
    return last_id


def update_table_brand(id, **kwargs):
    connection = create()
    c = connection.cursor()
    sql = ''
    sql += 'update brand set'
    sql += (',').join(k + ' = ?' for k, v in kwargs.iteritems())
    sql += '\twhere id = ?'
    params = list(v for k, v in kwargs.iteritems()).append(id)
    c.execute(sql, params)
    c.close()
    connection.close()
