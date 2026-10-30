import java.util.PriorityQueue;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n log k) time, O(k) space
    static double[] medianSlidingWindow(long[] nums, long k) {
        int K = (int) k;
        int n = nums.length;
        double[] result = new double[n - K + 1];
        PriorityQueue<Long> small = new PriorityQueue<>(Comparator.reverseOrder()); // max-heap
        PriorityQueue<Long> large = new PriorityQueue<>(); // min-heap
        Map<Long, Integer> delayed = new HashMap<>();
        int[] size = new int[2]; // size[0] = small, size[1] = large

        for (int i = 0; i < K; i++) {
            add(nums[i], small, large, size, delayed);
        }
        result[0] = median(small, large, K);
        for (int i = K; i < n; i++) {
            add(nums[i], small, large, size, delayed);
            remove(nums[i - K], small, large, size, delayed);
            result[i - K + 1] = median(small, large, K);
        }
        return result;
    }

    static void clean(PriorityQueue<Long> heap, Map<Long, Integer> delayed) {
        while (!heap.isEmpty() && delayed.getOrDefault(heap.peek(), 0) > 0) {
            long val = heap.peek();
            delayed.put(val, delayed.get(val) - 1);
            heap.poll();
        }
    }

    static void balance(PriorityQueue<Long> small, PriorityQueue<Long> large, int[] size, Map<Long, Integer> delayed) {
        if (size[0] > size[1] + 1) {
            long val = small.poll();
            large.offer(val);
            size[0]--;
            size[1]++;
            clean(small, delayed);
        } else if (size[0] < size[1]) {
            long val = large.poll();
            small.offer(val);
            size[1]--;
            size[0]++;
            clean(large, delayed);
        }
    }

    static void add(long x, PriorityQueue<Long> small, PriorityQueue<Long> large, int[] size, Map<Long, Integer> delayed) {
        if (small.isEmpty() || x <= small.peek()) {
            small.offer(x);
            size[0]++;
        } else {
            large.offer(x);
            size[1]++;
        }
        balance(small, large, size, delayed);
    }

    static void remove(long x, PriorityQueue<Long> small, PriorityQueue<Long> large, int[] size, Map<Long, Integer> delayed) {
        delayed.put(x, delayed.getOrDefault(x, 0) + 1);
        if (!small.isEmpty() && x <= small.peek()) {
            size[0]--;
            if (x == small.peek()) {
                clean(small, delayed);
            }
        } else {
            size[1]--;
            if (!large.isEmpty() && x == large.peek()) {
                clean(large, delayed);
            }
        }
        balance(small, large, size, delayed);
    }

    static double median(PriorityQueue<Long> small, PriorityQueue<Long> large, int k) {
        if (k % 2 == 1) {
            return (double) small.peek();
        } else {
            return ((double) small.peek() + (double) large.peek()) / 2.0;
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(medianSlidingWindow(new long[]{1L, 3L, -1L, -3L, 5L, 3L, 6L, 7L}, 3L)));
    }
}
