public class Main {
    static long longestUniqueSubstring(String s) {
        // O(n) time, O(min(n, charset)) space
        java.util.Map<Character, Integer> last = new java.util.HashMap<>();
        int start = 0;
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (last.containsKey(ch) && last.get(ch) >= start) {
                start = last.get(ch) + 1;
            }
            last.put(ch, i);
            int currentLen = i - start + 1;
            if (currentLen > best) {
                best = currentLen;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestUniqueSubstring("abcabcbb"));
    }
}
