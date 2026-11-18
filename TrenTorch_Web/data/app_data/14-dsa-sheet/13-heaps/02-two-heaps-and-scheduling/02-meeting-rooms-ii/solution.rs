use std::collections::BinaryHeap;
use std::cmp::Reverse;

// O(n log n) time, O(n) space
fn min_meeting_rooms(meetings: Vec<Vec<i64>>) -> i64 {
    let mut meetings = meetings;
    meetings.sort_by_key(|m| m[0]);
    let mut heap = BinaryHeap::new();
    for meeting in meetings {
        let start = meeting[0];
        let end = meeting[1];
        if let Some(&Reverse(min_end)) = heap.peek() {
            if min_end <= start {
                heap.pop();
                heap.push(Reverse(end));
            } else {
                heap.push(Reverse(end));
            }
        } else {
            heap.push(Reverse(end));
        }
    }
    heap.len() as i64
}

fn main() {
    println!("{:?}", min_meeting_rooms(vec![vec![0, 30], vec![5, 10], vec![15, 20]]));
}
