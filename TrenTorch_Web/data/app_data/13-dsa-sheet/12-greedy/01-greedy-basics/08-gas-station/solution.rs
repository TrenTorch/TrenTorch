// O(n) time, O(1) space
fn gas_station(gas: Vec<i64>, cost: Vec<i64>) -> i64 {
    let n = gas.len();
    if n == 0 {
        return -1;
    }
    let mut total = 0i64;
    let mut tank = 0i64;
    let mut start = 0usize;
    for i in 0..n {
        let diff = gas[i] - cost[i];
        total += diff;
        tank += diff;
        if tank < 0 {
            start = i + 1;
            tank = 0;
        }
    }
    if total >= 0 {
        start as i64
    } else {
        -1
    }
}

fn main() {
    println!("{:?}", gas_station(vec![1, 2, 3, 4, 5], vec![3, 4, 5, 1, 2]));
}
