import java.util.*;

public class Main {
    // O(sqrt(n)) time, O(log n) space (trial division by 2 and odd numbers)
    static long[][] primeFactors(long n) {
        List<long[]> out = new ArrayList<>();
        long d = 2;
        while (d * d <= n) {
            if (n % d == 0) {
                long e = 0;
                while (n % d == 0) {
                    n /= d;
                    e++;
                }
                out.add(new long[]{d, e});
            }
            d += (d == 2) ? 1 : 2;
        }
        if (n > 1) {
            out.add(new long[]{n, 1});
        }
        return out.toArray(new long[0][]);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(primeFactors(360L)));
    }
}
