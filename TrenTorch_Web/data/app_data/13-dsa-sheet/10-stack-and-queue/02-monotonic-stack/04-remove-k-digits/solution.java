public class Main {
    // O(n) time, O(n) space
    static String removeKDigits(String num, long k) {
        int n = num.length();
        if (n == 0) return "0";
        char[] stack = new char[n];
        int top = -1;
        int kInt = (int) k;
        for (char c : num.toCharArray()) {
            while (kInt > 0 && top >= 0 && stack[top] > c) {
                top--;
                kInt--;
            }
            stack[++top] = c;
        }
        if (kInt > 0) {
            top -= kInt;
        }
        int start = 0;
        while (start <= top && stack[start] == '0') {
            start++;
        }
        if (start > top) {
            return "0";
        }
        return new String(stack, start, top - start + 1);
    }

    public static void main(String[] args) {
        System.out.println(removeKDigits("1432219", 3L));
    }
}
