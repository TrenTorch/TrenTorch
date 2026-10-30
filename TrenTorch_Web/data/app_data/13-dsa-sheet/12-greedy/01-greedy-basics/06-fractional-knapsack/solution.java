import java.util.Arrays;
import java.util.Comparator;

public class Main {
    // O(n log n) time, O(1) extra space (sorting in-place)
    static double fractionalKnapsack(long[][] items, long capacity) {
        if (items == null || items.length == 0 || capacity == 0) {
            return 0.0;
        }
        Arrays.sort(items, new Comparator<long[]>() {
            @Override
            public int compare(long[] a, long[] b) {
                double ratioA = (double) a[0] / a[1];
                double ratioB = (double) b[0] / b[1];
                return Double.compare(ratioB, ratioA); // descending
            }
        });

        double total = 0.0;
        for (long[] item : items) {
            long value = item[0];
            long weight = item[1];
            long take = Math.min(weight, capacity);
            total += (double) value * take / weight;
            capacity -= take;
            if (capacity == 0) {
                break;
            }
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(fractionalKnapsack(new long[][]{new long[]{60L, 10L}, new long[]{100L, 20L}, new long[]{120L, 30L}}, 50L));
    }
}
