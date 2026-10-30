import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    // Time: O(N * 2^target) worst case, Space: O(target) recursion depth
    static long[][] combinationSum(long[] candidates, long target) {
        Arrays.sort(candidates);
        List<List<Long>> results = new ArrayList<>();
        backtrack(candidates, target, 0, new ArrayList<>(), results);
        long[][] ans = new long[results.size()][];
        for (int i = 0; i < results.size(); i++) {
            List<Long> comb = results.get(i);
            long[] arr = new long[comb.size()];
            for (int j = 0; j < comb.size(); j++) {
                arr[j] = comb.get(j);
            }
            ans[i] = arr;
        }
        return ans;
    }

    private static void backtrack(long[] candidates, long remaining, int start, List<Long> current, List<List<Long>> results) {
        if (remaining == 0) {
            results.add(new ArrayList<>(current));
            return;
        }
        for (int i = start; i < candidates.length; i++) {
            if (candidates[i] > remaining) {
                break;
            }
            current.add(candidates[i]);
            backtrack(candidates, remaining - candidates[i], i, current, results);
            current.remove(current.size() - 1);
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(combinationSum(new long[]{2L, 3L, 6L, 7L}, 7L)));
    }
}
