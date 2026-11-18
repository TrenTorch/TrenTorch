// O(n log n) time, O(n) space
fn find_maximized_capital(k: i64, w: i64, profits: Vec<i64>, capital: Vec<i64>) -> i64 {
    let mut projects: Vec<(i64, i64)> = capital.into_iter().zip(profits).collect();
    projects.sort_by_key(|p| p.0);
    let mut heap = std::collections::BinaryHeap::new();
    let mut i = 0;
    let mut w = w;
    for _ in 0..k {
        while i < projects.len() && projects[i].0 <= w {
            heap.push(projects[i].1);
            i += 1;
        }
        if let Some(profit) = heap.pop() {
            w += profit;
        } else {
            break;
        }
    }
    w
}

fn main() {
    println!("{:?}", find_maximized_capital(2, 0, vec![1, 2, 3], vec![0, 1, 1]));
}
