public class Main {
    // O(n) time, O(n) space
    static long[] zFunction(String s) {
        int n = s.length();
        long[] z = new long[n];
        int left = 0, right = 0;
        for (int i = 1; i < n; i++) {
            if (i < right) {
                z[i] = Math.min(right - i, z[i - left]);
            }
            while (i + z[i] < n && s.charAt((int)z[i]) == s.charAt(i + (int)z[i])) {
                z[i]++;
            }
            if (i + z[i] > right) {
                left = i;
                right = i + (int)z[i];
            }
        }
        return z;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(zFunction("aabxaab")));
    }
}
