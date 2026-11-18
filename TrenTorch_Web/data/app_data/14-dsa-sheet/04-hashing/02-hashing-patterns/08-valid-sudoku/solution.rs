use std::collections::HashSet;

// O(81) time, O(81) space
fn valid_sudoku(board: Vec<Vec<i64>>) -> bool {
    let mut seen: HashSet<(char, usize, i64)> = HashSet::new();
    for r in 0..9 {
        for c in 0..9 {
            let digit = board[r][c];
            if digit == 0 {
                continue;
            }
            let box_idx = (r / 3) * 3 + (c / 3);
            let keys = [
                ('r', r, digit),
                ('c', c, digit),
                ('b', box_idx, digit),
            ];
            for key in &keys {
                if seen.contains(key) {
                    return false;
                }
            }
            for key in &keys {
                seen.insert(*key);
            }
        }
    }
    true
}

fn main() {
    println!("{:?}", valid_sudoku(vec![
        vec![5, 3, 0, 0, 7, 0, 0, 0, 0],
        vec![6, 0, 0, 1, 9, 5, 0, 0, 0],
        vec![0, 9, 8, 0, 0, 0, 0, 6, 0],
        vec![8, 0, 0, 0, 6, 0, 0, 0, 3],
        vec![4, 0, 0, 8, 0, 3, 0, 0, 1],
        vec![7, 0, 0, 0, 2, 0, 0, 0, 6],
        vec![0, 6, 0, 0, 0, 0, 2, 8, 0],
        vec![0, 0, 0, 4, 1, 9, 0, 0, 5],
        vec![0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]));
}
