// O(n) time, O(1) space
fn rob(nums: Vec<i64>) -> i64 {
    let mut skip: i64 = 0;
    let mut take: i64 = 0;
    for x in nums {
        let new_skip = skip.max(take);
        let new_take = skip + x;
        skip = new_skip;
        take = new_take;
    }
    skip.max(take)
}

fn main() {
    println!("{:?}", rob(vec![1, 2, 3, 1]));
}
