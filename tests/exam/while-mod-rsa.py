#in=3233
#in=17
#in=413
#in=42
#golden=1
def pow(m:int, x:int, mod:int) -> int:
    r = 1
    while x > 0:
        r = (r * m) % mod
        x = x - 1
    return r

n = input_int()
e = input_int()
d = input_int()

m = input_int()
enc_m = pow (m, e, n)
dec_m = pow (enc_m, d, n)

print( 1 if m == dec_m else 0)
