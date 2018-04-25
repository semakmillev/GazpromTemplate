'''
import os
d = os.path.abspath(os.path.dirname(__file__)) + '/templates/first'

onlyfiles = [f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]
print onlyfiles
'''
import json
import uuid

f = file("db_creator/session.json")

str = f.read()
j = json.loads(str)

from db_creator.template_db import *

#print create_py(j['name'], j['fields'])

#print create_script(j['name'], j['fields'])
#print create_py(j['name'], j['fields'])

#a = uuid.uuid4()

#print a

from dblite.session import *

a = get_user_id("123fddde")
print a



'''
def tmp(**kwargs):
    # a =",\n".join(k + " = %s" for k,v in kwargs.iteritems())
    a = list(v for k, v in kwargs.iteritems())
    a.append(3)
    print a


tmp(a=1, b=2)

'''

