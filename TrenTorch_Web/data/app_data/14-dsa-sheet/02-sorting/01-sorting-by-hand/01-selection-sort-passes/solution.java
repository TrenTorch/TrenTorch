import java.util.ArrayList;
import java.util.Arrays;

public class Main {
    // O(n^2) time, O(n^2) space
    static long[][] selectionSortPasses(long[] nums) {
        int n = nums.length;
        if (n < 2) {
            return new long[0][];
        }
        long[] a = nums.clone();
        ArrayList<long[]> passes = new ArrayList<>();
        for (int i = 0; i < n - 1; i++) {
            int smallest = i;
            for (int j = i + 1; j < n; j++) {
                if (a[j] < a[smallest]) {
                    smallest = j;
                }
            }
            long temp = a[i];
            a[i] = a[smallest];
            a[smallest] = temp;
            passes.add(a.clone());
        }
        return passes.toArray(new long[0][]);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(selectionSortPasses(new long[]{64L, 25L, 12L, 22L, 11L})));
    }
}
