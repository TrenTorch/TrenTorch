// O(n log n) time, O(n) space
fn count_reverse_pairs(nums: Vec<i64>) -> i64 {
    fn sort(a: Vec<i64>) -> (Vec<i64>, i64) {
        if a.len() <= 1 {
            return (a, 0);
        }
        let mid = a.len() / 2;
        let (left, x) = sort(a[..mid].to_vec());
        let (right, y) = sort(a[mid..].to_vec());

        let mut count = x + y;
        let mut j = 0usize;
        for &v in &left {
            while j < right.len() && v > 2 * right[j] {
                j += 1;
            }
            count += j as i64;
        }

        // merge left and right into a sorted vector
        let mut merged = Vec::with_capacity(left.len() + right.len());
        let (mut i, mut k) = (0usize, 0usize);
        while i < left.len() && k < right.len() {
            if left[i] <= right[k] {
                merged.push(left[i]);
                i += 1;
            } else {
                merged.push(right[k]);
                k += 1;
            }
        }
        if i < left.len() {
            merged.extend_from_slice(&left[i..]);
        }
        if k < right.len() {
            merged.extend_from_slice(&right[k..]);
        }

        (merged, count)
    }

    sort(nums).1
}

fn main() {
    println!("{:?}", count_reverse_pairs(vec![1, 3, 2, 3, 1]));
}
