public class Main {
    // O(n) time, O(n) space
    static String firstNonRepeatingStream(String s) {
        java.util.HashMap<Character, Integer> counts = new java.util.HashMap<>();
        java.util.ArrayDeque<Character> queue = new java.util.ArrayDeque<>();
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            int c = counts.merge(ch, 1, Integer::sum);
            if (c == 1) {
                queue.addLast(ch);
            }
            while (!queue.isEmpty() && counts.get(queue.peekFirst()) > 1) {
                queue.pollFirst();
            }
            out.append(queue.isEmpty() ? '#' : queue.peekFirst().charValue());
        }
        return out.toString();
    }

    public static void main(String[] args) {
        System.out.println(firstNonRepeatingStream("aabc"));
    }
}
