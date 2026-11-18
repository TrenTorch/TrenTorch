import java.util.*;

public class Main {
    // O(N * L) time, O(N * L) space where N is number of unique words, L is max word length (<=7)
    static long minimumLengthEncoding(String[] words) {
        Set<String> unique = new HashSet<>(Arrays.asList(words));
        TrieNode root = new TrieNode();
        List<Entry> entries = new ArrayList<>();
        for (String word : unique) {
            TrieNode node = root;
            for (int i = word.length() - 1; i >= 0; i--) {
                char c = word.charAt(i);
                node = node.children.computeIfAbsent(c, k -> new TrieNode());
            }
            entries.add(new Entry(node, word.length()));
        }
        long ans = 0;
        for (Entry e : entries) {
            if (e.node.children.isEmpty()) {
                ans += e.length + 1;
            }
        }
        return ans;
    }

    static class TrieNode {
        Map<Character, TrieNode> children = new HashMap<>();
    }

    static class Entry {
        TrieNode node;
        int length;
        Entry(TrieNode node, int length) {
            this.node = node;
            this.length = length;
        }
    }

    public static void main(String[] args) {
        System.out.println(minimumLengthEncoding(new String[]{"time", "me", "bell"}));
    }
}
