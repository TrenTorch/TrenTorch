// O(n) time, O(1) space
fn rob_circle(nums: Vec<i64>) -> i64 {
    if nums.is_empty() {
        return 0;
    }
    if nums.len() == 1 {
        return nums[0];
    }

    fn line(houses: &[i64]) -> i64 {
        let mut skip = 0;
        let mut take = 0;
        for &x in houses {
            let new_skip = skip.max(take);
            let new_take = skip + x;
            skip = new_skip;
            take = new_take;
        }
        skip.max(take)
    }

    line(&nums[1..]).max(line(&nums[..nums.len() - 1]))
}

fn main() {
    println!("{:?}", rob_circle(vec![2, 3, 2]));
}
