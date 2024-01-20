iv = '7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'


def t(j):
    if j < 16:
        return 0x79cc4519
    return 0x7a879d8a


def csl(x, k):
    """左循环移位"""
    x = '{:032b}'.format(x)
    k = k % 32
    x = x[k:] + x[:k]
    return int(x, 2)


def ff(x, y, z, j):
    """布尔函数"""
    if j < 16:
        return x ^ y ^ z
    return (x & y) | (y & z) | (z & x)


def gg(x, y, z, j):
    """布尔函数"""
    if j < 16:
        return x ^ y ^ z
    return (x & y) | (~x & z)


def p0(x):
    """置换函数"""
    return x ^ csl(x, 9) ^ csl(x, 17)


def p1(x):
    """置换函数"""
    return x ^ csl(x, 15) ^ csl(x, 23)


def fill(m):
    """填充原始消息"""
    l = len(m) * 4
    m = m + '8'
    k = 112 - (len(m) % 128)
    m = m + '0' * k + '{:016x}'.format(l)
    return m


def grouping(m):
    """消息分组"""
    n = len(m) // 128
    b = []
    for i in range(n):
        b.append(m[i * 128:(i + 1) * 128])
    return b


def extend(bi):
    """消息扩展函数"""
    w = []
    for i in range(16):
        w.append(int(bi[i * 8:(i + 1) * 8], 16))
    for j in range(16, 68):
        w.append(p1(w[j - 16] ^ w[j - 9] ^ csl(w[j - 3], 15)) ^ csl(w[j - 13], 7) ^ w[j - 6])
    for j in range(68, 132):
        w.append(w[j - 68] ^ w[j - 64])
    return w


def cf(vi, bi):
    """压缩函数"""
    w = extend(bi)
    a, b, c, d, e, f, g, h = int(vi[0:8], 16), int(vi[8:16], 16), int(vi[16:24], 16), int(vi[24:32], 16), int(vi[32:40],
                                                                                                              16), int(
        vi[40:48], 16), int(vi[48:56], 16), int(vi[56:64], 16)
    for j in range(64):
        ss1 = csl((csl(a, 12) + e + csl(t(j), j)) % pow(2, 32), 7)
        ss2 = ss1 ^ csl(a, 12)
        tt1 = (ff(a, b, c, j) + d + ss2 + w[j + 68]) % pow(2, 32)
        tt2 = (gg(e, f, g, j) + h + ss1 + w[j]) % pow(2, 32)
        d = c
        c = csl(b, 9)
        b = a
        a = tt1
        h = g
        g = csl(f, 19)
        f = e
        e = p0(tt2)
    abcdefgh = int('{:08x}'.format(a) + '{:08x}'.format(b) + '{:08x}'.format(c) + '{:08x}'.format(d) + '{:08x}'.format(
        e) + '{:08x}'.format(f) + '{:08x}'.format(g) + '{:08x}'.format(h), 16)
    return '{:064x}'.format(abcdefgh ^ int(vi, 16))


def iteration(b):
    n = len(b)
    v = iv
    for i in range(n):
        v = cf(v, b[i])
    return v


def Hash(m):  # m为16进制串
    m = fill(m)
    b = grouping(m)
    return iteration(b)
