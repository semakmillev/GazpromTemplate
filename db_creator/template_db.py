import os
import sqlite3


def create_script(table_name, fields):
    i = 0
    script = "CREATE TABLE %s(" % table_name
    for field in fields:
        i += 1
        row = "\t"
        row += field['name'] + " " + field['type']
        row += " PRIMARY KEY" if field['primary'] else ""
        row += " AUTOINCREMENT" if field['autoincrement'] else ""
        row += " default " + field['default'] if len(field['default']) > 0 else ""
        row += "," if len(fields) != i else ""
        row += "\n"
        script += row
    script +=  ")"
    return script


def create_py(table_name, fields):
    field_row = ','.join(field['name'] for field in fields)
    field_template_row = ','.join('?' for field in fields)
    code = "def insert_table_%s(%s):\n" % (str(table_name).lower(), field_row.lower())
    code += "\tconnection = create()\n"
    code += "\tc = connection.cursor()\n"
    code += "\tc.execute('insert into %s (%s) values (%s)', (%s))\n" % (
        table_name, field_row, field_template_row, field_row.lower())
    code += "\tlast_id = c.lastrowid\n"
    code += "\tc.close()\n"
    code += "\tconnection.close()\n"
    code += "\treturn last_id\n"
    code += "\n\n"
    code += "def update_table_%s(id, **kwargs):\n" % (str(table_name).lower())
    code += "\tconnection = create()\n"
    code += "\tc = connection.cursor()\n"
    code += "\tsql = ''\n"
    code += "\tsql += 'update %s set'\n " % table_name
    code += "\tsql += (',').join(k + ' = ?' for k,v in kwargs.iteritems())\n"
    code += "\tsql +='\\"+"twhere id = ?'\n"
    code += "\tparams = list(v for k,v in kwargs.iteritems()).append(id)\n"
    code += "\tc.execute(sql,params)\n"
    code += "\tc.close()\n"
    code += "\tconnection.close()\n"
    return code


def create(fields):
    try:
        already_exists = os.path.exists("template.db")
        conn = sqlite3.connect("template.db")
        if already_exists:
            return conn

        c = conn.cursor()
        c.execute(
            '''CREATE TABLE user (_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  create_date  DATETIME DEFAULT current_timestamp ,
                                  email varchar2(200),
                                  user_name varchar2(200),
                                  company varchar2(200),
                                  default_lang varchar2(200) DEFAULT 'RUS',
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
        print '%s' % ex
        raise
