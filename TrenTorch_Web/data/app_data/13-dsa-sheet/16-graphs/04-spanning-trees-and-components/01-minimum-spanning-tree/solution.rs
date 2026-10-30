// O(E log E) time, O(V) space
fn find(parent: &mut [usize], mut x: usize) -> usize {
    while parent[x] != x {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    x
}

fn mst_weight(n: i64, edges: Vec<Vec<i64>>) -> i64 {
    let n_usize = n as usize;
    let mut parent: Vec<usize> = (0..n_usize).collect();
    let mut size: Vec<usize> = vec![1; n_usize];

    let mut edges = edges;
    edges.sort_by_key(|e| e[2]);

    let mut total = 0i64;
    let mut taken = 0usize;

    for e in edges {
        let a = e[0] as usize;
        let b = e[1] as usize;
        let w = e[2];
        let ra = find(&mut parent, a);
        let rb = find(&mut parent, b);
        if ra != rb {
            if size[ra] < size[rb] {
                parent[ra] = rb;
                size[rb] += size[ra];
            } else {
                parent[rb] = ra;
                size[ra] += size[rb];
            }
            total += w;
            taken += 1;
        }
    }

    if taken == n_usize - 1 {
        total
    } else {
        -1
    }
}

fn main() {
    println!("{:?}", mst_weight(4, vec![vec![0, 1, 1], vec![1, 2, 2], vec![2, 3, 3], vec![0, 3, 10], vec![0, 2, 5]]));
}
