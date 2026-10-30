public class Main {
    // O(q log n) time, O(q) space for output array
    static long[] countInRange(long[] sortedNums, long[][] queries) {
        long[] ans = new long[queries.length];
        for (int i = 0; i < queries.length; i++) {
            long lo = queries[i][0];
            long hi = queries[i][1];
            int left = lowerBound(sortedNums, lo);
            int right = upperBound(sortedNums, hi);
            ans[i] = right - left;
        }
        return ans;
    }

    private static int lowerBound(long[] arr, long target) {
        int low = 0, high = arr.length;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] < target) low = mid + 1;
            else high = mid;
        }
        return low;
    }

    private static int upperBound(long[] arr, long target) {
        int low = 0, high = arr.length;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] <= target) low = mid + 1;
            else high = mid;
        }
        return low;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(countInRange(new long[]{1L, 3L, 3L, 5L, 8L}, new long[][]{new long[]{3L, 5L}, new long[]{0L, 0L}, new long[]{2L, 9L}})));
    }
}
