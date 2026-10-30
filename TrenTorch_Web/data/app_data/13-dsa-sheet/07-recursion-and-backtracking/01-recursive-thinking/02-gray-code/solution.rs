// O(2^n) time, O(2^n) space
fn gray_code(n: i64) -> Vec<i64> {
    let mut result = Vec::new();
    if n < 0 {
        return result;
    }
    let count = 1usize << n as usize;
    result.reserve(count);
    for i in 0..count {
        let v = i as i64;
        result.push(v ^ (v >> 1));
    }
    result
}

fn main() {
    println!("{:?}", gray_code(2));
}
