import java.util.Arrays;

public class Main {
    // O(2^n) time, O(2^n) space
    static long[] grayCode(long n) {
        int nn = (int) n;
        int size = 1 << nn;
        long[] result = new long[size];
        for (int i = 0; i < size; i++) {
            result[i] = i ^ (i >> 1);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(grayCode(2L)));
    }
}
