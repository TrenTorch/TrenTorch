import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class Main {
    // O(n) time, O(1) space (alphabet size is constant)
    public static List<List<Object>> topCharacters(String s, int k) {
        int[] freq = new int[26];
        for (char c : s.toCharArray()) {
            freq[c - 'a']++;
        }
        List<int[]> entries = new ArrayList<>();
        for (int i = 0; i < 26; i++) {
            if (freq[i] > 0) {
                entries.add(new int[]{i, freq[i]});
            }
        }
        entries.sort((a, b) -> {
            if (a[1] != b[1]) {
                return Integer.compare(b[1], a[1]); // descending frequency
            }
            return Integer.compare(a[0], b[0]); // ascending character
        });
        List<List<Object>> result = new ArrayList<>();
        int limit = Math.min(k, entries.size());
        for (int i = 0; i < limit; i++) {
            int[] entry = entries.get(i);
            List<Object> pair = new ArrayList<>();
            pair.add((char) ('a' + entry[0]));
            pair.add(entry[1]);
            result.add(pair);
        }
        return result;
    }

    public static void main(String[] args) {
    }
}
