public class Main {
    // O(n) time, O(n) space (two-pointer minimal rotation on s + s)
    static String smallestRotation(String s) {
        int n = s.length();
        if (n == 0) {
            return "";
        }
        String s2 = s + s;
        int i = 0;
        int j = 1;
        int k = 0;
        while (i < n && j < n && k < n) {
            char a = s2.charAt(i + k);
            char b = s2.charAt(j + k);
            if (a == b) {
                k++;
                continue;
            }
            if (a > b) {
                i += k + 1;
            } else {
                j += k + 1;
            }
            if (i == j) {
                j++;
            }
            k = 0;
        }
        int start = Math.min(i, j);
        return s2.substring(start, start + n);
    }

    public static void main(String[] args) {
        System.out.println(smallestRotation("bca"));
    }
}
