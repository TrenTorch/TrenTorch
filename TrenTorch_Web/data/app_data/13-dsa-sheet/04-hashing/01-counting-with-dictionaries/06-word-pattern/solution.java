import java.util.HashMap;
import java.util.Map;

public class Main {
    // O(n) time, O(n) space
    static boolean wordPattern(String pattern, String[] words) {
        if (pattern.length() != words.length) {
            return false;
        }
        Map<Character, String> letterToWord = new HashMap<>();
        Map<String, Character> wordToLetter = new HashMap<>();
        for (int i = 0; i < words.length; i++) {
            char letter = pattern.charAt(i);
            String word = words[i];
            String mappedWord = letterToWord.putIfAbsent(letter, word);
            if (mappedWord != null && !mappedWord.equals(word)) {
                return false;
            }
            Character mappedLetter = wordToLetter.putIfAbsent(word, letter);
            if (mappedLetter != null && mappedLetter.charValue() != letter) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(wordPattern("abba", new String[]{"dog", "cat", "cat", "dog"}));
    }
}
