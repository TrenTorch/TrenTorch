public class Main {
    // O(n) time, O(n) space
    static long nthUglyNumber(long n) {
        int N = (int) n;
        long[] ugly = new long[N];
        ugly[0] = 1;
        int i2 = 0, i3 = 0, i5 = 0;
        for (int i = 1; i < N; i++) {
            long next2 = ugly[i2] * 2;
            long next3 = ugly[i3] * 3;
            long next5 = ugly[i5] * 5;
            long next = Math.min(next2, Math.min(next3, next5));
            ugly[i] = next;
            if (next == next2) i2++;
            if (next == next3) i3++;
            if (next == next5) i5++;
        }
        return ugly[N - 1];
    }

    public static void main(String[] args) {
        System.out.println(nthUglyNumber(10L));
    }
}
