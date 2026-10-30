public class Main {
    // O(n) time, O(1) space
    static long calculate(String s) {
        long total = 0;
        long last = 0;
        long num = 0;
        char op = '+';
        for (int i = 0; i <= s.length(); i++) {
            char ch = (i < s.length()) ? s.charAt(i) : '+';
            if (Character.isDigit(ch)) {
                num = num * 10 + (ch - '0');
            } else if (ch != ' ') {
                switch (op) {
                    case '+':
                        total += last;
                        last = num;
                        break;
                    case '-':
                        total += last;
                        last = -num;
                        break;
                    case '*':
                        last *= num;
                        break;
                    case '/':
                        last /= num; // Java division truncates toward zero
                        break;
                }
                op = ch;
                num = 0;
            }
        }
        return total + last;
    }

    public static void main(String[] args) {
        System.out.println(calculate("3+2*2"));
    }
}
