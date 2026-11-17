import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;

public class Main {
    // O(q) time for q operations, O(capacity) space
    static long[] runLru(long capacity, String[] ops) {
        LinkedHashMap<Long, Long> cache = new LinkedHashMap<>(16, 0.75f, true);
        List<Long> out = new ArrayList<>();
        for (String op : ops) {
            String[] parts = op.trim().split("\\s+");
            if (parts[0].equals("get")) {
                long key = Long.parseLong(parts[1]);
                Long value = cache.get(key);
                out.add(value == null ? -1L : value);
            } else if (capacity > 0) {
                long key = Long.parseLong(parts[1]);
                long value = Long.parseLong(parts[2]);
                if (!cache.containsKey(key) && cache.size() == capacity) {
                    Iterator<Long> it = cache.keySet().iterator();
                    it.next();
                    it.remove();
                }
                cache.put(key, value);
            }
        }
        long[] result = new long[out.size()];
        for (int i = 0; i < result.length; i++) {
            result[i] = out.get(i);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runLru(2L, new String[]{"put 1 1", "put 2 2", "get 1", "put 3 3", "get 2", "put 4 4", "get 1", "get 3", "get 4"})));
    }
}
