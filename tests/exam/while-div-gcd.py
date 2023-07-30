# in=240
# in=46
# golden=-9-11147-1112
a = input_int()
b = input_int()

old_r = a
r = b
old_s = 1
s = 0
old_t = 0
t = 1
while r != 0:
    q = old_r // r
    tmp = r
    r = old_r - q * r
    old_r = tmp
    tmp = s
    s = old_s - q * s
    old_s = tmp
    tmp = t
    t = old_t - q * t
    old_t = tmp

print(old_s)
print(-111)
print(old_t)
print(-111)
print(old_r)
