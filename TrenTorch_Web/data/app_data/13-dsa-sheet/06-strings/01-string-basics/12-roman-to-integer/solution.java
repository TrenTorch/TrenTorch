public class Main {
    // O(n) time, O(1) space
    static long romanToInteger(String s) {
        long total = 0;
        for (int i = 0; i < s.length(); i++) {
            long value = romanValue(s.charAt(i));
            if (i + 1 < s.length() && value < romanValue(s.charAt(i + 1))) {
                total -= value;
            } else {
                total += value;
            }
        }
        return total;
    }

    static long romanValue(char ch) {
        switch (ch) {
            case 'I': return 1L;
            case 'V': return 5L;
            case 'X': return 10L;
            case 'L': return 50L;
            case 'C': return 100L;
            case 'D': return 500L;
            case 'M': return 1000L;
            default: throw new IllegalArgumentException("invalid roman numeral symbol: " + ch);
        }
    }

    public static void main(String[] args) {
        System.out.println(romanToInteger("III"));
    }
}
