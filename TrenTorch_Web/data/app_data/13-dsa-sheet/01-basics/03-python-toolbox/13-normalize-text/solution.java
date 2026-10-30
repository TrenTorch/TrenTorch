import java.util.Locale;

public class Main {
    // O(n) time, O(n) space
    static String normalizeText(String s) {
        return s.toLowerCase(Locale.ROOT).replaceAll("[^a-z0-9]+", " ").trim();
    }

    public static void main(String[] args) {
        System.out.println(normalizeText("  Hello,   World!! 42 "));
    }
}
