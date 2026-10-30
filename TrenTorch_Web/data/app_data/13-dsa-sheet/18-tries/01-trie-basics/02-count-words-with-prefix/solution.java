public class Main {
    static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        long count = 0;
    }

    // O(total characters in words + total characters in queries) time, O(total characters in words) space
    static long[] countWithPrefix(String[] words, String[] queries) {
        TrieNode root = new TrieNode();
        for (String word : words) {
            TrieNode node = root;
            for (char c : word.toCharArray()) {
                int idx = c - 'a';
                if (node.children[idx] == null) {
                    node.children[idx] = new TrieNode();
                }
                node = node.children[idx];
                node.count++;
            }
        }
        long[] result = new long[queries.length];
        for (int i = 0; i < queries.length; i++) {
            TrieNode node = root;
            String q = queries[i];
            for (char c : q.toCharArray()) {
                int idx = c - 'a';
                if (node.children[idx] == null) {
                    node = null;
                    break;
                }
                node = node.children[idx];
            }
            result[i] = (node != null) ? node.count : 0;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(countWithPrefix(new String[]{"apple", "app", "apt", "bat"}, new String[]{"ap", "app", "b", "c"})));
    }
}
