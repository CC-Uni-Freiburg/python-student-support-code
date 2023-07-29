#in=10
#golden=55
x1 = 0
x2 = 1
n = input_int()
while (n > 0):
    t = x2
    x2 = x1 + x2
    x1 = t
    n = n - 1
print(x1)
