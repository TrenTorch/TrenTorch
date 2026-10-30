public class Main {
    // O(n) time, O(n) space
    static long sumSubarrayMins(long[] arr) {
        int n = arr.length;
        if (n == 0) return 0;
        int[] left = new int[n];
        int[] right = new int[n];
        int[] stack = new int[n];
        int top = -1;
        
        // previous less element (strictly less)
        for (int i = 0; i < n; i++) {
            while (top >= 0 && arr[stack[top]] >= arr[i]) {
                top--;
            }
            left[i] = (top >= 0) ? stack[top] : -1;
            stack[++top] = i;
        }
        
        top = -1;
        // next less or equal element
        for (int i = n - 1; i >= 0; i--) {
            while (top >= 0 && arr[stack[top]] > arr[i]) {
                top--;
            }
            right[i] = (top >= 0) ? stack[top] : n;
            stack[++top] = i;
        }
        
        final long MOD = 1_000_000_007L;
        long sum = 0;
        for (int i = 0; i < n; i++) {
            long leftCount = i - left[i];
            long rightCount = right[i] - i;
            long contrib = (arr[i] % MOD) * (leftCount % MOD) % MOD * (rightCount % MOD) % MOD;
            sum = (sum + contrib) % MOD;
        }
        return sum;
    }

    public static void main(String[] args) {
        System.out.println(sumSubarrayMins(new long[]{3L, 1L, 2L, 4L}));
    }
}
