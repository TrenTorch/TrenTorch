// O(n) time, O(1) space
fn next_permutation(nums: Vec<i64>) -> Vec<i64> {
    let mut a = nums;
    if a.len() <= 1 {
        return a;
    }
    let mut i = a.len() as isize - 2;
    while i >= 0 && a[i as usize] >= a[i as usize + 1] {
        i -= 1;
    }
    if i >= 0 {
        let mut j = a.len() as isize - 1;
        while a[j as usize] <= a[i as usize] {
            j -= 1;
        }
        a.swap(i as usize, j as usize);
    }
    let start = (i + 1) as usize;
    a[start..].reverse();
    a
}

fn main() {
    println!("{:?}", next_permutation(vec![1, 2, 3]));
}
