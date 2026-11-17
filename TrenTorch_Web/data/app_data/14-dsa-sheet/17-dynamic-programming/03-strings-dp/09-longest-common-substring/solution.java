import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Main {
    // O(|a| + |b|) time with hash-map transitions, O(|a|) space (suffix automaton of a)
    static long longestCommonSubstring(String a, String b) {
        List<Map<Character, Integer>> transitions = new ArrayList<>();
        List<Integer> link = new ArrayList<>();
        List<Integer> len = new ArrayList<>();
        transitions.add(new HashMap<>());
        link.add(-1);
        len.add(0);
        int last = 0;
        for (char ch : a.toCharArray()) {
            int cur = transitions.size();
            transitions.add(new HashMap<>());
            len.add(len.get(last) + 1);
            link.add(0);
            int p = last;
            while (p != -1 && !transitions.get(p).containsKey(ch)) {
                transitions.get(p).put(ch, cur);
                p = link.get(p);
            }
            if (p != -1) {
                int q = transitions.get(p).get(ch);
                if (len.get(p) + 1 == len.get(q)) {
                    link.set(cur, q);
                } else {
                    int clone = transitions.size();
                    transitions.add(new HashMap<>(transitions.get(q)));
                    len.add(len.get(p) + 1);
                    link.add(link.get(q));
                    while (p != -1) {
                        Integer target = transitions.get(p).get(ch);
                        if (target == null || target != q) {
                            break;
                        }
                        transitions.get(p).put(ch, clone);
                        p = link.get(p);
                    }
                    link.set(q, clone);
                    link.set(cur, clone);
                }
            }
            last = cur;
        }

        int best = 0;
        int match = 0;
        int state = 0;
        for (char ch : b.toCharArray()) {
            while (state != 0 && !transitions.get(state).containsKey(ch)) {
                state = link.get(state);
                match = len.get(state);
            }
            if (transitions.get(state).containsKey(ch)) {
                state = transitions.get(state).get(ch);
                match++;
            } else {
                state = 0;
                match = 0;
            }
            best = Math.max(best, match);
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestCommonSubstring("abcdxyz", "xyzabcd"));
    }
}
