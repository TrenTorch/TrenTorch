public class Main {
    // O(n) time, O(n) space (KMP prefix function over s + "#" + reverse(s))
    static String shortestPalindrome(String s) {
        String reversed = new StringBuilder(s).reverse().toString();
        String t = s + "#" + reversed;
        int n = t.length();
        int[] pi = new int[n];
        int k = 0;
        for (int i = 1; i < n; i++) {
            while (k > 0 && t.charAt(i) != t.charAt(k)) {
                k = pi[k - 1];
            }
            if (t.charAt(i) == t.charAt(k)) {
                k++;
            }
            pi[i] = k;
        }
        int border = pi[n - 1];
        String rest = s.substring(border);
        return new StringBuilder(rest).reverse().toString() + s;
    }

    public static void main(String[] args) {
        System.out.println(shortestPalindrome("aacecaaa"));
    }
}
