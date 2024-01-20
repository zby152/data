import struct
import random

global bytes_per_sector, sectors_per_cluster, data_start_sector, sectors_per_fat, fat_start, \
    reserved_sectors, number_of_fats


def initialize_fat32_parameters(file_path):
    """初始化，获得映像文件参数信息"""
    global bytes_per_sector, sectors_per_cluster, data_start_sector, sectors_per_fat, \
        fat_start, reserved_sectors, number_of_fats

    with open(file_path, 'rb') as f:
        # 读取BPB（BIOS参数块）中的一些基本信息
        f.seek(11, 0)
        bytes_per_sector = struct.unpack('H', f.read(2))[0]
        sectors_per_cluster = struct.unpack('B', f.read(1))[0]
        reserved_sectors = struct.unpack('H', f.read(2))[0]
        number_of_fats = struct.unpack('B', f.read(1))[0]

        # 跳过一些不必要的信息
        f.seek(36, 0)
        sectors_per_fat = struct.unpack('I', f.read(4))[0]

        # 计算FAT表和数据区的起始位置
        fat_start = reserved_sectors
        data_start_sector = reserved_sectors + number_of_fats * sectors_per_fat


def read_sector(f, sector_number):
    """读取指定扇区的数据"""
    f.seek(sector_number * bytes_per_sector)
    return f.read(bytes_per_sector)


def get_cluster_chain(f, start_cluster):
    """获取文件簇链"""

    global bytes_per_sector, fat_start
    cluster_chain = []
    current_cluster = start_cluster
    while current_cluster < 0x0FFFFFF8:
        cluster_chain.append(current_cluster)
        fat_offset = current_cluster * 4
        f.seek(fat_start * bytes_per_sector + fat_offset)
        current_cluster = struct.unpack('I', f.read(4))[0]
    return cluster_chain


def get_file_cluster_chain(file_path, filename_to_find):
    """找到文件名的簇链表"""
    global bytes_per_sector, sectors_per_cluster, reserved_sectors, number_of_fats, sectors_per_fat, fat_start
    with open(file_path, 'rb') as f:

        # 定位到根目录
        root_dir_sectors = (reserved_sectors + (number_of_fats * sectors_per_fat)) * bytes_per_sector
        f.seek(root_dir_sectors, 0)

        # 搜索文件
        while True:
            dir_entry = f.read(32)
            if not dir_entry or dir_entry[0] == 0xE5:
                continue
            if dir_entry[0] == 0x00:
                break

            filename = dir_entry[0:11].decode('ascii').rstrip()
            if filename == filename_to_find.upper():
                start_cluster = struct.unpack('H', dir_entry[26:28])[0] | (
                    struct.unpack('H', dir_entry[20:22])[0] << 16)
                cluster_chain = get_cluster_chain(f, start_cluster)
                return cluster_chain  # 返回簇链表

        return None  # 如果找不到文件，返回None


def get_filename(file_path):
    """取得映像文件中所有的文件名"""
    global bytes_per_sector, sectors_per_cluster, reserved_sectors, number_of_fats, sectors_per_fat
    filename = []
    # 打开IMG文件
    with open(file_path, 'rb') as f:

        # 定位到根目录
        root_dir_sectors = (reserved_sectors + (number_of_fats * sectors_per_fat)) * bytes_per_sector
        f.seek(root_dir_sectors, 0)

        # 读取根目录项
        while True:
            # 读取32字节的目录项
            dir_entry = f.read(32)
            if not dir_entry or dir_entry[0] == 0xE5:
                # 如果目录项为空或已删除，则跳过
                continue
            if dir_entry[0] == 0x00:
                # 如果目录项为0，则表示目录项列表结束
                break
            # 解析文件名
            filename.append(dir_entry[0:11].decode('ascii').rstrip())
    return filename


def read_cluster_data(f, cluster_number):
    global bytes_per_sector, sectors_per_cluster, data_start_sector

    cluster_offset = (cluster_number - 2) * sectors_per_cluster
    cluster_sector = data_start_sector + cluster_offset
    f.seek(cluster_sector * bytes_per_sector)
    return f.read(sectors_per_cluster * bytes_per_sector)


