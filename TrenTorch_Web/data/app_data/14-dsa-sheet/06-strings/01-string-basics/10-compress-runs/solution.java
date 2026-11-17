public class Main {
    // O(n) time, O(n) space
    static String compressRuns(String s) {
        StringBuilder sb = new StringBuilder();
        int i = 0;
        while (i < s.length()) {
            char ch = s.charAt(i);
            int j = i;
            while (j < s.length() && s.charAt(j) == ch) {
                j++;
            }
            int n = j - i;
            sb.append(ch);
            if (n > 1) {
                sb.append(n);
            }
            i = j;
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        System.out.println(compressRuns("aabcccccaaa"));
    }
}
