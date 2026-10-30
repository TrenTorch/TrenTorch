// O(n! * n) time, O(n! * n) space for the output
fn all_permutations(nums: Vec<i64>) -> Vec<Vec<i64>> {
    let mut a = nums;
    a.sort();
    let mut used: Vec<bool> = vec![false; a.len()];
    let mut out: Vec<Vec<i64>> = Vec::new();
    let mut current: Vec<i64> = Vec::new();
    permutations_go(&a, &mut used, &mut current, &mut out);
    out
}

fn permutations_go(a: &[i64], used: &mut Vec<bool>, current: &mut Vec<i64>, out: &mut Vec<Vec<i64>>) {
    if current.len() == a.len() {
        out.push(current.clone());
        return;
    }
    for j in 0..a.len() {
        if used[j] {
            continue;
        }
        used[j] = true;
        current.push(a[j]);
        permutations_go(a, used, current, out);
        current.pop();
        used[j] = false;
    }
}

fn main() {
    println!("{:?}", all_permutations(vec![1, 2, 3]));
}
