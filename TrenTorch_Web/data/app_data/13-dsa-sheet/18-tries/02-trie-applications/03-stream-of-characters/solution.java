import java.util.ArrayList;
import java.util.ArrayDeque;
import java.util.List;
import java.util.Queue;

public class Main {
    // O(|stream| + total_word_length) time, O(total_word_length) space
    static boolean[] streamChecker(String[] words, String stream) {
        List<int[]> gotoArr = new ArrayList<>();
        List<Integer> fail = new ArrayList<>();
        List<Boolean> ends = new ArrayList<>();

        // root node
        gotoArr.add(new int[26]);
        fail.add(0);
        ends.add(false);

        // Build trie
        for (String word : words) {
            int node = 0;
            for (char ch : word.toCharArray()) {
                int c = ch - 'a';
                int child = gotoArr.get(node)[c];
                if (child == 0) {
                    gotoArr.add(new int[26]);
                    fail.add(0);
                    ends.add(false);
                    child = gotoArr.size() - 1;
                    gotoArr.get(node)[c] = child;
                }
                node = child;
            }
            ends.set(node, true);
        }

        // Build fail links
        Queue<Integer> queue = new ArrayDeque<>();
        for (int c = 0; c < 26; c++) {
            int child = gotoArr.get(0)[c];
            if (child != 0) {
                queue.add(child);
            }
        }

        while (!queue.isEmpty()) {
            int node = queue.poll();
            if (ends.get(fail.get(node))) {
                ends.set(node, true);
            }
            for (int c = 0; c < 26; c++) {
                int child = gotoArr.get(node)[c];
                if (child != 0) {
                    int f = fail.get(node);
                    while (f != 0 && gotoArr.get(f)[c] == 0) {
                        f = fail.get(f);
                    }
                    if (gotoArr.get(f)[c] != 0) {
                        fail.set(child, gotoArr.get(f)[c]);
                    } else {
                        fail.set(child, 0);
                    }
                    queue.add(child);
                }
            }
        }

        // Process stream
        boolean[] out = new boolean[stream.length()];
        int state = 0;
        for (int i = 0; i < stream.length(); i++) {
            int c = stream.charAt(i) - 'a';
            while (state != 0 && gotoArr.get(state)[c] == 0) {
                state = fail.get(state);
            }
            if (gotoArr.get(state)[c] != 0) {
                state = gotoArr.get(state)[c];
            } else {
                state = 0;
            }
            out[i] = ends.get(state);
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(streamChecker(new String[]{"cd", "f", "kl"}, "abcdefghijkl")));
    }
}
