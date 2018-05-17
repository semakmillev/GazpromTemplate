from dblite import create

CREATE_SCRIPT = '''
  CREATE TABLE rules(USER_ID INTEGER,
                     TEMPLATE_ID INTEGER,
                     BRAND_ID INTEGER,
                     COMPANY_ID INTEGER,
                     ROLE VARCHAR2(40) default "USER")
                     '''
CREATE_INDEX_SCRIPT = '''
  CREATE INDEX i_rules_user_id ON rules (USER_ID)'''


def insert_table_rules(user_id, template_id, brand_id, company_id, role):
    connection = create()
    c = connection.cursor()
    c.execute('insert into rules (USER_ID,TEMPLATE_ID,BRAND_ID,COMPANY_ID,ROLE) values (?,?,?,?,?)',
              (user_id, template_id, brand_id, company_id, role))
    last_id = c.lastrowid
    c.close()
    connection.close()
    return last_id


def update_table_rules(id, **kwargs):
    connection = create()
    c = connection.cursor()
    sql = ''
    sql += 'update rules set'
    sql += (',').join(k + ' = ?' for k, v in kwargs.iteritems())
    sql += '\twhere id = ?'
    params = list(v for k, v in kwargs.iteritems()).append(id)
    c.execute(sql, params)
    c.close()
    connection.close()


def get_brand_rules(id):
    connection = create()
    c = connection.cursor()
    sql = 'select p.*, r.ROLE ' \
          '  from rules r,' \
          '       people p ' \
          ' where r.BRAND_ID = ?' \
          '   and p.ID = r.USER_ID'
    c.execute(sql, [id])
    rows = c.fetchall()
    c.close()
    connection.close()
    return [dict(row) for row in rows]

def get_company_rules(id):
    connection = create()
    c = connection.cursor()
    sql = 'select p.*, r.ROLE ' \
          '  from rules r,' \
          '       people p ' \
          ' where r.COMPANY_ID = ?' \
          '   and p.ID = USER_ID'
    c.execute(sql, [id])
    rows = c.fetchall()
    c.close()
    connection.close()
    return [dict(row) for row in rows]

def get_template_rules(id):
    connection = create()
    c = connection.cursor()
    sql = 'select p.*, r.ROLE ' \
          '  from rules r,' \
          '       people p ' \
          ' where r.TEMPLATE_ID = ?' \
          '   and p.ID = USER_ID'
    c.execute(sql, [id])
    rows = c.fetchall()
    c.close()
    connection.close()
    return [dict(row) for row in rows]