// O(n log n) time, O(n) space
fn find(parent: &mut [usize], mut x: usize) -> usize {
    while parent[x] != x {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    x
}

fn max_job_profit(jobs: Vec<Vec<i64>>) -> i64 {
    if jobs.is_empty() {
        return 0;
    }
    let n = jobs.len();
    let max_deadline = jobs.iter().map(|j| j[0]).max().unwrap_or(0);
    let limit = (max_deadline.min(n as i64)) as usize;
    let mut parent: Vec<usize> = (0..=limit).collect();

    let mut jobs = jobs;
    jobs.sort_by(|a, b| b[1].cmp(&a[1]));

    let mut total = 0i64;
    for job in jobs {
        let deadline = job[0];
        let profit = job[1];
        let d = deadline.min(limit as i64) as usize;
        let slot = find(&mut parent, d);
        if slot > 0 {
            parent[slot] = slot - 1;
            total += profit;
        }
    }
    total
}

fn main() {
    println!("{:?}", max_job_profit(vec![vec![4, 20], vec![1, 10], vec![1, 40], vec![1, 30]]));
}
