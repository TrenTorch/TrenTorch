import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n^2) time, O(n) space
    static String kthPermutation(long n, long k) {
        long[] fact = new long[19];
        fact[0] = 1;
        for (int i = 1; i <= 18; i++) {
            fact[i] = fact[i - 1] * i;
        }

        List<Long> remaining = new ArrayList<>();
        for (long i = 1; i <= n; i++) {
            remaining.add(i);
        }

        k--; // convert to 0-indexed
        StringBuilder sb = new StringBuilder();
        for (long size = n - 1; size >= 0; size--) {
            long idx = k / fact[(int) size];
            k = k % fact[(int) size];
            sb.append(remaining.remove((int) idx));
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        System.out.println(kthPermutation(3L, 3L));
    }
}
