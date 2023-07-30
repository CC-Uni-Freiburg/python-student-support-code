# in=3
# in=5
# in=-444
# golden=7-44454
x = [1, 2, 3, 4, 5, 6, 7]
i = len(x)
j = input_int()
k = input_int()
y = input_int()
if k >= 0 and k < i:
    x[k] = y
while i > 0:
    i = i - 1
    if i >= j:
        print(x[i])
