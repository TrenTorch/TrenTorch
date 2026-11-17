use std::cmp::Reverse;
use std::collections::{BTreeSet, BinaryHeap, HashMap};

// O(S + E log C) time, O(S + E) space (S total characters, C distinct letters <= 26, E ordering edges)
fn alien_order(words: Vec<String>) -> String {
    let letter_set: BTreeSet<char> = words.iter().flat_map(|w| w.chars()).collect();
    let letters: Vec<char> = letter_set.into_iter().collect();
    let index: HashMap<char, usize> = letters.iter().enumerate().map(|(i, &c)| (c, i)).collect();
    let mut edges: BTreeSet<(usize, usize)> = BTreeSet::new();
    for pair in words.windows(2) {
        let a: Vec<char> = pair[0].chars().collect();
        let b: Vec<char> = pair[1].chars().collect();
        let mut found = false;
        for (x, y) in a.iter().zip(b.iter()) {
            if x != y {
                edges.insert((index[x], index[y]));
                found = true;
                break;
            }
        }
        if !found && a.len() > b.len() {
            return String::new();
        }
    }
    let n = letters.len();
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); n];
    let mut in_degree = vec![0usize; n];
    for &(x, y) in &edges {
        adj[x].push(y);
        in_degree[y] += 1;
    }
    let mut heap: BinaryHeap<Reverse<usize>> = (0..n)
        .filter(|&i| in_degree[i] == 0)
        .map(Reverse)
        .collect();
    let mut out = String::new();
    let mut taken = 0usize;
    while let Some(Reverse(i)) = heap.pop() {
        out.push(letters[i]);
        taken += 1;
        for &nxt in &adj[i] {
            in_degree[nxt] -= 1;
            if in_degree[nxt] == 0 {
                heap.push(Reverse(nxt));
            }
        }
    }
    if taken == n {
        out
    } else {
        String::new()
    }
}

fn main() {
    println!("{:?}", alien_order(vec![String::from("wrt"), String::from("wrf"), String::from("er"), String::from("ett"), String::from("rftt")]));
}
