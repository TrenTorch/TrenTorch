import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    // O(n! * n) time, O(n! * n) space (output) + O(n) auxiliary
    static long[][] allPermutations(long[] nums) {
        long[] a = Arrays.copyOf(nums, nums.length);
        Arrays.sort(a);
        boolean[] used = new boolean[a.length];
        List<long[]> result = new ArrayList<>();
        long[] current = new long[a.length];
        backtrack(a, used, current, 0, result);
        long[][] res = new long[result.size()][];
        for (int i = 0; i < result.size(); i++) {
            res[i] = result.get(i);
        }
        return res;
    }

    private static void backtrack(long[] a, boolean[] used, long[] current, int depth, List<long[]> result) {
        if (depth == a.length) {
            result.add(Arrays.copyOf(current, current.length));
            return;
        }
        for (int j = 0; j < a.length; j++) {
            if (used[j]) continue;
            used[j] = true;
            current[depth] = a[j];
            backtrack(a, used, current, depth + 1, result);
            used[j] = false;
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(allPermutations(new long[]{1L, 2L, 3L})));
    }
}
