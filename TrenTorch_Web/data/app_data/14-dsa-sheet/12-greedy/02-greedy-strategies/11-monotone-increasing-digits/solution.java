public class Main {
    // O(log n) time, O(log n) space
    static long monotoneIncreasingDigits(long n) {
        char[] digits = String.valueOf(n).toCharArray();
        int mark = digits.length;
        for (int i = digits.length - 1; i > 0; i--) {
            if (digits[i - 1] > digits[i]) {
                digits[i - 1] = (char) (digits[i - 1] - 1);
                mark = i;
            }
        }
        for (int i = mark; i < digits.length; i++) {
            digits[i] = '9';
        }
        return Long.parseLong(new String(digits));
    }

    public static void main(String[] args) {
        System.out.println(monotoneIncreasingDigits(332L));
    }
}
