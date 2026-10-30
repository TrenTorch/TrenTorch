public class Main {
    // O(n) time (Manacher's algorithm), O(n) space
    static String longestPalindromicSubstring(String s) {
        if (s.isEmpty()) {
            return "";
        }
        int n = s.length();
        // t = "#s0#s1#...#s(n-1)#", so every real character sits at an odd index.
        char[] t = new char[2 * n + 1];
        for (int k = 0; k < t.length; k++) {
            t[k] = (k % 2 == 0) ? '#' : s.charAt(k / 2);
        }
        int len = t.length;
        int[] radius = new int[len];
        int centre = 0, right = 0;
        int bestLen = 0, bestCentre = 0;
        for (int i = 0; i < len; i++) {
            if (i < right) {
                radius[i] = Math.min(right - i, radius[2 * centre - i]);
            }
            while (i - radius[i] - 1 >= 0
                    && i + radius[i] + 1 < len
                    && t[i - radius[i] - 1] == t[i + radius[i] + 1]) {
                radius[i]++;
            }
            if (i + radius[i] > right) {
                centre = i;
                right = i + radius[i];
            }
            if (radius[i] > bestLen) {
                bestLen = radius[i];
                bestCentre = i;
            }
        }
        int start = (bestCentre - bestLen) / 2;
        return s.substring(start, start + bestLen);
    }

    public static void main(String[] args) {
        System.out.println(longestPalindromicSubstring("babad"));
    }
}
