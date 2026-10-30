import java.util.ArrayList;
import java.util.List;

public class Main {
    static class Node {
        Node[] children = new Node[26];
        boolean isEnd = false;
    }

    // O(total length of added words) time for adds, O(26^L) worst-case for search (L <= 12), O(total length of added words) space
    static boolean[] runWordDictionary(String[] ops) {
        Node root = new Node();
        List<Boolean> results = new ArrayList<>();
        for (String op : ops) {
            String[] parts = op.split(" ", 2);
            String kind = parts[0];
            String text = parts[1];
            if (kind.equals("add")) {
                Node node = root;
                for (char ch : text.toCharArray()) {
                    int idx = ch - 'a';
                    if (node.children[idx] == null) {
                        node.children[idx] = new Node();
                    }
                    node = node.children[idx];
                }
                node.isEnd = true;
            } else { // search
                results.add(searchHelper(root, text, 0));
            }
        }
        boolean[] ans = new boolean[results.size()];
        for (int i = 0; i < results.size(); i++) {
            ans[i] = results.get(i);
        }
        return ans;
    }

    private static boolean searchHelper(Node node, String pattern, int index) {
        if (index == pattern.length()) {
            return node.isEnd;
        }
        char c = pattern.charAt(index);
        if (c == '.') {
            for (Node child : node.children) {
                if (child != null && searchHelper(child, pattern, index + 1)) {
                    return true;
                }
            }
            return false;
        } else {
            Node child = node.children[c - 'a'];
            return child != null && searchHelper(child, pattern, index + 1);
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runWordDictionary(new String[]{"add bad", "add dad", "add mad", "search pad", "search bad", "search .ad", "search b.."})));
    }
}
