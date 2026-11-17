public class Main {
    // O(n) time, O(n) space
    static long[] asteroidCollision(long[] asteroids) {
        long[] stack = new long[asteroids.length];
        int top = 0;
        for (long a : asteroids) {
            boolean alive = true;
            while (alive && a < 0 && top > 0 && stack[top - 1] > 0) {
                if (stack[top - 1] < -a) {
                    top--;
                } else if (stack[top - 1] == -a) {
                    top--;
                    alive = false;
                } else {
                    alive = false;
                }
            }
            if (alive) {
                stack[top++] = a;
            }
        }
        return java.util.Arrays.copyOf(stack, top);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(asteroidCollision(new long[]{5L, 10L, -5L})));
    }
}
