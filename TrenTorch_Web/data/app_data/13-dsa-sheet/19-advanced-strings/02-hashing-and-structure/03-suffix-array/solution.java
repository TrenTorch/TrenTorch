public class Main {
    // O(n log^2 n) time, O(n) space (prefix doubling with counting sort)
    static long[] suffixArray(String s) {
        int len = s.length();
        if (len == 0) {
            return new long[0];
        }
        int n = len + 1;
        int[] text = new int[n];
        for (int i = 0; i < len; i++) {
            text[i] = s.charAt(i) + 1;
        }
        text[len] = 0;
        int maxVal = 0;
        for (int v : text) {
            maxVal = Math.max(maxVal, v);
        }
        int size = Math.max(maxVal + 1, n);
        int[] order = new int[n];
        int[] cls = new int[n];
        int[] count = new int[size];
        for (int v : text) {
            count[v]++;
        }
        for (int i = 1; i < size; i++) {
            count[i] += count[i - 1];
        }
        for (int i = n - 1; i >= 0; i--) {
            count[text[i]]--;
            order[count[text[i]]] = i;
        }
        int classes = 1;
        for (int i = 1; i < n; i++) {
            if (text[order[i]] != text[order[i - 1]]) {
                classes++;
            }
            cls[order[i]] = classes - 1;
        }
        int shift = 1;
        while (shift < n) {
            int[] bySecond = new int[n];
            for (int i = 0; i < n; i++) {
                bySecond[i] = ((order[i] - shift) % n + n) % n;
            }
            count = new int[classes];
            for (int i = 0; i < n; i++) {
                count[cls[bySecond[i]]]++;
            }
            for (int i = 1; i < classes; i++) {
                count[i] += count[i - 1];
            }
            for (int i = n - 1; i >= 0; i--) {
                int c = cls[bySecond[i]];
                count[c]--;
                order[count[c]] = bySecond[i];
            }
            int[] newCls = new int[n];
            classes = 1;
            for (int i = 1; i < n; i++) {
                int a = order[i];
                int b = order[i - 1];
                if (cls[a] != cls[b] || cls[(a + shift) % n] != cls[(b + shift) % n]) {
                    classes++;
                }
                newCls[a] = classes - 1;
            }
            newCls[order[0]] = 0;
            cls = newCls;
            shift *= 2;
        }
        long[] result = new long[n - 1];
        for (int i = 1; i < n; i++) {
            result[i - 1] = order[i];
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(suffixArray("banana")));
    }
}
