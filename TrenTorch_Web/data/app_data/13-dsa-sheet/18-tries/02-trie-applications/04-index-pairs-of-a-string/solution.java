public class Main {
    static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEnd = false;
    }

    // O(n * L) time, O(T) space where L = max word length, T = total characters in words
    static long[][] indexPairs(String text, String[] words) {
        TrieNode root = new TrieNode();
        for (String word : words) {
            TrieNode node = root;
            for (char ch : word.toCharArray()) {
                int idx = ch - 'a';
                if (node.children[idx] == null) {
                    node.children[idx] = new TrieNode();
                }
                node = node.children[idx];
            }
            node.isEnd = true;
        }

        java.util.List<long[]> result = new java.util.ArrayList<>();
        int n = text.length();
        for (int i = 0; i < n; i++) {
            TrieNode node = root;
            for (int j = i; j < n; j++) {
                int idx = text.charAt(j) - 'a';
                if (node.children[idx] == null) {
                    break;
                }
                node = node.children[idx];
                if (node.isEnd) {
                    result.add(new long[]{i, j});
                }
            }
        }

        long[][] ans = new long[result.size()][];
        for (int i = 0; i < result.size(); i++) {
            ans[i] = result.get(i);
        }
        return ans;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(indexPairs("thestoryofleetcodeandme", new String[]{"story", "fleet", "leetcode"})));
    }
}
