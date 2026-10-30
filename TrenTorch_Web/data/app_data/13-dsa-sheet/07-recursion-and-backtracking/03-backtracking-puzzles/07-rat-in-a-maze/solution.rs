const MOVES: [(char, isize, isize); 4] = [('D', 1, 0), ('L', 0, -1), ('R', 0, 1), ('U', -1, 0)];

fn dfs(
    maze: &Vec<Vec<i64>>,
    on_path: &mut Vec<Vec<bool>>,
    path: &mut Vec<char>,
    out: &mut Vec<String>,
    rows: isize,
    cols: isize,
    r: isize,
    c: isize,
) {
    if r == rows - 1 && c == cols - 1 {
        out.push(path.iter().collect());
        return;
    }
    on_path[r as usize][c as usize] = true;
    for &(ch, dr, dc) in &MOVES {
        let nr = r + dr;
        let nc = c + dc;
        if nr >= 0 && nr < rows && nc >= 0 && nc < cols {
            let nr_usize = nr as usize;
            let nc_usize = nc as usize;
            if maze[nr_usize][nc_usize] == 1 && !on_path[nr_usize][nc_usize] {
                path.push(ch);
                dfs(maze, on_path, path, out, rows, cols, nr, nc);
                path.pop();
            }
        }
    }
    on_path[r as usize][c as usize] = false;
}

// Exponential time, O(rows*cols) space
fn rat_in_a_maze(maze: Vec<Vec<i64>>) -> Vec<String> {
    let rows = maze.len();
    let cols = if rows > 0 { maze[0].len() } else { 0 };
    if rows == 0 || cols == 0 || maze[0][0] == 0 || maze[rows - 1][cols - 1] == 0 {
        return Vec::new();
    }
    let mut out = Vec::new();
    let mut path = Vec::new();
    let mut on_path = vec![vec![false; cols]; rows];
    dfs(&maze, &mut on_path, &mut path, &mut out, rows as isize, cols as isize, 0, 0);
    out
}

fn main() {
    println!("{:?}", rat_in_a_maze(vec![vec![1, 0, 0, 0], vec![1, 1, 0, 1], vec![1, 1, 0, 0], vec![0, 1, 1, 1]]));
}
