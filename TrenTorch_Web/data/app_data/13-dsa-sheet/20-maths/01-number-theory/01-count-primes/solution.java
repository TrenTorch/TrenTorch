public class Main {
    // O(n log log n) time, O(n) space (sieve of Eratosthenes)
    static long countPrimes(long n) {
        if (n < 3) {
            return 0;
        }
        int size = (int) n;
        boolean[] composite = new boolean[size];
        long count = 0;
        for (int i = 2; i < size; i++) {
            if (!composite[i]) {
                count++;
                if ((long) i * i < size) {
                    for (int j = i * i; j < size; j += i) {
                        composite[j] = true;
                    }
                }
            }
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countPrimes(10L));
    }
}
