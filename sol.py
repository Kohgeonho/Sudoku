import sys
from time import time

def input_single(dtype=int):
    return dtype(sys.stdin.readline().strip())

def input_list(dtype=int, fast=False):
    if not fast:
        return [dtype(i) for i in input().split()]
    return [dtype(i) for i in sys.stdin.readline().strip().split()]
monitor = False

B = []
for _ in range(9):
    B.append(input_list())

def confidence_blank(board=B):
    candidates = {}
    conf = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                candidates[(i, j)] = set(range(10))
                for k in range(9):
                    candidates[(i, j)].discard(board[i][k])
                    candidates[(i, j)].discard(board[k][j])
                bi, bj = i // 3, j // 3
                for ci in range(3):
                    for cj in range(3):
                        candidates[(i, j)].discard(board[3 * bi + ci][3 * bj + cj])

    while True:           
        again = False
        for i, j in list(candidates.keys()):
            if len(candidates[(i, j)]) == 0:
                return conf, None
            elif len(candidates[(i, j)]) == 1:
                again = True
                v = candidates.pop((i, j)).pop()
                for ci, cj in candidates:
                    if ci == i or cj == j or (ci // 3 == i // 3 and cj // 3 == j // 3):
                        candidates[(ci, cj)].discard(v)
                board[i][j] = v
                conf.append((i, j))

        if not again:
            break

    return conf, candidates

def solution():

    conf, candidates = confidence_blank()
    if candidates is None:
        for _i, _j in conf:
            B[_i][_j] = 0
        return False
    elif len(candidates) == 0:
        return True
    (i, j), _ = min(candidates.items(), key=lambda x: len(x[1]))

    for v in candidates[(i, j)]:
        B[i][j] = v
        if solution():
            return True

    B[i][j] = 0
    for _i, _j in conf:
        B[_i][_j] = 0
    return False

solution()
for i in range(9):
    print(' '.join([str(b) for b in B[i]]))
