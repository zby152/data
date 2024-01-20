import functools


def generate_m_sequence(primitive_poly, length):
    # 初始化LFSR状态（不全为0）
    lfsr = [1] * length

    # 生成序列
    sequence = []
    for _ in range(2 ** length - 1):
        # 将LFSR的当前状态作为序列的下一个元素
        sequence.append(lfsr[-1])

        # 计算新的反馈位
        feedback_bit = functools.reduce(lambda x, y: x ^ y, [lfsr[i] for i in range(length) if primitive_poly[i]])

        # 更新LFSR状态
        lfsr = [feedback_bit] + lfsr[:-1]

    return sequence


# 本原多项式
primitive_poly = [1, 0, 0, 1, 1]

# 生成m序列
m_sequence = generate_m_sequence(primitive_poly, len(primitive_poly) - 1)

print(m_sequence)
