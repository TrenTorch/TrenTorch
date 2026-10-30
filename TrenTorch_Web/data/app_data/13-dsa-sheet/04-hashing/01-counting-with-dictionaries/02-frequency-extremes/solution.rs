use std::collections::HashMap;

// O(n) time, O(n) space (average case)
fn frequency_extremes(nums: Vec<i64>) -> Vec<i64> {
    let mut counts = HashMap::new();
    for &x in &nums {
        *counts.entry(x).or_insert(0) += 1;
    }
    let mut most: Option<(i64, usize)> = None;
    let mut least: Option<(i64, usize)> = None;
    for (&val, &cnt) in &counts {
        // update most
        match most {
            None => most = Some((val, cnt)),
            Some((mval, mcnt)) => {
                if cnt > mcnt || (cnt == mcnt && val < mval) {
                    most = Some((val, cnt));
                }
            }
        }
        // update least
        match least {
            None => least = Some((val, cnt)),
            Some((lval, lcnt)) => {
                if cnt < lcnt || (cnt == lcnt && val < lval) {
                    least = Some((val, cnt));
                }
            }
        }
    }
    vec![most.unwrap().0, least.unwrap().0]
}

fn main() {
    println!("{:?}", frequency_extremes(vec![4, 4, 5, 5, 6]));
}
