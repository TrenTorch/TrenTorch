public class Main {
    // O(n) time, O(1) space
    static boolean checkValidString(String s) {
        int lo = 0;
        int hi = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                lo++;
                hi++;
            } else if (ch == ')') {
                lo--;
                hi--;
            } else {
                lo--;
                hi++;
            }
            if (hi < 0) {
                return false;
            }
            lo = Math.max(lo, 0);
        }
        return lo == 0;
    }

    public static void main(String[] args) {
        System.out.println(checkValidString("(*)"));
    }
}
