use std::collections::VecDeque;

// O(n log n) time (sorting), O(n) space
fn reveal_cards(deck: Vec<i64>) -> Vec<i64> {
    let n = deck.len();
    let mut result: Vec<i64> = vec![0; n];
    let mut positions: VecDeque<usize> = (0..n).collect();
    let mut sorted = deck;
    sorted.sort();
    for card in sorted {
        let p = positions.pop_front().unwrap();
        result[p] = card;
        if let Some(q) = positions.pop_front() {
            positions.push_back(q);
        }
    }
    result
}

fn main() {
    println!("{:?}", reveal_cards(vec![17, 13, 11, 2, 3, 5, 7]));
}
