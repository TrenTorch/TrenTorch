public class Main {
    // O(1) time, O(1) space
    static long lowestSetBit(long n) {
        return n & -n;
    }

    public static void main(String[] args) {
        System.out.println(lowestSetBit(12L));
    }
}
