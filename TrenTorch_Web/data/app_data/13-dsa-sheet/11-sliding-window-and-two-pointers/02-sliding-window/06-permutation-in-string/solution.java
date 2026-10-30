import java.util.Arrays;

public class Main {
    // O(n) time, O(1) space
    static boolean checkInclusion(String s1, String s2) {
        int m = s1.length();
        int n = s2.length();
        if (m > n) {
            return false;
        }
        int[] need = new int[26];
        int[] window = new int[26];
        for (char c : s1.toCharArray()) {
            need[c - 'a']++;
        }
        for (int i = 0; i < n; i++) {
            window[s2.charAt(i) - 'a']++;
            if (i >= m) {
                window[s2.charAt(i - m) - 'a']--;
            }
            if (i >= m - 1 && Arrays.equals(window, need)) {
                return true;
            }
        }
        return m == 0;
    }

    public static void main(String[] args) {
        System.out.println(checkInclusion("ab", "eidbaooo"));
    }
}
