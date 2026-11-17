// O(rows * log(max - min)) time, O(1) space
fn kth_smallest_matrix(matrix: Vec<Vec<i64>>, k: i64) -> i64 {
    let rows = matrix.len();
    let cols = matrix[0].len();

    let count_at_most = |x: i64| -> i64 {
        let mut count: i64 = 0;
        let mut col: i64 = cols as i64 - 1;
        for r in 0..rows {
            while col >= 0 && matrix[r][col as usize] > x {
                col -= 1;
            }
            count += col + 1;
        }
        count
    };

    let mut lo = matrix[0][0];
    let mut hi = matrix[rows - 1][cols - 1];
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if count_at_most(mid) >= k {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn main() {
    println!("{:?}", kth_smallest_matrix(vec![vec![1, 5, 9], vec![10, 11, 13], vec![12, 13, 15]], 8));
}
