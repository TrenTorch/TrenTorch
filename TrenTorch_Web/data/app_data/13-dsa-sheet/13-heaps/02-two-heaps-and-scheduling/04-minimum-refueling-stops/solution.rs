use std::collections::BinaryHeap;

// O(n log n) time, O(n) space
fn min_refuel_stops(target: i64, start_fuel: i64, stations: Vec<Vec<i64>>) -> i64 {
    let mut heap: BinaryHeap<i64> = BinaryHeap::new();
    let mut reach = start_fuel;
    let mut stops: i64 = 0;
    let mut i: usize = 0;
    while reach < target {
        while i < stations.len() && stations[i][0] <= reach {
            heap.push(stations[i][1]);
            i += 1;
        }
        match heap.pop() {
            None => return -1,
            Some(fuel) => {
                reach += fuel;
                stops += 1;
            }
        }
    }
    stops
}

fn main() {
    println!("{:?}", min_refuel_stops(100, 10, vec![vec![10, 60], vec![20, 30], vec![30, 30], vec![60, 40]]));
}
