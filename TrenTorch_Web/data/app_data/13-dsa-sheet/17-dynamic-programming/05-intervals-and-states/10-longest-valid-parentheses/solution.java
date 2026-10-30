import java.util.*;

public class Main {
    // O(n) time, O(1) space
    static long longestValidParentheses(String s) {
        int best = 0;
        // First pass: left to right, '(' is opener
        int left = 0, right = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                left++;
            } else {
                right++;
            }
            if (left == right) {
                best = Math.max(best, 2 * left);
            } else if (right > left) {
                left = right = 0;
            }
        }
        // Second pass: right to left, ')' is opener
        left = 0;
        right = 0;
        for (int i = s.length() - 1; i >= 0; i--) {
            char ch = s.charAt(i);
            if (ch == ')') {
                left++;
            } else {
                right++;
            }
            if (left == right) {
                best = Math.max(best, 2 * left);
            } else if (right > left) {
                left = right = 0;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestValidParentheses(")()())"));
    }
}
