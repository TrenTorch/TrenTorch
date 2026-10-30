public class Main {
    // O(n + m) time, O(1) space
    static boolean ransomNote(String note, String magazine) {
        int[] counts = new int[26];
        for (char c : magazine.toCharArray()) {
            counts[c - 'a']++;
        }
        for (char c : note.toCharArray()) {
            if (counts[c - 'a'] == 0) {
                return false;
            }
            counts[c - 'a']--;
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(ransomNote("aab", "baa"));
    }
}
