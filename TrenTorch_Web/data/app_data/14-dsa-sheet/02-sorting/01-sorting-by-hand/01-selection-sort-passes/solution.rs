// O(n^2) time, O(n^2) space
fn selection_sort_passes(nums: Vec<i64>) -> Vec<Vec<i64>> {
    let mut a = nums.clone();
    let n = a.len();
    let mut passes: Vec<Vec<i64>> = Vec::new();
    if n < 2 {
        return passes;
    }
    for i in 0..n - 1 {
        let mut smallest = i;
        for j in i + 1..n {
            if a[j] < a[smallest] {
                smallest = j;
            }
        }
        a.swap(i, smallest);
        passes.push(a.clone());
    }
    passes
}

fn main() {
    println!("{:?}", selection_sort_passes(vec![64, 25, 12, 22, 11]));
}
