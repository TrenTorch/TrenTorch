import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Main {
    // O(n) average time, O(n) space
    static long[] kSmallest(long[] nums, long k) {
        if (k <= 0) return new long[0];
        int n = nums.length;
        if (k >= n) {
            long[] copy = Arrays.copyOf(nums, n);
            Arrays.sort(copy);
            return copy;
        }
        int need = (int) k;
        List<Long> chosen = new ArrayList<>();
        List<Long> pool = new ArrayList<>(n);
        for (long num : nums) pool.add(num);
        Random rand = new Random();
        while (need > 0) {
            int pivotIndex = rand.nextInt(pool.size());
            long pivot = pool.get(pivotIndex);
            List<Long> less = new ArrayList<>();
            List<Long> equal = new ArrayList<>();
            List<Long> greater = new ArrayList<>();
            for (long x : pool) {
                if (x < pivot) less.add(x);
                else if (x == pivot) equal.add(x);
                else greater.add(x);
            }
            if (need <= less.size()) {
                pool = less;
            } else if (need <= less.size() + equal.size()) {
                chosen.addAll(less);
                int take = need - less.size();
                chosen.addAll(equal.subList(0, take));
                need = 0;
            } else {
                chosen.addAll(less);
                chosen.addAll(equal);
                need -= less.size() + equal.size();
                pool = greater;
            }
        }
        long[] result = new long[chosen.size()];
        for (int i = 0; i < chosen.size(); i++) {
            result[i] = chosen.get(i);
        }
        Arrays.sort(result);
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(kSmallest(new long[]{7L, 2L, 9L, 4L, 2L}, 3L)));
    }
}
