public class Main {
    // O(n) time, O(1) space (fixed 65536-entry table for char codes)
    static long firstUniqueCharacter(String s) {
        int[] counts = new int[65536];
        for (int i = 0; i < s.length(); i++) {
            counts[s.charAt(i)]++;
        }
        for (int i = 0; i < s.length(); i++) {
            if (counts[s.charAt(i)] == 1) {
                return i;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        System.out.println(firstUniqueCharacter("leetcode"));
    }
}
