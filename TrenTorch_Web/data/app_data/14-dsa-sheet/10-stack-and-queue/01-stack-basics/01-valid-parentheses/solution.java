public class Main {
    // O(n) time, O(n) space
    static boolean validBrackets(String s) {
        java.util.ArrayDeque<Character> stack = new java.util.ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == ')' || ch == ']' || ch == '}') {
                char open = ch == ')' ? '(' : (ch == ']' ? '[' : '{');
                if (stack.isEmpty() || stack.pop().charValue() != open) {
                    return false;
                }
            } else {
                stack.push(ch);
            }
        }
        return stack.isEmpty();
    }

    public static void main(String[] args) {
        System.out.println(validBrackets("()[]{}"));
    }
}
