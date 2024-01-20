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
        if (index + 1) % 16 == 0:
            part_msgs.append(msg)
            msg = ""
    if len(msg) > 0:
        part_msgs.append(msg)
    return part_msgs


def CFB(key, msg, I):
    messages = divide(msg)
    secrets = []
    E_in = I
    for message in messages:
        length = len(message)
        E_out = AES.encode(key, E_in)
        E_out_ = E_out[:length]
        secret = MATH.xor(E_out_, message)
        secrets.append(secret)
        E_in = (E_in[len(I) - length:] + secret)
    secrets_str = "".join(secrets)
    return secrets_str


def enCFB(key, secret_str, I):
    secrets = divide(secret_str)
    Ms = []
    D_in = I
    for secret in secrets:
        length = len(secret)
        D_out = AES.encode(key, D_in)
        D_out_ = D_out[:length]
        M = MATH.xor(D_out_, secret)
        Ms.append(M)
        D_in = D_in[len(I) - length:] + secret
    message_str = " ".join(Ms)
    return message_str


if __name__ == '__main__':
    # 设置工作目录为脚本所在目录
    script_dir = os.path.dirname(__file__)
    os.chdir("E:\\Python_code\\codes\\cryptography\\lab_3\\work_style\\CFB")

    key = AES.read_file("key.txt")
    msg = AES.read_file("message.txt")
    characters = '0123456789abcdef'

    # 加密
    I = ''.join(random.choice(characters) for _ in range(32))
    secret_str = CFB(key, msg, I)
    print("加密前的明文为:" + msg)
    print("正确加密后的密文：" + secret_str)

    # 解密
    M = enCFB(key, secret_str, I)
    print("解密后的明文为：" + M)

    # print(len(msg))
