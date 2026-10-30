import java.util.*;

public class Main {
    // O(n * sigma) time, O(n * sigma) space: suffix automaton with occurrence counts
    static long longestRepeatedLength(String s) {
        int n = s.length();
        int maxStates = 2 * n + 2;
        List<Map<Character, Integer>> nxt = new ArrayList<>();
        int[] link = new int[maxStates];
        int[] length = new int[maxStates];
        long[] occ = new long[maxStates];
        nxt.add(new HashMap<>());
        link[0] = -1;
        int size = 1;
        int last = 0;
        for (int idx = 0; idx < n; idx++) {
            char ch = s.charAt(idx);
            int cur = size++;
            nxt.add(new HashMap<>());
            link[cur] = 0;
            length[cur] = length[last] + 1;
            occ[cur] = 1;
            int p = last;
            while (p != -1 && !nxt.get(p).containsKey(ch)) {
                nxt.get(p).put(ch, cur);
                p = link[p];
            }
            if (p != -1) {
                int q = nxt.get(p).get(ch);
                if (length[p] + 1 == length[q]) {
                    link[cur] = q;
                } else {
                    int copy = size++;
                    nxt.add(new HashMap<>(nxt.get(q)));
                    link[copy] = link[q];
                    length[copy] = length[p] + 1;
                    occ[copy] = 0;
                    while (p != -1 && Integer.valueOf(q).equals(nxt.get(p).get(ch))) {
                        nxt.get(p).put(ch, copy);
                        p = link[p];
                    }
                    link[q] = copy;
                    link[cur] = copy;
                }
            }
            last = cur;
        }

        List<List<Integer>> byLength = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            byLength.add(new ArrayList<>());
        }
        for (int v = 1; v < size; v++) {
            byLength.get(length[v]).add(v);
        }
        long best = 0;
        for (int sz = n; sz >= 1; sz--) {
            for (int v : byLength.get(sz)) {
                if (occ[v] >= 2) {
                    best = Math.max(best, sz);
                }
                occ[link[v]] += occ[v];
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestRepeatedLength("banana"));
    }
}
