// O(n log n) time, O(1) auxiliary space
fn car_fleet(target: i64, mut cars: Vec<Vec<i64>>) -> i64 {
    cars.sort_by(|a, b| b[0].cmp(&a[0]));
    let mut fleets = 0;
    let mut slow_num = 0;
    let mut slow_den = 1;
    for car in cars {
        let pos = car[0];
        let spd = car[1];
        let num = target - pos;
        let den = spd;
        if num * slow_den > slow_num * den {
            fleets += 1;
            slow_num = num;
            slow_den = den;
        }
    }
    fleets
}

fn main() {
    println!("{:?}", car_fleet(12, vec![vec![10, 2], vec![8, 4], vec![0, 1], vec![5, 1], vec![3, 3]]));
}
