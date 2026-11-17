import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n log n + n * 2^n) time, O(n * 2^n) space
    static long[][] subsetsWithDuplicates(long[] nums) {
        long[] a = Arrays.copyOf(nums, nums.length);
        Arrays.sort(a);
        List<long[]> results = new ArrayList<>();
        List<Long> current = new ArrayList<>();
        backtrack(a, 0, current, results);
        return results.toArray(new long[0][]);
    }

    private static void backtrack(long[] a, int start, List<Long> current, List<long[]> results) {
        long[] subset = new long[current.size()];
        for (int i = 0; i < current.size(); i++) {
            subset[i] = current.get(i);
        }
        results.add(subset);
        for (int i = start; i < a.length; i++) {
            if (i > start && a[i] == a[i - 1]) continue;
            current.add(a[i]);
            backtrack(a, i + 1, current, results);
            current.remove(current.size() - 1);
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(subsetsWithDuplicates(new long[]{1L, 2L, 2L})));
    }
}
