def mod_inv(a, m):
    """求解模逆运算"""
    x1, x2, x3 = 1, 0, a
    y1, y2, y3 = 0, 1, m
    while y3 != 0:
        q = x3 // y3
        t1, t2, t3 = x1 - q * y1, x2 - q * y2, x3 - q * y3
        x1, x2, x3 = y1, y2, y3
        y1, y2, y3 = t1, t2, t3
    return x1 % m


def int_hex(int_x, length):
    """十进制转固定位数16进制"""
    len0 = length - len(hex(int_x)[2:])
    hex_x = len0 * '0' + hex(int_x)[2:]
    return hex_x


def str_bit(str_x):
    """读入的明文信息转换成二进制比特形式,高位补0"""
    bits = ""
    for i in str_x:
        ascii = bin(ord(i))[2:]
        for j in range(8 - len(ascii)):
            ascii = '0' + ascii
        bits += ascii
    return bits


def add_points(x1, y1, x2, y2, a, p):
    """求解两点在椭圆曲线上加和"""
    if x1 == x2 and y1 == p - y2:
        return False
    if x1 != x2:
        lamda = ((y2 - y1) * mod_inv(x2 - x1, p)) % p
    else:
        lamda = (((3 * x1 * x1 + a) % p) * mod_inv(2 * y1, p)) % p
    x3 = (lamda * lamda - x1 - x2) % p
    y3 = (lamda * (x1 - x3) - y1) % p
    return x3, y3


def mul_point(x, y, k, a, p):
    """椭圆曲线上点与数乘积"""
    k = bin(k)[2:]
    qx, qy = x, y
    n = 1
    for i in range(1, len(k)):
        qx, qy = add_points(qx, qy, qx, qy, a, p)
        n = n * 2
        if k[i] == '1':
            qx, qy = add_points(qx, qy, x, y, a, p)
            n = n + 1
    return qx, qy


def xor_2(a, b, length):
    """二进制字符串按位异或,结果长度固定"""
    len0 = len(hex(int(a, 2) ^ int(b, 2))[2:])
    return ((length // 4) - len0) * '0' + hex(int(a, 2) ^ int(b, 2))[2:]


def xor_16(a, b, length):
    """16进制字符串按位异或，长度固定"""
    len0 = length - len(bin(int(a, 16) ^ int(b, 2))[2:])
    return '0' * len0 + bin(int(a, 16) ^ int(b, 2))[2:]

def e_gcd(a, b):
    """计算模的逆元"""
    if b == 0:
        return a, 1, 0
    g, x, y = e_gcd(b, a % b)
    return g, y, x - a // b * y