'''
import os
d = os.path.abspath(os.path.dirname(__file__)) + '/templates/first'

onlyfiles = [f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]
print onlyfiles
'''
import json
f = file("db_creator/people.json")

str = f.read()
j = json.loads(str)

from db_creator.template_db import *

print create_script(j['name'], j['fields'])d
