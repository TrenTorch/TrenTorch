// O(V + E log V) time, O(V + E) space
fn find_order(num_courses: i64, prerequisites: Vec<Vec<i64>>) -> Vec<i64> {
    use std::cmp::Reverse;
    use std::collections::BinaryHeap;

    let n = num_courses as usize;
    if n == 0 {
        return Vec::new();
    }

    let mut adj = vec![Vec::new(); n];
    let mut in_degree = vec![0i64; n];

    for pre in prerequisites {
        let course = pre[0];
        let prereq = pre[1];
        adj[prereq as usize].push(course);
        in_degree[course as usize] += 1;
    }

    let mut heap = BinaryHeap::new();
    for i in 0..n {
        if in_degree[i] == 0 {
            heap.push(Reverse(i as i64));
        }
    }

    let mut order = Vec::with_capacity(n);
    while let Some(Reverse(node)) = heap.pop() {
        order.push(node);
        for &nxt in &adj[node as usize] {
            let idx = nxt as usize;
            in_degree[idx] -= 1;
            if in_degree[idx] == 0 {
                heap.push(Reverse(nxt));
            }
        }
    }

    if order.len() == n {
        order
    } else {
        Vec::new()
    }
}

fn main() {
    println!("{:?}", find_order(4, vec![vec![1, 0], vec![2, 0], vec![3, 1], vec![3, 2]]));
}
