if True or False:
    print(1)
else: 
    print(0)
if True and True:
    print(1)
else:
    print(0)
if False or (True and False):
    print(1)
else:
    print(0)
print((3 if True else 5) + (5 if (False or False) else 3))
