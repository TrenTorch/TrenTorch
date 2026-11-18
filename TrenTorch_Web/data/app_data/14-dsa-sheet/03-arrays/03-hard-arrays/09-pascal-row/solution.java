public class Main {
    // O(n) time, O(n) space where n = row
    static long[] pascalRow(long row) {
        long[] out = new long[(int) row + 1];
        long value = 1;
        for (int i = 0; i <= row; i++) {
            out[i] = value;
            value = value * (row - i) / (i + 1);
        }
        return out;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(pascalRow(4L)));
    }
}
