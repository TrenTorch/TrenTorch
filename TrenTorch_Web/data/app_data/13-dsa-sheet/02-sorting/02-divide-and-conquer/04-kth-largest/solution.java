import java.util.Random;

public class Main {
    // O(n) expected time (randomized quickselect), O(n) space
    static long kthLargest(long[] nums, long k) {
        Random random = new Random();
        long[] a = nums.clone();
        long target = a.length - k;
        while (true) {
            long pivot = a[random.nextInt(a.length)];
            int less = 0;
            int equal = 0;
            for (long x : a) {
                if (x < pivot) {
                    less++;
                } else if (x == pivot) {
                    equal++;
                }
            }
            if (target < less) {
                a = keep(a, pivot, true);
            } else if (target < less + equal) {
                return pivot;
            } else {
                target -= less + equal;
                a = keep(a, pivot, false);
            }
        }
    }

    // below = true keeps values < pivot, below = false keeps values > pivot
    private static long[] keep(long[] a, long pivot, boolean below) {
        int count = 0;
        for (long x : a) {
            if (below ? x < pivot : x > pivot) {
                count++;
            }
        }
        long[] out = new long[count];
        int idx = 0;
        for (long x : a) {
            if (below ? x < pivot : x > pivot) {
                out[idx++] = x;
            }
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(kthLargest(new long[]{3L, 2L, 1L, 5L, 6L, 4L}, 2L));
    }
}
