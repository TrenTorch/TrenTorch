import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    // O(n) time, O(1) space (excluding output)
    static long[] findAnagrams(String s, String p) {
        int m = p.length();
        if (m == 0 || m > s.length()) {
            return new long[0];
        }
        int[] need = new int[26];
        int[] window = new int[26];
        for (char ch : p.toCharArray()) {
            need[ch - 'a']++;
        }
        List<Long> out = new ArrayList<>();
        for (int i = 0; i < s.length(); i++) {
            window[s.charAt(i) - 'a']++;
            if (i >= m) {
                window[s.charAt(i - m) - 'a']--;
            }
            if (i >= m - 1 && Arrays.equals(window, need)) {
                out.add((long) (i - m + 1));
            }
        }
        long[] result = new long[out.size()];
        for (int i = 0; i < out.size(); i++) {
            result[i] = out.get(i);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(findAnagrams("cbaebabacd", "abc")));
    }
}
