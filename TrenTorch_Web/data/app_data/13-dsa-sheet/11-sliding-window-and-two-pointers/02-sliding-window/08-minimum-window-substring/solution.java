public class Main {
    // O(n + m) time, O(1) space
    static String minWindow(String s, String t) {
        if (t.isEmpty()) {
            return "";
        }
        int[] need = new int[128];
        for (char c : t.toCharArray()) {
            need[c]++;
        }
        int missing = 0;
        for (int count : need) {
            if (count > 0) missing++;
        }
        int[] have = new int[128];
        int bestStart = 0;
        int bestLen = s.length() + 1;
        int left = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            have[c]++;
            if (need[c] > 0 && have[c] == need[c]) {
                missing--;
            }
            while (missing == 0) {
                if (right - left + 1 < bestLen) {
                    bestStart = left;
                    bestLen = right - left + 1;
                }
                char gone = s.charAt(left);
                have[gone]--;
                if (need[gone] > 0 && have[gone] < need[gone]) {
                    missing++;
                }
                left++;
            }
        }
        return bestLen <= s.length() ? s.substring(bestStart, bestStart + bestLen) : "";
    }

    public static void main(String[] args) {
        System.out.println(minWindow("ADOBECODEBANC", "ABC"));
    }
}
