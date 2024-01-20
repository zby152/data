from RSA import *


def test1():
    p = 3
    q = 11
    d = 7
    m = 5
    fn = (p - 1) * (q - 1)
    temp = e_gcd(d, fn)  # 欧几里得算法求逆元
    e = temp[1]
    e, n, d = init(p, q, e)
    secret = RSA_encode(m, e, n)
    print("p=3,q=11,d=7,m=5的加密结果为：" + str(secret))


def test2():
    fn = 2 * 10
    e = 3
    temp = e_gcd(e, fn)  # 欧几里得算法求逆元
    d = temp[1]
    if d < 0:  # 由于e和fn互素故一定存在逆元
        d = d + fn  # 保证d为正数
    result = RSA_decode(9, d, 33)
    print("e=3,n=33,C=9解密的明文为：" + str(result))


def test3():
    p = 17
    q = 11
    e = 7
    e, n, d = init(p, q, e)
    m = 88
    result = RSA_encode(m, e, n)
    print("p=17,q=11, e=7,m=88时加密结果为" + str(result))


if __name__ == '__main__':
    test3()
