public class Main {
    // O(n * m) time where m is the prefix length, O(1) extra space
    static String longestCommonPrefix(String[] words) {
        if (words.length == 0) {
            return "";
        }
        String first = words[0];
        String last = words[0];
        for (String w : words) {
            if (w.compareTo(first) < 0) {
                first = w;
            }
            if (w.compareTo(last) > 0) {
                last = w;
            }
        }
        int i = 0;
        while (i < first.length() && i < last.length() && first.charAt(i) == last.charAt(i)) {
            i++;
        }
        return first.substring(0, i);
    }

    public static void main(String[] args) {
        System.out.println(longestCommonPrefix(new String[]{"flower", "flow", "flight"}));
    }
}
