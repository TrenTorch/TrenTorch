// O(n) time, O(1) space
fn equations_possible(equations: Vec<String>) -> bool {
    let mut parent: [usize; 26] = [0; 26];
    for i in 0..26 {
        parent[i] = i;
    }

    fn find(parent: &mut [usize; 26], mut x: usize) -> usize {
        while parent[x] != x {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        x
    }

    for eq in &equations {
        let bytes = eq.as_bytes();
        if bytes[1] == b'=' {
            let a = (bytes[0] - b'a') as usize;
            let b = (bytes[3] - b'a') as usize;
            let root_a = find(&mut parent, a);
            let root_b = find(&mut parent, b);
            parent[root_a] = root_b;
        }
    }

    for eq in &equations {
        let bytes = eq.as_bytes();
        if bytes[1] == b'!' {
            let a = (bytes[0] - b'a') as usize;
            let b = (bytes[3] - b'a') as usize;
            if find(&mut parent, a) == find(&mut parent, b) {
                return false;
            }
        }
    }

    true
}

fn main() {
    println!("{:?}", equations_possible(vec![String::from("a==b"), String::from("b!=a")]));
}
