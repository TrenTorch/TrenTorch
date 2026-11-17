// O(n log n + m log m) time, O(1) extra space
fn assign_cookies(greed: Vec<i64>, sizes: Vec<i64>) -> i64 {
    let mut greed = greed;
    let mut sizes = sizes;
    greed.sort_unstable();
    sizes.sort_unstable();
    let mut child = 0;
    for cookie in sizes {
        if child < greed.len() && greed[child] <= cookie {
            child += 1;
        }
    }
    child as i64
}

fn main() {
    println!("{:?}", assign_cookies(vec![1, 2, 3], vec![1, 1]));
}
