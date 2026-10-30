// O(len(haystack) + len(needle)) time, O(len(needle)) space
fn find_needle(haystack: String, needle: String) -> i64 {
    let h = haystack.as_bytes();
    let nd = needle.as_bytes();
    if nd.is_empty() {
        return 0;
    }
    let m = nd.len();
    let mut fail = vec![0usize; m];
    let mut k = 0usize;
    for i in 1..m {
        while k > 0 && nd[i] != nd[k] {
            k = fail[k - 1];
        }
        if nd[i] == nd[k] {
            k += 1;
        }
        fail[i] = k;
    }
    k = 0;
    for (i, &ch) in h.iter().enumerate() {
        while k > 0 && ch != nd[k] {
            k = fail[k - 1];
        }
        if ch == nd[k] {
            k += 1;
        }
        if k == m {
            return (i + 1 - k) as i64;
        }
    }
    -1
}

fn main() {
    println!("{:?}", find_needle(String::from("sadbutsad"), String::from("sad")));
}
