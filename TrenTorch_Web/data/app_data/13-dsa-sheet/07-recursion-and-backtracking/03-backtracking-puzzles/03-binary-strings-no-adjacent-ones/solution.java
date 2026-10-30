import java.util.*;

public class Main {
    // O(F(n) * n) time where F(n) is the answer count (about 1.6^n), O(n) recursion space
    static String[] noAdjacentOnes(long n) {
        List<String> out = new ArrayList<>();
        binaryGo((int) n, new StringBuilder(), out);
        return out.toArray(new String[0]);
    }

    static void binaryGo(int n, StringBuilder prefix, List<String> out) {
        if (prefix.length() == n) {
            out.add(prefix.toString());
            return;
        }
        prefix.append('0');
        binaryGo(n, prefix, out);
        prefix.setLength(prefix.length() - 1);
        if (prefix.length() == 0 || prefix.charAt(prefix.length() - 1) != '1') {
            prefix.append('1');
            binaryGo(n, prefix, out);
            prefix.setLength(prefix.length() - 1);
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(noAdjacentOnes(3L)));
    }
}
