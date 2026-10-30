public class Main {
    // O(n log n) time, O(n) space
    static long maxJobProfit(long[][] jobs) {
        long maxDeadline = 0;
        for (long[] job : jobs) {
            maxDeadline = Math.max(maxDeadline, job[0]);
        }
        int limit = (int) Math.min(maxDeadline, (long) jobs.length);
        int[] parent = new int[limit + 1];
        for (int t = 0; t <= limit; t++) {
            parent[t] = t;
        }
        long[][] sorted = jobs.clone();
        java.util.Arrays.sort(sorted, (a, b) -> Long.compare(b[1], a[1]));
        long total = 0;
        for (long[] job : sorted) {
            int slot = find(parent, (int) Math.min(job[0], (long) limit));
            if (slot > 0) {
                parent[slot] = slot - 1;
                total += job[1];
            }
        }
        return total;
    }

    private static int find(int[] parent, int t) {
        while (parent[t] != t) {
            parent[t] = parent[parent[t]];
            t = parent[t];
        }
        return t;
    }

    public static void main(String[] args) {
        System.out.println(maxJobProfit(new long[][]{new long[]{4L, 20L}, new long[]{1L, 10L}, new long[]{1L, 40L}, new long[]{1L, 30L}}));
    }
}
