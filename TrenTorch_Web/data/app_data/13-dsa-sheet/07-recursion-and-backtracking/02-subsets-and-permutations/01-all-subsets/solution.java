import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n * 2^n) time, O(n * 2^n) space
    static long[][] allSubsets(long[] nums) {
        long[] a = Arrays.copyOf(nums, nums.length);
        Arrays.sort(a);
        List<long[]> result = new ArrayList<>();
        long[] current = new long[a.length];
        go(0, a, current, 0, result);
        return result.toArray(new long[0][]);
    }

    static void go(int start, long[] a, long[] current, int size, List<long[]> result) {
        long[] subset = new long[size];
        System.arraycopy(current, 0, subset, 0, size);
        result.add(subset);
        for (int j = start; j < a.length; j++) {
            current[size] = a[j];
            go(j + 1, a, current, size + 1, result);
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(allSubsets(new long[]{1L, 2L, 3L})));
    }
}
