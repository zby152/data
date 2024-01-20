from codes.cryptography.lab_3.AES_encode import AES
from codes.cryptography.lab_3.AES_encode import MATH
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


def EBC(key, msg):
    messages = divide(msg)
    secrets = []
    for message in messages:
        secret = AES.encode(key, message)
        secrets.append(secret)
    secrets_str = "".join(secrets)
    return secrets_str


def enEBC(key, secret_str):
    secrets = divide(secret_str)
    Ms = []
    for secret in secrets:
        M = AES.decode(key, secret)
        Ms.append(M)
    message_str = " ".join(Ms)
    return message_str


if __name__ == '__main__':
    # 设置工作目录为脚本所在目录
    script_dir = os.path.dirname(__file__)
    os.chdir("E:\\Python_code\\codes\\cryptography\\lab_3\\work_style\\ECB")

    key = AES.read_file("key.txt")
    msg = AES.read_file("message.txt")

    secret_str = EBC(key, msg)
    print("加密前的明文为:" + msg)
    print("加密后的密文为：" + secret_str)

    # 解密
    M = enEBC(key, secret_str)
    print("解密后的明文为：" + M)
    # print(len(msg))
