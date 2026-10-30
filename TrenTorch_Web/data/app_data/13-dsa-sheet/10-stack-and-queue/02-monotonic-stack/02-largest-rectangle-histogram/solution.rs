// O(n) time, O(n) space
fn largest_rectangle(heights: Vec<i64>) -> i64 {
    let n = heights.len();
    let mut best: i64 = 0;
    let mut stack: Vec<usize> = Vec::new();
    for i in 0..=n {
        let h: i64 = if i == n { 0 } else { heights[i] };
        while !stack.is_empty() && heights[*stack.last().unwrap()] >= h {
            let j = stack.pop().unwrap();
            let height = heights[j];
            let left: i64 = match stack.last() {
                Some(&l) => l as i64,
                None => -1,
            };
            let width = i as i64 - left - 1;
            best = best.max(height * width);
        }
        stack.push(i);
    }
    best
}

fn main() {
    println!("{:?}", largest_rectangle(vec![2, 1, 5, 6, 2, 3]));
}
