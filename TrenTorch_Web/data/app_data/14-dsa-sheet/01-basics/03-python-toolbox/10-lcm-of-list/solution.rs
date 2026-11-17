// O(n log M) time, O(1) extra space where M is the maximum number
fn gcd(mut a: i64, mut b: i64) -> i64 {
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a.abs()
}

fn lcm(a: i64, b: i64) -> i64 {
    if a == 0 || b == 0 {
        return 0;
    }
    let g = gcd(a, b);
    // Use i128 to avoid overflow during multiplication
    let result = (a as i128 / g as i128) * b as i128;
    result as i64
}

fn lcm_of_list(nums: Vec<i64>) -> i64 {
    let mut result: i64 = 1;
    for n in nums {
        result = lcm(result, n);
    }
    result
}

fn main() {
    println!("{:?}", lcm_of_list(vec![4, 6, 10]));
}
