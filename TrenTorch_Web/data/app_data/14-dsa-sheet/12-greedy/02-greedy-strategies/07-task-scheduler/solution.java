public class Main {
    // O(n) time, O(1) space where n is the length of tasks
    static long leastInterval(String tasks, long n) {
        if (tasks == null || tasks.isEmpty()) {
            return 0;
        }
        int[] freq = new int[26];
        for (char c : tasks.toCharArray()) {
            freq[c - 'A']++;
        }
        int maxFreq = 0;
        for (int f : freq) {
            if (f > maxFreq) maxFreq = f;
        }
        int countMax = 0;
        for (int f : freq) {
            if (f == maxFreq) countMax++;
        }
        long result = Math.max(tasks.length(), (maxFreq - 1) * (n + 1) + countMax);
        return result;
    }

    public static void main(String[] args) {
        System.out.println(leastInterval("AAABBB", 2L));
    }
}
