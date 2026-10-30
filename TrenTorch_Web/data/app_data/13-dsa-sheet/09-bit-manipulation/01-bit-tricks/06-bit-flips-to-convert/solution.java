public class Main {
    // O(number of set bits) time, O(1) space
    static long bitFlipsToConvert(long a, long b) {
        long diff = a ^ b;
        long count = 0;
        while (diff != 0) {
            diff &= diff - 1;
            count++;
        }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(bitFlipsToConvert(10L, 7L));
    }
}
