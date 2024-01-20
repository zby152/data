from RSA import *

if __name__ == "__main__":

    msg = read_file('message.txt')
    messages = divide(msg)
    print("明文为:" + str(msg))

    e, n, d = init()
    # e=79
    # n=3337
    # d=1019

    # 加密
    secrets = []
    for message in messages:
        secret = RSA_encode(int(message), e, n)
        secrets.append(secret)
    C = ''.join(map(str, secrets))
    print("RSA签名得到的结果为:" + C)

    # 解密
    Message = []
    for secret in secrets:
        M = RSA_decode(int(secret), d, n)
        Message.append(M)
    M = ''.join(map(str, Message))
    print("RSA验证签名的结果为:" + M)
