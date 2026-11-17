import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class Main {
    // O(n log n) time, O(n) space
    public static List<String> sortRecords(List<List<Object>> records) {
        List<List<Object>> sorted = new ArrayList<>(records);
        sorted.sort(Comparator
                .comparing((List<Object> r) -> ((Number) r.get(1)).longValue(), Comparator.reverseOrder())
                .thenComparing(r -> (String) r.get(0)));
        List<String> result = new ArrayList<>(sorted.size());
        for (List<Object> r : sorted) {
            result.add((String) r.get(0));
        }
        return result;
    }

    public static void main(String[] args) {
    }
}
