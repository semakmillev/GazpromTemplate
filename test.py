'''
import os
d = os.path.abspath(os.path.dirname(__file__)) + '/templates/first'

onlyfiles = [f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]
print onlyfiles
'''
import json
import uuid
'''
f = file("db_creator/rules.json")

str = f.read()
j = json.loads(str)



from db_creator import template_db

print template_db.create_script(j['name'], j['fields'])
print template_db.create_py(j['name'], j['fields'])
'''

from dblite import create

c = create()
sql = "select * from template"
connection = create()
cursor = connection.cursor()
cursor.execute(sql)
rows = cursor.fetchall()
for row in rows:
    print(row[1])
c.close()



'''
def tmp(**kwargs):
    # a =",\n".join(k + " = %s" for k,v in kwargs.iteritems())
    a = list(v for k, v in kwargs.iteritems())
    a.append(3)
    print a


tmp(a=1, b=2)

'''

