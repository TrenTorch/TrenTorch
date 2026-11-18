import java.util.Arrays;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    // O(n log n) time, O(n) space
    static long[] revealCards(long[] deck) {
        int n = deck.length;
        long[] result = new long[n];
        Deque<Integer> positions = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            positions.add(i);
        }
        long[] sorted = deck.clone();
        Arrays.sort(sorted);
        for (long card : sorted) {
            int pos = positions.removeFirst();
            result[pos] = card;
            if (!positions.isEmpty()) {
                positions.addLast(positions.removeFirst());
            }
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(revealCards(new long[]{17L, 13L, 11L, 2L, 3L, 5L, 7L})));
    }
}
