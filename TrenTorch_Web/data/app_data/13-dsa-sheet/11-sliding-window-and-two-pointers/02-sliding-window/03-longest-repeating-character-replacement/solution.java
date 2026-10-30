public class Main {
    // O(n) time, O(1) space (at most 26 distinct letter keys)
    static long characterReplacement(String s, long k) {
        java.util.Map<Character, Integer> count = new java.util.HashMap<>();
        int left = 0;
        int maxCount = 0;
        for (int right = 0; right < s.length(); right++) {
            char ch = s.charAt(right);
            int c = count.merge(ch, 1, Integer::sum);
            maxCount = Math.max(maxCount, c);
            if ((long) (right - left + 1) - maxCount > k) {
                char lc = s.charAt(left);
                count.put(lc, count.get(lc) - 1);
                left++;
            }
        }
        return s.length() - left;
    }

    public static void main(String[] args) {
        System.out.println(characterReplacement("AABABBA", 1L));
    }
}
