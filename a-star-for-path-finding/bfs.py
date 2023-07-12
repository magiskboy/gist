from queue import LifoQueue
import time


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


def find(start, finish):
    visited = [[False] * len(matrix[0]) for _ in range(len(matrix))]

    q = LifoQueue()
    q.put(start)

    while not q.empty():
        current = q.get()
        if current == finish:
            return True

        visited[current[0]][current[1]] = True
        for dx, dy in d:
            nx = current[0] + dx
            ny = current[1] + dy
            if nx < 0 or nx >= len(matrix):
                continue
            if ny < 0 or ny >= len(matrix[0]):
                continue
            if visited[nx][ny] or matrix[nx][ny] == 1:
                continue

            q.put((nx, ny))

    return False


def main():
    n = 100_000

    start = time.perf_counter()
    for i in range(n):
        find((0, 0), (9, 9))

    print(f"{time.perf_counter()-start:.2f}")


if __name__ == "__main__":
    main()
