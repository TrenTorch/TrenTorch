public class Main {
    // O(|s| * |t|) time, O(|t|) space
    static long numDistinct(String s, String t) {
        final long mod = 1_000_000_007L;
        int m = t.length();
        long[] row = new long[m + 1];
        row[0] = 1;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            for (int j = m; j >= 1; j--) {
                if (t.charAt(j - 1) == ch) {
                    row[j] = (row[j] + row[j - 1]) % mod;
                }
            }
        }
        return row[m];
    }

    public static void main(String[] args) {
        System.out.println(numDistinct("rabbbit", "rabbit"));
    }
}
