from math import pow, sqrt
import time
from heapq import heappop, heappush


d = [
    (0, 1),
    (1, 0),
    (-1, 0),
    (0, -1),
]
matrix = [
    [0, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 0, 1, 0, 0, 1, 0, 1, 1],
    [1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
]


class Node:
    __slots__ = ("x", "y", "score")

    def __init__(self, x: int, y: int, score: float):
        self.x = x
        self.y = y
        self.score = score

    def __lt__(self, o):
        return self.score < o.score


def distance(u, v) -> float:
    return sqrt(pow(v[0] - u[0], 2) + pow(v[1] - u[1], 2))


def find(start, finish):
    m = len(matrix)
    n = len(matrix[0])

    visited = [[False] * n for _ in range(m)]

    priority_queue = [Node(start[0], start[1], distance(start, finish))]

    while len(priority_queue) > 0:
        current = heappop(priority_queue)
        if current.x == finish[0] and current.y == finish[1]:
            return True

        visited[current.x][current.y] = True
        for dx, dy in d:
            nx = current.x + dx
            ny = current.y + dy
            if nx < 0 or nx >= m:
                continue
            if ny < 0 or ny >= n:
                continue
            if visited[nx][ny] or matrix[nx][ny] == 1:
                continue

            heappush(priority_queue, Node(nx, ny, distance((nx, ny), finish)))

    return False


def main():
    n = 100_000

    start = time.perf_counter()
    for i in range(n):
        find((0, 0), (9, 9))

    print(f"{time.perf_counter()-start:.2f}")


if __name__ == "__main__":
    main()
