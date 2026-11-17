fn find(parent: &mut [usize], mut a: usize) -> usize {
    while parent[a] != a {
        parent[a] = parent[parent[a]];
        a = parent[a];
    }
    a
}

// O(n * alpha(n)) time, O(n) space (union by size with path halving)
fn find_redundant_connection(edges: Vec<Vec<i64>>) -> Vec<i64> {
    let total = edges.len() + 2;
    let mut parent: Vec<usize> = (0..total).collect();
    let mut size: Vec<usize> = vec![1; total];
    for e in &edges {
        let (a, b) = (e[0] as usize, e[1] as usize);
        let mut ra = find(&mut parent, a);
        let mut rb = find(&mut parent, b);
        if ra == rb {
            return vec![e[0], e[1]];
        }
        if size[ra] < size[rb] {
            std::mem::swap(&mut ra, &mut rb);
        }
        parent[rb] = ra;
        size[ra] += size[rb];
    }
    Vec::new()
}

fn main() {
    println!("{:?}", find_redundant_connection(vec![vec![1, 2], vec![1, 3], vec![2, 3]]));
}
