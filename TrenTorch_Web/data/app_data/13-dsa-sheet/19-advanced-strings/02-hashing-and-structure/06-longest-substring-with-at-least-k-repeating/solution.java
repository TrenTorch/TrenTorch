import java.util.*;

public class Main {
    // O(26 * n) time, O(n) space (recursive split on rare letters)
    static long longestSubstringKRepeating(String s, long k) {
        return solve(s, 0, s.length(), k);
    }

    static long solve(String s, int lo, int hi, long k) {
        if (hi - lo < k) {
            return 0;
        }
        Map<Character, Integer> counts = new HashMap<>();
        for (int i = lo; i < hi; i++) {
            counts.merge(s.charAt(i), 1, Integer::sum);
        }
        Set<Character> rare = new HashSet<>();
        for (Map.Entry<Character, Integer> e : counts.entrySet()) {
            if (e.getValue() < k) {
                rare.add(e.getKey());
            }
        }
        if (rare.isEmpty()) {
            return hi - lo;
        }
        long best = 0;
        int start = lo;
        for (int i = lo; i <= hi; i++) {
            if (i == hi || rare.contains(s.charAt(i))) {
                best = Math.max(best, solve(s, start, i, k));
                start = i + 1;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(longestSubstringKRepeating("aaabb", 3L));
    }
}
