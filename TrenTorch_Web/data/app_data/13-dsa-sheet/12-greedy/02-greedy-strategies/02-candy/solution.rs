// O(n) time, O(1) space
fn candy(ratings: Vec<i64>) -> i64 {
    let n = ratings.len();
    if n == 0 {
        return 0;
    }
    let mut total = 1;
    let mut up = 0;
    let mut down = 0;
    let mut peak = 0;
    for i in 1..n {
        if ratings[i] > ratings[i - 1] {
            up += 1;
            down = 0;
            peak = up;
            total += 1 + up;
        } else if ratings[i] == ratings[i - 1] {
            up = 0;
            down = 0;
            peak = 0;
            total += 1;
        } else {
            up = 0;
            down += 1;
            total += 1 + down;
            if peak >= down {
                total -= 1;
            }
        }
    }
    total
}

fn main() {
    println!("{:?}", candy(vec![1, 0, 2]));
}
