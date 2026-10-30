public class Main {
    // O(log m) time, O(1) space (extended Euclidean algorithm)
    static long modInverse(long a, long m) {
        if (m == 1) {
            return 0;
        }
        long oldR = a % m;
        long r = m;
        long oldX = 1;
        long x = 0;
        while (r != 0) {
            long q = oldR / r;
            long tmp = oldR - q * r;
            oldR = r;
            r = tmp;
            tmp = oldX - q * x;
            oldX = x;
            x = tmp;
        }
        return oldR == 1 ? Math.floorMod(oldX, m) : -1;
    }

    public static void main(String[] args) {
        System.out.println(modInverse(3L, 11L));
    }
}
