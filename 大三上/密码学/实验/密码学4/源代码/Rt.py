# S = [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1]
S = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1]
N = 15
R = []

for t in range(N):
    Rt = 0
    for i in range(N):
        Rt += (2 * S[i] - 1) * (2 * S[(i + t) % N] - 1)
    R.append(Rt)
print(R)
