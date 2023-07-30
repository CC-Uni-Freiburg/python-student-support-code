# in=5
# in=10
# in=11
# in=20
# in=22
# in=30
# in=33
# in=40
# in=44
# in=50
# in=55
# golden=6050
n = input_int()
out = 0
while n > 0:
    x = input_int()
    y = input_int()
    out = out + x * y
    n = n - 1
print(out)
