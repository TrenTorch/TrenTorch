// O(n) time, O(n) space
fn daily_temperatures(temps: Vec<i64>) -> Vec<i64> {
    let n = temps.len();
    let mut out: Vec<i64> = vec![0; n];
    let mut stack: Vec<usize> = Vec::new();
    for i in 0..n {
        let t = temps[i];
        while !stack.is_empty() {
            let j = *stack.last().unwrap();
            if temps[j] < t {
                stack.pop();
                out[j] = (i - j) as i64;
            } else {
                break;
            }
        }
        stack.push(i);
    }
    out
}

fn main() {
    println!("{:?}", daily_temperatures(vec![73, 74, 75, 71, 69, 72, 76, 73]));
}
