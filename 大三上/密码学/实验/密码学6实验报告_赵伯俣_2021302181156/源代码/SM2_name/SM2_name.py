from SM2 import *
from MATH import *


def sm2_sign(message, dA, a, b, p, Gx, Gy, n):
    """SM2数字签名"""
    e = int(Hash(message), 16)
    while True:
        k = randint(1, n - 1)
        x1, y1 = mul_point(Gx, Gy, k, a, p)
        r = (e + x1) % n
        if r == 0 or r + k == n:
            continue
        s = (e_gcd(1 + dA, n)[1] * (k - r * dA)) % n
        if s == 0:
            continue
        break
    return r, s


def sm2_verify(message, r, s, PAx, PAy, a, b, p, Gx, Gy, n):
    """SM2签名验证"""
    if not (1 <= r < n and 1 <= s < n):
        return False
    e = int(Hash(message), 16)
    t = (r + s) % n
    if t == 0:
        return False
    a1,a2=mul_point(Gx, Gy, s, a, p)
    b1,b2=mul_point(PAx, PAy, t, a, p)
    x1, y1 = add_points(a1,a2, b1,b2, a, p)
    R = (e + x1) % n
    return R == r


# 示例使用
if __name__ == '__main__':
    message = read_file('message.txt')
    m_bit=str_bit(message)
    m=hex(int(m_bit, 2))[2:]

    dA = randint(1, n - 1)  # 私钥
    PAx, PAy = mul_point(gx, gy, dA, a, p)  # 公钥

    # 生成签名
    r, s = sm2_sign(m, dA, a, b, p, gx, gy, n)
    print("SM2数字签名后的结果为:")
    print("r="+str(r))
    print("s="+str(s))

    # 验证签名
    is_valid = sm2_verify(m, r, s, PAx, PAy, a, b, p, gx, gy, n)
    print("SM2数字签名验证结果为：", is_valid)
