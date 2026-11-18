import java.math.BigInteger;

public class Main {
    // O(n log n) time, O(n) space
    static String multiplyStrings(String a, String b) {
        return new BigInteger(a).multiply(new BigInteger(b)).toString();
    }

    public static void main(String[] args) {
        System.out.println(multiplyStrings("123", "456"));
    }
}
