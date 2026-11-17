// O(n + m) time, O(1) space
fn check_inclusion(s1: String, s2: String) -> bool {
    let m = s1.len();
    let n = s2.len();
    if m > n {
        return false;
    }
    if m == 0 {
        return true;
    }

    let s1_bytes = s1.as_bytes();
    let s2_bytes = s2.as_bytes();

    let mut need = [0; 26];
    let mut window = [0; 26];

    for &ch in s1_bytes {
        need[(ch - b'a') as usize] += 1;
    }

    for i in 0..n {
        window[(s2_bytes[i] - b'a') as usize] += 1;

        if i >= m {
            window[(s2_bytes[i - m] - b'a') as usize] -= 1;
        }

        if i >= m - 1 && window == need {
            return true;
        }
    }

    false
}

fn main() {
    println!("{:?}", check_inclusion(String::from("ab"), String::from("eidbaooo")));
}
