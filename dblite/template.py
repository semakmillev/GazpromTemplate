from dblite import create

CREATE_SCRIPT = '''
CREATE TABLE template(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
	NAME VARCHAR2(200),
	BRAND_ID INTEGER,
	PATH VARCHAR2(500))
'''


def insert_table_template(name, brand_id, path):
    connection = create()
    c = connection.cursor()
    c.execute('insert into template (NAME,BRAND_ID,PATH) values (?,?,?)', (name, brand_id, path))
    last_id = c.lastrowid
    c.close()
    connection.commit()
    connection.close()
    return last_id


def update_table_template(id, **kwargs):
    connection = create()
    c = connection.cursor()
    sql = ''
    sql += 'update template set'
    sql += (',').join(k + ' = ?' for k, v in kwargs.iteritems())
    sql += '\twhere id = ?'
    params = list(v for k, v in kwargs.iteritems()).append(id)
    c.execute(sql, params)
    c.close()
    connection.commit()
    connection.close()
