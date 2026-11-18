import java.util.PriorityQueue;

public class Main {
    // O(rows * cols * log(rows * cols)) time, O(rows * cols) space
    static long minimumEffortPath(long[][] heights) {
        int rows = heights.length;
        int cols = heights[0].length;
        long[][] effort = new long[rows][cols];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                effort[i][j] = Long.MAX_VALUE;
            }
        }
        effort[0][0] = 0;

        PriorityQueue<Node> pq = new PriorityQueue<>();
        pq.offer(new Node(0, 0, 0));

        int[] dx = {1, -1, 0, 0};
        int[] dy = {0, 0, 1, -1};

        while (!pq.isEmpty()) {
            Node cur = pq.poll();
            long e = cur.effort;
            int x = cur.x;
            int y = cur.y;

            if (x == rows - 1 && y == cols - 1) {
                return e;
            }
            if (e > effort[x][y]) {
                continue;
            }

            for (int dir = 0; dir < 4; dir++) {
                int nx = x + dx[dir];
                int ny = y + dy[dir];
                if (nx >= 0 && nx < rows && ny >= 0 && ny < cols) {
                    long diff = Math.abs(heights[nx][ny] - heights[x][y]);
                    long ne = Math.max(e, diff);
                    if (ne < effort[nx][ny]) {
                        effort[nx][ny] = ne;
                        pq.offer(new Node(ne, nx, ny));
                    }
                }
            }
        }
        return 0;
    }

    private static class Node implements Comparable<Node> {
        long effort;
        int x;
        int y;

        Node(long effort, int x, int y) {
            this.effort = effort;
            this.x = x;
            this.y = y;
        }

        @Override
        public int compareTo(Node other) {
            return Long.compare(this.effort, other.effort);
        }
    }

    public static void main(String[] args) {
        System.out.println(minimumEffortPath(new long[][]{new long[]{1L, 2L, 2L}, new long[]{3L, 8L, 2L}, new long[]{5L, 3L, 5L}}));
    }
}
