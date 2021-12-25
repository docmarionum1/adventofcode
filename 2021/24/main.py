import itertools

a = (1, 1, 1, 1, 26, 26, 1, 26, 1, 26, 1, 26, 26, 26)
b = (11, 11, 14, 11, -8, -5, 11, -13, 12, -1, 14, -5, -4, -8)
c = (1, 11, 1, 11, 2, 9, 7, 11, 6, 15, 7, 1, 8, 6)

def calc_z(z, i, model_number):
    o = z%26 + b[i]
    w = model_number[i]
    ne = (o != w)
    return (z//a[i])*(25*ne + 1) + ne*(w + c[i])

def solve(default, product):
    for w0, w1, w2, w3, w6, w8, w10 in product:
        model_number = [
            w0, w1, 
            w2, w3, 
            default, default, 
            w6, default, 
            w8, default, 
            w10, default, 
            default, default
        ]

        z = 0

        for i in range(14):
            o = z%26 + b[i]

            if (b[i] < 11):
                if (o > 0) and (o < 10):
                    model_number[i] = o

            w = model_number[i]
            ne = (o != w)
            z = (z//a[i])*(25*ne + 1) + ne*(w + c[i])

        if z == 0:
            return "".join(str(n) for n in model_number)

print("Part 1:", solve(9, itertools.product(*[range(9, 0, -1) for _ in range(7)])))
print("Part 2:", solve(1, itertools.product(*[range(1, 10) for _ in range(7)])))