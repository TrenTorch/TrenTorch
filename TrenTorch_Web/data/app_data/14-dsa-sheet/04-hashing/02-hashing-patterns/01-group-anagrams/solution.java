import java.util.*;

public class Main {
    // O(n log n) time, O(n) space
    static String[][] groupAnagrams(String[] words) {
        Map<String, List<String>> map = new HashMap<>();
        for (String word : words) {
            char[] chars = word.toCharArray();
            Arrays.sort(chars);
            String key = new String(chars);
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(word);
        }
        List<List<String>> groups = new ArrayList<>(map.values());
        for (List<String> group : groups) {
            Collections.sort(group);
        }
        groups.sort(Comparator.comparing(list -> list.get(0)));
        String[][] result = new String[groups.size()][];
        for (int i = 0; i < groups.size(); i++) {
            result[i] = groups.get(i).toArray(new String[0]);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(groupAnagrams(new String[]{"eat", "tea", "tan", "ate", "nat", "bat"})));
    }
}
