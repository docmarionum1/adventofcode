import itertools

# The program is 14 blocks which each follow the same pattern:
# inp w
# mul x 0
# add x z
# mod x 26
# div z <a>
# add x <b>
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y <c>
# mul y x
# add z y

# I manually got these constants from the input by using that pattern
a = (1, 1, 1, 1, 26, 26, 1, 26, 1, 26, 1, 26, 26, 26)
b = (11, 11, 14, 11, -8, -5, 11, -13, 12, -1, 14, -5, -4, -8)
c = (1, 11, 1, 11, 2, 9, 7, 11, 6, 15, 7, 1, 8, 6)

def solve(default, product):
    # These 7 digits we will enumerate in either decending or acsending order to find the first
    # match
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
            # For digits where b is less than 0, we have a chance to reduce z, in which case, pick the
            # largest digit such that we can make model_number[i] == o
            o = z%26 + b[i]
            if (b[i] < 11):
                if (o > 0) and (o < 10):
                    model_number[i] = o

            # The above instructions simplify to this formula that takes
            # the current z and returns a new z given the constants above
            # and the current model number
            w = model_number[i]
            ne = (o != w)
            z = (z//a[i])*(25*ne + 1) + ne*(w + c[i])

        if z == 0:
            return "".join(str(n) for n in model_number)

print("Part 1:", solve(9, itertools.product(*[range(9, 0, -1) for _ in range(7)])))
print("Part 2:", solve(1, itertools.product(*[range(1, 10) for _ in range(7)])))