// O(n * 2^n) time, O(n * 2^n) space for the output
fn all_subsets(nums: Vec<i64>) -> Vec<Vec<i64>> {
    let mut a = nums;
    a.sort();
    let mut out: Vec<Vec<i64>> = Vec::new();
    let mut current: Vec<i64> = Vec::new();
    subsets_go(&a, 0, &mut current, &mut out);
    out
}

fn subsets_go(a: &[i64], start: usize, current: &mut Vec<i64>, out: &mut Vec<Vec<i64>>) {
    out.push(current.clone());
    for j in start..a.len() {
        current.push(a[j]);
        subsets_go(a, j + 1, current, out);
        current.pop();
    }
}

fn main() {
    println!("{:?}", all_subsets(vec![1, 2, 3]));
}
