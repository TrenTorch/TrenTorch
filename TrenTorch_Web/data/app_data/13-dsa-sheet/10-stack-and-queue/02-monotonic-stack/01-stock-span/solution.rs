// O(n) time, O(n) space
fn stock_span(prices: Vec<i64>) -> Vec<i64> {
    let mut out = Vec::with_capacity(prices.len());
    let mut stack: Vec<usize> = Vec::new();
    for (i, &p) in prices.iter().enumerate() {
        while let Some(&top) = stack.last() {
            if prices[top] <= p {
                stack.pop();
            } else {
                break;
            }
        }
        let span = if let Some(&top) = stack.last() {
            i as i64 - top as i64
        } else {
            i as i64 + 1
        };
        out.push(span);
        stack.push(i);
    }
    out
}

fn main() {
    println!("{:?}", stock_span(vec![100, 80, 60, 70, 60, 75, 85]));
}
