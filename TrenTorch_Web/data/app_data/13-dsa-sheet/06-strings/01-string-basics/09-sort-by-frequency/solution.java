import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Main {
    // O(n + k log k) time where k is the number of distinct characters, O(n) space
    static String sortByFrequency(String s) {
        Map<Character, Integer> counts = new HashMap<>();
        for (char ch : s.toCharArray()) {
            counts.merge(ch, 1, Integer::sum);
        }
        List<Character> order = new ArrayList<>(counts.keySet());
        order.sort((x, y) -> {
            int cx = counts.get(x);
            int cy = counts.get(y);
            if (cx != cy) {
                return Integer.compare(cy, cx);
            }
            return Character.compare(x, y);
        });
        StringBuilder sb = new StringBuilder();
        for (char ch : order) {
            int n = counts.get(ch);
            for (int i = 0; i < n; i++) {
                sb.append(ch);
            }
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        System.out.println(sortByFrequency("tree"));
    }
}
