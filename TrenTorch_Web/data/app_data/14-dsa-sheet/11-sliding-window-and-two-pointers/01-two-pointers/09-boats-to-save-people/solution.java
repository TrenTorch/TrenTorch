public class Main {
    // O(n log n) time (sort), O(n) space for the sorted copy
    static long boatsNeeded(long[] people, long limit) {
        long[] a = people.clone();
        java.util.Arrays.sort(a);
        int light = 0;
        int heavy = a.length - 1;
        long boats = 0;
        while (light <= heavy) {
            if (a[light] + a[heavy] <= limit) {
                light++;
            }
            heavy--;
            boats++;
        }
        return boats;
    }

    public static void main(String[] args) {
        System.out.println(boatsNeeded(new long[]{3L, 2L, 2L, 1L}, 3L));
    }
}
