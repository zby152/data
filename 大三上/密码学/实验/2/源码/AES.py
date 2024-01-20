from KEY import *
from ROUND import *


def read_file(filename):
    """读取文件名中的字符串并返回"""
    try:
        fp = open(filename, "r", encoding='utf-8')
        msg = fp.read()
        fp.close()
        return msg
    except:
        print("Open file error!")


def encode(key, message):
    """AES加密"""

    # 计算相关参数
    Nrs = [[10, 12, 14], [12, 12, 14], [14, 14, 14]]
    Nb = int(len(message) * 4 / 32)  # 4
    Nk = int(len(key) * 4 / 32)  # 4
    Nr = Nrs[int(Nk / 2) - 2][int(Nb / 2) - 2]  # 10

    # 计算加密拓展密钥得到轮密钥
    round_keys = get_round_keys(Nb, Nr, Nk, key)

    # 论函数得到密文
    secret = Round(Nb, Nr, round_keys, message)

    # 输出密文
    return secret


def decode(secret):
    """AES解密"""
    # 计算相关参数
    Nrs = [[10, 12, 14], [12, 12, 14], [14, 14, 14]]
    i_Nb = int(len(secret) * 4 / 32)  # 4
    i_Nk = int(len(key) * 4 / 32)  # 4
    i_Nr = Nrs[int(i_Nk / 2) - 2][int(i_Nb / 2) - 2]  # 10
    # 计算逆轮密钥
    i_round_keys = i_get_round_keys(i_Nb, i_Nr, i_Nk, key)
    # 计算明文
    message = i_Round(i_Nb, i_Nr, i_round_keys, secret)
    return message


if __name__ == '__main__':
    key = read_file("key.txt")  # 128bit 16byte 4word
    msg = read_file("message.txt")
    # 加密
    secrets = encode(key, msg)
    print("明文"+msg+"加密得到的密文为："+secrets)

    # 解密
    Msg = decode(secrets)

    print("密文"+secrets+"解密得到的明文为："+Msg)
