public class Main {
    // O(n) time, O(1) space (fixed 65536-entry tables for char codes)
    static boolean isomorphicStrings(String s, String t) {
        if (s.length() != t.length()) {
            return false;
        }
        // Stored values are the mapped char + 1, so 0 means "not yet mapped".
        int[] forward = new int[65536];
        int[] backward = new int[65536];
        for (int i = 0; i < s.length(); i++) {
            char a = s.charAt(i);
            char b = t.charAt(i);
            if (forward[a] == 0) {
                forward[a] = b + 1;
            } else if (forward[a] != b + 1) {
                return false;
            }
            if (backward[b] == 0) {
                backward[b] = a + 1;
            } else if (backward[b] != a + 1) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isomorphicStrings("egg", "add"));
    }
}
