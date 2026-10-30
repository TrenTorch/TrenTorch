// O(n * 2^n) time, O(n * 2^n) space for the output
fn subsets_with_duplicates(nums: Vec<i64>) -> Vec<Vec<i64>> {
    let mut a = nums;
    a.sort();
    let mut out: Vec<Vec<i64>> = Vec::new();
    let mut current: Vec<i64> = Vec::new();
    dup_subsets_go(&a, 0, &mut current, &mut out);
    out
}

fn dup_subsets_go(a: &[i64], start: usize, current: &mut Vec<i64>, out: &mut Vec<Vec<i64>>) {
    out.push(current.clone());
    for j in start..a.len() {
        if j > start && a[j] == a[j - 1] {
            continue;
        }
        current.push(a[j]);
        dup_subsets_go(a, j + 1, current, out);
        current.pop();
    }
}

fn main() {
    println!("{:?}", subsets_with_duplicates(vec![1, 2, 2]));
}
