import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Main {
    // O(n) time, O(n) space
    static String reverseWords(String s) {
        List<String> words = new ArrayList<>();
        int n = s.length();
        int i = 0;
        while (i < n) {
            while (i < n && s.charAt(i) == ' ') i++;
            if (i >= n) break;
            int j = i;
            while (j < n && s.charAt(j) != ' ') j++;
            words.add(s.substring(i, j));
            i = j;
        }
        Collections.reverse(words);
        return String.join(" ", words);
    }

    public static void main(String[] args) {
        System.out.println(reverseWords("the sky is blue"));
    }
}
