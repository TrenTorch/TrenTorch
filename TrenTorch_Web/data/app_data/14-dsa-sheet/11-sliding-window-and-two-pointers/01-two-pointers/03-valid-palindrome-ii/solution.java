public class Main {
    // O(n) time, O(1) space
    static boolean validPalindromeIi(String s) {
        int i = 0;
        int j = s.length() - 1;
        while (i < j) {
            if (s.charAt(i) != s.charAt(j)) {
                return isPal(s, i + 1, j) || isPal(s, i, j - 1);
            }
            i++;
            j--;
        }
        return true;
    }

    static boolean isPal(String s, int i, int j) {
        while (i < j) {
            if (s.charAt(i) != s.charAt(j)) {
                return false;
            }
            i++;
            j--;
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(validPalindromeIi("aba"));
    }
}
