import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Main {
    // O(q log s) time for q operations (s = changes per index), O(total sets) space
    static long[] runSnapshotArray(long length, String[] ops) {
        HashMap<Integer, List<Integer>> ids = new HashMap<>();
        HashMap<Integer, List<Long>> vals = new HashMap<>();
        int snapId = 0;
        List<Long> out = new ArrayList<>();
        for (String op : ops) {
            String[] parts = op.trim().split("\\s+");
            if (parts[0].equals("set")) {
                int i = Integer.parseInt(parts[1]);
                long v = Long.parseLong(parts[2]);
                List<Integer> idList = ids.get(i);
                if (idList != null && idList.get(idList.size() - 1) == snapId) {
                    vals.get(i).set(vals.get(i).size() - 1, v);
                } else {
                    ids.computeIfAbsent(i, k -> new ArrayList<>()).add(snapId);
                    vals.computeIfAbsent(i, k -> new ArrayList<>()).add(v);
                }
            } else if (parts[0].equals("snap")) {
                out.add((long) snapId);
                snapId++;
            } else {
                int i = Integer.parseInt(parts[1]);
                int want = Integer.parseInt(parts[2]);
                List<Integer> idList = ids.getOrDefault(i, new ArrayList<>());
                // bisect_right: number of change ids <= want
                int lo = 0;
                int hi = idList.size();
                while (lo < hi) {
                    int mid = (lo + hi) >>> 1;
                    if (idList.get(mid) <= want) {
                        lo = mid + 1;
                    } else {
                        hi = mid;
                    }
                }
                int k = lo - 1;
                out.add(k >= 0 ? vals.get(i).get(k) : 0L);
            }
        }
        long[] result = new long[out.size()];
        for (int i = 0; i < result.length; i++) {
            result[i] = out.get(i);
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runSnapshotArray(3L, new String[]{"set 0 5", "snap", "set 0 6", "get 0 0", "snap", "get 0 1"})));
    }
}
