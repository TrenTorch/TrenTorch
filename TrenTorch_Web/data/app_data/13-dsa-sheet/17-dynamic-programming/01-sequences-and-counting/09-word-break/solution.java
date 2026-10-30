import java.util.*;

public class Main {
    static boolean wordBreak(String s, String[] words) {
        // O(n * L) time, O(total chars in words) space, where n = s.length(), L = max word length
        class TrieNode {
            TrieNode[] children = new TrieNode[26];
            boolean isEnd = false;
        }
        TrieNode root = new TrieNode();
        for (String word : words) {
            TrieNode node = root;
            for (char c : word.toCharArray()) {
                int idx = c - 'a';
                if (node.children[idx] == null) {
                    node.children[idx] = new TrieNode();
                }
                node = node.children[idx];
            }
            node.isEnd = true;
        }
        int n = s.length();
        boolean[] reachable = new boolean[n + 1];
        reachable[0] = true;
        for (int i = 0; i < n; i++) {
            if (!reachable[i]) continue;
            TrieNode node = root;
            for (int j = i; j < n; j++) {
                int idx = s.charAt(j) - 'a';
                if (node.children[idx] == null) break;
                node = node.children[idx];
                if (node.isEnd) {
                    reachable[j + 1] = true;
                }
            }
        }
        return reachable[n];
    }

    public static void main(String[] args) {
        System.out.println(wordBreak("leetcode", new String[]{"leet", "code"}));
    }
}
