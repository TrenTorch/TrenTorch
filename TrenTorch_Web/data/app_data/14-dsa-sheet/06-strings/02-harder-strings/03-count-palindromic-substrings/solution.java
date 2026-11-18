public class Main {
    // O(n) time, O(n) space (Manacher's algorithm on the transformed string)
    static long countPalindromicSubstrings(String s) {
        StringBuilder sb = new StringBuilder("#");
        for (int i = 0; i < s.length(); i++) {
            if (i > 0) sb.append('#');
            sb.append(s.charAt(i));
        }
        sb.append('#');
        String t = sb.toString();
        int n = t.length();
        int[] radius = new int[n];
        int centre = 0, right = 0;
        for (int i = 0; i < n; i++) {
            if (i < right) {
                radius[i] = Math.min(right - i, radius[2 * centre - i]);
            }
            while (i - radius[i] - 1 >= 0
                    && i + radius[i] + 1 < n
                    && t.charAt(i - radius[i] - 1) == t.charAt(i + radius[i] + 1)) {
                radius[i]++;
            }
            if (i + radius[i] > right) {
                centre = i;
                right = i + radius[i];
            }
        }
        long total = 0;
        for (int r : radius) {
            total += (r + 1) / 2;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(countPalindromicSubstrings("abc"));
    }
}
