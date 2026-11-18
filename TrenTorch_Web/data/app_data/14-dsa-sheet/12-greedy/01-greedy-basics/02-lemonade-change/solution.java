public class Main {
    // O(n) time, O(1) space
    static boolean lemonadeChange(long[] bills) {
        long fives = 0;
        long tens = 0;
        for (long bill : bills) {
            if (bill == 5) {
                fives++;
            } else if (bill == 10) {
                if (fives == 0) {
                    return false;
                }
                fives--;
                tens++;
            } else {
                if (tens > 0 && fives > 0) {
                    tens--;
                    fives--;
                } else if (fives >= 3) {
                    fives -= 3;
                } else {
                    return false;
                }
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(lemonadeChange(new long[]{5L, 5L, 5L, 10L, 20L}));
    }
}
