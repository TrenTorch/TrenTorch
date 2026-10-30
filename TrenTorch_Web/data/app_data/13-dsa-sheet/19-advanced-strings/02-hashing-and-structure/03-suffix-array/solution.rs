// O(n log n) time, O(n) space
fn suffix_array(s: String) -> Vec<i64> {
    if s.is_empty() {
        return Vec::new();
    }
    let mut text: Vec<usize> = s.chars().map(|c| c as usize + 1).collect();
    text.push(0); // sentinel
    let n = text.len();
    let mut order = vec![0; n];
    let mut cls = vec![0; n];

    // initial counting sort by first character
    let max_val = *text.iter().max().unwrap();
    let size = (max_val + 1).max(n);
    let mut count = vec![0; size];
    for &v in &text {
        count[v] += 1;
    }
    for i in 1..size {
        count[i] += count[i - 1];
    }
    for i in (0..n).rev() {
        let v = text[i];
        count[v] -= 1;
        order[count[v]] = i;
    }

    // assign initial classes
    let mut classes = 1;
    cls[order[0]] = 0;
    for i in 1..n {
        if text[order[i]] != text[order[i - 1]] {
            classes += 1;
        }
        cls[order[i]] = classes - 1;
    }

    // doubling
    let mut shift = 1;
    while shift < n {
        // sort by second half (shifted positions)
        let mut by_second = vec![0; n];
        for i in 0..n {
            by_second[i] = (order[i] + n - shift) % n;
        }

        // counting sort by class of first half
        count = vec![0; classes];
        for i in 0..n {
            count[cls[by_second[i]]] += 1;
        }
        for i in 1..classes {
            count[i] += count[i - 1];
        }
        for i in (0..n).rev() {
            let c = cls[by_second[i]];
            count[c] -= 1;
            order[count[c]] = by_second[i];
        }

        // recompute classes
        let mut new_cls = vec![0; n];
        classes = 1;
        new_cls[order[0]] = 0;
        for i in 1..n {
            let a = order[i];
            let b = order[i - 1];
            if (cls[a], cls[(a + shift) % n]) != (cls[b], cls[(b + shift) % n]) {
                classes += 1;
            }
            new_cls[a] = classes - 1;
        }
        cls = new_cls;
        shift *= 2;
    }

    // order[0] is the sentinel position; return the rest as i64
    order[1..].iter().map(|&x| x as i64).collect()
}

fn main() {
    println!("{:?}", suffix_array(String::from("banana")));
}
