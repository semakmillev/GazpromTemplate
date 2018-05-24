from queue.tasks import add, generate_picture

#result = generate_picture.apply_async((u'first', 100, 50, u'JPEG', 96.0, 7), queue='TEMPLATE.Q')

result = add.apply_async((7, 3), queue='hipri')
#result = add.apply_async((2, 2), queue='hipri')
#print result.backend
#while not result.ready():
#    pass
print result.status
'''
from celery.result import AsyncResult
from test_task import app
res = AsyncResult('f51b3454-c0f5-48b6-a0cd-2fdb0c94610b', app=app)
print res.backend
'''
# f89dfdfc-c7d3-4b48-8e1f-5062d13c2840