public class Main {
    // O(n) time, O(1) space
    static long maxNestingDepth(String s) {
        long depth = 0;
        long best = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                depth++;
                if (depth > best) best = depth;
            } else if (ch == ')') {
                depth--;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(maxNestingDepth("(1+(2*3)+((8)/4))+1"));
    }
}
