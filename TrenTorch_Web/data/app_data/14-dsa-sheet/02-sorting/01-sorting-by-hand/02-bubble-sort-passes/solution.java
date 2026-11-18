import java.util.Arrays;
import java.util.HashMap;

public class Main {
    // O(n log n) time, O(n) space
    static long bubbleSortPasses(long[] nums) {
        if (nums.length <= 1) {
            return 1;
        }
        // coordinate compression
        long[] unique = Arrays.stream(nums).distinct().sorted().toArray();
        HashMap<Long, Integer> rank = new HashMap<>();
        for (int i = 0; i < unique.length; i++) {
            rank.put(unique[i], i + 1); // 1-indexed
        }
        int size = unique.length;
        int[] tree = new int[size + 1];
        int mostBiggerBefore = 0;
        for (int seen = 0; seen < nums.length; seen++) {
            long x = nums[seen];
            int i = rank.get(x);
            int notBigger = 0;
            // query prefix sum
            while (i > 0) {
                notBigger += tree[i];
                i -= i & -i;
            }
            int biggerBefore = seen - notBigger;
            if (biggerBefore > mostBiggerBefore) {
                mostBiggerBefore = biggerBefore;
            }
            // update tree
            i = rank.get(x);
            while (i <= size) {
                tree[i] += 1;
                i += i & -i;
            }
        }
        return mostBiggerBefore + 1L;
    }

    public static void main(String[] args) {
        System.out.println(bubbleSortPasses(new long[]{3L, 2L, 1L}));
    }
}
