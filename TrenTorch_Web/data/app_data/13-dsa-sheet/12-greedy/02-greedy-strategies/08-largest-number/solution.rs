// O(n log n) time, O(n) space
fn largest_number(nums: Vec<i64>) -> String {
    let mut strings: Vec<String> = nums.iter().map(|x| x.to_string()).collect();
    strings.sort_by(|a, b| {
        let ab = a.to_owned() + b;
        let ba = b.to_owned() + a;
        ba.cmp(&ab)
    });
    let result = strings.join("");
    if result.is_empty() || result.starts_with('0') {
        "0".to_string()
    } else {
        result
    }
}

fn main() {
    println!("{:?}", largest_number(vec![10, 2]));
}
