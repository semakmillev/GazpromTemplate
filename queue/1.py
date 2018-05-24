from tasks import add, generate_picture

#result = generate_picture.apply_async((u'first', 100, 50, u'JPEG', 96.0, 7), queue='TEMPLATE.Q')

#result = add.apply_async((7, 3), queue='hipri')
result = add.apply_async((2, 2), queue='hipri')
#print result.backend
#while not result.ready():
#    pass
print result.status