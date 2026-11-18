// O(L) time per step where L is the length of the current term, O(L) space
fn count_and_say(n: i64) -> String {
    let mut term: Vec<u8> = b"1".to_vec();
    for _ in 1..n {
        let mut next: Vec<u8> = Vec::new();
        let mut i: usize = 0;
        while i < term.len() {
            let digit = term[i];
            let mut run: usize = 0;
            while i < term.len() && term[i] == digit {
                run += 1;
                i += 1;
            }
            next.extend_from_slice(run.to_string().as_bytes());
            next.push(digit);
        }
        term = next;
    }
    String::from_utf8(term).unwrap()
}

fn main() {
    println!("{:?}", count_and_say(4));
}
