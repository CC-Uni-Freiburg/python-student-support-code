x = input_int()
y = input_int()
if (x > 1) and (y < 10 or y >= 20):
    print (20 if x + 5 < y + y else x - y)
else:
    print (0)
if (x <= 10) and (y < 10 or y >= 20):
    print (20 if x + 5 > y + y else x - y)
else:
    print (0)
