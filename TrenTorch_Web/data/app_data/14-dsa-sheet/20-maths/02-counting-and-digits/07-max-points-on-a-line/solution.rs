use std::collections::HashMap;

// O(n^2) time, O(n) space (normalized slopes counted per anchor point)
fn max_points(points: Vec<Vec<i64>>) -> i64 {
    let n = points.len();
    if n <= 2 {
        return n as i64;
    }
    let mut best: i64 = 2;
    for i in 0..n {
        let mut slopes: HashMap<(i64, i64), i64> = HashMap::new();
        let x0 = points[i][0];
        let y0 = points[i][1];
        for j in (i + 1)..n {
            let mut dx = points[j][0] - x0;
            let mut dy = points[j][1] - y0;
            let g = gcd(dx, dy);
            dx /= g;
            dy /= g;
            if dx < 0 || (dx == 0 && dy < 0) {
                dx = -dx;
                dy = -dy;
            }
            *slopes.entry((dx, dy)).or_insert(0) += 1;
        }
        if let Some(&m) = slopes.values().max() {
            best = best.max(m + 1);
        }
    }
    best
}

fn gcd(a: i64, b: i64) -> i64 {
    let (mut a, mut b) = (a.abs(), b.abs());
    while b != 0 {
        let t = a % b;
        a = b;
        b = t;
    }
    a
}

fn main() {
    println!("{:?}", max_points(vec![vec![1, 1], vec![2, 2], vec![3, 3]]));
}
