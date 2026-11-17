public class Main {
    // O(log n) time, O(log n) space (digits of one number)
    static long nthDigit(long n) {
        long length = 1;
        long count = 9;
        long start = 1;
        while (n > length * count) {
            n -= length * count;
            length++;
            count *= 10;
            start *= 10;
        }
        long number = start + (n - 1) / length;
        String digits = Long.toString(number);
        return digits.charAt((int) ((n - 1) % length)) - '0';
    }

    public static void main(String[] args) {
        System.out.println(nthDigit(11L));
    }
}
