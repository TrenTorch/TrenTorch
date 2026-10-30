import java.util.*;

public class Main {
    // O(log n) time, O(1) space
    static long countSquareLoop(long n) {
        long r = (long) Math.sqrt((double) n);
        while ((r + 1) > 0 && (r + 1) * (r + 1) <= n) {
            r++;
        }
        while (r * r > n) {
            r--;
        }
        return r;
    }

    public static void main(String[] args) {
        System.out.println(countSquareLoop(10L));
    }
}
