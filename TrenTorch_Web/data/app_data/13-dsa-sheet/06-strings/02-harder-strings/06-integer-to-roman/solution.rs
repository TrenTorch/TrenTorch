// O(1) time, O(1) space (the output has at most 15 symbols)
fn integer_to_roman(num: i64) -> String {
    const TABLE: [(i64, &str); 13] = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ];
    let mut remaining = num;
    let mut out = String::new();
    for &(value, symbol) in TABLE.iter() {
        let count = remaining / value;
        remaining %= value;
        for _ in 0..count {
            out.push_str(symbol);
        }
    }
    out
}

fn main() {
    println!("{:?}", integer_to_roman(3));
}
