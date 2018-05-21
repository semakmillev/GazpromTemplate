import uuid

from dblite import create
from dblite import people, consts

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
    connection.commit()
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


def delete_rule(id):
    connection = create()
    c = connection.cursor()
    sql = 'delete from rules where id = ?'
    c.execute(sql, [id])
    c.close()
    connection.commit()
    connection.close()


def get_brand_rules(id):
    connection = create()
    c = connection.cursor()
    sql = consts.SQL_GET_BRAND_USERS
    c.execute(sql, {"brand_id": id})
    rows = c.fetchall()
    c.close()
    connection.close()
    return [dict(row) for row in rows]


def get_company_rules(id):
    connection = create()
    c = connection.cursor()
    sql = 'select p.*, r.ROLE, r.ID RULE_ID ' \
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
    sql = 'select p.*, r.ROLE, r.ID RULE_ID ' \
          '  from rules r,' \
          '       people p ' \
          ' where r.TEMPLATE_ID = ?' \
          '   and p.ID = USER_ID'
    c.execute(sql, [id])
    rows = c.fetchall()
    c.close()
    connection.close()
    return [dict(row) for row in rows]


def check_rule_access(user_id, source, item_id):
    user_items = []
    if source == 'template':
        user_items = people.get_user_items(
            "select * from (" + consts.SQL_GET_USER_TEMPLATES + ") where ID = :template_id",
            user_id, None, template_id=item_id)
    elif source == 'brand':
        user_items = people.get_user_items(
            "select * from (" + consts.SQL_GET_USER_BRANDS + ") where ID = :brand_id",
            user_id, None, brand_id=item_id)
    elif source == 'company':
        user_items = people.get_user_items(
            "select * from (" + consts.SQL_GET_USER_COMPANIES + ") where ID = :company_id",
            user_id, None, company_id=item_id)
    return len(user_items) > 0


def send_invitation(email):
    sid = str(uuid.uuid4())
    sql = "insert into invitation values(:sid,:email)"
    connection = create()
    cursor = connection.cursor()
    cursor.execute(sql, {'sid': sid, 'email': email})
    # send email here
    cursor.close()
    connection.commit()
    connection.close()
