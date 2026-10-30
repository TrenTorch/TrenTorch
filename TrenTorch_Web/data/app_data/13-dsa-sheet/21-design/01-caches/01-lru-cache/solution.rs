use std::collections::HashMap;

const HEAD: usize = 0;
const TAIL: usize = 1;

struct LruNode {
    key: i64,
    value: i64,
    prev: usize,
    next: usize,
}

// O(1) time per operation, O(capacity) space (hash map plus doubly linked list in an arena)
fn run_lru(capacity: i64, ops: Vec<String>) -> Vec<i64> {
    let cap: usize = if capacity > 0 { capacity as usize } else { 0 };
    let mut nodes: Vec<LruNode> = vec![
        LruNode { key: 0, value: 0, prev: HEAD, next: TAIL },
        LruNode { key: 0, value: 0, prev: HEAD, next: TAIL },
    ];
    let mut free: Vec<usize> = Vec::new();
    let mut index: HashMap<i64, usize> = HashMap::new();
    let mut out: Vec<i64> = Vec::new();

    for op in ops.iter() {
        let parts: Vec<&str> = op.split_whitespace().collect();
        if parts[0] == "get" {
            let key: i64 = parts[1].parse().unwrap();
            match index.get(&key).copied() {
                Some(idx) => {
                    lru_move_to_front(&mut nodes, idx);
                    out.push(nodes[idx].value);
                }
                None => out.push(-1),
            }
        } else if cap > 0 {
            let key: i64 = parts[1].parse().unwrap();
            let value: i64 = parts[2].parse().unwrap();
            if let Some(idx) = index.get(&key).copied() {
                nodes[idx].value = value;
                lru_move_to_front(&mut nodes, idx);
            } else {
                if index.len() == cap {
                    let lru = nodes[TAIL].prev;
                    lru_unlink(&mut nodes, lru);
                    let evicted_key = nodes[lru].key;
                    index.remove(&evicted_key);
                    free.push(lru);
                }
                let fresh = LruNode { key, value, prev: HEAD, next: HEAD };
                let idx = match free.pop() {
                    Some(slot) => {
                        nodes[slot] = fresh;
                        slot
                    }
                    None => {
                        nodes.push(fresh);
                        nodes.len() - 1
                    }
                };
                index.insert(key, idx);
                lru_push_front(&mut nodes, idx);
            }
        }
    }
    out
}

fn lru_unlink(nodes: &mut [LruNode], idx: usize) {
    let p = nodes[idx].prev;
    let n = nodes[idx].next;
    nodes[p].next = n;
    nodes[n].prev = p;
}

fn lru_push_front(nodes: &mut [LruNode], idx: usize) {
    let first = nodes[HEAD].next;
    nodes[idx].prev = HEAD;
    nodes[idx].next = first;
    nodes[first].prev = idx;
    nodes[HEAD].next = idx;
}

fn lru_move_to_front(nodes: &mut [LruNode], idx: usize) {
    lru_unlink(nodes, idx);
    lru_push_front(nodes, idx);
}

fn main() {
    println!("{:?}", run_lru(2, vec![String::from("put 1 1"), String::from("put 2 2"), String::from("get 1"), String::from("put 3 3"), String::from("get 2"), String::from("put 4 4"), String::from("get 1"), String::from("get 3"), String::from("get 4")]));
}
