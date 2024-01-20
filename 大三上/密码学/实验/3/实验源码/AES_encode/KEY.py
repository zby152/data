from codes.cryptography.lab_3.AES_encode.MATH import *


def get_keys(Nb, Nr, Nk, key):
    """计算加密拓展密钥函数"""

    # 保存初始密钥
    W = ['' for _ in range(Nb * (Nr + 1))]  # 元素保存一个字
    for index in range(Nk):
        W[index] = key[index * 8:index * 8 + 8]

    # 计算RC
    max_size = int(Nb * (Nr + 1) / Nk)
    RC = ['' for _ in range(max_size)]
    RC[0] = '01'
    for index in range(max_size - 1):
        RC[index + 1] = xtime(RC[index])
        if len(RC[index + 1]) < 2:
            RC[index + 1] = '0' + RC[index + 1]

    # 计算Rcon
    Rcon = []
    for x in RC:
        Rcon.append(x + '000000')

    # 密钥拓展策略
    if Nk <= 6:
        for i in range(4, Nb * (Nr + 1)):
            temp = W[i - 1]
            if i % Nk == 0:
                temp = xor(SubByte(Rotl(temp)), Rcon[int(i / Nk) - 1])
            W[i] = xor(W[i - Nk], temp)
    else:
        for i in range(4, Nb * (Nr + 1)):
            temp = W[i - 1]
            if i % Nk == 0:
                temp = xor(SubByte(Rotl(temp)), Rcon[int(i / Nk) - 1])
            elif i % Nk == 4:
                temp = SubByte(temp)
            W[i] = xor(W[i - Nk], temp)
    return W


def i_get_round_keys(i_Nb, i_Nr, i_Nk, key):
    """得到逆轮密钥"""
    # 轮密钥拓展
    keys = get_round_keys(i_Nb, i_Nr, i_Nk, key)

    # 对除去首部和尾部的轮密钥执行列混合
    for index in range(1, i_Nr):
        keys[index] = i_MixColumn(keys[index])
    return keys


def get_round_keys(Nb, Nr, Nk, key):
    """获取轮密钥"""
    # 密钥拓展
    keys = get_keys(Nb, Nr, Nk, key)
    # 轮密钥选择
    result = ['' for _ in range(Nr + 1)]
    for index in range(Nr + 1):
        for j in range(Nb):
            result[index] += keys[index * Nb + j]

    # 返回轮密钥
    return result
