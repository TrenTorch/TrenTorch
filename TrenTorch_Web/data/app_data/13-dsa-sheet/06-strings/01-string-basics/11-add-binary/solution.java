public class Main {
    // O(max(n, m)) time, O(max(n, m)) space
    static String addBinary(String a, String b) {
        StringBuilder out = new StringBuilder();
        int i = a.length() - 1, j = b.length() - 1, carry = 0;
        while (i >= 0 || j >= 0 || carry > 0) {
            int total = carry;
            if (i >= 0) {
                total += a.charAt(i) - '0';
                i--;
            }
            if (j >= 0) {
                total += b.charAt(j) - '0';
                j--;
            }
            out.append(total % 2);
            carry = total / 2;
        }
        return out.reverse().toString();
    }

    public static void main(String[] args) {
        System.out.println(addBinary("11", "1"));
    }
}
