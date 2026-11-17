import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

public class Main {
    // O(n * k^2) time, O(n * k) space, where n = words.length, k = max word length
    static long[][] palindromePairs(String[] words) {
        Map<String, List<Integer>> index = new HashMap<>();
        for (int i = 0; i < words.length; i++) {
            index.computeIfAbsent(words[i], k -> new ArrayList<>()).add(i);
        }

        Set<Pair> found = new TreeSet<>();

        for (int i = 0; i < words.length; i++) {
            String w = words[i];
            for (int cut = 0; cut <= w.length(); cut++) {
                String prefix = w.substring(0, cut);
                String suffix = w.substring(cut);

                if (isPalindrome(prefix)) {
                    String revSuffix = new StringBuilder(suffix).reverse().toString();
                    List<Integer> candidates = index.get(revSuffix);
                    if (candidates != null) {
                        for (int j : candidates) {
                            if (j != i) {
                                found.add(new Pair(j, i));
                            }
                        }
                    }
                }

                if (isPalindrome(suffix)) {
                    String revPrefix = new StringBuilder(prefix).reverse().toString();
                    List<Integer> candidates = index.get(revPrefix);
                    if (candidates != null) {
                        for (int j : candidates) {
                            if (j != i) {
                                found.add(new Pair(i, j));
                            }
                        }
                    }
                }
            }
        }

        long[][] result = new long[found.size()][2];
        int idx = 0;
        for (Pair p : found) {
            result[idx][0] = p.i;
            result[idx][1] = p.j;
            idx++;
        }
        return result;
    }

    private static boolean isPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            if (s.charAt(left++) != s.charAt(right--)) return false;
        }
        return true;
    }

    static class Pair implements Comparable<Pair> {
        long i, j;

        Pair(long i, long j) {
            this.i = i;
            this.j = j;
        }

        @Override
        public int compareTo(Pair other) {
            if (this.i != other.i) return Long.compare(this.i, other.i);
            return Long.compare(this.j, other.j);
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Pair)) return false;
            Pair other = (Pair) o;
            return i == other.i && j == other.j;
        }

        @Override
        public int hashCode() {
            return Long.hashCode(i * 31 + j);
        }
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(palindromePairs(new String[]{"abcd", "dcba", "lls", "s", "sssll"})));
    }
}
