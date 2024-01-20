def xor(byte_a, byte_b):
    """2进制多项式加法"""
    # 获取两个加数最长长度
    size = max(len(byte_a), len(byte_b))

    # 将被加数转换成二进制列表形式并补齐最高位
    a_bits = bin(int(byte_a, 16))[2:]
    a = [int(bit) for bit in a_bits]
    b_bits = bin(int(byte_b, 16))[2:]
    b = [int(bit) for bit in b_bits]
    while len(a) < size * 4:
        a.insert(0, 0)
    while len(b) < size * 4:
        b.insert(0, 0)

    # 按位异或
    result = ''
    for index in range(size * 4):
        result += str(a[index] ^ b[index])

    # 运算结果转为16进制
    result = int(result, 2)
    result = hex(result)[2:]

    # 若结果为0则返回'0'
    while len(result) < size:
        result = '0' + result
    return result


def mul_x(byte_a, byte_b):
    """二进制多项式乘法"""
    # 将16进制转换成二进制列表形式
    a_bits = bin(int(byte_a, 16))[2:]
    a = [int(bit) for bit in a_bits]
    b_bits = bin(int(byte_b, 16))[2:]
    b = [int(bit) for bit in b_bits]
    # 初始化乘积多项式
    product = [0] * (len(a) + len(b) - 1)

    # 遍历第一个多项式的每个元素
    for i, coeff1 in enumerate(a):
        if coeff1 == 1:  # 只处理系数为1的项
            # 对第二个多项式的每个元素进行操作
            for j, coeff2 in enumerate(b):
                # 对应位的系数相乘，并在模 2 的条件下累加到乘积多项式中
                product[i + j] ^= (coeff1 & coeff2)
    result = ''
    for bit in product:
        result += str(bit)
    num = int(result, 2)
    # 将整数转换为十六进制字符串并返回（去掉前缀'0x'）
    return hex(num)[2:]


def mod_x(byte):
    """二进制多项式与不可约多项式的模除"""
    # 不可约多项式
    divisor = [1, 0, 0, 0, 1, 1, 0, 1, 1]
    divisor_length = len(divisor)

    # 被除数
    bits = bin(int(byte, 16))[2:]
    bits = [int(bit) for bit in bits]
    bits_length = len(bits)

    # 只要被除数位数大于不可约多项式则循环
    while bits_length >= divisor_length:
        coefficient = bits[0]

        # 对被除数的高位开始每一位与不可约多项式异或
        for i in range(divisor_length):
            bits[i] ^= (divisor[i] & coefficient)

        # 清除高位的0
        while bits_length > 0 and bits[0] == 0:
            bits.pop(0)
            bits_length -= 1

    result = ''
    for bit in bits:
        result += str(bit)
    if len(result) == 0:
        result = '0'
    num = int(result, 2)
    # 将整数转换为十六进制字符串并返回（去掉前缀'0x'）
    return hex(num)[2:]


def Rotl(word):
    """循环左移1个字节"""
    A = word[0:2]
    B = word[2:4]
    C = word[4:6]
    D = word[6:8]
    result = (B + C + D + A)
    return result


def SubByte(byte):
    """S盒变换"""
    S_box = [['63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB', '76'],
             ['CA', '82', 'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0'],
             ['B7', 'FD', '93', '26', '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15'],
             ['04', 'C7', '23', 'C3', '18', '96', '05', '9A', '07', '12', '80', 'E2', 'EB', '27', 'B2', '75'],
             ['09', '83', '2C', '1A', '1B', '6E', '5A', 'A0', '52', '3B', 'D6', 'B3', '29', 'E3', '2F', '84'],
             ['53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB', 'BE', '39', '4A', '4C', '58', 'CF'],
             ['D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', '7F', '50', '3C', '9F', 'A8'],
             ['51', 'A3', '40', '8F', '92', '9D', '38', 'F5', 'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2'],
             ['CD', '0C', '13', 'EC', '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73'],
             ['60', '81', '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DB'],
             ['E0', '32', '3A', '0A', '49', '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79'],
             ['E7', 'C8', '37', '6D', '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08'],
             ['BA', '78', '25', '2E', '1C', 'A6', 'B4', 'C6', 'E8', 'DD', '74', '1F', '4B', 'BD', '8B', '8A'],
             ['70', '3E', 'B5', '66', '48', '03', 'F6', '0E', '61', '35', '57', 'B9', '86', 'C1', '1D', '9E'],
             ['E1', 'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55', '28', 'DF'],
             ['8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F', 'B0', '54', 'BB', '16']]
    result = ''
    # 对每一个字节分别操作，高四位为行，第四位为列
    for i in range(0, len(byte), 2):
        x = int(byte[i], 16)
        y = int(byte[i + 1], 16)
        result += S_box[x][y]
    return result


