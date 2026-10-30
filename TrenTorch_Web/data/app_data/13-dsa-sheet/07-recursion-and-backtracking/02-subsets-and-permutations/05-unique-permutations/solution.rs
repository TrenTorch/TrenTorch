// O(n! * n) time, O(n! * n) space for the output
fn unique_permutations(nums: Vec<i64>) -> Vec<Vec<i64>> {
    let mut a = nums;
    a.sort();
    let mut used: Vec<bool> = vec![false; a.len()];
    let mut out: Vec<Vec<i64>> = Vec::new();
    let mut current: Vec<i64> = Vec::new();
    unique_perm_go(&a, &mut used, &mut current, &mut out);
    out
}

fn unique_perm_go(a: &[i64], used: &mut Vec<bool>, current: &mut Vec<i64>, out: &mut Vec<Vec<i64>>) {
    if current.len() == a.len() {
        out.push(current.clone());
        return;
    }
    for j in 0..a.len() {
        if used[j] || (j > 0 && a[j] == a[j - 1] && !used[j - 1]) {
            continue;
        }
        used[j] = true;
        current.push(a[j]);
        unique_perm_go(a, used, current, out);
        current.pop();
        used[j] = false;
    }
}

fn main() {
    println!("{:?}", unique_permutations(vec![1, 1, 2]));
}
