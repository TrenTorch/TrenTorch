import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;

public class Main {
    // O(q) time for q operations, O(capacity) space
    static long[] runLfu(long capacity, String[] ops) {
        Map<Long, Long> value = new HashMap<>();
        Map<Long, Long> count = new HashMap<>();
        Map<Long, LinkedHashSet<Long>> groups = new HashMap<>();
        long low = 0;
        List<Long> out = new ArrayList<>();

        for (String op : ops) {
            String[] parts = op.trim().split("\\s+");
            long key = Long.parseLong(parts[1]);
            if (parts[0].equals("get")) {
                if (value.containsKey(key)) {
                    // touch(key)
                    long c = count.get(key);
                    groups.get(c).remove(key);
                    if (groups.get(c).isEmpty()) {
                        groups.remove(c);
                        if (low == c) {
                            low++;
                        }
                    }
                    count.put(key, c + 1);
                    groups.computeIfAbsent(c + 1, k -> new LinkedHashSet<>()).add(key);
                    out.add(value.get(key));
                } else {
                    out.add(-1L);
                }
            } else if (capacity > 0) {
                long v = Long.parseLong(parts[2]);
                if (value.containsKey(key)) {
                    value.put(key, v);
                    // touch(key)
                    long c = count.get(key);
                    groups.get(c).remove(key);
                    if (groups.get(c).isEmpty()) {
                        groups.remove(c);
                        if (low == c) {
                            low++;
                        }
                    }
                    count.put(key, c + 1);
                    groups.computeIfAbsent(c + 1, k -> new LinkedHashSet<>()).add(key);
                } else {
                    if (value.size() == capacity) {
                        LinkedHashSet<Long> lowest = groups.get(low);
                        Iterator<Long> it = lowest.iterator();
                        long oldest = it.next();
                        it.remove();
                        if (lowest.isEmpty()) {
                            groups.remove(low);
                        }
                        value.remove(oldest);
                        count.remove(oldest);
                    }
                    value.put(key, v);
                    count.put(key, 1L);
                    groups.computeIfAbsent(1L, k -> new LinkedHashSet<>()).add(key);
                    low = 1;
                }
            }
        }

        long[] result = new long[out.size()];
        for (int i = 0; i < result.length; i++) {
            result[i] = out.get(i);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runLfu(2L, new String[]{"put 1 1", "put 2 2", "get 1", "put 3 3", "get 2", "get 3", "put 4 4", "get 1", "get 3", "get 4"})));
    }
}
