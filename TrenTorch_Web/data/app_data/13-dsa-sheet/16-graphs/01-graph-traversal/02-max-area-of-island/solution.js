// O(m * n) time, O(m * n) space where m = rows, n = cols
function maxIslandArea(grid) {
    const rows = grid.length;
    const cols = rows > 0 ? grid[0].length : 0;
    const seen = Array.from({ length: rows }, () => Array(cols).fill(false));
    let best = 0;
    
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            if (grid[r][c] === 1 && !seen[r][c]) {
                seen[r][c] = true;
                const stack = [[r, c]];
                let size = 0;
                
                while (stack.length > 0) {
                    const [x, y] = stack.pop();
                    size++;
                    
                    const neighbors = [
                        [x + 1, y],
                        [x - 1, y],
                        [x, y + 1],
                        [x, y - 1]
                    ];
                    
                    for (const [nx, ny] of neighbors) {
                        if (
                            nx >= 0 && nx < rows &&
                            ny >= 0 && ny < cols &&
                            grid[nx][ny] === 1 &&
                            !seen[nx][ny]
                        ) {
                            seen[nx][ny] = true;
                            stack.push([nx, ny]);
                        }
                    }
                }
                
                best = Math.max(best, size);
            }
        }
    }
    
    return best;
}

console.log(maxIslandArea([[1, 1, 0], [0, 1, 0], [0, 0, 1]]));
