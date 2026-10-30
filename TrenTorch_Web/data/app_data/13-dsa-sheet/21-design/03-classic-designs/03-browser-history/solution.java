import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(q + total visited pages) time, O(history length) space
    static String[] runBrowserHistory(String homepage, String[] ops) {
        List<String> history = new ArrayList<>();
        history.add(homepage);
        int index = 0;
        List<String> out = new ArrayList<>();
        for (String op : ops) {
            String[] parts = op.trim().split("\\s+");
            String kind = parts[0];
            String arg = parts[1];
            if (kind.equals("visit")) {
                history.subList(index + 1, history.size()).clear();
                history.add(arg);
                index++;
            } else if (kind.equals("back")) {
                index = Math.max(0, index - Integer.parseInt(arg));
                out.add(history.get(index));
            } else {
                index = Math.min(history.size() - 1, index + Integer.parseInt(arg));
                out.add(history.get(index));
            }
        }
        return out.toArray(new String[0]);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.toString(runBrowserHistory("a", new String[]{"visit b", "visit c", "back 1", "back 5", "forward 1", "visit d", "forward 3"})));
    }
}
