import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n) time, O(k) space
    static long longestKDistinct(String s, long k) {
        Map<Character, Integer> count = new HashMap<>();
        int left = 0;
        int best = 0;
        for (int right = 0; right < s.length(); right++) {
            char ch = s.charAt(right);
            count.put(ch, count.getOrDefault(ch, 0) + 1);
            while (count.size() > k) {
                char leftChar = s.charAt(left);
                count.put(leftChar, count.get(leftChar) - 1);
                if (count.get(leftChar) == 0) {
                    count.remove(leftChar);
                }
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestKDistinct("eceba", 2L));
    }
}
