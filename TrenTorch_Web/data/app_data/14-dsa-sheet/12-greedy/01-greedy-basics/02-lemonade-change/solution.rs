// O(n) time, O(1) space
fn lemonade_change(bills: Vec<i64>) -> bool {
    let mut fives = 0;
    let mut tens = 0;
    for bill in bills {
        match bill {
            5 => fives += 1,
            10 => {
                if fives == 0 {
                    return false;
                }
                fives -= 1;
                tens += 1;
            }
            20 => {
                if tens > 0 && fives > 0 {
                    tens -= 1;
                    fives -= 1;
                } else if fives >= 3 {
                    fives -= 3;
                } else {
                    return false;
                }
            }
            _ => {}
        }
    }
    true
}

fn main() {
    println!("{:?}", lemonade_change(vec![5, 5, 5, 10, 20]));
}
