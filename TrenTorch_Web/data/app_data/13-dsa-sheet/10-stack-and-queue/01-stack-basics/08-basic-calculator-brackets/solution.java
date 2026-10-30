public class Main {
    // O(n) time, O(n) space (stack depth of the brackets)
    static long calculateBrackets(String s) {
        java.util.ArrayDeque<long[]> stack = new java.util.ArrayDeque<>();
        long result = 0;
        long num = 0;
        long sign = 1;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch >= '0' && ch <= '9') {
                num = num * 10 + (ch - '0');
            } else if (ch == '+' || ch == '-') {
                result += sign * num;
                num = 0;
                sign = ch == '+' ? 1 : -1;
            } else if (ch == '(') {
                stack.push(new long[]{result, sign});
                result = 0;
                sign = 1;
            } else if (ch == ')') {
                result += sign * num;
                num = 0;
                long[] saved = stack.pop();
                result = saved[0] + saved[1] * result;
            }
        }
        return result + sign * num;
    }

    public static void main(String[] args) {
        System.out.println(calculateBrackets("(1+(4+5+2)-3)+(6+8)"));
    }
}
