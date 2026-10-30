use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap};

// Dual-heap median with lazy deletion (same algorithm as the Python solution)
struct SlidingMedian {
    small: BinaryHeap<i64>,          // max-heap of the lower half
    large: BinaryHeap<Reverse<i64>>, // min-heap of the upper half
    delayed: HashMap<i64, i64>,      // value -> copies that left the window but are still in a heap
    size_small: i64,
    size_large: i64,
    k: usize,
}

impl SlidingMedian {
    fn new(k: usize) -> Self {
        SlidingMedian {
            small: BinaryHeap::new(),
            large: BinaryHeap::new(),
            delayed: HashMap::new(),
            size_small: 0,
            size_large: 0,
            k,
        }
    }

    fn clean_small(&mut self) {
        while let Some(&top) = self.small.peek() {
            match self.delayed.get_mut(&top) {
                Some(c) if *c > 0 => {
                    *c -= 1;
                    self.small.pop();
                }
                _ => break,
            }
        }
    }

    fn clean_large(&mut self) {
        while let Some(&Reverse(top)) = self.large.peek() {
            match self.delayed.get_mut(&top) {
                Some(c) if *c > 0 => {
                    *c -= 1;
                    self.large.pop();
                }
                _ => break,
            }
        }
    }

    fn balance(&mut self) {
        if self.size_small > self.size_large + 1 {
            let v = self.small.pop().unwrap();
            self.large.push(Reverse(v));
            self.size_small -= 1;
            self.size_large += 1;
            self.clean_small();
        } else if self.size_small < self.size_large {
            let Reverse(v) = self.large.pop().unwrap();
            self.small.push(v);
            self.size_large -= 1;
            self.size_small += 1;
            self.clean_large();
        }
    }

    fn add(&mut self, x: i64) {
        let goes_small = match self.small.peek() {
            None => true,
            Some(&top) => x <= top,
        };
        if goes_small {
            self.small.push(x);
            self.size_small += 1;
        } else {
            self.large.push(Reverse(x));
            self.size_large += 1;
        }
        self.balance();
    }

    fn remove(&mut self, x: i64) {
        *self.delayed.entry(x).or_insert(0) += 1;
        let small_top = *self.small.peek().unwrap();
        if x <= small_top {
            self.size_small -= 1;
            if x == small_top {
                self.clean_small();
            }
        } else {
            self.size_large -= 1;
            let large_top = self.large.peek().unwrap().0;
            if x == large_top {
                self.clean_large();
            }
        }
        self.balance();
    }

    fn median(&self) -> f64 {
        let small_top = *self.small.peek().unwrap();
        if self.k % 2 == 1 {
            small_top as f64
        } else {
            let large_top = self.large.peek().unwrap().0;
            (small_top + large_top) as f64 / 2.0
        }
    }
}

// O(n log k) time, O(k) space
fn median_sliding_window(nums: Vec<i64>, k: i64) -> Vec<f64> {
    let k = k as usize;
    let mut sm = SlidingMedian::new(k);
    for &x in &nums[..k] {
        sm.add(x);
    }
    let mut out: Vec<f64> = Vec::with_capacity(nums.len() - k + 1);
    out.push(sm.median());
    for i in k..nums.len() {
        sm.add(nums[i]);
        sm.remove(nums[i - k]);
        out.push(sm.median());
    }
    out
}

fn main() {
    println!("{:?}", median_sliding_window(vec![1, 3, -1, -3, 5, 3, 6, 7], 3));
}
