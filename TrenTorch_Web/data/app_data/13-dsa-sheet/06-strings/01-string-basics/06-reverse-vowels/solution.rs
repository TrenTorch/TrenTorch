// O(n) time, O(n) space
fn reverse_vowels(s: String) -> String {
    fn is_vowel(c: char) -> bool {
        matches!(c,
            'a' | 'e' | 'i' | 'o' | 'u' |
            'A' | 'E' | 'I' | 'O' | 'U')
    }

    let vowels: Vec<char> = s.chars().filter(|&c| is_vowel(c)).collect();
    let mut rev_iter = vowels.iter().rev();
    let mut result = String::with_capacity(s.len());
    for ch in s.chars() {
        if is_vowel(ch) {
            result.push(*rev_iter.next().unwrap());
        } else {
            result.push(ch);
        }
    }
    result
}

fn main() {
    println!("{:?}", reverse_vowels(String::from("hello")));
}
