// O(n) time, O(1) space
function gasStation(gas, cost) {
    let total = 0, tank = 0, start = 0;
    for (let i = 0; i < gas.length; i++) {
        const diff = gas[i] - cost[i];
        total += diff;
        tank += diff;
        if (tank < 0) {
            start = i + 1;
            tank = 0;
        }
    }
    return (total >= 0 && gas.length > 0) ? start : -1;
}

console.log(gasStation([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]));
