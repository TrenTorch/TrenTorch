// O(n + m) time, O(1) space
fn ransom_note(note: String, magazine: String) -> bool {
    let mut freq = [0i32; 26];
    for ch in magazine.bytes() {
        let idx = (ch - b'a') as usize;
        freq[idx] += 1;
    }
    for ch in note.bytes() {
        let idx = (ch - b'a') as usize;
        if freq[idx] == 0 {
            return false;
        }
        freq[idx] -= 1;
    }
    true
}

fn main() {
    println!("{:?}", ransom_note(String::from("aab"), String::from("baa")));
}
