// O((n + q) log n) time, O(n) space
fn run_range_add(n: i64, ops: Vec<String>) -> Vec<i64> {
    let n_usize = n as usize;
    let mut tree = vec![0i64; n_usize + 2];
    let mut out = Vec::new();

    for op in ops {
        let parts: Vec<&str> = op.split_whitespace().collect();
        if parts[0] == "add" {
            let left = parts[1].parse::<usize>().unwrap();
            let right = parts[2].parse::<usize>().unwrap();
            let v = parts[3].parse::<i64>().unwrap();

            // add(left, v)
            let mut idx = left + 1;
            while idx <= n_usize + 1 {
                tree[idx] += v;
                idx += idx & idx.wrapping_neg();
            }
            // add(right + 1, -v)
            let mut idx = right + 2;
            while idx <= n_usize + 1 {
                tree[idx] -= v;
                idx += idx & idx.wrapping_neg();
            }
        } else if parts[0] == "get" {
            let i = parts[1].parse::<usize>().unwrap();
            let mut idx = i + 1;
            let mut total = 0i64;
            while idx > 0 {
                total += tree[idx];
                idx -= idx & idx.wrapping_neg();
            }
            out.push(total);
        }
    }
    out
}

fn main() {
    println!("{:?}", run_range_add(5, vec![String::from("add 1 3 10"), String::from("get 2"), String::from("add 0 4 -1"), String::from("get 0"), String::from("get 3")]));
}
