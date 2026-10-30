public class Main {
    // O(n) time, O(n) space
    static String zigzagConversion(String s, long rows) {
        if (rows == 1 || rows >= s.length()) {
            return s;
        }
        int r = (int) rows;
        StringBuilder[] lines = new StringBuilder[r];
        for (int i = 0; i < r; i++) {
            lines[i] = new StringBuilder();
        }
        int row = 0;
        int step = 1;
        for (char ch : s.toCharArray()) {
            lines[row].append(ch);
            if (row == 0) {
                step = 1;
            } else if (row == r - 1) {
                step = -1;
            }
            row += step;
        }
        StringBuilder result = new StringBuilder();
        for (StringBuilder line : lines) {
            result.append(line);
        }
        return result.toString();
    }

    public static void main(String[] args) {
        System.out.println(zigzagConversion("PAYPALISHIRING", 3L));
    }
}
