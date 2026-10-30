import java.util.*;

public class Main {
    // O(n * Catalan(n)) time, O(n) recursion space (plus the output)
    static String[] generateParentheses(long n) {
        List<String> out = new ArrayList<>();
        parenGo((int) n, new StringBuilder(), 0, 0, out);
        return out.toArray(new String[0]);
    }

    static void parenGo(int n, StringBuilder prefix, int opens, int closes, List<String> out) {
        if (prefix.length() == 2 * n) {
            out.add(prefix.toString());
            return;
        }
        if (opens < n) {
            prefix.append('(');
            parenGo(n, prefix, opens + 1, closes, out);
            prefix.setLength(prefix.length() - 1);
        }
        if (closes < opens) {
            prefix.append(')');
            parenGo(n, prefix, opens, closes + 1, out);
            prefix.setLength(prefix.length() - 1);
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(generateParentheses(3L)));
    }
}
