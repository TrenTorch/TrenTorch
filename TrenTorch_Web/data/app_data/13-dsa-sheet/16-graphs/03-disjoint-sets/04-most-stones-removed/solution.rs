use std::collections::{HashMap, HashSet};

fn find(parent: &mut HashMap<i64, i64>, size: &mut HashMap<i64, i64>, start: i64) -> i64 {
    parent.entry(start).or_insert(start);
    size.entry(start).or_insert(1);
    let mut a = start;
    while parent[&a] != a {
        let gp = parent[&parent[&a]];
        parent.insert(a, gp);
        a = gp;
    }
    a
}

// O(n * alpha(n)) time, O(n) space (union-find over rows and shifted columns)
fn remove_stones(stones: Vec<Vec<i64>>) -> i64 {
    let mut parent: HashMap<i64, i64> = HashMap::new();
    let mut size: HashMap<i64, i64> = HashMap::new();
    for s in &stones {
        let (x, y) = (s[0], s[1]);
        let mut ra = find(&mut parent, &mut size, x);
        let mut rb = find(&mut parent, &mut size, y + 10001);
        if ra != rb {
            if size[&ra] < size[&rb] {
                std::mem::swap(&mut ra, &mut rb);
            }
            parent.insert(rb, ra);
            let add = size[&rb];
            *size.get_mut(&ra).unwrap() += add;
        }
    }
    let mut groups: HashSet<i64> = HashSet::new();
    for s in &stones {
        let root = find(&mut parent, &mut size, s[0]);
        groups.insert(root);
    }
    stones.len() as i64 - groups.len() as i64
}

fn main() {
    println!("{:?}", remove_stones(vec![vec![0, 0], vec![0, 1], vec![1, 0], vec![1, 2], vec![2, 1], vec![2, 2]]));
}
