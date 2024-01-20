import random


def fastExpMod(b, n, m):
    '''
    return : b^n mod m
    '''
    result = 1
    while n != 0:
        if (n & 1) == 1:  # 按位与&操作
            result = (result * b) % m
        b = (b * b) % m
        n = n >> 1  # 位数右移>>操作
    return result


def fastExpmod(a, e, m):
    a = a % m
    res = 1
    while e != 0:
        if e & 1:
            res = (res * a) % m
        e >>= 1
        a = (a * a) % m
    return res


def fermatPrimeTest(m, k):
    """费马素性检验算法"""
    if m % 2 == 0:
        return False
    for i in range(k):
        a = random.randint(2, m - 2)
        g = e_gcd(a, m)
        if g[0] == 1:
            r = fastExpMod(a, m - 1, m)
            if r == 1:
                continue
            else:
                return False
        else:
            return False
    return True


def findPrime(lower, upper):
    """计算大素数"""
    while True:
        n = random.randint(lower, upper)
        if fermatPrimeTest(n, 6) == True:
            return n


def e_gcd(a, b):
    """计算模的逆元"""
    if b == 0:
        return a, 1, 0
    g, x, y = e_gcd(b, a % b)
    return g, y, x - a // b * y
