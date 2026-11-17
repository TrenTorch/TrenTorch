// O(n log n) time (sorting), O(n) space for the sorted copy
fn boats_needed(people: Vec<i64>, limit: i64) -> i64 {
    let mut a = people;
    a.sort();
    let mut light: i64 = 0;
    let mut heavy: i64 = (a.len() as i64) - 1;
    let mut boats: i64 = 0;
    while light <= heavy {
        if a[light as usize] + a[heavy as usize] <= limit {
            light += 1;
        }
        heavy -= 1;
        boats += 1;
    }
    boats
}

fn main() {
    println!("{:?}", boats_needed(vec![3, 2, 2, 1], 3));
}
