public class Main {
    // O(k) time, O(1) space where k is the number of set bits (worst-case O(log n))
    static long countSetBits(long n) {
        long count = 0;
        while (n != 0) {
            n &= n - 1;
            count++;
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countSetBits(13L));
    }
}
