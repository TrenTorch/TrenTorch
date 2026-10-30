import java.util.ArrayList;
import java.util.Arrays;

public class Main {
    // O(n) time, O(1) space
    static long[] partitionLabels(String s) {
        int n = s.length();
        if (n == 0) {
            return new long[0];
        }
        int[] last = new int[26];
        for (int i = 0; i < n; i++) {
            last[s.charAt(i) - 'a'] = i;
        }
        ArrayList<Long> sizes = new ArrayList<>();
        int start = 0;
        int end = 0;
        for (int i = 0; i < n; i++) {
            end = Math.max(end, last[s.charAt(i) - 'a']);
            if (i == end) {
                sizes.add((long) (end - start + 1));
                start = i + 1;
            }
        }
        long[] result = new long[sizes.size()];
        for (int i = 0; i < sizes.size(); i++) {
            result[i] = sizes.get(i);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(partitionLabels("ababcbacadefegdehijhklij")));
    }
}
