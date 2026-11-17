public class Main {
    // O(eggs * answer) time, O(eggs) space
    static long eggDrop(long eggs, long floors) {
        if (floors == 0 || eggs == 0) {
            return 0;
        }
        int maxEggs = (int) eggs;
        long[] reach = new long[maxEggs + 1];
        long drops = 0;
        while (reach[maxEggs] < floors) {
            drops++;
            for (int e = maxEggs; e >= 1; e--) {
                reach[e] = reach[e - 1] + reach[e] + 1;
            }
        }
        return drops;
    }

    public static void main(String[] args) {
        System.out.println(eggDrop(2L, 6L));
    }
}
