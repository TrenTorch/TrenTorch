import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    // O(n) time, O(n) space
    static long evaluateRpn(String[] tokens) {
        Deque<Long> stack = new ArrayDeque<>();
        for (String token : tokens) {
            switch (token) {
                case "+":
                    stack.push(stack.pop() + stack.pop());
                    break;
                case "-":
                    long b = stack.pop();
                    long a = stack.pop();
                    stack.push(a - b);
                    break;
                case "*":
                    stack.push(stack.pop() * stack.pop());
                    break;
                case "/":
                    long divisor = stack.pop();
                    long dividend = stack.pop();
                    stack.push(dividend / divisor); // Java truncates toward zero
                    break;
                default:
                    stack.push(Long.parseLong(token));
            }
        }
        return stack.pop();
    }

    public static void main(String[] args) {
        System.out.println(evaluateRpn(new String[]{"2", "1", "+", "3", "*"}));
    }
}
