def read_exe_file(exe_path):
    """读取exe文件后以字符串数组形式返回"""
    hex_data = []
    with open(exe_path, 'rb') as f:
        byte = f.read(1)
        while byte:
            hex_data.append(byte.hex())
            byte = f.read(1)

    return hex_data


def write_bytes_to_exe(exe_path, start_offset, data):
    """将指定数据写入exe的指定位置"""
    k = 0
    with open(exe_path, 'r+b') as f:
        for x in data:
            f.seek(start_offset + k)
            f.write(x)
            k = k + 1


def string_to_hex(string):
    """将字符串类型数据转换为16进制类型"""
    decimal = int(string, 16)
    # 将整数转换为十六进制字符串
    hex_string = hex(decimal)

    return hex_string


def get_entry_point(hex_datas):
    """计算程序入口地址并得到程序入口地址的内容"""
    Signature_add = int('0x' + hex_datas[63] + hex_datas[62] + hex_datas[61] + hex_datas[60], 16)

    entry_point_add = Signature_add + 40

    entry_point = [hex_datas[entry_point_add], hex_datas[entry_point_add + 1],
                   hex_datas[entry_point_add + 2], hex_datas[entry_point_add + 3]]
    return entry_point, entry_point_add


def get_old_entry_b(datas, entry_point):
    """找到旧的程序入口点地址并转换成字节类型"""
    other_entry_add = 0

    for index in range(0, len(datas)):
        if (datas[index] == entry_point[0] and datas[index + 1] == entry_point[1] and
                datas[index + 2] == entry_point[2] and datas[index + 3] == entry_point[3]):
            other_entry_add = index

    old_entry_add = other_entry_add + 4
    old_entry = [datas[old_entry_add], datas[old_entry_add + 1],
                 datas[old_entry_add + 2], datas[old_entry_add + 3]]

    old_entry_b = [bytes([int(s, 16)]) for s in old_entry]
    return old_entry_b


if __name__ == '__main__':
    # 指定要读取的可执行文件路径
    exe_path = 'E:\\lab3_PE\\test.exe'

    # 得到可执行文件的数据以字符数组的方式存放
    exe_datas = read_exe_file(exe_path)
    # print(datas)

    # 得到程序入口点地址和内容
    entry_point, entry_point_add = get_entry_point(exe_datas)
    # print(entry_point)

    # 得到旧的程序入口点地址
    old_entry_b = get_old_entry_b(exe_datas, entry_point)
    # print(old_entry_b)

    # 将旧的程序入口点地址写入程序入口地址
    write_bytes_to_exe(exe_path, entry_point_add, old_entry_b)
