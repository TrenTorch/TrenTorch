// O(4^n * n) time, O(4^n * n) space for the output
fn letter_combinations(digits: String) -> Vec<String> {
    if digits.is_empty() {
        return Vec::new();
    }
    let chars: Vec<char> = digits.chars().collect();
    let mut out: Vec<String> = Vec::new();
    let mut prefix = String::new();
    letters_go(&chars, 0, &mut prefix, &mut out);
    out
}

fn key_letters(digit: char) -> &'static str {
    match digit {
        '2' => "abc",
        '3' => "def",
        '4' => "ghi",
        '5' => "jkl",
        '6' => "mno",
        '7' => "pqrs",
        '8' => "tuv",
        '9' => "wxyz",
        other => panic!("invalid keypad digit: {other}"),
    }
}

fn letters_go(digits: &[char], i: usize, prefix: &mut String, out: &mut Vec<String>) {
    if i == digits.len() {
        out.push(prefix.clone());
        return;
    }
    for letter in key_letters(digits[i]).chars() {
        prefix.push(letter);
        letters_go(digits, i + 1, prefix, out);
        prefix.pop();
    }
}

fn main() {
    println!("{:?}", letter_combinations(String::from("23")));
}
