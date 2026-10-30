use std::collections::BinaryHeap;
use std::cmp::Reverse;

// O(n log k) time, O(k) space where k = min(ladders, number of climbs)
fn furthest_building(heights: Vec<i64>, bricks: i64, ladders: i64) -> i64 {
    let mut heap = BinaryHeap::new();
    let mut bricks = bricks;
    for i in 1..heights.len() {
        let climb = heights[i] - heights[i - 1];
        if climb <= 0 {
            continue;
        }
        heap.push(Reverse(climb));
        if heap.len() > ladders as usize {
            if let Some(Reverse(smallest)) = heap.pop() {
                bricks -= smallest;
                if bricks < 0 {
                    return (i - 1) as i64;
                }
            }
        }
    }
    (heights.len() - 1) as i64
}

fn main() {
    println!("{:?}", furthest_building(vec![4, 2, 7, 6, 9, 14, 12], 5, 1));
}
