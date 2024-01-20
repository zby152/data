def find_points_on_elliptic_curve(a, b, p):
    points = []
    for x in range(p):
        y_squared = (x ** 3 + a * x + b) % p
        for y in range(p):
            if (y * y) % p == y_squared:
                points.append((x, y))
    return points


def print_points_in_groups(points,  width=2):
    for i, point in enumerate(points):
        # 使用字符串格式化来确保对齐
        formatted_point = f"({point[0]:>{width}}, {point[1]:>{width}})"
        print(formatted_point, end=' ')
        if (i + 1) % 10 == 0:
            print()  # 每 group_size 个点后换行
    print()  # 在列表末尾换行


if __name__ == '__main__':
    a = 1  # 曲线参数 a
    b = 1  # 曲线参数 b
    p = 23  # 质数 p

    points = find_points_on_elliptic_curve(a, b, p)
    print("给出的椭圆曲线的所有解点为")
    print_points_in_groups(points)
