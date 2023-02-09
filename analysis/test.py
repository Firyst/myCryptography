from cryptos.affine_rec import encrypt
t = "BBDJ"

for i in range(100000):
    new_t = encrypt(t, "ABCDEFJ", False, 3, 11, 11, 8)
    if new_t == "JABA":
        print(i, t)
    t = new_t