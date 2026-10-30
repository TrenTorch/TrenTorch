// O(C(n,k) * k) time, O(k) auxiliary space (excluding output)
fn all_combinations(n: i64, k: i64) -> Vec<Vec<i64>> {
    fn go(start: i64, n: i64, k: i64, current: &mut Vec<i64>, out: &mut Vec<Vec<i64>>) {
        let need = k - current.len() as i64;
        if need == 0 {
            out.push(current.clone());
            return;
        }
        // j runs from start to n - need + 1 inclusive
        let max_j = n - need + 1;
        let mut j = start;
        while j <= max_j {
            current.push(j);
            go(j + 1, n, k, current, out);
            current.pop();
            j += 1;
        }
    }

    let mut out: Vec<Vec<i64>> = Vec::new();
    let mut current: Vec<i64> = Vec::new();
    go(1, n, k, &mut current, &mut out);
    out
}

fn main() {
    println!("{:?}", all_combinations(4, 2));
}
