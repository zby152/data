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
        part_msgs.append(msg)
    return part_msgs


def Pad(msg):
    pad = 1
    msg = msg + '1'
    while len(msg) < 32:
        pad += 1
        msg = msg + '0'
    return pad, msg


def dePad(msg, pad):
    msg = msg[:-pad]
    return msg


def XCBC(key, msg, Z):
    Ms = divide(msg)
    Cs = []
    E_in = MATH.xor(Ms[0], Z)
    Cs.append(AES.encode(key[0], E_in))
    pad = 0
    for i in range(1, len(Ms) - 1):
        E_in = MATH.xor(Ms[i], Cs[i - 1])
        Cs.append(AES.encode(key[0], E_in))
    if len(Ms[-1]) < 32:
        pad, M_p = Pad(Ms[-1])
        E_in = MATH.xor(M_p, Cs[-1])
        E_in = MATH.xor(E_in, key[2])
        Cs.append(AES.encode(key[0], E_in))
    else:
        E_in = MATH.xor(Ms[-1], Cs[-1])
        E_in = MATH.xor(E_in, key[1])
        Cs.append(AES.encode(key[0], E_in))

    secrets_str = "".join(Cs)

    return pad, secrets_str


def enXCBC(key, secret_str, Z, pad):
    secrets = divide(secret_str)
    Ms = []
    D_out = AES.decode(key[0], secrets[0])
    Ms.append(MATH.xor(D_out, Z))
    for i in range(1, len(secrets) - 1):
        D_out = AES.decode(key[0], secrets[i])
        Ms.append(MATH.xor(D_out, secrets[i - 1]))
    if pad > 0:
        D_out = AES.decode(key[0], secrets[-1])
        M_P = MATH.xor(D_out, key[2])
        M_P = MATH.xor(M_P, secrets[-2])
        M = dePad(M_P, pad)
        Ms.append(M)
    else:
        D_out = AES.decode(key[0], secrets[-1])
        M = MATH.xor(D_out, key[1])
        M = MATH.xor(M, secrets[-2])
        Ms.append(M)

    message_str = " ".join(Ms)
    return message_str


if __name__ == '__main__':
    # 设置工作目录为脚本所在目录
    script_dir = os.path.dirname(__file__)
    os.chdir("E:\\Python_code\\codes\\cryptography\\lab_3\\work_style\\XCBC")

    keys = AES.read_file("keys.txt")
    keys = keys.split()
    msg = AES.read_file("message.txt")
    characters = '0123456789abcdef'

    # 加密
    Z = ''.join(random.choice(characters) for _ in range(32))
    pad, secret_str = XCBC(keys, msg, Z)
    print("加密前的明文为:" + msg)
    print("XCBC加密后的密文为:" + secret_str)

    # 解密
    M = enXCBC(keys, secret_str, Z, pad)
    print("解密后的明文为：" + M)
    # print(len(msg))
