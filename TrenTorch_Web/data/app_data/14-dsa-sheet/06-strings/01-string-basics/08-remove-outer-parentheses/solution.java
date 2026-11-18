public class Main {
    // O(n) time, O(n) space
    static String removeOuterParentheses(String s) {
        StringBuilder out = new StringBuilder();
        int depth = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                if (depth > 0) {
                    out.append(ch);
                }
                depth++;
            } else {
                depth--;
                if (depth > 0) {
                    out.append(ch);
                }
            }
        }
        return out.toString();
    }

    public static void main(String[] args) {
        System.out.println(removeOuterParentheses("(()())(())"));
    }
}
