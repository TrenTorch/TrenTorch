public class Main {
    // O(1) time, O(1) space
    static long countPairs(long n) {
        return n * (n - 1) / 2;
    }

    public static void main(String[] args) {
        System.out.println(countPairs(4L));
    }
}
