import java.util.Arrays;

public class Main {
    // O(n^2) time, O(n) space
    static long minInsertions(String s) {
        int n = s.length();
        if (n == 0) {
            return 0;
        }
        int[] prev = new int[n];
        for (int i = n - 1; i >= 0; i--) {
            int[] cur = new int[n];
            cur[i] = 1;
            for (int j = i + 1; j < n; j++) {
                if (s.charAt(i) == s.charAt(j)) {
                    cur[j] = 2 + prev[j - 1];
                } else {
                    cur[j] = Math.max(prev[j], cur[j - 1]);
                }
            }
            prev = cur;
        }
        return n - prev[n - 1];
    }

    public static void main(String[] args) {
        System.out.println(minInsertions("mbadm"));
    }
}
