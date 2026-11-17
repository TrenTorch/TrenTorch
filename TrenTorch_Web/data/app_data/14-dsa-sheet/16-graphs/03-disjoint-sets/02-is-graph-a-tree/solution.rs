// O(n α(n)) time, O(n) space
fn find(parent: &mut [usize], mut x: usize) -> usize {
    while parent[x] != x {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    x
}

fn valid_tree(n: i64, edges: Vec<Vec<i64>>) -> bool {
    if n == 0 || edges.len() != (n - 1) as usize {
        return false;
    }
    let n_usize = n as usize;
    let mut parent: Vec<usize> = (0..n_usize).collect();
    let mut size = vec![1; n_usize];

    for edge in edges {
        let a = edge[0] as usize;
        let b = edge[1] as usize;
        let mut ra = find(&mut parent, a);
        let mut rb = find(&mut parent, b);
        if ra == rb {
            return false;
        }
        if size[ra] < size[rb] {
            std::mem::swap(&mut ra, &mut rb);
        }
        parent[rb] = ra;
        size[ra] += size[rb];
    }
    true
}

fn main() {
    println!("{:?}", valid_tree(5, vec![vec![0, 1], vec![0, 2], vec![0, 3], vec![1, 4]]));
}
