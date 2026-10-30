import java.util.ArrayDeque;

public class Main {
    // O(R*C) time, O(R*C) space (R rows, C columns)
    static long largestIsland(long[][] grid) {
        int rows = grid.length;
        int cols = rows > 0 ? grid[0].length : 0;
        int[][] label = new int[rows][cols];
        int[] size = new int[rows * cols + 2];
        int nextId = 1;
        int[] dxs = {1, -1, 0, 0};
        int[] dys = {0, 0, 1, -1};
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 1 && label[r][c] == 0) {
                    label[r][c] = nextId;
                    ArrayDeque<int[]> stack = new ArrayDeque<>();
                    stack.push(new int[]{r, c});
                    int count = 0;
                    while (!stack.isEmpty()) {
                        int[] cell = stack.pop();
                        int x = cell[0];
                        int y = cell[1];
                        count++;
                        for (int d = 0; d < 4; d++) {
                            int nx = x + dxs[d];
                            int ny = y + dys[d];
                            if (nx >= 0 && nx < rows && ny >= 0 && ny < cols
                                    && grid[nx][ny] == 1 && label[nx][ny] == 0) {
                                label[nx][ny] = nextId;
                                stack.push(new int[]{nx, ny});
                            }
                        }
                    }
                    size[nextId] = count;
                    nextId++;
                }
            }
        }
        long best = 0;
        for (int id = 1; id < nextId; id++) {
            best = Math.max(best, size[id]);
        }
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 0) {
                    int[] around = new int[4];
                    int k = 0;
                    for (int d = 0; d < 4; d++) {
                        int nx = r + dxs[d];
                        int ny = c + dys[d];
                        if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && label[nx][ny] != 0) {
                            int id = label[nx][ny];
                            boolean dup = false;
                            for (int i = 0; i < k; i++) {
                                if (around[i] == id) {
                                    dup = true;
                                    break;
                                }
                            }
                            if (!dup) {
                                around[k++] = id;
                            }
                        }
                    }
                    long total = 1;
                    for (int i = 0; i < k; i++) {
                        total += size[around[i]];
                    }
                    best = Math.max(best, total);
                }
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(largestIsland(new long[][]{new long[]{1L, 0L}, new long[]{0L, 1L}}));
    }
}
