import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n) time, O(1) space
    static long totalFruit(long[] fruits) {
        Map<Long, Integer> count = new HashMap<>();
        int left = 0;
        int best = 0;
        for (int right = 0; right < fruits.length; right++) {
            long f = fruits[right];
            count.put(f, count.getOrDefault(f, 0) + 1);
            while (count.size() > 2) {
                long leftFruit = fruits[left];
                int newCount = count.get(leftFruit) - 1;
                if (newCount == 0) {
                    count.remove(leftFruit);
                } else {
                    count.put(leftFruit, newCount);
                }
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(totalFruit(new long[]{1L, 2L, 3L, 2L, 2L}));
    }
}
