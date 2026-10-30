// O(n!) time, O(n) space
fn n_queens_count(n: i64) -> i64 {
    let n = n as usize;
    let mut cols = std::collections::HashSet::new();
    let mut diag1 = std::collections::HashSet::new();
    let mut diag2 = std::collections::HashSet::new();

    fn backtrack(
        r: usize,
        n: usize,
        cols: &mut std::collections::HashSet<usize>,
        diag1: &mut std::collections::HashSet<i32>,
        diag2: &mut std::collections::HashSet<i32>,
    ) -> i64 {
        if r == n {
            return 1;
        }
        let mut total = 0;
        for c in 0..n {
            let d1 = r as i32 - c as i32;
            let d2 = r as i32 + c as i32;
            if cols.contains(&c) || diag1.contains(&d1) || diag2.contains(&d2) {
                continue;
            }
            cols.insert(c);
            diag1.insert(d1);
            diag2.insert(d2);
            total += backtrack(r + 1, n, cols, diag1, diag2);
            cols.remove(&c);
            diag1.remove(&d1);
            diag2.remove(&d2);
        }
        total
    }

    backtrack(0, n, &mut cols, &mut diag1, &mut diag2)
}

fn main() {
    println!("{:?}", n_queens_count(4));
}
