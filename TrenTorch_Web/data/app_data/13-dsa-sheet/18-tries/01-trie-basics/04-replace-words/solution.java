import java.util.*;

public class Main {
    static class TrieNode {
        Map<Character, TrieNode> next = new HashMap<>();
        boolean end;
    }

    // O(total root length + sentence length) time, O(total root length) space
    static String replaceWords(String[] roots, String sentence) {
        TrieNode trie = new TrieNode();
        for (String root : roots) {
            TrieNode node = trie;
            for (int i = 0; i < root.length(); i++) {
                node = node.next.computeIfAbsent(root.charAt(i), k -> new TrieNode());
            }
            node.end = true;
        }
        String trimmed = sentence.trim();
        if (trimmed.isEmpty()) {
            return "";
        }
        String[] words = trimmed.split("\\s+");
        List<String> out = new ArrayList<>();
        for (String word : words) {
            String result = word;
            TrieNode node = trie;
            for (int i = 0; i < word.length(); i++) {
                node = node.next.get(word.charAt(i));
                if (node == null) {
                    break;
                }
                if (node.end) {
                    result = word.substring(0, i + 1);
                    break;
                }
            }
            out.add(result);
        }
        return String.join(" ", out);
    }

    public static void main(String[] args) {
        System.out.println(replaceWords(new String[]{"cat", "bat", "rat"}, "the cattle was rattled by the battery"));
    }
}
