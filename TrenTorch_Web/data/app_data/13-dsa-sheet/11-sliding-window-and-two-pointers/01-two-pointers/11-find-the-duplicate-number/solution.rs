// O(n) time, O(1) extra space (Floyd cycle detection, nums is not modified)
fn find_duplicate(nums: Vec<i64>) -> i64 {
    let at = |i: i64| nums[i as usize];
    let mut slow = nums[0];
    let mut fast = nums[0];
    loop {
        slow = at(slow);
        fast = at(at(fast));
        if slow == fast {
            break;
        }
    }
    slow = nums[0];
    while slow != fast {
        slow = at(slow);
        fast = at(fast);
    }
    slow
}

fn main() {
    println!("{:?}", find_duplicate(vec![1, 3, 4, 2, 2]));
}
