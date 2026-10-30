// O(n) time, O(n) space where n = row
fn pascal_row(row: i64) -> Vec<i64> {
    let mut out = Vec::with_capacity((row + 1) as usize);
    let mut value = 1i64;
    for i in 0..=row {
        out.push(value);
        if i != row {
            value = value * (row - i) / (i + 1);
        }
    }
    out
}

fn main() {
    println!("{:?}", pascal_row(4));
}
