import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Main {
    // O(q log m) time for q operations (m = values per key), O(total sets) space
    static String[] runTimeMap(String[] ops) {
        HashMap<String, List<Long>> times = new HashMap<>();
        HashMap<String, List<String>> values = new HashMap<>();
        List<String> out = new ArrayList<>();
        for (String op : ops) {
            String[] parts = op.trim().split("\\s+");
            if (parts[0].equals("set")) {
                String key = parts[1];
                times.computeIfAbsent(key, k -> new ArrayList<>()).add(Long.parseLong(parts[3]));
                values.computeIfAbsent(key, k -> new ArrayList<>()).add(parts[2]);
            } else {
                String key = parts[1];
                long t = Long.parseLong(parts[2]);
                List<Long> ts = times.getOrDefault(key, new ArrayList<>());
                // bisect_right: number of stored times <= t
                int lo = 0;
                int hi = ts.size();
                while (lo < hi) {
                    int mid = (lo + hi) >>> 1;
                    if (ts.get(mid) <= t) {
                        lo = mid + 1;
                    } else {
                        hi = mid;
                    }
                }
                out.add(lo > 0 ? values.get(key).get(lo - 1) : "");
            }
        }
        return out.toArray(new String[0]);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runTimeMap(new String[]{"set love high 10", "get love 10", "get love 15", "set love low 20", "get love 15", "get love 25", "get love 5"})));
    }
}
