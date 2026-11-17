// O(log s) per get where s is the number of changes at that index, O(total ops) space
fn run_snapshot_array(length: i64, ops: Vec<String>) -> Vec<i64> {
    // per index: (snapshot id, value) pairs in increasing snapshot order
    let mut history: Vec<Vec<(i64, i64)>> = vec![Vec::new(); length as usize];
    let mut snap_id: i64 = 0;
    let mut out: Vec<i64> = Vec::new();
    for op in ops.iter() {
        let parts: Vec<&str> = op.split_whitespace().collect();
        match parts[0] {
            "set" => {
                let i: usize = parts[1].parse().unwrap();
                let v: i64 = parts[2].parse().unwrap();
                let list = &mut history[i];
                let same_snap = matches!(list.last(), Some(&(sid, _)) if sid == snap_id);
                if same_snap {
                    list.last_mut().unwrap().1 = v;
                } else {
                    list.push((snap_id, v));
                }
            }
            "snap" => {
                out.push(snap_id);
                snap_id += 1;
            }
            _ => {
                let i: usize = parts[1].parse().unwrap();
                let want: i64 = parts[2].parse().unwrap();
                let list = &history[i];
                let k = list.partition_point(|&(sid, _)| sid <= want);
                out.push(if k > 0 { list[k - 1].1 } else { 0 });
            }
        }
    }
    out
}

fn main() {
    println!("{:?}", run_snapshot_array(3, vec![String::from("set 0 5"), String::from("snap"), String::from("set 0 6"), String::from("get 0 0"), String::from("snap"), String::from("get 0 1")]));
}
