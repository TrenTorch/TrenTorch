import java.util.ArrayList;
import java.util.Arrays;

public class Main {
    // O(N) time, O(N) space where N is total number of characters in all operations
    static boolean[] runTrie(String[] ops) {
        class TrieNode {
            TrieNode[] children = new TrieNode[26];
            boolean isEnd = false;
        }

        TrieNode root = new TrieNode();
        ArrayList<Boolean> results = new ArrayList<>();

        for (String op : ops) {
            String[] parts = op.split(" ");
            String kind = parts[0];
            String word = parts[1];

            if (kind.equals("insert")) {
                TrieNode node = root;
                for (char ch : word.toCharArray()) {
                    int idx = ch - 'a';
                    if (node.children[idx] == null) {
                        node.children[idx] = new TrieNode();
                    }
                    node = node.children[idx];
                }
                node.isEnd = true;
            } else if (kind.equals("search")) {
                TrieNode node = root;
                boolean found = true;
                for (char ch : word.toCharArray()) {
                    int idx = ch - 'a';
                    if (node.children[idx] == null) {
                        found = false;
                        break;
                    }
                    node = node.children[idx];
                }
                results.add(found && node.isEnd);
            } else { // starts
                TrieNode node = root;
                boolean found = true;
                for (char ch : word.toCharArray()) {
                    int idx = ch - 'a';
                    if (node.children[idx] == null) {
                        found = false;
                        break;
                    }
                    node = node.children[idx];
                }
                results.add(found);
            }
        }

        boolean[] ans = new boolean[results.size()];
        for (int i = 0; i < ans.length; i++) {
            ans[i] = results.get(i);
        }
        return ans;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runTrie(new String[]{"insert apple", "search apple", "search app", "starts app", "insert app", "search app"})));
    }
}
