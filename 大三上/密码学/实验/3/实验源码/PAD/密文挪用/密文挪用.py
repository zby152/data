from codes.cryptography.lab_3.AES_encode import AES


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


def divide_c(msgs):
    part_c = []
    part = ""
    final_part = msgs[len(msgs) - 32:]
    msgs = msgs[:len(msgs) - 32]
    for index in range(len(msgs)):
        part += msgs[index]
        if (index + 1) % 32 == 0:
            part_c.append(part)
            part = ""
    if len(part) > 0:
        part_c.append(part)
    part_c.append(final_part)

    return part_c


def nuoyong(key, msg):
    messages = divide(msg)
    secrets = []
    length = 0
    for message in messages:
        if len(message) < 32:
            length = len(message)
            a = secrets[-1][:length]
            b = secrets[-1][length:]
            secrets[-1] = a
            b_M = b + message
            E_out = AES.encode(key, b_M)
            secrets.append(E_out)

        else:
            secret = AES.encode(key, message)
            secrets.append(secret)

    secrets_str = "".join(secrets)
    return length, secrets_str


def ennuoyong(key, secret_str, length):
    secrets = divide_c(secret_str)
    Ms = []
    for secret in secrets:
        if len(secret) < 32:
            Dn_out = AES.decode(key, secrets[-1])
            Mn = Dn_out[32-length:]
            b = Dn_out[:32-length]
            D_in = secret + b
            M = AES.decode(key, D_in)
            Ms.append(M)
            Ms.append(Mn)
            break

        else:
            M = AES.decode(key, secret)
            Ms.append(M)

    message_str = "".join(Ms)
    return message_str


if __name__ == '__main__':
    # 加密
    key = AES.read_file("key.txt")
    msg = AES.read_file("message.txt")
    length, secret_str = nuoyong(key, msg)
    print("加密后的密文：")
    print(secret_str)

    # 解密
    M = ennuoyong(key, secret_str, length)
    print("解密后的明文为：")
    print(M)
