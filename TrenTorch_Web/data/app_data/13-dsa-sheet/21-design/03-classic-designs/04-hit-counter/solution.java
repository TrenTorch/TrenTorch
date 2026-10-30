import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(q) amortized time, O(hits in last 300 seconds) space
    static long[] runHitCounter(String[] ops) {
        ArrayDeque<Long> window = new ArrayDeque<>();
        List<Long> out = new ArrayList<>();
        for (String op : ops) {
            String[] parts = op.trim().split("\\s+");
            String kind = parts[0];
            long t = Long.parseLong(parts[1]);
            if (kind.equals("hit")) {
                window.addLast(t);
            } else {
                while (!window.isEmpty() && window.peekFirst() <= t - 300) {
                    window.pollFirst();
                }
                out.add((long) window.size());
            }
        }
        long[] result = new long[out.size()];
        for (int i = 0; i < result.length; i++) {
            result[i] = out.get(i);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runHitCounter(new String[]{"hit 1", "hit 2", "hit 3", "count 4", "hit 300", "count 300", "count 301"})));
    }
}
