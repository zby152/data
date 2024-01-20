from KEY import *
from F import *


def str_bit(msg):
    """读入的明文信息转换成二进制比特形式,高位补0"""
    bits = ""
    for i in msg:
        ascii = bin(ord(i))[2:]
        for j in range(8 - len(ascii)):
            ascii = '0' + ascii
        bits += ascii
    return bits


def encode(message_bit):
    """加密"""
    # 初始置换
    message_PC = PC_IP(message_bit)
    # 取得L0和R0
    Ls = [[] * 32] * 17
    Rs = [[] * 32] * 17
    Ls[0] = message_PC[0:32]
    Rs[0] = message_PC[32:]

    # 加密迭代
    for i in range(16):
        Ls[i + 1] = Rs[i]
        Rs[i + 1] = xor(Ls[i], f(Rs[i], keys[i + 1]))
    # 逆初始置换
    LandR = Rs[16] + Ls[16]
    result = PC_IP_1(LandR)
    return result


def decode(secret):
    """解密"""
    keys = get_keys("key.txt")

    message_PC = PC_IP(secret)
    Ls = [[] * 32] * 17
    Rs = [[] * 32] * 17
    Ls[0] = message_PC[0:32]
    Rs[0] = message_PC[32:]

    for i in range(16):
        Ls[i + 1] = Rs[i]
        Rs[i + 1] = xor(Ls[i], f(Rs[i], keys[16 - i]))  # 密钥从16开始使用

    LandR = Rs[16] + Ls[16]
    result = PC_IP_1(LandR)
    letters = ""

    for i in range(8):
        bits = ""
        for j in range(8):
            bits += str(result[i * 8 + j])
        letter = chr(int(bits, 2))
        letters += letter

    return letters


def divide(msgs):
    """分割函数将输入每64个分割成一个列表"""
    part_msgs = []
    msg = ""
    for index in range(len(msgs)):
        msg += msgs[index]
        if (index + 1) % 64 == 0:
            part_msgs.append(msg)
            msg = ""
    if len(msg) > 0:
        for index in range(64 - len(msg)):
            msg += '0'
        part_msgs.append(msg)
    return part_msgs


if __name__ == "__main__":
    # 密钥迭代生成子密钥
    keys = get_keys("key.txt")
    # 读出明文转换为二进制流后分割成组
    messages = read_file("message.txt")
    print("明文为：")
    print(messages)
    message_bit = str_bit(messages)
    messages = divide(message_bit)
    # 加密
    secrets = []
    for message in messages:
        secret = encode(message)
        secrets.append(secret)
    print("加密得到的密文为")
    for index in range(len(secrets)):
        print(secrets[index])

    # 解密
    M = ""
    for secret in secrets:
        m = decode(secret)
        M += m
    print("解密过程得到的明文为：")
    print(M)
