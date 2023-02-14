from cryptos.affine_rec import encrypt
from math import gcd

i = 0
for a in range(26):
    if gcd(a, 25) == 1:
        print(a)
        i += 1
print(i)