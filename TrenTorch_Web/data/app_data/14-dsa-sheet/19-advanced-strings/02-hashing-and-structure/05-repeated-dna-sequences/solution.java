import java.util.*;

public class Main {
    // O(n) time (10-letter windows, hashed), O(n) space
    static String[] repeatedDna(String s) {
        Set<String> seen = new HashSet<>();
        Set<String> repeated = new HashSet<>();
        for (int i = 0; i + 10 <= s.length(); i++) {
            String part = s.substring(i, i + 10);
            if (!seen.add(part)) {
                repeated.add(part);
            }
        }
        List<String> sorted = new ArrayList<>(repeated);
        Collections.sort(sorted);
        return sorted.toArray(new String[0]);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(repeatedDna("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT")));
    }
}
