public class Main {
    // O(n) time, O(n) space
    static long[] minStack(String[] ops) {
        long[] values = new long[ops.length];
        long[] mins = new long[ops.length];
        long[] out = new long[ops.length];
        int size = 0;
        int outCount = 0;
        for (String op : ops) {
            if (op.startsWith("push")) {
                long x = Long.parseLong(op.trim().split("\\s+")[1]);
                values[size] = x;
                mins[size] = size > 0 ? Math.min(x, mins[size - 1]) : x;
                size++;
            } else if (op.equals("pop")) {
                size--;
            } else if (op.equals("top")) {
                out[outCount++] = values[size - 1];
            } else {
                out[outCount++] = mins[size - 1];
            }
        }
        return java.util.Arrays.copyOf(out, outCount);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(minStack(new String[]{"push 5", "push 3", "get_min", "pop", "top", "get_min"})));
    }
}
