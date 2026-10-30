// O(2^n * n) time, O(n) space
fn backtrack(candidates: &[i64], start: usize, remaining: i64, current: &mut Vec<i64>, out: &mut Vec<Vec<i64>>) {
    if remaining == 0 {
        out.push(current.clone());
        return;
    }
    for j in start..candidates.len() {
        if j > start && candidates[j] == candidates[j - 1] {
            continue;
        }
        if candidates[j] > remaining {
            break;
        }
        current.push(candidates[j]);
        backtrack(candidates, j + 1, remaining - candidates[j], current, out);
        current.pop();
    }
}

fn combination_sum_ii(candidates: Vec<i64>, target: i64) -> Vec<Vec<i64>> {
    let mut a = candidates;
    a.sort();
    let mut out = Vec::new();
    let mut current = Vec::new();
    backtrack(&a, 0, target, &mut current, &mut out);
    out
}

fn main() {
    println!("{:?}", combination_sum_ii(vec![10, 1, 2, 7, 6, 1, 5], 8));
}
