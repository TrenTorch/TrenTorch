public class Main {
    // O(n) time, O(1) space
    static long gasStation(long[] gas, long[] cost) {
        long total = 0;
        long tank = 0;
        int start = 0;
        int n = gas.length;
        for (int i = 0; i < n; i++) {
            long diff = gas[i] - cost[i];
            total += diff;
            tank += diff;
            if (tank < 0) {
                start = i + 1;
                tank = 0;
            }
        }
        return (total >= 0 && n > 0) ? start : -1;
    }

    public static void main(String[] args) {
        System.out.println(gasStation(new long[]{1L, 2L, 3L, 4L, 5L}, new long[]{3L, 4L, 5L, 1L, 2L}));
    }
}
