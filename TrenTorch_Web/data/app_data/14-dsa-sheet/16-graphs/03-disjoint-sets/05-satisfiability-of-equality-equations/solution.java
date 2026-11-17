public class Main {
    // O(N) time, O(1) space
    static boolean equationsPossible(String[] equations) {
        int[] parent = new int[26];
        for (int i = 0; i < 26; i++) {
            parent[i] = i;
        }

        for (String eq : equations) {
            if (eq.charAt(1) == '=') {
                int a = eq.charAt(0) - 'a';
                int b = eq.charAt(3) - 'a';
                int rootA = find(parent, a);
                int rootB = find(parent, b);
                parent[rootA] = rootB;
            }
        }

        for (String eq : equations) {
            if (eq.charAt(1) == '!') {
                int a = eq.charAt(0) - 'a';
                int b = eq.charAt(3) - 'a';
                if (find(parent, a) == find(parent, b)) {
                    return false;
                }
            }
        }
        return true;
    }

    private static int find(int[] parent, int a) {
        while (parent[a] != a) {
            parent[a] = parent[parent[a]];
            a = parent[a];
        }
        return a;
    }

    public static void main(String[] args) {
        System.out.println(equationsPossible(new String[]{"a==b", "b!=a"}));
    }
}
