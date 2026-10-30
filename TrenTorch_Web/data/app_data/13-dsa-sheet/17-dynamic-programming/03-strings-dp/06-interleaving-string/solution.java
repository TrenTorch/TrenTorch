public class Main {
    // O(len(a) * len(b)) time, O(len(b)) space
    static boolean isInterleave(String a, String b, String c) {
        if (a.length() + b.length() != c.length()) {
            return false;
        }
        boolean[] row = new boolean[b.length() + 1];
        row[0] = true;
        for (int j = 1; j <= b.length(); j++) {
            row[j] = row[j - 1] && b.charAt(j - 1) == c.charAt(j - 1);
        }
        for (int i = 1; i <= a.length(); i++) {
            row[0] = row[0] && a.charAt(i - 1) == c.charAt(i - 1);
            for (int j = 1; j <= b.length(); j++) {
                row[j] = (row[j] && a.charAt(i - 1) == c.charAt(i + j - 1))
                        || (row[j - 1] && b.charAt(j - 1) == c.charAt(i + j - 1));
            }
        }
        return row[b.length()];
    }

    public static void main(String[] args) {
        System.out.println(isInterleave("aabcc", "dbbca", "aadbbcbcac"));
    }
}
