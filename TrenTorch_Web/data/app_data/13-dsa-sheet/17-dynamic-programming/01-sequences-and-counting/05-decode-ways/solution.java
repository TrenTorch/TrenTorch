public class Main {
    // O(n) time, O(1) space
    static long numDecodings(String s) {
        final long mod = 1_000_000_007L;
        if (s == null || s.length() == 0) {
            return 0;
        }
        long a = 1; // dp[i-2]
        long b = 1; // dp[i-1]
        for (int i = 1; i <= s.length(); i++) {
            long now = 0;
            // single digit
            if (s.charAt(i - 1) != '0') {
                now += b;
            }
            // two digits
            if (i >= 2) {
                int twoDigit = (s.charAt(i - 2) - '0') * 10 + (s.charAt(i - 1) - '0');
                if (twoDigit >= 10 && twoDigit <= 26) {
                    now += a;
                }
            }
            a = b;
            b = now % mod;
        }
        return b % mod;
    }

    public static void main(String[] args) {
        System.out.println(numDecodings("12"));
    }
}
