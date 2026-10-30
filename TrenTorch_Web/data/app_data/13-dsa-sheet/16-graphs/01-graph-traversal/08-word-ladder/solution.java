import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class Main {
    // O(N * L^2) time, O(N * L^2) space (N words of length L; each wildcard key is O(L) to build)
    static long ladderLength(String begin, String end, String[] words) {
        Set<String> allowed = new HashSet<>(Arrays.asList(words));
        if (!allowed.contains(end)) {
            return 0;
        }
        Set<String> all = new HashSet<>(allowed);
        all.add(begin);
        Map<String, List<String>> groups = new HashMap<>();
        for (String word : all) {
            for (int i = 0; i < word.length(); i++) {
                String key = word.substring(0, i) + "*" + word.substring(i + 1);
                groups.computeIfAbsent(key, k -> new ArrayList<>()).add(word);
            }
        }
        Set<String> seen = new HashSet<>();
        seen.add(begin);
        ArrayDeque<String> queue = new ArrayDeque<>();
        ArrayDeque<Long> steps = new ArrayDeque<>();
        queue.add(begin);
        steps.add(1L);
        while (!queue.isEmpty()) {
            String word = queue.poll();
            long s = steps.poll();
            if (word.equals(end)) {
                return s;
            }
            for (int i = 0; i < word.length(); i++) {
                String key = word.substring(0, i) + "*" + word.substring(i + 1);
                for (String other : groups.getOrDefault(key, Collections.emptyList())) {
                    if (seen.add(other)) {
                        queue.add(other);
                        steps.add(s + 1);
                    }
                }
            }
        }
        return 0;
    }

    public static void main(String[] args) {
        System.out.println(ladderLength("hit", "cog", new String[]{"hot", "dot", "dog", "lot", "log", "cog"}));
    }
}
