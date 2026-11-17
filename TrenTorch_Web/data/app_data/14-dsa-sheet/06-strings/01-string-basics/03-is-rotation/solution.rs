// O(n) time, O(n) space
fn is_rotation(s: String, goal: String) -> bool {
    if s.len() != goal.len() {
        return false;
    }
    let doubled = format!("{}{}", s, s);
    doubled.contains(&goal)
}

fn main() {
    println!("{:?}", is_rotation(String::from("abcde"), String::from("cdeab")));
}
