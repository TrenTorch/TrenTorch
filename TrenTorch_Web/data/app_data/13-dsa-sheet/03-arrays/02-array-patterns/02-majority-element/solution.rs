// O(n) time, O(1) extra space
fn majority_element(nums: Vec<i64>) -> i64 {
    let mut candidate: Option<i64> = None;
    let mut count: i64 = 0;
    for &x in nums.iter() {
        if count == 0 {
            candidate = Some(x);
            count = 1;
        } else if Some(x) == candidate {
            count += 1;
        } else {
            count -= 1;
        }
    }
    if let Some(c) = candidate {
        let mut occ: i64 = 0;
        for &x in nums.iter() {
            if x == c {
                occ += 1;
            }
        }
        if occ > (nums.len() as i64) / 2 {
            return c;
        }
    }
    -1
}

fn main() {
    println!("{:?}", majority_element(vec![2, 2, 1, 1, 2, 2, 3]));
}
