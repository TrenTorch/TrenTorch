// O(n*m) time, O(n+m) space
fn multiply_strings(a: String, b: String) -> String {
    if a == "0" || b == "0" {
        return "0".to_string();
    }
    const BASE: u32 = 10_000;
    const WIDTH: usize = 4;

    fn str_to_blocks(s: &str, width: usize) -> Vec<u32> {
        let mut blocks = Vec::new();
        let mut i = s.len();
        while i > 0 {
            let start = if i >= width { i - width } else { 0 };
            let chunk = &s[start..i];
            let val = chunk.parse::<u32>().unwrap();
            blocks.push(val);
            i = start;
        }
        blocks
    }

    fn multiply_blocks(a: &[u32], b: &[u32], base: u64) -> Vec<u64> {
        let mut result = vec![0u64; a.len() + b.len()];
        for (i, &av) in a.iter().enumerate() {
            for (j, &bv) in b.iter().enumerate() {
                result[i + j] += av as u64 * bv as u64;
            }
        }
        let mut carry = 0u64;
        for k in 0..result.len() {
            let total = result[k] + carry;
            result[k] = total % base;
            carry = total / base;
        }
        while carry > 0 {
            result.push(carry % base);
            carry /= base;
        }
        while let Some(&0) = result.last() {
            result.pop();
        }
        result
    }

    fn blocks_to_string(blocks: &[u64], width: usize) -> String {
        if blocks.is_empty() {
            return "0".to_string();
        }
        let mut s = String::new();
        let mut i = blocks.len();
        while i > 0 && blocks[i - 1] == 0 {
            i -= 1;
        }
        if i == 0 {
            return "0".to_string();
        }
        s.push_str(&blocks[i - 1].to_string());
        for idx in (0..i - 1).rev() {
            s.push_str(&format!("{:0width$}", blocks[idx], width = width));
        }
        s
    }

    let a_blocks = str_to_blocks(&a, WIDTH);
    let b_blocks = str_to_blocks(&b, WIDTH);
    let prod_blocks = multiply_blocks(&a_blocks, &b_blocks, BASE as u64);
    blocks_to_string(&prod_blocks, WIDTH)
}

fn main() {
    println!("{:?}", multiply_strings(String::from("123"), String::from("456")));
}
