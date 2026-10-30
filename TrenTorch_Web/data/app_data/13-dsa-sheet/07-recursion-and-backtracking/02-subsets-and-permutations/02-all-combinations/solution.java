import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(C(n,k) * k) time, O(C(n,k) * k) space
    static long[][] allCombinations(long n, long k) {
        List<long[]> result = new ArrayList<>();
        if (k == 0) {
            result.add(new long[0]);
            return result.toArray(new long[0][]);
        }
        int nInt = (int) n;
        int kInt = (int) k;
        int[] comb = new int[kInt];
        backtrack(1, 0, nInt, kInt, comb, result);
        return result.toArray(new long[0][]);
    }

    private static void backtrack(int start, int idx, int n, int k, int[] comb, List<long[]> result) {
        int need = k - idx;
        if (need == 0) {
            long[] copy = new long[k];
            for (int i = 0; i < k; i++) {
                copy[i] = comb[i];
            }
            result.add(copy);
            return;
        }
        for (int j = start; j <= n - need + 1; j++) {
            comb[idx] = j;
            backtrack(j + 1, idx + 1, n, k, comb, result);
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(allCombinations(4L, 2L)));
    }
}
