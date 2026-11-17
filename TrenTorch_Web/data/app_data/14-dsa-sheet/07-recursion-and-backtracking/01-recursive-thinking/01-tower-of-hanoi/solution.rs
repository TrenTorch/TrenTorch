// O(2^n) time, O(2^n) space
fn tower_of_hanoi(n: i64) -> Vec<Vec<i64>> {
    fn move_disks(k: i64, source: i64, target: i64, spare: i64, moves: &mut Vec<Vec<i64>>) {
        if k == 0 {
            return;
        }
        move_disks(k - 1, source, spare, target, moves);
        moves.push(vec![source, target]);
        move_disks(k - 1, spare, target, source, moves);
    }

    let mut moves: Vec<Vec<i64>> = Vec::new();
    move_disks(n, 1, 3, 2, &mut moves);
    moves
}

fn main() {
    println!("{:?}", tower_of_hanoi(2));
}
