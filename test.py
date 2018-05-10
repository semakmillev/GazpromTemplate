'''
import os
d = os.path.abspath(os.path.dirname(__file__)) + '/templates/first'

onlyfiles = [f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]
print onlyfiles
'''
import json
import os
import uuid

import sqlite3

from dblite.consts import SQL_GET_USER_COMPANIES




path = '/media/semak/DATA/Development/GazpromTemplate/templates/first/'
files = [f for f in os.listdir(path)if os.path.isfile(path+f)]
print files
'''
f = file("db_creator/rules.json")

str = f.read()
j = json.loads(str)



from db_creator import template_db

print template_db.create_script(j['name'], j['fields'])
print template_db.create_py(j['name'], j['fields'])


from dblite import create

c = create()
sql = SQL_GET_USER_COMPANIES
connection = create()
cursor = connection.cursor()
cursor.execute(sql, [7, None])
rows = cursor.fetchall()
res = [dict(row) for row in rows]
print res

c.close()


def tmp(**kwargs):
    # a =",\n".join(k + " = %s" for k,v in kwargs.iteritems())
    a = list(v for k, v in kwargs.iteritems())
    a.append(3)
    print a


tmp(a=1, b=2)

'''
