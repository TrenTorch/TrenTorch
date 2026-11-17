public class Main {
    // O(n) time, O(n) space
    static String simplifyPath(String path) {
        java.util.ArrayList<String> stack = new java.util.ArrayList<>();
        for (String name : path.split("/")) {
            if (name.equals("..")) {
                if (!stack.isEmpty()) {
                    stack.remove(stack.size() - 1);
                }
            } else if (!name.isEmpty() && !name.equals(".")) {
                stack.add(name);
            }
        }
        return "/" + String.join("/", stack);
    }

    public static void main(String[] args) {
        System.out.println(simplifyPath("/home/"));
    }
}
