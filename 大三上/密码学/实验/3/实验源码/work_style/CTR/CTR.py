from codes.cryptography.lab_3.AES_encode import AES
from codes.cryptography.lab_3.AES_encode import MATH
import random
import os


def divide(msgs):
    """分割函数将输入每16个分割成一个列表"""
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


def CTR(key, msg, T):
    messages = divide(msg)
    secrets = []
    E_in = T
    for message in messages:
        length = len(message)
        E_out = AES.encode(key, E_in)
        E_out_ = E_out[:length]
        secret = MATH.xor(E_out_, message)
        secrets.append(secret)
        E_in = MATH.xor(E_in, '1')
    secrets_str = "".join(secrets)
    return secrets_str


def enCTR(key, secret_str, T):
    secrets = divide(secret_str)
    Ms = []
    D_in = T
    for secret in secrets:
        length = len(secret)
        D_out = AES.encode(key, D_in)
        D_out_ = D_out[:length]
        M = MATH.xor(D_out_, secret)
        Ms.append(M)
        D_in = MATH.xor(D_in, '1')
    message_str = " ".join(Ms)
    return message_str


if __name__ == '__main__':
    # 设置工作目录为脚本所在目录
    script_dir = os.path.dirname(__file__)
    os.chdir("E:\\Python_code\\codes\\cryptography\\lab_3\\work_style\\CTR")

    key = AES.read_file("key.txt")
    msg = AES.read_file("message.txt")
    characters = '0123456789abcdef'
    # 加密
    T = ''.join(random.choice(characters) for _ in range(32))
    secret_str = CTR(key, msg, T)
    print("加密前的明文为:" + msg)
    print("加密后的密文：" + secret_str)

    # 解密
    M = enCTR(key, secret_str, T)
    print("解密后的明文为：" + M)
    # print(len(msg))
