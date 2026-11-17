import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    // O(2^n * n) time, O(n) space
    static long[][] combinationSumIi(long[] candidates, long target) {
        Arrays.sort(candidates);
        List<List<Long>> result = new ArrayList<>();
        backtrack(candidates, 0, target, new ArrayList<>(), result);
        long[][] ans = new long[result.size()][];
        for (int i = 0; i < result.size(); i++) {
            List<Long> comb = result.get(i);
            long[] arr = new long[comb.size()];
            for (int j = 0; j < comb.size(); j++) {
                arr[j] = comb.get(j);
            }
            ans[i] = arr;
        }
        return ans;
    }

    private static void backtrack(long[] candidates, int start, long remaining, List<Long> current, List<List<Long>> result) {
        if (remaining == 0) {
            result.add(new ArrayList<>(current));
            return;
        }
        for (int i = start; i < candidates.length; i++) {
            if (i > start && candidates[i] == candidates[i - 1]) {
                continue;
            }
            if (candidates[i] > remaining) {
                break;
            }
            current.add(candidates[i]);
            backtrack(candidates, i + 1, remaining - candidates[i], current, result);
            current.remove(current.size() - 1);
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(combinationSumIi(new long[]{10L, 1L, 2L, 7L, 6L, 1L, 5L}, 8L)));
    }
}