def get_cluster_contents(file_path, filename_to_find, cluster_number_to_get):
    """找到磁盘映像对应文件选中簇号的数据"""
    global bytes_per_sector, sectors_per_cluster, reserved_sectors, number_of_fats, \
        sectors_per_fat, fat_start, data_start_sector

    with open(file_path, 'rb') as f:

        # 搜索文件的簇链
        f.seek((reserved_sectors + number_of_fats * sectors_per_fat) * bytes_per_sector, 0)
        while True:
            dir_entry = f.read(32)
            if not dir_entry or dir_entry[0] == 0xE5:
                continue
            if dir_entry[0] == 0x00:
                break

            filename = dir_entry[0:11].decode('ascii').rstrip()
            if filename == filename_to_find.upper():
                start_cluster = struct.unpack('H', dir_entry[26:28])[0] | (
                    struct.unpack('H', dir_entry[20:22])[0] << 16)
                cluster_chain = get_cluster_chain(f, start_cluster)
                if cluster_number_to_get in cluster_chain:
                    return read_cluster_data(f, cluster_number_to_get)
                else:
                    print("簇号为"+cluster_number_to_get+"的簇不在文件"+filename+"的簇链中")
                    return None
        print("文件"+filename_to_find+"不存在")
        return None


def replace_with_random_bytes(cluster_data):
    """替换cluster_data的内容为相同长度的随机字节"""
    # 获取原始数据的长度
    data_length = len(cluster_data)

    # 生成相同长度的随机字节
    random_bytes = bytes(random.getrandbits(8) for _ in range(data_length))

    return random_bytes


def write_cluster_data(file_path, cluster_number, new_data):
    """将数据写入簇号的指定位置"""
    global bytes_per_sector, sectors_per_cluster, data_start_sector

    cluster_offset = (cluster_number - 2) * sectors_per_cluster
    cluster_sector = data_start_sector + cluster_offset

    with open(file_path, 'r+b') as f:  # 'r+b' 模式用于读写
        f.seek(cluster_sector * bytes_per_sector)
        f.write(new_data)


def clear_directory_entry(file_path, filename_to_clear):
    """清理文件目录表"""
    global bytes_per_sector, sectors_per_cluster, reserved_sectors, number_of_fats, sectors_per_fat
    with open(file_path, 'r+b') as f:
        # 计算根目录的起始位置
        root_dir_sectors = (reserved_sectors + (number_of_fats * sectors_per_fat)) * bytes_per_sector
        f.seek(root_dir_sectors, 0)

        # 搜索文件
        while True:
            dir_entry_pos = f.tell()
            dir_entry = f.read(32)
            if not dir_entry or dir_entry[0] == 0xE5:
                continue
            if dir_entry[0] == 0x00:
                break

            filename = dir_entry[0:11].decode('ascii').rstrip()
            if filename == filename_to_clear.upper():
                f.seek(dir_entry_pos)
                f.write(b'\x00' * 32)  # 清零目录项
                print(filename_to_clear + "文件的目录表已经被清除")
                return

        print(filename_to_clear + "文件不存在")


def clear_fat_chain(file_path, cluster_chain):
    """清理文件簇链表"""
    global bytes_per_sector, fat_start

    with open(file_path, 'r+b') as f:
        # 将选中文件的簇链表所有项替换为0
        for cluster in cluster_chain:
            # FAT表中每个簇的条目是4字节
            fat_offset = cluster * 4
            f.seek(fat_start * bytes_per_sector + fat_offset)
            f.write(b'\x00\x00\x00\x00')


if __name__ == '__main__':

    # 磁盘映像文件
    filepath = 'image.img'
    # 要删除的文件名
    file = 'TEST    TXT'

    # 读取文件得FAT32参数
    initialize_fat32_parameters(filepath)

    # 打印所有文件名
    filenames = get_filename(filepath)
    print("该软盘映像文件中所有的文件的文件名为：")
    print(filenames[1::2])

    # 查找文件的簇链表
    cluster_chain = get_file_cluster_chain(filepath, file)
    print("选中的文件的簇链表为：")
    print(cluster_chain)

    # 打印对应文件对应簇内容,并生成替换后的簇
    cluster_datas = []
    replaced_cluster_datas = []
    for cluster in cluster_chain:
        # 原始簇号数据
        cluster_data = get_cluster_contents(filepath, file, cluster)
        cluster_datas.append(cluster_data)
        # 替换簇号数据
        replaced_cluster_data = replace_with_random_bytes(cluster_data)
        replaced_cluster_datas.append(replaced_cluster_data)
        # 簇内容替换
        write_cluster_data(filepath, cluster, replaced_cluster_data)

    # 打印原始簇内容
    print(cluster_datas)
    # 打印替换簇内容
    print(replaced_cluster_datas)

    # 清理文件目录项
    clear_directory_entry(filepath, file)
    # 清理文件簇链表
    clear_fat_chain(filepath, cluster_chain)
