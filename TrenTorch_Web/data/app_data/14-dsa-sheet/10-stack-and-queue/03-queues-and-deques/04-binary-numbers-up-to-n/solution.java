import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    // O(n log n) time, O(n log n) space
    static String[] binaryNumbersUpTo(long n) {
        if (n <= 0) {
            return new String[0];
        }
        String[] out = new String[(int) n];
        Deque<String> queue = new ArrayDeque<>();
        queue.add("1");
        for (int i = 0; i < n; i++) {
            String front = queue.removeFirst();
            out[i] = front;
            queue.add(front + "0");
            queue.add(front + "1");
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(binaryNumbersUpTo(5L)));
    }
}
