import java.util.*;

public class Main {
    // O(4^n * n) time for the output, O(n) recursion space (n = number of digits, at most 4 letters each)
    static String[] letterCombinations(String digits) {
        String[] keys = new String[10];
        keys[2] = "abc";
        keys[3] = "def";
        keys[4] = "ghi";
        keys[5] = "jkl";
        keys[6] = "mno";
        keys[7] = "pqrs";
        keys[8] = "tuv";
        keys[9] = "wxyz";
        if (digits.isEmpty()) {
            return new String[0];
        }
        List<String> out = new ArrayList<>();
        letterGo(digits, keys, 0, new StringBuilder(), out);
        return out.toArray(new String[0]);
    }

    static void letterGo(String digits, String[] keys, int i, StringBuilder prefix, List<String> out) {
        if (i == digits.length()) {
            out.add(prefix.toString());
            return;
        }
        String letters = keys[digits.charAt(i) - '0'];
        for (int k = 0; k < letters.length(); k++) {
            prefix.append(letters.charAt(k));
            letterGo(digits, keys, i + 1, prefix, out);
            prefix.setLength(prefix.length() - 1);
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(letterCombinations("23")));
    }
}
