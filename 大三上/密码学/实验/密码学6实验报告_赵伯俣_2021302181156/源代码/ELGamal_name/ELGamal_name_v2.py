from ELGamal import *


def elgamal_sign(message, p, g, d):
    """生成ElGamal数字签名"""
    M = message
    while True:
        k = randint(2, p - 2)
        if e_gcd(k, p - 1)[0] == 1:  # 确保k和p-1互质
            break
    r = fastExpMod(g, k, p)

    k_inv = e_gcd(k, p - 1)[1] % (p - 1)
    s = (k_inv * (M * d - r)) % (p - 1)
    return r, s


def elgamal_verify(message, r, s, p, g, y):
    """验证ElGamal数字签名"""
    M = message
    if r < 1 or r > p - 1:
        return False

    left = fastExpMod(y, M, p)
    right = (fastExpMod(g, r, p) * fastExpMod(r, s, p)) % p
    return left == right


# 示例使用
if __name__ == '__main__':
    message = read_file("message.txt")

    p, y, d, g = generate_key()  # 生成ElGamal密钥
    # 生成签名

    r, s = elgamal_sign(int(message), p, g, d)
    print("ELGamal签名后的结果为：")
    print("r=" + str(r))
    print("s=" + str(s))

    # 验证签名
    m = elgamal_verify(int(message), r, s, p, g, y)
    print("ELGamal签名验证的结果为：", m)
