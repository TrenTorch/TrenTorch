import java.util.*;

public class Main {
    // O(N! * N) time, O(N) space
    static String[] distinctPermutations(String s) {
        // Count characters and keep them sorted
        TreeMap<Character, Integer> freq = new TreeMap<>();
        for (char c : s.toCharArray()) {
            freq.put(c, freq.getOrDefault(c, 0) + 1);
        }
        int m = freq.size();
        char[] letters = new char[m];
        int[] left = new int[m];
        int idx = 0;
        for (Map.Entry<Character, Integer> e : freq.entrySet()) {
            letters[idx] = e.getKey();
            left[idx] = e.getValue();
            idx++;
        }
        int n = s.length();
        List<String> out = new ArrayList<>();
        StringBuilder prefix = new StringBuilder();
        build(out, letters, left, n, prefix);
        return out.toArray(new String[0]);
    }

    private static void build(List<String> out, char[] letters, int[] left, int n, StringBuilder prefix) {
        if (prefix.length() == n) {
            out.add(prefix.toString());
            return;
        }
        for (int i = 0; i < letters.length; i++) {
            if (left[i] > 0) {
                left[i]--;
                prefix.append(letters[i]);
                build(out, letters, left, n, prefix);
                prefix.deleteCharAt(prefix.length() - 1);
                left[i]++;
            }
        }
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(distinctPermutations("abc")));
    }
}
