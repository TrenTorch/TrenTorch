fn monotone_increasing_digits(n: i64) -> i64 {
    // O(log n) time, O(log n) space
    let mut digits: Vec<char> = n.to_string().chars().collect();
    let mut mark = digits.len();
    for i in (1..digits.len()).rev() {
        if digits[i - 1] > digits[i] {
            let d = digits[i - 1].to_digit(10).unwrap() - 1;
            digits[i - 1] = char::from_digit(d, 10).unwrap();
            mark = i;
        }
    }
    for i in mark..digits.len() {
        digits[i] = '9';
    }
    digits.iter().collect::<String>().parse().unwrap()
}

fn main() {
    println!("{:?}", monotone_increasing_digits(332));
}
