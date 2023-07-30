# in=3
# golden=4
x = [1, 2, 3, 4, 5, 6, 7]
i = len(x)
j = input_int()
while i > 0:
    i = i - 1
    if i == j:
        print(x[i])
