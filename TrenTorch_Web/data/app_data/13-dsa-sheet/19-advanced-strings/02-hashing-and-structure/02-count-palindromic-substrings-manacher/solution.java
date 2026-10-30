public class Main {
    // O(n) time, O(n) space
    static long countPalindromesFast(String s) {
        int n = s.length();
        long total = 0;
        char[] arr = s.toCharArray();
        int[] d1 = new int[n];
        int left = 0, right = -1;
        for (int i = 0; i < n; i++) {
            int k = (i > right) ? 1 : Math.min(d1[left + right - i], right - i + 1);
            while (i - k >= 0 && i + k < n && arr[i - k] == arr[i + k]) {
                k++;
            }
            d1[i] = k;
            total += k;
            if (i + k - 1 > right) {
                left = i - k + 1;
                right = i + k - 1;
            }
        }
        int[] d2 = new int[n];
        left = 0;
        right = -1;
        for (int i = 0; i < n; i++) {
            int k = (i > right) ? 0 : Math.min(d2[left + right - i + 1], right - i + 1);
            while (i - k - 1 >= 0 && i + k < n && arr[i - k - 1] == arr[i + k]) {
                k++;
            }
            d2[i] = k;
            total += k;
            if (i + k - 1 > right) {
                left = i - k;
                right = i + k - 1;
            }
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(countPalindromesFast("aaa"));
    }
}
