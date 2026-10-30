// O(q log n) time, O(q) space
fn count_in_range(sorted_nums: Vec<i64>, queries: Vec<Vec<i64>>) -> Vec<i64> {
    let mut answers = Vec::with_capacity(queries.len());
    for q in queries {
        let lo = q[0];
        let hi = q[1];
        let left = sorted_nums.as_slice().partition_point(|&x| x < lo);
        let right = sorted_nums.as_slice().partition_point(|&x| x <= hi);
        answers.push((right - left) as i64);
    }
    answers
}

fn main() {
    println!("{:?}", count_in_range(vec![1, 3, 3, 5, 8], vec![vec![3, 5], vec![0, 0], vec![2, 9]]));
}
