public class Main {
    // O(n) time, O(n) space
    static String removeAdjacentDuplicates(String s) {
        int n = s.length();
        char[] stack = new char[n];
        int top = -1;
        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);
            if (top >= 0 && stack[top] == c) {
                top--;
            } else {
                stack[++top] = c;
            }
        }
        return new String(stack, 0, top + 1);
    }

    public static void main(String[] args) {
        System.out.println(removeAdjacentDuplicates("abbaca"));
    }
}
