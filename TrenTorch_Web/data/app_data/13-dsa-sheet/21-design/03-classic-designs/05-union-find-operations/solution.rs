// O(n + m α(n)) time, O(n) space
fn run_union_find(n: i64, ops: Vec<String>) -> Vec<i64> {
    let n_usize = n as usize;
    let mut parent: Vec<usize> = (0..n_usize).collect();
    let mut size: Vec<usize> = vec![1; n_usize];

    fn find(parent: &mut [usize], mut x: usize) -> usize {
        while parent[x] != x {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        x
    }

    let mut out = Vec::new();
    for op in ops {
        let parts: Vec<&str> = op.split_whitespace().collect();
        match parts[0] {
            "union" => {
                let a = parts[1].parse::<usize>().unwrap();
                let b = parts[2].parse::<usize>().unwrap();
                let ra = find(&mut parent, a);
                let rb = find(&mut parent, b);
                if ra != rb {
                    if size[ra] < size[rb] {
                        parent[ra] = rb;
                        size[rb] += size[ra];
                    } else {
                        parent[rb] = ra;
                        size[ra] += size[rb];
                    }
                }
            }
            "connected" => {
                let a = parts[1].parse::<usize>().unwrap();
                let b = parts[2].parse::<usize>().unwrap();
                let ra = find(&mut parent, a);
                let rb = find(&mut parent, b);
                out.push(if ra == rb { 1 } else { 0 });
            }
            "size" => {
                let a = parts[1].parse::<usize>().unwrap();
                let ra = find(&mut parent, a);
                out.push(size[ra] as i64);
            }
            _ => {}
        }
    }
    out
}

fn main() {
    println!("{:?}", run_union_find(5, vec![String::from("union 0 1"), String::from("union 1 2"), String::from("connected 0 2"), String::from("connected 0 3"), String::from("size 2")]));
}
