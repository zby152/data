from place_change import *


def read_file(filename):
    """读取文件名中的字符串并返回"""
    try:
        fp = open(filename, "r", encoding='utf-8')
        msg = fp.read()
        fp.close()
        return msg
    except:
        print("Open file error!")


def key_str_bit(msg):
    """将密钥字符串转变为二进制流"""
    bits = ""
    count = 0
    for i in msg:
        ascii = bin(ord(i))[2:]  # 得到msg其中一个字符的ascii码的二进制表示

        # 第八位偶校验位
        count = 0
        for j in range(7 - len(ascii)):
            ascii = '0' + ascii
        for j in ascii:
            if j == '1':
                count += 1
        if count % 2 == 0:
            ascii += '0'
        else:
            ascii += '1'

        bits += ascii
    return bits


def left_shift(c, times):
    """循环左移一定位数"""
    d = c.copy()
    for index in range(times):
        d.insert(len(d), d[0])
        d.remove(d[0])
    return d


def get_keys(key_path):
    """获得16个子密钥函数"""
    # 读取密钥文件
    key = read_file(key_path)
    # 密钥转换成比特流形式
    key_bit = key_str_bit(key)
    # key_bit = '0011000100110010001100110011010000110101001101100011011100111000'
    # 密钥置换选择1
    key1 = PC_1(key_bit)
    key_c = [[] * 28] * 17
    key_d = [[] * 28] * 17
    key_c[0] = key1[0:28]
    key_d[0] = key1[28:]
    # 将所有的c和d循环左移得到所有c和d
    left_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    for i in range(16):
        key_c[i + 1] = left_shift(key_c[i], left_table[i])
        key_d[i + 1] = left_shift(key_d[i], left_table[i])

    # 获取16个子密钥
    keys = [[] * 48] * 17
    for i in range(1, 17):
        key_cx = key_c[i]
        key_dx = key_d[i]
        key_cx.extend(key_dx)
        keys[i] = PC_2(key_cx)
    return keys
