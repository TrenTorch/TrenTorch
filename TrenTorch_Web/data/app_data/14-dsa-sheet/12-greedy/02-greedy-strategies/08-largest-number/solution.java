import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n log n) time, O(n) space
    static String largestNumber(long[] nums) {
        if (nums == null || nums.length == 0) {
            return "0";
        }
        List<String> strings = new ArrayList<>(nums.length);
        for (long num : nums) {
            strings.add(String.valueOf(num));
        }
        strings.sort((a, b) -> (b + a).compareTo(a + b));
        if (strings.get(0).equals("0")) {
            return "0";
        }
        StringBuilder sb = new StringBuilder();
        for (String s : strings) {
            sb.append(s);
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        System.out.println(largestNumber(new long[]{10L, 2L}));
    }
}
