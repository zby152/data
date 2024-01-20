from MATH import *


def read_file(filename):
    """读取文件名中的字符串并返回"""
    try:
        fp = open(filename, "r", encoding='utf-8')
        msg = fp.read()
        fp.close()
        return msg
    except:
        print("Open file error!")


def divide(string):
    """明文每3个数值一分组"""
    return [string[i:i + 3] for i in range(0, len(string), 3)]


def selectE(fn):
    """生成e"""
    while True:
        e = random.randint(1, fn)
        temp = e_gcd(e, fn)
        if temp[0] == 1:
            return e


def keyGenerate(lower, upper, p, q, e):
    """生成密钥"""
    # 在p,q没有给出时自己生成
    if p == 0:
        p = findPrime(lower, upper)
        q = findPrime(lower, upper)

    # 求fn的值
    n = p * q
    fn = (p - 1) * (q - 1)
    # 求e的值,没有给出就自己生成
    if e == 0:
        e = selectE(fn)
    # 求d的值
    temp = e_gcd(e, fn)  # 欧几里得算法求逆元
    d = temp[1]
    if d < 0:  # 由于e和fn互素故一定存在逆元
        d = d + fn  # 保证d为正数

    return p, q, e, n, d, fn


def RSA_encode(M, e, n):
    """RSA加密"""
    c = fastExpmod(int(M), e, n)  # 加密  c为密文 m^e mod n
    return c


def RSA_decode(c, d, n):
    """RSA解密"""
    M = fastExpmod(c, d, n)  # 解密 c^d mod n
    return M


def init(p=0, q=0, e=0):
    """计算初始参数"""
    # p=47
    # q=71
    p, q, e, n, d, fn = keyGenerate(1000, 10000, p, q, e)  # 密钥生成
    # 更改keyGenerate函数的两个参数，可以改变生成素数的位数大小。


    print("公钥<n,e>为:" + str(n) + " " + str(e))
    print("私钥<p,q,d,fn>为：" + str(p) + " " + str(q) + " " + str(d) + " " + str(fn))
    return e, n, d


if __name__ == "__main__":

    msg = read_file('message.txt')
    messages = divide(msg)
    print("明文为:" + str(msg))

    e, n, d = init()

    # 加密
    secrets = []
    for message in messages:
        secret = RSA_encode(message, e, n)
        secrets.append(secret)
    C = ''.join(map(str, secrets))
    print("RSA加密得到密文为:" + C)

    # 解密
    Message = []
    for secret in secrets:
        M = RSA_decode(secret, d, n)
        Message.append(M)
    M = ''.join(map(str, Message))
    print("RSA解密得到明文为:" + M)



