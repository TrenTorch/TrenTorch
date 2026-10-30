import java.util.*;

public class Main {
    // O(n * L) time, O(n * L) space where L is the maximum word length
    static String longestWord(String[] words) {
        Map<Integer, List<String>> byLength = new HashMap<>();
        for (String word : new HashSet<>(Arrays.asList(words))) {
            byLength.computeIfAbsent(word.length(), k -> new ArrayList<>()).add(word);
        }
        Set<String> built = new HashSet<>();
        built.add("");
        String best = "";
        int length = 1;
        while (true) {
            List<String> good = new ArrayList<>();
            for (String w : byLength.getOrDefault(length, Collections.emptyList())) {
                if (built.contains(w.substring(0, w.length() - 1))) {
                    good.add(w);
                }
            }
            if (good.isEmpty()) {
                return best;
            }
            built.addAll(good);
            best = Collections.min(good);
            length++;
        }
    }

    public static void main(String[] args) {
        System.out.println(longestWord(new String[]{"w", "wo", "wor", "worl", "world"}));
    }
}
