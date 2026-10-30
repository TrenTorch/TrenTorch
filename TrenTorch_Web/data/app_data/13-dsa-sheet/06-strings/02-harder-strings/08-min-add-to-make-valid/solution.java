public class Main {
    // O(n) time, O(1) space
    static long minAddToMakeValid(String s) {
        long openCount = 0;
        long need = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                openCount++;
            } else if (openCount > 0) {
                openCount--;
            } else {
                need++;
            }
        }
        return need + openCount;
    }

    public static void main(String[] args) {
        System.out.println(minAddToMakeValid("())"));
    }
}
