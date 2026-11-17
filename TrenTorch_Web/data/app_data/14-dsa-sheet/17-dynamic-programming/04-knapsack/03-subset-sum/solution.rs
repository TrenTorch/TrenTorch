// O(n * target / 64) time, O(target / 64) space
fn subset_sum(nums: Vec<i64>, target: i64) -> bool {
    if target < 0 {
        return false;
    }
    if target == 0 {
        return true;
    }
    let target = target as usize;
    let words = (target + 64) / 64;
    let mut bits = vec![0u64; words];
    let mut shifted = vec![0u64; words];
    bits[0] = 1;

    for &x in &nums {
        let x = x as usize;
        if x > target {
            continue;
        }
        let word_shift = x / 64;
        let bit_shift = x % 64;

        for w in &mut shifted {
            *w = 0;
        }

        for i in 0..words {
            let src = i as isize - word_shift as isize;
            if src >= 0 {
                let src = src as usize;
                shifted[i] = bits[src] << bit_shift;
                if bit_shift != 0 && src > 0 {
                    shifted[i] |= bits[src - 1] >> (64 - bit_shift);
                }
            }
        }

        let excess = words * 64 - (target + 1);
        if excess > 0 {
            let mask = !0u64 >> excess;
            shifted[words - 1] &= mask;
        }

        for i in 0..words {
            bits[i] |= shifted[i];
        }
    }

    let word = target / 64;
    let bit = target % 64;
    (bits[word] >> bit) & 1 == 1
}

fn main() {
    println!("{:?}", subset_sum(vec![3, 34, 4, 12, 5, 2], 9));
}
