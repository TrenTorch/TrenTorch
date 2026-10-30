import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

public class Main {
    // O(N * L) time, O(1) space (where N = number of words, L = max word length, alphabet size is constant 26)
    static String alienOrder(String[] words) {
        boolean[] present = new boolean[26];
        for (String w : words) {
            for (char c : w.toCharArray()) {
                present[c - 'a'] = true;
            }
        }

        boolean[][] edge = new boolean[26][26];
        for (int i = 0; i < words.length - 1; i++) {
            String w1 = words[i];
            String w2 = words[i + 1];
            int len = Math.min(w1.length(), w2.length());
            boolean foundDiff = false;
            for (int j = 0; j < len; j++) {
                char c1 = w1.charAt(j);
                char c2 = w2.charAt(j);
                if (c1 != c2) {
                    if (!edge[c1 - 'a'][c2 - 'a']) {
                        edge[c1 - 'a'][c2 - 'a'] = true;
                    }
                    foundDiff = true;
                    break;
                }
            }
            if (!foundDiff && w1.length() > w2.length()) {
                return "";
            }
        }

        List<Integer>[] adj = new ArrayList[26];
        int[] inDegree = new int[26];
        for (int i = 0; i < 26; i++) {
            adj[i] = new ArrayList<>();
        }
        for (int u = 0; u < 26; u++) {
            for (int v = 0; v < 26; v++) {
                if (edge[u][v]) {
                    adj[u].add(v);
                    inDegree[v]++;
                }
            }
        }

        PriorityQueue<Character> pq = new PriorityQueue<>();
        int totalLetters = 0;
        for (int i = 0; i < 26; i++) {
            if (present[i]) {
                totalLetters++;
                if (inDegree[i] == 0) {
                    pq.offer((char)('a' + i));
                }
            }
        }

        StringBuilder sb = new StringBuilder();
        while (!pq.isEmpty()) {
            char c = pq.poll();
            sb.append(c);
            int u = c - 'a';
            for (int v : adj[u]) {
                inDegree[v]--;
                if (inDegree[v] == 0) {
                    pq.offer((char)('a' + v));
                }
            }
        }

        if (sb.length() != totalLetters) {
            return "";
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        System.out.println(alienOrder(new String[]{"wrt", "wrf", "er", "ett", "rftt"}));
    }
}
