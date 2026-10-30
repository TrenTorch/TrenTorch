// O(n) time, O(1) space
fn min_cost_climbing(cost: Vec<i64>) -> i64 {
    let mut prev2 = 0i64;
    let mut prev1 = 0i64;
    for i in 2..=cost.len() {
        let new_prev1 = std::cmp::min(prev1 + cost[i - 1], prev2 + cost[i - 2]);
        prev2 = prev1;
        prev1 = new_prev1;
    }
    prev1
}

fn main() {
    println!("{:?}", min_cost_climbing(vec![10, 15, 20]));
}
