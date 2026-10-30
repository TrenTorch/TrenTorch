// Exponential time, O(target) space
fn combination_sum(candidates: Vec<i64>, target: i64) -> Vec<Vec<i64>> {
    let mut a = candidates;
    a.sort_unstable();
    let mut out = Vec::new();
    let mut current = Vec::new();
    backtrack(&a, 0, target, &mut current, &mut out);
    out
}

fn backtrack(candidates: &[i64], start: usize, remaining: i64, current: &mut Vec<i64>, out: &mut Vec<Vec<i64>>) {
    if remaining == 0 {
        out.push(current.clone());
        return;
    }
    for j in start..candidates.len() {
        let val = candidates[j];
        if val > remaining {
            break;
        }
        current.push(val);
        backtrack(candidates, j, remaining - val, current, out);
        current.pop();
    }
}

fn main() {
    println!("{:?}", combination_sum(vec![2, 3, 6, 7], 7));
}
