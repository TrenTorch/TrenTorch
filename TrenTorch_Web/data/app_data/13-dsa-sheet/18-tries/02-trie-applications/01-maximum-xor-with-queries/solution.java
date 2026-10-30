public class Main {
    // O((N+Q) * 30) time, O(N * 30) space
    static long[] maxXorQueries(long[] nums, long[] queries) {
        class TrieNode {
            TrieNode[] children = new TrieNode[2];
        }
        TrieNode root = new TrieNode();
        // Build trie from nums
        for (long n : nums) {
            int val = (int) n;
            TrieNode node = root;
            for (int b = 29; b >= 0; b--) {
                int bit = (val >> b) & 1;
                if (node.children[bit] == null) {
                    node.children[bit] = new TrieNode();
                }
                node = node.children[bit];
            }
        }
        long[] result = new long[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int val = (int) queries[i];
            TrieNode node = root;
            int best = 0;
            for (int b = 29; b >= 0; b--) {
                int bit = (val >> b) & 1;
                int desired = 1 - bit;
                if (node.children[desired] != null) {
                    best |= (1 << b);
                    node = node.children[desired];
                } else {
                    node = node.children[bit];
                }
            }
            result[i] = best;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(maxXorQueries(new long[]{0L, 1L, 2L, 3L, 4L}, new long[]{3L, 5L})));
    }
}
