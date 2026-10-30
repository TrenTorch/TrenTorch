// O(n * Catalan(n)) time, O(n) extra space beyond the output
fn generate_parentheses(n: i64) -> Vec<String> {
    let n = n as usize;
    let mut out: Vec<String> = Vec::new();
    let mut prefix = String::new();
    paren_go(n, &mut prefix, 0, 0, &mut out);
    out
}

fn paren_go(n: usize, prefix: &mut String, opens: usize, closes: usize, out: &mut Vec<String>) {
    if prefix.len() == 2 * n {
        out.push(prefix.clone());
        return;
    }
    if opens < n {
        prefix.push('(');
        paren_go(n, prefix, opens + 1, closes, out);
        prefix.pop();
    }
    if closes < opens {
        prefix.push(')');
        paren_go(n, prefix, opens, closes + 1, out);
        prefix.pop();
    }
}

fn main() {
    println!("{:?}", generate_parentheses(3));
}
