import os
import ctypes


def search_exe_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".exe"):
                file_path = os.path.join(root, file)
                ctypes.windll.user32.MessageBoxW(0, file_path, "EXE File Found", 1)


# 指定要搜索的目录路径
directory_path = r"E:\lab3_PE"

search_exe_files(directory_path)
