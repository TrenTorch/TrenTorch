import java.util.ArrayList;

public class Main {
    // O(n + m) time, O(min(n, m)) space
    static long[] intersectionSorted(long[] a, long[] b) {
        ArrayList<Long> out = new ArrayList<>();
        int i = 0, j = 0;
        while (i < a.length && j < b.length) {
            if (a[i] == b[j]) {
                out.add(a[i]);
                i++;
                j++;
            } else if (a[i] < b[j]) {
                i++;
            } else {
                j++;
            }
        }
        long[] result = new long[out.size()];
        for (int k = 0; k < out.size(); k++) {
            result[k] = out.get(k);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(intersectionSorted(new long[]{1L, 2L, 2L, 3L}, new long[]{2L, 2L, 2L, 4L})));
    }
}
