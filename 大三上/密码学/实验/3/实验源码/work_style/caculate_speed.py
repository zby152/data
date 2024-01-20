import subprocess
import time


def measure_runtime(script_path):
    """计算程序运行速度"""
    start_time = time.time()  # 开始时间

    # 运行外部Python脚本
    result = subprocess.run(["python", script_path], capture_output=True, text=True)

    end_time = time.time()  # 结束时间
    runtime = end_time - start_time  # 计算运行时间

    byte_number = float(result.stdout)
    run_speed = runtime / byte_number
    return run_speed


# 调用函数，传入您想测量的Python脚本的路径
if __name__ == '__main__':
    speed_ECB = measure_runtime("ECB/ECB.py")
    print("ECB的每字节加密速度为： " + str(speed_ECB)+" s/byte")

    speed_MCBC = measure_runtime("MCBC/MCBC.py")
    print("MCBC的每字节加密速度为：" + str(speed_MCBC)+" s/byte")

    speed_CBC = measure_runtime("CBC/CBC.py")
    print("CBC的每字节加密速度为： " + str(speed_CBC) + " s/byte")

    speed_OFB = measure_runtime("OFB/OFB.py")
    print("OFB的每字节加密速度为： " + str(speed_OFB) + " s/byte")

    speed_CFB = measure_runtime("CFB/CFB.py")
    print("CFB的每字节加密速度为： " + str(speed_CFB) + " s/byte")

    speed_XCBC = measure_runtime("XCBC/XCBC.py")
    print("XCBC的每字节加密速度为：" + str(speed_XCBC) + " s/byte")

    speed_CTR = measure_runtime("CTR/CTR.py")
    print("CTR的每字节加密速度为： " + str(speed_CTR) + " s/byte")