// O(n) time, O(1) extra space (in place on the owned vector)
fn keep_at_most_twice(nums: Vec<i64>) -> Vec<i64> {
    let mut a = nums;
    let mut write: usize = 0;
    for read in 0..a.len() {
        if write < 2 || a[read] != a[write - 2] {
            a[write] = a[read];
            write += 1;
        }
    }
    a.truncate(write);
    a
}

fn main() {
    println!("{:?}", keep_at_most_twice(vec![1, 1, 1, 2, 2, 3]));
}
