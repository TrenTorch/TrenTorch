import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n! * n) time, O(n! * n) space
    static long[][] uniquePermutations(long[] nums) {
        long[] a = nums.clone();
        Arrays.sort(a);
        boolean[] used = new boolean[a.length];
        List<long[]> result = new ArrayList<>();
        long[] current = new long[a.length];
        backtrack(a, used, current, 0, result);
        return result.toArray(new long[0][]);
    }

    private static void backtrack(long[] a, boolean[] used, long[] current, int depth, List<long[]> result) {
        if (depth == a.length) {
            result.add(Arrays.copyOf(current, depth));
            return;
        }
        for (int j = 0; j < a.length; j++) {
            if (used[j] || (j > 0 && a[j] == a[j - 1] && !used[j - 1])) {
                continue;
            }
            used[j] = true;
            current[depth] = a[j];
            backtrack(a, used, current, depth + 1, result);
            used[j] = false;
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(uniquePermutations(new long[]{1L, 1L, 2L})));
    }
}
