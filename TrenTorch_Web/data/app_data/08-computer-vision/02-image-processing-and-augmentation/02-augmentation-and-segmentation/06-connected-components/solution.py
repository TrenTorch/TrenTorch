import numpy as np
from collections import deque


def label_components(binary):
    b = np.asarray(binary)
    H, W = b.shape
    labels = np.zeros((H, W), dtype=int)
    count = 0
    for i in range(H):
        for j in range(W):
            if b[i, j] and labels[i, j] == 0:
                count += 1
                labels[i, j] = count
                queue = deque([(i, j)])
                while queue:
                    y, x = queue.popleft()
                    for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= ny < H and 0 <= nx < W and b[ny, nx] and labels[ny, nx] == 0:
                            labels[ny, nx] = count
                            queue.append((ny, nx))
    return labels, count
