// O(n) time, O(1) space
function lemonadeChange(bills) {
    let fives = 0;
    let tens = 0;
    for (const bill of bills) {
        if (bill === 5) {
            fives++;
        } else if (bill === 10) {
            if (fives === 0) return false;
            fives--;
            tens++;
        } else {
            if (tens > 0 && fives > 0) {
                tens--;
                fives--;
            } else if (fives >= 3) {
                fives -= 3;
            } else {
                return false;
            }
        }
    }
    return true;
}

console.log(lemonadeChange([5, 5, 5, 10, 20]));
