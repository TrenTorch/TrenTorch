// O(n log n) time, O(n) space
fn sort_records(records: Vec<(String, i64)>) -> Vec<String> {
    let mut recs = records;
    recs.sort_by(|a, b| {
        match b.1.cmp(&a.1) {
            std::cmp::Ordering::Equal => a.0.cmp(&b.0),
            ord => ord,
        }
    });
    recs.into_iter().map(|(name, _)| name).collect()
}

fn main() {
}
