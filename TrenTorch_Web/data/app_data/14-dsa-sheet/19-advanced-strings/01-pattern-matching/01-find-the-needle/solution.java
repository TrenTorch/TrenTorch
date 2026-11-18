public class Main {
    // O(n + m) time, O(m) space (KMP failure function)
    static long findNeedle(String haystack, String needle) {
        if (needle.isEmpty()) {
            return 0;
        }
        int m = needle.length();
        int[] fail = new int[m];
        int k = 0;
        for (int i = 1; i < m; i++) {
            while (k > 0 && needle.charAt(i) != needle.charAt(k)) {
                k = fail[k - 1];
            }
            if (needle.charAt(i) == needle.charAt(k)) {
                k++;
            }
            fail[i] = k;
        }
        k = 0;
        for (int i = 0; i < haystack.length(); i++) {
            char ch = haystack.charAt(i);
            while (k > 0 && ch != needle.charAt(k)) {
                k = fail[k - 1];
            }
            if (ch == needle.charAt(k)) {
                k++;
            }
            if (k == m) {
                return i - k + 1;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        System.out.println(findNeedle("sadbutsad", "sad"));
    }
}
