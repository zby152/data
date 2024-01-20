m32 = pow(2, 32)


def rot(X, i):
    """循环左移"""
    return ((X << i) & 0xffffffff) | (X >> (32 - i))


def mod32(R, X):
    """模2^32加法"""
    return (R + X) % m32


def H_15(X):
    """取高16"""
    bits = (X >> 15) & 0xffff
    return bits


def H_16(X):
    """取高16"""
    bits = (X >> 16) & 0xffff
    return bits


def L(X):
    """取低16位"""
    bits = X & 0xffff
    return bits


def splicing_word(W1, W2):
    """将两个16bit的值拼接到一起"""
    W1_ = W1 << 16
    return W1_ | W2


def splicing_s(k, d, iv):
    """密钥装入拼接"""
    s = (k << 23) | (d << 8) | iv
    return s


def int_hex(number):
    """整型转为16进制，便于调试"""
    return hex(number)[2:]
