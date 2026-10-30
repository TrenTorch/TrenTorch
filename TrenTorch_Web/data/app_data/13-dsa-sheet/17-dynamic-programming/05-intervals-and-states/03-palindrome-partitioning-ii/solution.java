public class Main {
    // O(n^2) time, O(n) space
    static long minCutPalindromes(String s) {
        int n = s.length();
        if (n == 0) return 0;
        long[] cuts = new long[n + 1];
        for (int i = 0; i <= n; i++) {
            cuts[i] = i - 1;
        }
        for (int centre = 0; centre < n; centre++) {
            // odd length palindromes
            int left = centre;
            int right = centre;
            while (left >= 0 && right < n && s.charAt(left) == s.charAt(right)) {
                if (cuts[left] + 1 < cuts[right + 1]) {
                    cuts[right + 1] = cuts[left] + 1;
                }
                left--;
                right++;
            }
            // even length palindromes
            left = centre;
            right = centre + 1;
            while (left >= 0 && right < n && s.charAt(left) == s.charAt(right)) {
                if (cuts[left] + 1 < cuts[right + 1]) {
                    cuts[right + 1] = cuts[left] + 1;
                }
                left--;
                right++;
            }
        }
        return cuts[n];
    }

    public static void main(String[] args) {
        System.out.println(minCutPalindromes("aab"));
    }
}
