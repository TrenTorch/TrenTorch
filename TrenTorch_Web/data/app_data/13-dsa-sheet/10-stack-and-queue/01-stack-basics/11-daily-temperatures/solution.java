import java.util.Arrays;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    // O(n) time, O(n) space
    static long[] dailyTemperatures(long[] temps) {
        int n = temps.length;
        long[] out = new long[n];
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            long t = temps[i];
            while (!stack.isEmpty() && temps[stack.peek()] < t) {
                int j = stack.pop();
                out[j] = i - j;
            }
            stack.push(i);
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(dailyTemperatures(new long[]{73L, 74L, 75L, 71L, 69L, 72L, 76L, 73L})));
    }
}
