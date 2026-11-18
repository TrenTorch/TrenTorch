public class Main {
    // O(log n) time, O(1) space
    static boolean happyNumber(long n) {
        long slow = n;
        long fast = step(n);
        while (fast != 1 && slow != fast) {
            slow = step(slow);
            fast = step(step(fast));
        }
        return fast == 1;
    }

    static long step(long x) {
        long total = 0;
        while (x != 0) {
            long digit = x % 10;
            total += digit * digit;
            x /= 10;
        }
        return total;
    }

    public static void main(String[] args) {
        System.out.println(happyNumber(19L));
    }
}
