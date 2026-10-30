public class Main {
    // O(n) time, O(1) space
    static boolean validPalindrome(String s) {
        int i = 0, j = s.length() - 1;
        while (i < j) {
            char ci = s.charAt(i);
            char cj = s.charAt(j);
            if (!Character.isLetterOrDigit(ci)) {
                i++;
            } else if (!Character.isLetterOrDigit(cj)) {
                j--;
            } else {
                if (Character.toLowerCase(ci) != Character.toLowerCase(cj)) {
                    return false;
                }
                i++;
                j--;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(validPalindrome("A man, a plan, a canal: Panama"));
    }
}
