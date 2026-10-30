// O(n) time, O(1) space
fn my_atoi(s: String) -> i64 {
    let bytes = s.as_bytes();
    let n = bytes.len();
    let mut i = 0;

    // skip leading spaces
    while i < n && bytes[i] == b' ' {
        i += 1;
    }

    // sign
    let mut sign: i64 = 1;
    if i < n && (bytes[i] == b'+' || bytes[i] == b'-') {
        if bytes[i] == b'-' {
            sign = -1;
        }
        i += 1;
    }

    // digits
    let mut value: i64 = 0;
    while i < n {
        let c = bytes[i];
        if c >= b'0' && c <= b'9' {
            value = value * 10 + (c - b'0') as i64;
            i += 1;
            if value > (1i64 << 31) {
                break;
            }
        } else {
            break;
        }
    }

    value *= sign;

    let int_min: i64 = -(1i64 << 31);
    let int_max: i64 = (1i64 << 31) - 1;
    if value < int_min {
        int_min
    } else if value > int_max {
        int_max
    } else {
        value
    }
}

fn main() {
    println!("{:?}", my_atoi(String::from("42")));
}
