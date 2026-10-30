public class Main {
    // O(n) time, O(1) space
    static long longestMountain(long[] arr) {
        int n = arr.length;
        long best = 0;
        int i = 1;
        while (i < n - 1) {
            if (arr[i - 1] < arr[i] && arr[i] > arr[i + 1]) {
                int left = i - 1;
                while (left > 0 && arr[left - 1] < arr[left]) {
                    left--;
                }
                int right = i + 1;
                while (right < n - 1 && arr[right] > arr[right + 1]) {
                    right++;
                }
                long length = right - left + 1;
                if (length > best) best = length;
                i = right + 1;
            } else {
                i++;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestMountain(new long[]{2L, 1L, 4L, 7L, 3L, 2L, 5L}));
    }
}
