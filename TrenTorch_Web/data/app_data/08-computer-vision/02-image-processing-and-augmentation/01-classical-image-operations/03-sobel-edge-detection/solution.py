import numpy as np

KX = np.array([[-1.0, 0.0, 1.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 1.0]])


def sobel_gradients(img):
    img = np.asarray(img, dtype=float)
    H, W = img.shape
    gx = np.zeros((H - 2, W - 2))
    gy = np.zeros((H - 2, W - 2))
    for di in range(3):
        for dj in range(3):
            patch = img[di:H - 2 + di, dj:W - 2 + dj]
            gx += KX[di, dj] * patch
            gy += KX.T[di, dj] * patch
    return gx, gy


def sobel_magnitude(img):
    gx, gy = sobel_gradients(img)
    return np.sqrt(gx ** 2 + gy ** 2)
