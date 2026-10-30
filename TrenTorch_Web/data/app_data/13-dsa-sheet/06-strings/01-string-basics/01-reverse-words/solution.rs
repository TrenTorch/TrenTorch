// O(n) time, O(n) space
fn reverse_words(s: String) -> String {
    s.split_whitespace().rev().collect::<Vec<&str>>().join(" ")
}

fn main() {
    println!("{:?}", reverse_words(String::from("the sky is blue")));
}
