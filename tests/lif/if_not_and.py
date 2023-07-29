x = input_int() # 42
y = input_int() # 0
u = x == y # false
v = x != y # true
print(x - y if not (u and v) else 0)
