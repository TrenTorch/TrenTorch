public class Main {
    // O(n) time, O(n) space (KMP prefix function)
    static long[] prefixFunction(String s) {
        int n = s.length();
        long[] pi = new long[n];
        int k = 0;
        for (int i = 1; i < n; i++) {
            while (k > 0 && s.charAt(i) != s.charAt(k)) {
                k = (int) pi[k - 1];
            }
            if (s.charAt(i) == s.charAt(k)) {
                k++;
            }
            pi[i] = k;
        }
        return pi;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(prefixFunction("abcabca")));
    }
}
