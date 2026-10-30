import java.util.*;

public class Main {
    // O(n) time, O(1) space
    static boolean backspaceCompare(String s, String t) {
        int i = s.length() - 1;
        int j = t.length() - 1;

        while (true) {
            i = nextTyped(s, i);
            j = nextTyped(t, j);
            if (i < 0 && j < 0) {
                return true;
            }
            if (i < 0 || j < 0 || s.charAt(i) != t.charAt(j)) {
                return false;
            }
            i--;
            j--;
        }
    }

    private static int nextTyped(String text, int index) {
        int skip = 0;
        while (index >= 0) {
            char c = text.charAt(index);
            if (c == '#') {
                skip++;
            } else if (skip > 0) {
                skip--;
            } else {
                return index;
            }
            index--;
        }
        return -1;
    }

    public static void main(String[] args) {
        System.out.println(backspaceCompare("ab#c", "ad#c"));
    }
}
