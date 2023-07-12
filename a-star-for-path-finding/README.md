## A* algorithm for path finding problem


```
Check existence a path from `start` to `finish`
```


Simple algorithm like BFS

```python
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
```


A* algorithm with a simple heuristic using Euclid distances

```python
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
```
