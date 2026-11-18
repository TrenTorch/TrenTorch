use std::collections::{BTreeMap, HashMap};

// O(log n) time per operation, O(capacity) space (hash map plus ordered map keyed by (uses, last use))
fn run_lfu(capacity: i64, ops: Vec<String>) -> Vec<i64> {
    let cap: usize = if capacity > 0 { capacity as usize } else { 0 };
    // key -> (value, uses, last-use stamp)
    let mut entries: HashMap<i64, (i64, i64, u64)> = HashMap::new();
    // (uses, last-use stamp) -> key; the first entry is the eviction victim
    let mut order: BTreeMap<(i64, u64), i64> = BTreeMap::new();
    let mut clock: u64 = 0;
    let mut out: Vec<i64> = Vec::new();

    for op in ops.iter() {
        let parts: Vec<&str> = op.split_whitespace().collect();
        let key: i64 = parts[1].parse().unwrap();
        if parts[0] == "get" {
            if let Some((value, uses, stamp)) = entries.get(&key).copied() {
                clock += 1;
                order.remove(&(uses, stamp));
                order.insert((uses + 1, clock), key);
                entries.insert(key, (value, uses + 1, clock));
                out.push(value);
            } else {
                out.push(-1);
            }
        } else if cap > 0 {
            let value: i64 = parts[2].parse().unwrap();
            if let Some((_, uses, stamp)) = entries.get(&key).copied() {
                clock += 1;
                order.remove(&(uses, stamp));
                order.insert((uses + 1, clock), key);
                entries.insert(key, (value, uses + 1, clock));
            } else {
                if entries.len() == cap {
                    let (victim_uses, victim_stamp) = *order.keys().next().unwrap();
                    let victim = order.remove(&(victim_uses, victim_stamp)).unwrap();
                    entries.remove(&victim);
                }
                clock += 1;
                entries.insert(key, (value, 1, clock));
                order.insert((1, clock), key);
            }
        }
    }
    out
}

fn main() {
    println!("{:?}", run_lfu(2, vec![String::from("put 1 1"), String::from("put 2 2"), String::from("get 1"), String::from("put 3 3"), String::from("get 2"), String::from("get 3"), String::from("put 4 4"), String::from("get 1"), String::from("get 3"), String::from("get 4")]));
}
