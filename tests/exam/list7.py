#in=
#golden=1014

x= [1,2,3,4,5]
y= [3,4,5,2,1]
z= [0,0,0,0,0,0,0,0,0,0]

m = 0
while m < len(z):
    i = 0
    while i <= m:
        j = m - i
        if i < len(x) and j < len(y):
            z[m] = z[m] + x[i] * y[j]
        i = i + 1
    m = m + 1
print(z[1])
print(z[7])
