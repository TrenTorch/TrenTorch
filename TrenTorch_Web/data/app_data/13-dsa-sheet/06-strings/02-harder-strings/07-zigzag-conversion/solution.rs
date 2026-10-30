// O(n) time, O(n) space
fn zigzag_conversion(s: String, rows: i64) -> String {
    if rows == 1 || (rows as usize) >= s.len() {
        return s;
    }
    let rows = rows as usize;
    let mut lines: Vec<Vec<u8>> = vec![Vec::new(); rows];
    let mut row: usize = 0;
    let mut step: i64 = 1;
    for &ch in s.as_bytes() {
        lines[row].push(ch);
        if row == 0 {
            step = 1;
        } else if row == rows - 1 {
            step = -1;
        }
        row = ((row as i64) + step) as usize;
    }
    let out: Vec<u8> = lines.into_iter().flatten().collect();
    String::from_utf8(out).unwrap()
}

fn main() {
    println!("{:?}", zigzag_conversion(String::from("PAYPALISHIRING"), 3));
}
