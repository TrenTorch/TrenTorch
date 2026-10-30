// O(n * S) time, O(S) space where S = sum(nums)
fn min_subset_difference(nums: Vec<i64>) -> i64 {
    let total: i64 = nums.iter().sum();
    if total == 0 {
        return 0;
    }
    let total_usize = total as usize;
    let word_count = (total_usize + 64) / 64;
    let mut bits = vec![0u64; word_count];
    bits[0] = 1; // bit 0 set

    for &x in &nums {
        let x = x as usize;
        let shift_words = x / 64;
        let shift_bits = x % 64;
        let mut shifted = vec![0u64; word_count];
        if shift_bits == 0 {
            for i in 0..word_count {
                let j = i + shift_words;
                if j < word_count {
                    shifted[j] = bits[i];
                }
            }
        } else {
            for i in 0..word_count {
                let j = i + shift_words;
                if j < word_count {
                    shifted[j] |= bits[i] << shift_bits;
                }
                if j + 1 < word_count {
                    shifted[j + 1] |= bits[i] >> (64 - shift_bits);
                }
            }
        }
        for i in 0..word_count {
            bits[i] |= shifted[i];
        }
    }

    for s in (0..=total_usize / 2).rev() {
        let word = s / 64;
        let bit = s % 64;
        if (bits[word] >> bit) & 1 != 0 {
            return total - 2 * (s as i64);
        }
    }
    total
}

fn main() {
    println!("{:?}", min_subset_difference(vec![1, 6, 11, 5]));
}
