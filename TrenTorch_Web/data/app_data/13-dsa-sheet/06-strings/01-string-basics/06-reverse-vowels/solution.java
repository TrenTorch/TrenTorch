import java.util.ArrayList;
import java.util.List;

public class Main {
    // O(n) time, O(n) space
    static String reverseVowels(String s) {
        List<Character> vowels = new ArrayList<>();
        for (char c : s.toCharArray()) {
            if (isVowel(c)) {
                vowels.add(c);
            }
        }
        char[] arr = s.toCharArray();
        int idx = vowels.size() - 1;
        for (int i = 0; i < arr.length; i++) {
            if (isVowel(arr[i])) {
                arr[i] = vowels.get(idx--);
            }
        }
        return new String(arr);
    }

    private static boolean isVowel(char c) {
        return "aeiouAEIOU".indexOf(c) >= 0;
    }

    public static void main(String[] args) {
        System.out.println(reverseVowels("hello"));
    }
}
