// O(n) time, O(1) space
fn second_largest(nums: Vec<i64>) -> i64 {
    let mut largest: Option<i64> = None;
    let mut second: Option<i64> = None;
    for x in nums {
        match largest {
            None => {
                largest = Some(x);
            }
            Some(l) => {
                if x > l {
                    second = largest;
                    largest = Some(x);
                } else if x < l {
                    match second {
                        None => {
                            second = Some(x);
                        }
                        Some(s) => {
                            if x > s {
                                second = Some(x);
                            }
                        }
                    }
                }
            }
        }
    }
    second.unwrap_or(-1)
}

fn main() {
    println!("{:?}", second_largest(vec![4, 9, 9, 6]));
}
