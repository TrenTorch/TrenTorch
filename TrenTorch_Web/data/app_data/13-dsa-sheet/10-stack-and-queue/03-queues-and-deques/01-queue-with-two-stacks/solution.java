import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n) time, O(n) space
    static long[] queueWithTwoStacks(String[] ops) {
        ArrayDeque<Long> inbox = new ArrayDeque<>();
        ArrayDeque<Long> outbox = new ArrayDeque<>();
        List<Long> out = new ArrayList<>();

        for (String op : ops) {
            if (op.startsWith("push")) {
                String[] parts = op.split(" ");
                long x = Long.parseLong(parts[1]);
                inbox.push(x);
            } else if (op.equals("pop")) {
                if (outbox.isEmpty()) {
                    while (!inbox.isEmpty()) {
                        outbox.push(inbox.pop());
                    }
                }
                out.add(outbox.pop());
            } else if (op.equals("peek")) {
                if (outbox.isEmpty()) {
                    while (!inbox.isEmpty()) {
                        outbox.push(inbox.pop());
                    }
                }
                out.add(outbox.peek());
            } else { // empty
                out.add((inbox.isEmpty() && outbox.isEmpty()) ? 1L : 0L);
            }
        }

        long[] result = new long[out.size()];
        for (int i = 0; i < out.size(); i++) {
            result[i] = out.get(i);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(queueWithTwoStacks(new String[]{"push 1", "push 2", "peek", "pop", "empty"})));
    }
}
