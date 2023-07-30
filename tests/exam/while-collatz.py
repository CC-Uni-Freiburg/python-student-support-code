# in=42
# golden=8
n = input_int()
c = 0
while n > 1:
    c = c + 1
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
print(c)
