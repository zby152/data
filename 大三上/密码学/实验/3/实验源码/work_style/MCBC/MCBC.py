from codes.cryptography.lab_3.AES_encode import AES
from codes.cryptography.lab_3.AES_encode import MATH
import random
import os


def divide(msgs):
    """分割函数将输入每32个分割成一个列表"""
    part_msgs = []
    msg = ""
    for index in range(len(msgs)):
        msg += msgs[index]
        if (index + 1) % 32 == 0:
            part_msgs.append(msg)
            msg = ""
    if len(msg) > 0:
        print("出现短块，报错")
    return part_msgs


def MCBC(key, msg, Z):
    Ms = divide(msg)
    Cs = []
    E_in = MATH.xor(Ms[0], Z)
    Cs.append(AES.encode(key, E_in))
    for i in range(1, len(Ms)):
        E_M = MATH.xor(Cs[i - 1], Ms[i - 1])
        E_in = MATH.xor(Ms[i], E_M)

        Cs.append(AES.encode(key, E_in))

    secrets_str = "".join(Cs)

    return secrets_str


def enMCBC(key, secret_str, Z):
    secrets = divide(secret_str)
    Ms = []
    D_out = AES.decode(key, secrets[0])
    Ms.append(MATH.xor(D_out, Z))
    for i in range(1, len(secrets)):
        D_M = MATH.xor(secrets[i - 1], Ms[i - 1])
        D_out = AES.decode(key, secrets[i])
        Ms.append(MATH.xor(D_out, D_M))
    message_str = " ".join(Ms)
    return message_str


if __name__ == '__main__':
    # 设置工作目录为脚本所在目录
    script_dir = os.path.dirname(__file__)
    os.chdir("E:\\Python_code\\codes\\cryptography\\lab_3\\work_style\\MCBC")

    key = AES.read_file("key.txt")
    msg = AES.read_file("message.txt")
    characters = '0123456789abcdef'

    # 加密
    Z = ''.join(random.choice(characters) for _ in range(32))
    secret_str = MCBC(key, msg, Z)
    print("加密前的明文为:" + msg)
    print("MCBC加密后的密文为:" + secret_str)

    # 解密
    M = enMCBC(key, secret_str, Z)
    print("解密后的明文为：" + M)

    # print(len(msg))
