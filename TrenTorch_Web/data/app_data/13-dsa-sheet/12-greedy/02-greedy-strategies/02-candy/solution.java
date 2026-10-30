public class Main {
    // O(n) time, O(1) space
    static long candy(long[] ratings) {
        int n = ratings.length;
        if (n == 0) {
            return 0;
        }
        long total = 1;
        long up = 0;
        long down = 0;
        long peak = 0;
        for (int i = 1; i < n; i++) {
            if (ratings[i] > ratings[i - 1]) {
                up += 1;
                down = 0;
                peak = up;
                total += 1 + up;
            } else if (ratings[i] == ratings[i - 1]) {
                up = 0;
                down = 0;
                peak = 0;
                total += 1;
            } else {
                up = 0;
                down += 1;
                total += 1 + down;
                if (peak >= down) {
                    total -= 1;
                }
            }
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(candy(new long[]{1L, 0L, 2L}));
    }
}
