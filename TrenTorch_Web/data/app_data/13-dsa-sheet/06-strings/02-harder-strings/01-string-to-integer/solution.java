public class Main {
    // O(n) time, O(1) space
    static long myAtoi(String s) {
        int i = 0;
        int n = s.length();
        // Skip leading spaces
        while (i < n && s.charAt(i) == ' ') {
            i++;
        }
        int sign = 1;
        if (i < n) {
            char c = s.charAt(i);
            if (c == '+' || c == '-') {
                sign = (c == '-') ? -1 : 1;
                i++;
            }
        }
        long value = 0;
        final long LIMIT = 2147483648L; // 2^31
        while (i < n) {
            char c = s.charAt(i);
            if (c < '0' || c > '9') {
                break;
            }
            value = value * 10 + (c - '0');
            i++;
            if (value > LIMIT) {
                break;
            }
        }
        value *= sign;
        final long INT_MAX = 2147483647L;
        final long INT_MIN = -2147483648L;
        if (value > INT_MAX) return INT_MAX;
        if (value < INT_MIN) return INT_MIN;
        return value;
    }

    public static void main(String[] args) {
        System.out.println(myAtoi("42"));
    }
}
