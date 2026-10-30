public class Main {
    // O(1) time, O(1) space
    static long xorOfRange(long left, long right) {
        return prefix(right) ^ prefix(left - 1);
    }

    static long prefix(long n) {
        if (n < 0) {
            return 0;
        }
        switch ((int) (n % 4)) {
            case 0: return n;
            case 1: return 1;
            case 2: return n + 1;
            case 3: return 0;
        }
        return 0; // unreachable
    }

    public static void main(String[] args) {
        System.out.println(xorOfRange(3L, 9L));
    }
}
