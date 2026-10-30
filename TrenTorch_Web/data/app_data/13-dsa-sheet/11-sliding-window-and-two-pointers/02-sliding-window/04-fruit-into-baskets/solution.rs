// O(n) time, O(1) space
fn total_fruit(fruits: Vec<i64>) -> i64 {
    use std::collections::HashMap;
    let mut count = HashMap::new();
    let mut left = 0;
    let mut best = 0;
    for (right, &f) in fruits.iter().enumerate() {
        *count.entry(f).or_insert(0) += 1;
        while count.len() > 2 {
            let left_fruit = fruits[left];
            let cnt = count.get_mut(&left_fruit).unwrap();
            *cnt -= 1;
            if *cnt == 0 {
                count.remove(&left_fruit);
            }
            left += 1;
        }
        let current_len = right - left + 1;
        if current_len > best {
            best = current_len;
        }
    }
    best as i64
}

fn main() {
    println!("{:?}", total_fruit(vec![1, 2, 3, 2, 2]));
}
