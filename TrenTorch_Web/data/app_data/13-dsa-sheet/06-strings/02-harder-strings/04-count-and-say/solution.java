public class Main {
    // O(L) time and O(L) space per step, where L is the length of term n (about 1.3^n growth)
    static String countAndSay(long n) {
        String term = "1";
        for (long k = 1; k < n; k++) {
            StringBuilder sb = new StringBuilder();
            int i = 0;
            while (i < term.length()) {
                char digit = term.charAt(i);
                int j = i;
                while (j < term.length() && term.charAt(j) == digit) {
                    j++;
                }
                sb.append(j - i).append(digit);
                i = j;
            }
            term = sb.toString();
        }
        return term;
    }

    public static void main(String[] args) {
        System.out.println(countAndSay(4L));
    }
}
