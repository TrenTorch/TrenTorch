// O(min(m,n) log max(m,n)) time, O(log min(m,n)) space
fn search(matrix: &Vec<Vec<i64>>, target: i64, r0: i64, r1: i64, c0: i64, c1: i64) -> bool {
    if r0 > r1 || c0 > c1 {
        return false;
    }
    if r1 - r0 <= c1 - c0 {
        let r = (r0 + r1) / 2;
        let mut lo = c0;
        let mut hi = c1 + 1;
        while lo < hi {
            let mid = (lo + hi) / 2;
            if matrix[r as usize][mid as usize] < target {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        if lo <= c1 && matrix[r as usize][lo as usize] == target {
            return true;
        }
        search(matrix, target, r0, r - 1, lo, c1) || search(matrix, target, r + 1, r1, c0, lo - 1)
    } else {
        let c = (c0 + c1) / 2;
        let mut lo = r0;
        let mut hi = r1 + 1;
        while lo < hi {
            let mid = (lo + hi) / 2;
            if matrix[mid as usize][c as usize] < target {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        if lo <= r1 && matrix[lo as usize][c as usize] == target {
            return true;
        }
        search(matrix, target, r0, lo - 1, c + 1, c1) || search(matrix, target, lo, r1, c0, c - 1)
    }
}

fn search_matrix_ii(matrix: Vec<Vec<i64>>, target: i64) -> bool {
    if matrix.is_empty() || matrix[0].is_empty() {
        return false;
    }
    let rows = matrix.len() as i64;
    let cols = matrix[0].len() as i64;
    search(&matrix, target, 0, rows - 1, 0, cols - 1)
}

fn main() {
    println!("{:?}", search_matrix_ii(vec![vec![1, 4, 7, 11], vec![2, 5, 8, 12], vec![3, 6, 9, 16], vec![10, 13, 14, 17]], 5));
}
