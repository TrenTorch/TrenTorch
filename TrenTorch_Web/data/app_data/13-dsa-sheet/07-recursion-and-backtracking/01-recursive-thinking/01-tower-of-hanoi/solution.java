import java.util.ArrayList;
import java.util.List;
import java.util.Arrays;

public class Main {
    // O(2^n) time, O(2^n) space
    static long[][] towerOfHanoi(long n) {
        List<long[]> moves = new ArrayList<>();
        move((int) n, 1, 3, 2, moves);
        return moves.toArray(new long[0][]);
    }

    private static void move(int k, int source, int target, int spare, List<long[]> moves) {
        if (k == 0) return;
        move(k - 1, source, spare, target, moves);
        moves.add(new long[]{source, target});
        move(k - 1, spare, target, source, moves);
    }

    public static void main(String[] args) {
        System.out.println(java.util.Arrays.deepToString(towerOfHanoi(2L)));
    }
}
