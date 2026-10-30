import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n) time, O(k) space where k is the number of distinct characters
    static boolean isAnagram(String a, String b) {
        if (a.length() != b.length()) {
            return false;
        }
        Map<Character, Integer> counts = new HashMap<>();
        for (char c : a.toCharArray()) {
            counts.merge(c, 1, Integer::sum);
        }
        for (char c : b.toCharArray()) {
            int left = counts.getOrDefault(c, 0);
            if (left == 0) {
                return false;
            }
            counts.put(c, left - 1);
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isAnagram("listen", "silent"));
    }
}
