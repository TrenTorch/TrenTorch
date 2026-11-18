use std::collections::BTreeSet;

struct TrieNode {
    children: [Option<usize>; 26],
    word: Option<String>,
}

impl TrieNode {
    fn new() -> Self {
        TrieNode {
            children: [None; 26],
            word: None,
        }
    }
}

fn dfs(
    grid: &mut Vec<Vec<u8>>,
    nodes: &[TrieNode],
    node: usize,
    r: usize,
    c: usize,
    rows: usize,
    cols: usize,
    found: &mut BTreeSet<String>,
) {
    let ch = grid[r][c];
    let idx = (ch - b'a') as usize;
    let next = match nodes[node].children[idx] {
        Some(next) => next,
        None => return,
    };
    if let Some(word) = &nodes[next].word {
        found.insert(word.clone());
    }
    grid[r][c] = b'#';
    let mut neighbours: Vec<(usize, usize)> = Vec::with_capacity(4);
    if r + 1 < rows {
        neighbours.push((r + 1, c));
    }
    if r > 0 {
        neighbours.push((r - 1, c));
    }
    if c + 1 < cols {
        neighbours.push((r, c + 1));
    }
    if c > 0 {
        neighbours.push((r, c - 1));
    }
    for (nr, nc) in neighbours {
        if grid[nr][nc] != b'#' {
            dfs(grid, nodes, next, nr, nc, rows, cols, found);
        }
    }
    grid[r][c] = ch;
}

// O(rows * cols * 4^L) time where L <= 10, O(total characters in words) space
fn find_words(board: Vec<String>, words: Vec<String>) -> Vec<String> {
    let mut nodes: Vec<TrieNode> = vec![TrieNode::new()];
    for word in words {
        let mut cur = 0usize;
        for ch in word.bytes() {
            let idx = (ch - b'a') as usize;
            let existing = nodes[cur].children[idx];
            cur = match existing {
                Some(next) => next,
                None => {
                    nodes.push(TrieNode::new());
                    let new_idx = nodes.len() - 1;
                    nodes[cur].children[idx] = Some(new_idx);
                    new_idx
                }
            };
        }
        nodes[cur].word = Some(word);
    }

    let rows = board.len();
    let cols = board.first().map_or(0, |row| row.len());
    let mut grid: Vec<Vec<u8>> = board.iter().map(|s| s.as_bytes().to_vec()).collect();
    let mut found: BTreeSet<String> = BTreeSet::new();

    for r in 0..rows {
        for c in 0..cols {
            dfs(&mut grid, &nodes, 0, r, c, rows, cols, &mut found);
        }
    }

    found.into_iter().collect()
}

fn main() {
    println!("{:?}", find_words(vec![String::from("oaan"), String::from("etae"), String::from("ihkr"), String::from("iflv")], vec![String::from("oath"), String::from("pea"), String::from("eat"), String::from("rain")]));
}
