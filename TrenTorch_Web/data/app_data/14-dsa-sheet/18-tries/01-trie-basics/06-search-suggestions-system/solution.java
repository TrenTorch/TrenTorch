import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n log n + m log n) time, O(n) space
    static String[][] suggestedProducts(String[] products, String searchWord) {
        Arrays.sort(products);
        List<String[]> result = new ArrayList<>();
        for (int i = 1; i <= searchWord.length(); i++) {
            String prefix = searchWord.substring(0, i);
            int start = lowerBound(products, prefix);
            List<String> suggestions = new ArrayList<>();
            for (int j = start; j < Math.min(start + 3, products.length); j++) {
                if (products[j].startsWith(prefix)) {
                    suggestions.add(products[j]);
                } else {
                    break;
                }
            }
            result.add(suggestions.toArray(new String[0]));
        }
        return result.toArray(new String[0][]);
    }

    private static int lowerBound(String[] arr, String target) {
        int low = 0;
        int high = arr.length;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (arr[mid].compareTo(target) < 0) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }
        return low;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(suggestedProducts(new String[]{"mobile", "mouse", "moneypot", "monitor", "mousepad"}, "mouse")));
    }
}
