public class Main {
    // O(n) time, O(n) space (KMP prefix function; period = n - border)
    static boolean repeatedSubstringPattern(String s) {
        int n = s.length();
        if (n < 2) {
            return false;
        }
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
        int period = n - pi[n - 1];
        return pi[n - 1] > 0 && n % period == 0;
    }

    public static void main(String[] args) {
        System.out.println(repeatedSubstringPattern("abab"));
    }
}
