use std::collections::VecDeque;

// O(n + p) time, O(n + p) space (n courses, p prerequisite pairs)
fn can_finish(num_courses: i64, prerequisites: Vec<Vec<i64>>) -> bool {
    let n = num_courses as usize;
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); n];
    let mut in_degree = vec![0usize; n];
    for p in &prerequisites {
        let course = p[0] as usize;
        let pre = p[1] as usize;
        adj[pre].push(course);
        in_degree[course] += 1;
    }
    let mut queue: VecDeque<usize> = (0..n).filter(|&v| in_degree[v] == 0).collect();
    let mut taken = 0usize;
    while let Some(node) = queue.pop_front() {
        taken += 1;
        for &nxt in &adj[node] {
            in_degree[nxt] -= 1;
            if in_degree[nxt] == 0 {
                queue.push_back(nxt);
            }
        }
    }
    taken == n
}

fn main() {
    println!("{:?}", can_finish(2, vec![vec![1, 0]]));
}
