// O(n log n) time, O(n) space
fn length_of_lis(nums: Vec<i64>) -> i64 {
    let mut tails: Vec<i64> = Vec::new();
    for x in nums {
        // bisect_left: first index whose tail is not less than x
        let i = tails.partition_point(|&t| t < x);
        if i == tails.len() {
            tails.push(x);
        } else {
            tails[i] = x;
        }
    }
    tails.len() as i64
}

fn main() {
    println!("{:?}", length_of_lis(vec![10, 9, 2, 5, 3, 7, 101, 18]));
}
