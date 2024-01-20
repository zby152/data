from codes.cryptography.lab_3.AES_encode import AES
from codes.cryptography.lab_3.AES_encode import MATH


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


def xulie(key, msg):
    messages = divide(msg)
    secrets = []
    for message in messages:
        if len(message) < 32:
            X_in = AES.encode(key, secrets[-1])
            X_in = X_in[:len(message)]
            X_out=MATH.xor(X_in, message)
            secrets.append(X_out)
        else:
            secret = AES.encode(key, message)
            secrets.append(secret)

    secrets_str = "".join(secrets)
    return secrets_str


def enxulie(key, secret_str):
    secrets = divide(secret_str)
    Ms = []
    for secret in secrets:
        if len(secret) < 32:
            X_in = AES.encode(key, secrets[-2])
            X_in = X_in[:len(secret)]
            X_out=MATH.xor(X_in, secret)
            Ms.append(X_out)
        else:
            M = AES.decode(key, secret)
            Ms.append(M)

    message_str = "".join(Ms)
    return message_str


if __name__ == '__main__':
    # 加密
    key = AES.read_file("key.txt")
    msg = AES.read_file("message.txt")
    secret_str = xulie(key, msg)
    print("加密后的密文：")
    print(secret_str)

    # 解密
    M = enxulie(key, secret_str)
    print("解密后的明文为：")
    print(M)
