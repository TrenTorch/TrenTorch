// O(n + m α(n)) time, O(n) space
fn make_connected(n: i64, connections: Vec<Vec<i64>>) -> i64 {
    let n_usize = n as usize;
    if connections.len() < n_usize - 1 {
        return -1;
    }

    let mut parent: Vec<usize> = (0..n_usize).collect();
    let mut size: Vec<usize> = vec![1; n_usize];
    let mut components = n_usize;

    for conn in connections {
        let a = conn[0] as usize;
        let b = conn[1] as usize;
        let ra = find(&mut parent, a);
        let rb = find(&mut parent, b);
        if ra != rb {
            if size[ra] < size[rb] {
                // union by size
                parent[ra] = rb;
                size[rb] += size[ra];
            } else {
                parent[rb] = ra;
                size[ra] += size[rb];
            }
            components -= 1;
        }
    }

    (components - 1) as i64
}

fn find(parent: &mut [usize], mut a: usize) -> usize {
    while parent[a] != a {
        parent[a] = parent[parent[a]];
        a = parent[a];
    }
    a
}

fn main() {
    println!("{:?}", make_connected(4, vec![vec![0, 1], vec![0, 2], vec![1, 2]]));
}
