import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class Main {
    // O(n + m) time, O(n + m) space
    static long[] commonValues(long[] a, long[] b) {
        Set<Long> setA = new HashSet<>();
        for (long x : a) {
            setA.add(x);
        }
        Set<Long> common = new HashSet<>();
        for (long x : b) {
            if (setA.contains(x)) {
                common.add(x);
            }
        }
        long[] result = new long[common.size()];
        int i = 0;
        for (long x : common) {
            result[i++] = x;
        }
        Arrays.sort(result);
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(commonValues(new long[]{1L, 2L, 2L, 3L}, new long[]{2L, 2L, 3L, 4L})));
    }
}
