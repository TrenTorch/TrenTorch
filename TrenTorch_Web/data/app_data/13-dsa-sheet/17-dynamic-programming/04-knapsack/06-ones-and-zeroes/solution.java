public class Main {
    // O(len(strs) * m * n) time, O(m * n) space
    static long findMaxForm(String[] strs, long m, long n) {
        int maxZeros = (int) m;
        int maxOnes = (int) n;
        int[][] best = new int[maxZeros + 1][maxOnes + 1];
        for (String s : strs) {
            int zeros = 0;
            for (int i = 0; i < s.length(); i++) {
                if (s.charAt(i) == '0') {
                    zeros++;
                }
            }
            int ones = s.length() - zeros;
            for (int z = maxZeros; z >= zeros; z--) {
                int[] row = best[z];
                int[] source = best[z - zeros];
                for (int o = maxOnes; o >= ones; o--) {
                    if (source[o - ones] + 1 > row[o]) {
                        row[o] = source[o - ones] + 1;
                    }
                }
            }
        }
        return best[maxZeros][maxOnes];
    }

    public static void main(String[] args) {
        System.out.println(findMaxForm(new String[]{"10", "0001", "111001", "1", "0"}, 5L, 3L));
    }
}
