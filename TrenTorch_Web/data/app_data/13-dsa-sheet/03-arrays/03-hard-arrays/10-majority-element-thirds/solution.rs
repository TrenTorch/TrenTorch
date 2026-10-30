// O(n) time, O(1) space
fn majority_element_thirds(nums: Vec<i64>) -> Vec<i64> {
    let mut a: Option<i64> = None;
    let mut b: Option<i64> = None;
    let mut ca = 0;
    let mut cb = 0;

    for &x in &nums {
        if ca > 0 && a == Some(x) {
            ca += 1;
        } else if cb > 0 && b == Some(x) {
            cb += 1;
        } else if ca == 0 {
            a = Some(x);
            ca = 1;
        } else if cb == 0 {
            b = Some(x);
            cb = 1;
        } else {
            ca -= 1;
            cb -= 1;
        }
    }

    let n = nums.len();
    let mut result = Vec::new();

    if let Some(val) = a {
        if nums.iter().filter(|&&y| y == val).count() * 3 > n {
            result.push(val);
        }
    }
    if let Some(val) = b {
        if a != Some(val) && nums.iter().filter(|&&y| y == val).count() * 3 > n {
            result.push(val);
        }
    }

    result.sort();
    result
}

fn main() {
    println!("{:?}", majority_element_thirds(vec![3, 2, 3]));
}
