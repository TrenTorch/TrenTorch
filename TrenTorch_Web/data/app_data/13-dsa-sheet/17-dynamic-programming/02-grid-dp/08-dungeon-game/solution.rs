// O(rows * cols) time, O(cols) space
fn calculate_minimum_hp(dungeon: Vec<Vec<i64>>) -> i64 {
    let rows = dungeon.len();
    let cols = if rows > 0 { dungeon[0].len() } else { 0 };
    if rows == 0 || cols == 0 {
        return 1;
    }
    let inf: i64 = i64::MAX / 4;
    let mut need = vec![inf; cols + 1];
    need[cols - 1] = 1;
    for r in (0..rows).rev() {
        for c in (0..cols).rev() {
            let mut best_next = std::cmp::min(need[c], need[c + 1]);
            if r == rows - 1 && c == cols - 1 {
                best_next = 1;
            }
            need[c] = std::cmp::max(1, best_next - dungeon[r][c]);
        }
        need[cols] = inf;
    }
    need[0]
}

fn main() {
    println!("{:?}", calculate_minimum_hp(vec![vec![-2, -3, 3], vec![-5, -10, 1], vec![10, 30, -5]]));
}
