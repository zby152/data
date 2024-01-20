from random import randint
import sympy
import sys
from MATH import *

sys.setrecursionlimit(1000)


def read_file(filename):
    """读取文件名中的字符串并返回"""
    try:
        fp = open(filename, "r", encoding='utf-8')
        msg = fp.read()
        fp.close()
        return msg
    except:
        print("Open file error!")


def primitive_element(p, q):
    while True:
        g = randint(2, p - 2)
        if fastExpMod(g, 2, p) != 1 and fastExpMod(g, q, p) != 1:
            return g


def generate_key(p=0, a=0, d=0):
    """计算公钥y"""
    # 若没有给出p，需要自己生成p,a,d

    if p == 0:
        while True:
            q = sympy.randprime(10 ** 149, 10 ** 150 / 2 - 1)
            if sympy.isprime(q):
                p = 2 * q + 1
                if len(str(p)) == 150 and sympy.isprime(p):
                    break
        a = primitive_element(p, q)
        d = randint(2, p - 2)

    y = fastExpMod(a, d, p)
    return p, y, d, a


def ELGamal_encode(M, p=0, a=0, d=0, k=0):
    y, d, p, a = generate_key(p, a, d)

    y = fastExpMod(a, d, p)
    print("计算得公钥y=" + str(y))
    print("   私钥d=" + str(d))
    if k == 0:
        k = randint(2, p - 1)
    U = fastExpMod(y, k, p)
    c1 = fastExpMod(a, k, p)
    UM = U * int(M)
    c2 = fastExpMod(UM, 1, p)

    return c1, c2, d, p


def ELGamal_decode(c1, c2, d, p):
    V = fastExpMod(c1, d, p)
    V_1 = e_gcd(V, p)[1]
    C2V_1 = c2 * V_1
    M = fastExpMod(C2V_1, 1, p)
    return M


if __name__ == '__main__':
    # p = 5
    # a = 2
    # d = 765
    # k = 853
    m = read_file("message.txt")
    print("明文为：" + str(m))
    c1, c2, d, p = ELGamal_encode(m)

    print("加密后的密文(c1,c2)为：")
    print(c1)
    print(c2)

    M = ELGamal_decode(c1, c2, d, p)
    print("解密后的明文为：" + str(M))
