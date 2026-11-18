// O(n * S / 64) time, O(S / 64) space (S = sum of nums; bitset of reachable sums)
fn can_partition(nums: Vec<i64>) -> bool {
    let total: i64 = nums.iter().sum();
    if total % 2 != 0 {
        return false;
    }
    let target = (total / 2) as usize;
    let words = (total as usize) / 64 + 2;
    let mut bits = vec![0u64; words];
    bits[0] = 1;
    for &x in &nums {
        if x == 0 {
            continue;
        }
        shift_or(&mut bits, x as usize);
    }
    (bits[target / 64] >> (target % 64)) & 1 == 1
}

// bits |= bits << shift, done in place from the high words down
fn shift_or(bits: &mut [u64], shift: usize) {
    let ws = shift / 64;
    let bs = shift % 64;
    for j in (0..bits.len()).rev() {
        if j < ws {
            break;
        }
        let mut incoming = bits[j - ws] << bs;
        if bs > 0 && j > ws {
            incoming |= bits[j - ws - 1] >> (64 - bs);
        }
        bits[j] |= incoming;
    }
}

fn main() {
    println!("{:?}", can_partition(vec![1, 5, 11, 5]));
}
