// O(n) time, O(n) space
fn isomorphic_strings(s: String, t: String) -> bool {
    if s.len() != t.len() {
        return false;
    }
    use std::collections::hash_map::Entry;
    use std::collections::HashMap;

    let mut forward: HashMap<char, char> = HashMap::new();
    let mut backward: HashMap<char, char> = HashMap::new();

    for (a, b) in s.chars().zip(t.chars()) {
        match forward.entry(a) {
            Entry::Occupied(o) => {
                if *o.get() != b {
                    return false;
                }
            }
            Entry::Vacant(v) => {
                v.insert(b);
            }
        }
        match backward.entry(b) {
            Entry::Occupied(o) => {
                if *o.get() != a {
                    return false;
                }
            }
            Entry::Vacant(v) => {
                v.insert(a);
            }
        }
    }
    true
}

fn main() {
    println!("{:?}", isomorphic_strings(String::from("egg"), String::from("add")));
}
