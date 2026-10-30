import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    // O(n) time, O(n) space where n is length of decoded string
    static String decodeString(String s) {
        StringBuilder out = new StringBuilder();
        Deque<int[]> openBlocks = new ArrayDeque<>();
        int num = 0;
        for (char ch : s.toCharArray()) {
            if (Character.isDigit(ch)) {
                num = num * 10 + (ch - '0');
            } else if (ch == '[') {
                openBlocks.push(new int[]{out.length(), num});
                num = 0;
            } else if (ch == ']') {
                int[] block = openBlocks.pop();
                int start = block[0];
                int count = block[1];
                if (count == 0) {
                    out.delete(start, out.length());
                } else if (count > 1) {
                    String segment = out.substring(start, out.length());
                    for (int i = 1; i < count; i++) {
                        out.append(segment);
                    }
                }
            } else {
                out.append(ch);
            }
        }
        return out.toString();
    }

    public static void main(String[] args) {
        System.out.println(decodeString("3[a2[c]]"));
    }
}
