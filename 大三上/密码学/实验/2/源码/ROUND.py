from MATH import *


def AddRoundKey(State, round_key):
    """轮密钥加"""
    # 直接异或
    return xor(State, round_key)


def ShiftRow(Nb, State):
    """行移位变换"""

    # 行移位矩阵
    shift_table = [[1, 2, 3], [1, 2, 3], [1, 3, 4]]
    c = shift_table[int(Nb / 2) - 2]

    # 整个状态拆分成4块
    states = ['', '', '', '']
    for j in range(4):
        states[j] = [State[i + j * 2:i + j * 2 + 2] for i in range(0, len(State), 8)]
        states[j] = ''.join(states[j])

    # 对后三块按照移位矩阵移位后保存到result中
    result = ['', '', '', '']
    result[0] = states[0]
    result[1] = shift(states[1], c[0])
    result[2] = shift(states[2], c[1])
    result[3] = shift(states[3], c[2])

    # 结果转换成一整个字符串
    output = ''
    for i in range(4):
        output += ''.join(item[i * 2:2 + i * 2] for item in result)
    return output


def i_ShiftRow(Nb, State):
    """逆行移位变换"""
    # 行移位矩阵
    shift_table = [[1, 2, 3], [1, 2, 3], [1, 3, 4]]
    c = shift_table[int(Nb / 2) - 2]

    # 整个状态拆分成4块
    states = ['', '', '', '']
    for j in range(4):
        states[j] = [State[i + j * 2:i + j * 2 + 2] for i in range(0, len(State), 8)]
        states[j] = ''.join(states[j])

    # 对后三块按照移位矩阵移位后保存到result中
    result = ['', '', '', '']
    result[0] = states[0]
    result[1] = shift(states[1], Nb - c[0])
    result[2] = shift(states[2], Nb - c[1])
    result[3] = shift(states[3], Nb - c[2])

    # 结果转换成一整个字符串
    output = ''
    for i in range(4):
        output += ''.join(item[i * 2:2 + i * 2] for item in result)
    return output


def shift(input, times):
    """根据次数进行4字节的移位"""
    for i in range(times):
        input = Rotl(input)
    return input


def MixColumn(State):
    """列混合变换"""
    # 状态转为字节形式存储
    states = [State[i * 2:i * 2 + 2] for i in range(16)]

    # 变换矩阵
    MIX_C = [['2', '3', '1', '1'], ['1', '2', '3', '1'], ['1', '1', '2', '3'], ['3', '1', '1', '2']]

    # 矩阵乘法
    result = ['00'] * 16
    for row in range(4):
        for col in range(4):
            for Round in range(4):
                result[row + col * 4] = xor(mul_x(MIX_C[row][Round], states[Round + col * 4]), result[row + col * 4])
            result[row + col * 4] = mod_x(result[row + col * 4])  # 模不可约多项式

    # 结果拼接成整个字符串
    state = ''
    for i in range(16):
        while len(result[i]) < 2:
            result[i] = '0' + result[i]
        state += result[i]
    return state


def Round(Nb, Nr, round_keys, message):
    """轮函数"""
    state = message
    # 初始密钥加
    state = AddRoundKey(state, round_keys[0])

    # 迭代控制
    for i in range(1, Nr):
        Round_key = round_keys[i]
        state = SubByte(state)
        state = ShiftRow(Nb, state)
        state = MixColumn(state)
        state = AddRoundKey(state, Round_key)

    # 最后一轮迭代
    Round_key = round_keys[Nr]
    state = SubByte(state)
    state = ShiftRow(Nb, state)
    state = AddRoundKey(state, Round_key)

    # 返回密文
    return state


def i_Round(Nb, Nr, round_keys, secret):
    """逆轮函数"""
    # 初始密钥加
    state = secret
    state = AddRoundKey(state, round_keys[-1])

    # 迭代控制
    for i in range(Nr, 1, -1):
        Round_key = round_keys[i - 1]
        state = i_SubByte(state)
        state = i_ShiftRow(Nb, state)
        state = i_MixColumn(state)
        state = AddRoundKey(state, Round_key)
    # 最后一轮迭代
    Round_key = round_keys[0]
    state = i_SubByte(state)
    state = i_ShiftRow(Nb, state)
    state = AddRoundKey(state, Round_key)

    # 返回明文
    return state
