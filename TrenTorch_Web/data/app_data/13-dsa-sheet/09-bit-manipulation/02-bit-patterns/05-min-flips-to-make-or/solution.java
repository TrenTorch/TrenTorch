public class Main {
    // O(1) time, O(1) space
    static long minFlips(long a, long b, long c) {
        long flips = 0;
        for (int i = 0; i < 31; i++) {
            int x = (int)((a >> i) & 1);
            int y = (int)((b >> i) & 1);
            int z = (int)((c >> i) & 1);
            if (z == 0) {
                flips += x + y;
            } else if (x == 0 && y == 0) {
                flips += 1;
            }
        }
        return flips;
    }

    public static void main(String[] args) {
        System.out.println(minFlips(2L, 6L, 5L));
    }
}
