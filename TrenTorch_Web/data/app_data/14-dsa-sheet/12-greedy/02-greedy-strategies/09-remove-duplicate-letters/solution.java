import java.util.ArrayList;

public class Main {
    // O(n) time, O(1) space
    static String removeDuplicateLetters(String s) {
        int n = s.length();
        int[] last = new int[26];
        for (int i = 0; i < n; i++) {
            last[s.charAt(i) - 'a'] = i;
        }
        ArrayList<Character> stack = new ArrayList<>();
        boolean[] inStack = new boolean[26];
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            int idx = ch - 'a';
            if (inStack[idx]) continue;
            while (!stack.isEmpty() && stack.get(stack.size() - 1) > ch && last[stack.get(stack.size() - 1) - 'a'] > i) {
                inStack[stack.remove(stack.size() - 1) - 'a'] = false;
            }
            stack.add(ch);
            inStack[idx] = true;
        }
        StringBuilder sb = new StringBuilder();
        for (char c : stack) {
            sb.append(c);
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        System.out.println(removeDuplicateLetters("bcabc"));
    }
}
