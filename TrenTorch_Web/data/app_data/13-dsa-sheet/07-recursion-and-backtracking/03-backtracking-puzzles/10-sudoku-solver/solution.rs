// Exponential time (backtracking with MRV), O(1) space (fixed 9x9 board)
fn backtrack(
    grid: &mut [[i64; 9]; 9],
    rows: &mut [u16; 9],
    cols: &mut [u16; 9],
    boxes: &mut [u16; 9],
    empty: &[(usize, usize)],
) -> bool {
    let mut best: Option<(usize, usize, u16)> = None;
    for &(r, c) in empty {
        if grid[r][c] == 0 {
            let used = rows[r] | cols[c] | boxes[r / 3 * 3 + c / 3];
            let candidates = (!used) & 0x3FE; // bits 1-9
            let count = candidates.count_ones();
            if best.is_none() || count < best.as_ref().unwrap().2.count_ones() {
                best = Some((r, c, candidates));
                if count <= 1 {
                    break;
                }
            }
        }
    }
    let (r, c, candidates) = match best {
        Some(b) => b,
        None => return true,
    };
    for v in 1..=9u32 {
        let bit = 1u16 << v;
        if candidates & bit != 0 {
            grid[r][c] = v as i64;
            rows[r] |= bit;
            cols[c] |= bit;
            boxes[r / 3 * 3 + c / 3] |= bit;
            if backtrack(grid, rows, cols, boxes, empty) {
                return true;
            }
            grid[r][c] = 0;
            rows[r] &= !bit;
            cols[c] &= !bit;
            boxes[r / 3 * 3 + c / 3] &= !bit;
        }
    }
    false
}

fn sudoku_solver(board: Vec<Vec<i64>>) -> Vec<Vec<i64>> {
    let mut grid = [[0i64; 9]; 9];
    for (r, row) in board.iter().enumerate() {
        for (c, &val) in row.iter().enumerate() {
            grid[r][c] = val;
        }
    }
    let mut rows = [0u16; 9];
    let mut cols = [0u16; 9];
    let mut boxes = [0u16; 9];
    let mut empty = Vec::new();
    for r in 0..9 {
        for c in 0..9 {
            let v = grid[r][c];
            if v != 0 {
                let bit = 1u16 << (v as u32);
                rows[r] |= bit;
                cols[c] |= bit;
                boxes[r / 3 * 3 + c / 3] |= bit;
            } else {
                empty.push((r, c));
            }
        }
    }
    backtrack(&mut grid, &mut rows, &mut cols, &mut boxes, &empty);
    let mut result = Vec::with_capacity(9);
    for r in 0..9 {
        let mut row = Vec::with_capacity(9);
        for c in 0..9 {
            row.push(grid[r][c]);
        }
        result.push(row);
    }
    result
}

fn main() {
    println!("{:?}", sudoku_solver(vec![vec![5, 3, 0, 0, 7, 0, 0, 0, 0], vec![6, 0, 0, 1, 9, 5, 0, 0, 0], vec![0, 9, 8, 0, 0, 0, 0, 6, 0], vec![8, 0, 0, 0, 6, 0, 0, 0, 3], vec![4, 0, 0, 8, 0, 3, 0, 0, 1], vec![7, 0, 0, 0, 2, 0, 0, 0, 6], vec![0, 6, 0, 0, 0, 0, 2, 8, 0], vec![0, 0, 0, 4, 1, 9, 0, 0, 5], vec![0, 0, 0, 0, 8, 0, 0, 7, 9]]));
}
