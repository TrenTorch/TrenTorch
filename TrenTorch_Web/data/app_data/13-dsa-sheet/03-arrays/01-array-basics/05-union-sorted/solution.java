import java.util.ArrayList;
import java.util.Arrays;

public class Main {
    // O(n + m) time, O(n + m) space
    static long[] unionSorted(long[] a, long[] b) {
        ArrayList<Long> out = new ArrayList<>();
        int i = 0, j = 0;
        while (i < a.length || j < b.length) {
            long x;
            if (j == b.length || (i < a.length && a[i] <= b[j])) {
                x = a[i];
                i++;
            } else {
                x = b[j];
                j++;
            }
            if (out.isEmpty() || out.get(out.size() - 1) != x) {
                out.add(x);
            }
        }
        long[] result = new long[out.size()];
        for (int k = 0; k < out.size(); k++) {
            result[k] = out.get(k);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(unionSorted(new long[]{1L, 2L, 2L, 4L}, new long[]{2L, 3L, 4L, 5L})));
    }
}
