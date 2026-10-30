public class Main {
    // O(n) time, O(n) space
    static String longestHappyPrefix(String s) {
        int n = s.length();
        if (n == 0) return "";
        int[] pi = new int[n];
        int k = 0;
        for (int i = 1; i < n; i++) {
            while (k > 0 && s.charAt(i) != s.charAt(k)) {
                k = pi[k - 1];
            }
            if (s.charAt(i) == s.charAt(k)) {
                k++;
            }
            pi[i] = k;
        }
        return s.substring(0, pi[n - 1]);
    }

    public static void main(String[] args) {
        System.out.println(longestHappyPrefix("level"));
    }
}
