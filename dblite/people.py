from dblite import create

CREATE_SCRIPT = '''
CREATE TABLE people(	ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME VARCHAR2(400),
                        EMAIL VARCHAR2(200),
                        PASSWORD VARCHAR2(200),
                        COUNTRY VARCHAR2(80),
                        COMPANY VARCHAR2(200),
                        PHONE VARCHAR2(80),
                        CITY VARCHAR2(80),
                        USER_GROUP VARCHAR2(20)
)
'''
def insert_table_people(id,name,email,password,country,company,phone,city,user_group):
    connection = create()
    c = connection.cursor()
    c.execute('insert into people (ID,NAME,EMAIL,PASSWORD,COUNTRY,COMPANY,PHONE,CITY,USER_GROUP) values (?,?,?,?,?,?,?,?,?)', (id,name,email,password,country,company,phone,city,user_group))
    last_id = c.lastrowid
    c.close()
    connection.close()
    return last_id


def update_table_people(id, **kwargs):
    connection = create()
    c = connection.cursor()
    sql = ''
    sql += 'update people set'
    sql += (',').join(k + ' = ?' for k,v in kwargs.iteritems())
    sql +='\twhere id = ?'
    params = list(v for k,v in kwargs.iteritems()).append(id)
    c.execute(sql,params)
    c.close()
    connection.close()
