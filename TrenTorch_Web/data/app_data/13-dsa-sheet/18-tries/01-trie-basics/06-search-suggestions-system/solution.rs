// O(n log n + m log n + m * k) time, O(n) space (k = 3 suggestions per prefix)
fn suggested_products(products: Vec<String>, search_word: String) -> Vec<Vec<String>> {
    let mut products = products;
    products.sort();
    let mut out: Vec<Vec<String>> = Vec::new();
    for i in 1..=search_word.len() {
        let prefix: &str = &search_word[..i];
        let start = products.partition_point(|p| p.as_str() < prefix);
        let end = std::cmp::min(start + 3, products.len());
        let suggestions: Vec<String> = products[start..end]
            .iter()
            .filter(|p| p.starts_with(prefix))
            .cloned()
            .collect();
        out.push(suggestions);
    }
    out
}

fn main() {
    println!("{:?}", suggested_products(vec![String::from("mobile"), String::from("mouse"), String::from("moneypot"), String::from("monitor"), String::from("mousepad")], String::from("mouse")));
}
