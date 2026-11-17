// O(n) time, O(n) space
fn simplify_path(path: String) -> String {
    let mut stack: Vec<&str> = Vec::new();
    for name in path.split('/') {
        if name == ".." {
            stack.pop();
        } else if !name.is_empty() && name != "." {
            stack.push(name);
        }
    }
    let mut out = String::new();
    for name in &stack {
        out.push('/');
        out.push_str(name);
    }
    if out.is_empty() {
        out.push('/');
    }
    out
}

fn main() {
    println!("{:?}", simplify_path(String::from("/home/")));
}
