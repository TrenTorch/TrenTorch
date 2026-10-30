public class Main {
    // O(n) time, O(1) space where n = t.length()
    static boolean isSubsequence(String s, String t) {
        int i = 0;
        for (char ch : t.toCharArray()) {
            if (i < s.length() && s.charAt(i) == ch) {
                i++;
            }
        }
        return i == s.length();
    }

    public static void main(String[] args) {
        System.out.println(isSubsequence("ace", "abcde"));
    }
}
