from random import randint
import math
from sm3 import *
from MATH import *

# 参数定义
p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7

# dB = 0x1649AB77A00637BD5E2EFE283FBF353534AA7F7CB89463F208DDBC2920BB0DA0
# xB = 0x435B39CCA8F3B508C1488AFC67BE491A0F7BA07E581A0E4849A5CF70628A7E0A
# yB = 0x75DDBA78F15FEECB4C7895E2C1CDF5FE01DEBB2CDBADF45399CCF77BBA076A42


dB = randint(1, n - 1)
xB, yB = mul_point(gx, gy, dB, a, p)

def read_file(filename):
    """读取文件名中的字符串并返回"""
    try:
        fp = open(filename, "r", encoding='utf-8')
        msg = fp.read()
        fp.close()
        return msg
    except:
        print("Open file error!")


def kdf(z, klen):
    """密钥派生函数"""
    ct = 1
    k = ''
    for _ in range(math.ceil(klen / 256)):
        k = k + Hash(hex(int(z + '{:032b}'.format(ct), 2))[2:])
        ct = ct + 1
    k = '0' * ((256 - (len(bin(int(k, 16))[2:]) % 256)) % 256) + bin(int(k, 16))[2:]
    return k[:klen]


def enSM2(message: str):
    """SM2加密"""
    plen = len(hex(p)[2:])
    m = str_bit(message)
    klen = len(m)

    while True:
        # k = 0x4C62EEFD6ECFC2B95B92FD6C3D9575148AFA17425546D49018E5388D49DD7B4F
        k = randint(1, n)
        while k == dB:
            k = randint(1, n)
        x2, y2 = mul_point(xB, yB, k, a, p)
        x2, y2 = '{:0256b}'.format(x2), '{:0256b}'.format(y2)
        t = kdf(x2 + y2, klen)
        if int(t, 2) != 0:
            break
    # C1计算
    x1, y1 = mul_point(gx, gy, k, a, p)
    x1 = int_hex(x1, plen)
    y1 = int_hex(y1, plen)

    c1 = '04' + x1 + y1
    c2 = xor_2(m, t, klen)
    c3 = Hash(hex(int(x2 + m + y2, 2))[2:])
    return c1, c2, c3


def deSM2(c1, c2, c3, a, b, p):
    c1 = c1[2:]
    x1, y1 = int(c1[:len(c1) // 2], 16), int(c1[len(c1) // 2:], 16)
    # 验证c1是否在椭圆曲线上
    if pow(y1, 2, p) != (pow(x1, 3, p) + a * x1 + b) % p:
        return False
    # 计算点S
    x2, y2 = mul_point(x1, y1, dB, a, p)
    x2, y2 = '{:0256b}'.format(x2), '{:0256b}'.format(y2)
    # 计算t，若t全0则退出
    klen = len(c2) * 4
    t = kdf(x2 + y2, klen)
    if int(t, 2) == 0:
        return False
    # 计算m‘
    m = xor_16(c2, t, klen)
    # hash计算u
    u = Hash(hex(int(x2 + m + y2, 2))[2:])
    if u != c3:
        return False

    return hex(int(m, 2))[2:]


if __name__ == '__main__':

    fstr = read_file('message.txt')
    print("待加密明文为：" + fstr)
    # 加密
    c1, c2, c3 = enSM2(fstr)
    c = (c1 + c2 + c3).upper()
    # 密文输出
    print('加密后的密文为：')
    for i in range(0, len(c), 64):
        for j in range(8):
            print(c[i + j * 8: i + (j + 1) * 8], end=' ')
        print()

    # 解密
    m1 = deSM2(c1, c2, c3, a, b, p)
    m1 = str(bytes.fromhex(m1))
    m1 = '\n'.join(m1[2:-1].split('\\n'))
    print("解密后的明文为："+m1)