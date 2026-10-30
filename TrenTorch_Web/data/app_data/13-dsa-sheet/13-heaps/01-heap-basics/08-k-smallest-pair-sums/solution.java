public class Main {
    // O(k log min(k, n1)) time, O(min(k, n1)) space
    static long[] kSmallestPairSums(long[] nums1, long[] nums2, long k) {
        if (nums1.length == 0 || nums2.length == 0 || k <= 0) {
            return new long[0];
        }
        // heap entries: {sum, i, j}, ordered like the Python tuples
        java.util.PriorityQueue<long[]> heap = new java.util.PriorityQueue<>((a, b) -> {
            if (a[0] != b[0]) {
                return Long.compare(a[0], b[0]);
            }
            if (a[1] != b[1]) {
                return Long.compare(a[1], b[1]);
            }
            return Long.compare(a[2], b[2]);
        });
        for (int i = 0; i < Math.min((long) nums1.length, k); i++) {
            heap.add(new long[]{nums1[i] + nums2[0], i, 0});
        }
        long[] out = new long[(int) Math.min(k, (long) nums1.length * nums2.length)];
        int outLen = 0;
        while (!heap.isEmpty() && outLen < k) {
            long[] top = heap.poll();
            long i = top[1];
            long j = top[2];
            out[outLen++] = top[0];
            if (j + 1 < nums2.length) {
                heap.add(new long[]{nums1[(int) i] + nums2[(int) (j + 1)], i, j + 1});
            }
        }
        return java.util.Arrays.copyOf(out, outLen);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(kSmallestPairSums(new long[]{1L, 7L, 11L}, new long[]{2L, 4L, 6L}, 3L)));
    }
}
