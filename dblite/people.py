from dblite import create
from dblite.session import create_session

CREATE_SCRIPT = '''
CREATE TABLE people(	ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME VARCHAR2(400),
                        EMAIL VARCHAR2(200),
                        PASSWORD VARCHAR2(200),
                        COUNTRY VARCHAR2(80),
                        COMPANY VARCHAR2(200),
                        PHONE VARCHAR2(80),
                        CITY VARCHAR2(80),
                        VERIFIED INT
)
'''


def insert_table_people(name, email, password, country, company, phone, city, verified):
    connection = create()
    c = connection.cursor()
    c.execute(
        'insert into people (NAME,EMAIL,PASSWORD,COUNTRY,COMPANY,PHONE,CITY,VERIFIED) values (?,?,?,?,?,?,?,?)',
        (name, email, password, country, company, phone, city, verified))
    last_id = c.lastrowid
    c.close()
    connection.commit()
    connection.close()
    return last_id


def update_table_people(id, **kwargs):
    connection = create()
    c = connection.cursor()
    sql = ''
    sql += 'update people set '
    sql += (',').join(k + ' = ?' for k, v in kwargs.iteritems())
    sql += '\twhere id = ?'
    params =  list(v for k, v in kwargs.iteritems())
    params.append(id)
    # params = list(v for k, v in kwargs.iteritems()).append(id)
    # print sql
    # print params
    c.execute(sql, params)
    c.close()
    connection.commit()
    connection.close()


def register(email, password):
    user_id = insert_table_people("", email, password, "", "", "", "", 0)
    session_id = create_session(user_id)
    return session_id


def login(email, password):
    sql = '''select * from people where EMAIL = ? and PASSWORD = ?'''
    connection = create()
    c = connection.cursor()
    print email, password
    res = c.execute(sql, [email, password])
    rows = res.fetchall()
    user_id = None if len(rows) == 0 else rows[0][0]
    if user_id == None:
        return None
    return create_session(user_id)



def get_user_by_email(email):
    sql = '''select * from people where EMAIL = ?'''
    connection = create()
    c = connection.cursor()
    res = c.execute(sql, [email])
    rows = res.fetchall()
    return None if len(rows) == 0 else rows[0][0]
