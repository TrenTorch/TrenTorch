// O(n) time, O(n) space (Manacher's algorithm)
fn count_palindromes_fast(s: String) -> i64 {
    let b = s.as_bytes();
    let n = b.len() as i64;
    let mut total: i64 = 0;

    let mut d1 = vec![0i64; n as usize];
    let (mut left, mut right): (i64, i64) = (0, -1);
    for i in 0..n {
        let mut k: i64 = if i > right {
            1
        } else {
            std::cmp::min(d1[(left + right - i) as usize], right - i + 1)
        };
        while i - k >= 0 && i + k < n && b[(i - k) as usize] == b[(i + k) as usize] {
            k += 1;
        }
        d1[i as usize] = k;
        total += k;
        if i + k - 1 > right {
            left = i - k + 1;
            right = i + k - 1;
        }
    }

    let mut d2 = vec![0i64; n as usize];
    left = 0;
    right = -1;
    for i in 0..n {
        let mut k: i64 = if i > right {
            0
        } else {
            std::cmp::min(d2[(left + right - i + 1) as usize], right - i + 1)
        };
        while i - k - 1 >= 0 && i + k < n && b[(i - k - 1) as usize] == b[(i + k) as usize] {
            k += 1;
        }
        d2[i as usize] = k;
        total += k;
        if i + k - 1 > right {
            left = i - k;
            right = i + k - 1;
        }
    }
    total
}

fn main() {
    println!("{:?}", count_palindromes_fast(String::from("aaa")));
}