def i_SubByte(byte):
    """逆S盒变换"""
    S_box = [['52', '09', '6A', 'D5', '30', '36', 'A5', '38', 'BF', '40', 'A3', '9E', '81', 'F3', 'D7', 'FB'],
             ['7C', 'E3', '39', '82', '9B', '2F', 'FF', '87', '34', '8E', '43', '44', 'C4', 'DE', 'E9', 'CB'],
             ['54', '7B', '94', '32', 'A6', 'C2', '23', '3D', 'EE', '4C', '95', '0B', '42', 'FA', 'C3', '4E'],
             ['08', '2E', 'A1', '66', '28', 'D9', '24', 'B2', '76', '5B', 'A2', '49', '6D', '8B', 'D1', '25'],
             ['72', 'F8', 'F6', '64', '86', '68', '98', '16', 'D4', 'A4', '5C', 'CC', '5D', '65', 'B6', '92'],
             ['6C', '70', '48', '50', 'FD', 'ED', 'B9', 'DA', '5E', '15', '46', '57', 'A7', '8D', '9D', '84'],
             ['90', 'D8', 'AB', '00', '8C', 'BC', 'D3', '0A', 'F7', 'E4', '58', '05', 'B8', 'B3', '45', '06'],
             ['D0', '2C', '1E', '8F', 'CA', '3F', '0F', '02', 'C1', 'AF', 'BD', '03', '01', '13', '8A', '6B'],
             ['3A', '91', '11', '41', '4F', '67', 'DC', 'EA', '97', 'F2', 'CF', 'CE', 'F0', 'B4', 'E6', '73'],
             ['96', 'AC', '74', '22', 'E7', 'AD', '35', '85', 'E2', 'F9', '37', 'E8', '1C', '75', 'DF', '6E'],
             ['47', 'F1', '1A', '71', '1D', '29', 'C5', '89', '6F', 'B7', '62', '0E', 'AA', '18', 'BE', '1B'],
             ['FC', '56', '3E', '4B', 'C6', 'D2', '79', '20', '9A', 'DB', 'C0', 'FE', '78', 'CD', '5A', 'F4'],
             ['1F', 'DD', 'A8', '33', '88', '07', 'C7', '31', 'B1', '12', '10', '59', '27', '80', 'EC', '5F'],
             ['60', '51', '7F', 'A9', '19', 'B5', '4A', '0D', '2D', 'E5', '7A', '9F', '93', 'C9', '9C', 'EF'],
             ['A0', 'E0', '3B', '4D', 'AE', '2A', 'F5', 'B0', 'C8', 'EB', 'BB', '3C', '83', '53', '99', '61'],
             ['17', '2B', '04', '7E', 'BA', '77', 'D6', '26', 'E1', '69', '14', '63', '55', '21', '0C', '7D']]

    # 对每一个字节分别操作，高四位为行，第四位为列
    result = ''
    for i in range(0, len(byte), 2):
        x = int(byte[i], 16)
        y = int(byte[i + 1], 16)
        result += S_box[x][y]
    return result


def xtime(byte):
    """倍乘函数"""
    x = mul_x(byte, '02')
    result = mod_x(x)
    return result


def i_MixColumn(State):
    """逆列混合变换"""
    # 状态转为字节形式存储
    states = [State[i * 2:i * 2 + 2] for i in range(16)]

    # 逆变换矩阵
    MIX_C = [['e', 'b', 'd', '9'], ['9', 'e', 'b', 'd'], ['d', '9', 'e', 'b'], ['b', 'd', '9', 'e']]

    # 矩阵乘法
    result = ['00'] * 16
    for row in range(4):
        for col in range(4):
            for Round in range(4):
                result[row + col * 4] = xor(mul_x(MIX_C[row][Round], states[Round + col * 4]), result[row + col * 4])
            result[row + col * 4] = mod_x(result[row + col * 4])

    # 结果拼接成整个字符串
    state = ''
    for i in range(16):
        while len(result[i]) < 2:
            result[i] = '0' + result[i]
        state += result[i]
    return state
