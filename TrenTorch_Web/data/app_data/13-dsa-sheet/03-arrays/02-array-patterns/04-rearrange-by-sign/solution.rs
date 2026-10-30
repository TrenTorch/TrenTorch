// O(n) time, O(n) space
fn rearrange_by_sign(nums: Vec<i64>) -> Vec<i64> {
    let mut pos: Vec<i64> = Vec::new();
    let mut neg: Vec<i64> = Vec::new();

    for x in nums {
        if x >= 0 {
            pos.push(x);
        } else {
            neg.push(x);
        }
    }

    let mut out: Vec<i64> = Vec::with_capacity(pos.len() + neg.len());
    let total = pos.len().max(neg.len());

    for i in 0..total {
        if i < pos.len() {
            out.push(pos[i]);
        }
        if i < neg.len() {
            out.push(neg[i]);
        }
    }

    out
}

fn main() {
    println!("{:?}", rearrange_by_sign(vec![3, 1, -2, -5, 2, -4]));
}
