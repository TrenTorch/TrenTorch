// O(n) time, O(1) space
fn partition_labels(s: String) -> Vec<i64> {
    let bytes = s.as_bytes();
    let mut last = [0usize; 26];
    for (i, &b) in bytes.iter().enumerate() {
        last[(b - b'a') as usize] = i;
    }
    let mut sizes = Vec::new();
    let mut start = 0;
    let mut end = 0;
    for (i, &b) in bytes.iter().enumerate() {
        let idx = (b - b'a') as usize;
        if last[idx] > end {
            end = last[idx];
        }
        if i == end {
            sizes.push((end - start + 1) as i64);
            start = i + 1;
        }
    }
    sizes
}

fn main() {
    println!("{:?}", partition_labels(String::from("ababcbacadefegdehijhklij")));
}
