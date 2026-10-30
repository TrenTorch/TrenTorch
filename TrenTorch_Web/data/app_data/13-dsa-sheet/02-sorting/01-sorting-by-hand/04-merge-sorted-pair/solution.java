import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n + m) time, O(n + m) space
    public static List<Object> mergeSortedPair(List<Long> a, List<Long> b) {
        List<Long> merged = new ArrayList<>();
        int i = 0, j = 0;
        long comparisons = 0;
        while (i < a.size() && j < b.size()) {
            comparisons++;
            if (a.get(i) <= b.get(j)) {
                merged.add(a.get(i));
                i++;
            } else {
                merged.add(b.get(j));
                j++;
            }
        }
        while (i < a.size()) {
            merged.add(a.get(i));
            i++;
        }
        while (j < b.size()) {
            merged.add(b.get(j));
            j++;
        }
        List<Object> result = new ArrayList<>();
        result.add(merged);
        result.add(comparisons);
        return result;
    }

    public static void main(String[] args) {
    }
}
