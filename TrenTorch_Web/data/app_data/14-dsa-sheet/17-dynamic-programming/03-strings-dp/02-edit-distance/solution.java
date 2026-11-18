public class Main {
    // O(m*n) time, O(min(m,n)) space
    static long editDistance(String a, String b) {
        if (b.length() > a.length()) {
            String temp = a;
            a = b;
            b = temp;
        }
        int n = a.length();
        int m = b.length();
        long[] prev = new long[m + 1];
        for (int j = 0; j <= m; j++) {
            prev[j] = j;
        }
        for (int i = 1; i <= n; i++) {
            long[] cur = new long[m + 1];
            cur[0] = i;
            for (int j = 1; j <= m; j++) {
                if (a.charAt(i - 1) == b.charAt(j - 1)) {
                    cur[j] = prev[j - 1];
                } else {
                    cur[j] = 1 + Math.min(Math.min(prev[j - 1], prev[j]), cur[j - 1]);
                }
            }
            prev = cur;
        }
        return prev[m];
    }

    public static void main(String[] args) {
        System.out.println(editDistance("horse", "ros"));
    }
}
