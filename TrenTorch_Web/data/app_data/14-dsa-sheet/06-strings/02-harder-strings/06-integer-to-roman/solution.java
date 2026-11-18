public class Main {
    // O(1) time, O(1) space
    static String integerToRoman(long num) {
        long[] values = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
        String[] symbols = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < values.length; i++) {
            long count = num / values[i];
            num %= values[i];
            for (int j = 0; j < count; j++) {
                out.append(symbols[i]);
            }
        }
        return out.toString();
    }

    public static void main(String[] args) {
        System.out.println(integerToRoman(3L));
    }
}
