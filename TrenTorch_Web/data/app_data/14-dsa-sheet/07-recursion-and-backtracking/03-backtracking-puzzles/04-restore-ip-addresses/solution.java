import java.util.*;

public class Main {
    // O(1) time for a bounded input (at most 3^4 splits), O(n) space for the recursion and output
    static String[] restoreIpAddresses(String s) {
        List<String> out = new ArrayList<>();
        ipGo(s, 0, new ArrayList<>(), out);
        Collections.sort(out);
        return out.toArray(new String[0]);
    }

    static boolean validPart(String part) {
        return (part.equals("0") || !part.startsWith("0")) && Integer.parseInt(part) <= 255;
    }

    static void ipGo(String s, int start, List<String> parts, List<String> out) {
        if (parts.size() == 4) {
            if (start == s.length()) {
                out.add(String.join(".", parts));
            }
            return;
        }
        for (int length = 1; length <= 3; length++) {
            if (start + length > s.length()) {
                break;
            }
            String part = s.substring(start, start + length);
            if (validPart(part)) {
                parts.add(part);
                ipGo(s, start + length, parts, out);
                parts.remove(parts.size() - 1);
            }
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(restoreIpAddresses("25525511135")));
    }
}
