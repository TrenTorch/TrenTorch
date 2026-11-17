// O(R * C * 4^L) time, O(R * C + L) extra space (R rows, C cols, L word length)
fn word_search(board: Vec<String>, word: String) -> bool {
    if word.is_empty() {
        return true;
    }
    let mut grid: Vec<Vec<u8>> = board.iter().map(|row| row.as_bytes().to_vec()).collect();
    let target: Vec<u8> = word.into_bytes();
    let rows = grid.len();
    let cols = if rows > 0 { grid[0].len() } else { 0 };
    for r in 0..rows {
        for c in 0..cols {
            if search_from(&mut grid, &target, r as isize, c as isize, 0) {
                return true;
            }
        }
    }
    false
}

fn search_from(grid: &mut Vec<Vec<u8>>, word: &[u8], r: isize, c: isize, i: usize) -> bool {
    if i == word.len() {
        return true;
    }
    let rows = grid.len() as isize;
    let cols = if rows > 0 { grid[0].len() as isize } else { 0 };
    if !(0 <= r && r < rows && 0 <= c && c < cols) {
        return false;
    }
    let (ru, cu) = (r as usize, c as usize);
    if grid[ru][cu] != word[i] {
        return false;
    }
    let saved = grid[ru][cu];
    grid[ru][cu] = b'#';
    let found = search_from(grid, word, r + 1, c, i + 1)
        || search_from(grid, word, r - 1, c, i + 1)
        || search_from(grid, word, r, c + 1, i + 1)
        || search_from(grid, word, r, c - 1, i + 1);
    grid[ru][cu] = saved;
    found
}

fn main() {
    println!(
        "{:?}",
        word_search(
            vec![String::from("abce"), String::from("sfcs"), String::from("adee")],
            String::from("abcced")
        )
    );
}
