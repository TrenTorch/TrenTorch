def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:
        return image
    rows, cols = len(image), len(image[0])
    image[sr][sc] = color
    stack = [(sr, sc)]
    while stack:
        x, y = stack.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < rows and 0 <= ny < cols and image[nx][ny] == old:
                image[nx][ny] = color
                stack.append((nx, ny))
    return image
