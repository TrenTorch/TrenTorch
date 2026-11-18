// O(n) time, O(n) space
fn asteroid_collision(asteroids: Vec<i64>) -> Vec<i64> {
    let mut stack: Vec<i64> = Vec::with_capacity(asteroids.len());
    for a in asteroids {
        let mut alive = true;
        while alive && a < 0 && !stack.is_empty() && *stack.last().unwrap() > 0 {
            let top = *stack.last().unwrap();
            if top < -a {
                stack.pop();
            } else if top == -a {
                stack.pop();
                alive = false;
            } else {
                alive = false;
            }
        }
        if alive {
            stack.push(a);
        }
    }
    stack
}

fn main() {
    println!("{:?}", asteroid_collision(vec![5, 10, -5]));
}
