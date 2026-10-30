import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n) time, O(n) space
    public static List<Object> partitionArray(int[] nums) {
        int[] a = nums.clone();
        int pivot = a[a.length - 1];
        int i = -1;
        for (int j = 0; j < a.length - 1; j++) {
            if (a[j] <= pivot) {
                i++;
                int temp = a[i];
                a[i] = a[j];
                a[j] = temp;
            }
        }
        int temp = a[i + 1];
        a[i + 1] = a[a.length - 1];
        a[a.length - 1] = temp;
        List<Object> result = new ArrayList<>();
        result.add(a);
        result.add(i + 1);
        return result;
    }

    public static void main(String[] args) {
    }
}
