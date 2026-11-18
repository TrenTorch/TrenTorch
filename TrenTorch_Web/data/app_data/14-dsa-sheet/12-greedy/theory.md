> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Greedy algorithms)

This page teaches greedy algorithms: solving a problem by making the choice that looks best right now, again and again, and never going back. When this works it gives very short and very fast programs. When it does not work it gives wrong answers that look convincing, so the page also teaches you how to tell the two cases apart.

The page is a staircase. **Chapter 1 is gentle**: change-making with coins, handing out cookies, and giving change at a lemonade stand, with no proofs. Chapter 2 asks the key question, "when is a greedy choice safe?", and introduces the exchange argument in plain words. The later chapters collect the classic families: choosing intervals, jumping and driving along a line, scanning in two directions, counting and scheduling, and finally ordering things with a custom comparison. Every code example is shown in Python and in C++, so pick whichever you like.

# Chapter 1. Taking the best bite now

## 1.1 The idea of a greedy choice

Imagine you must pay 70 rupees using as few notes and coins as possible. You have 1, 2, 5, 10, 20, 50, 100, 500 and 2000 rupee pieces. Nobody needs a computer to solve this: you grab the biggest piece that still fits, which is the 50. Twenty remains, so you grab the biggest piece that still fits, which is the 20. Done: two pieces.

That is a **greedy algorithm**. At every step it makes the **locally best choice**, the one that looks best right now, never reconsiders it, and hopes that all those small good choices add up to a good final answer. The rest of this page is about the hope: sometimes it is true and sometimes it is not.

## 1.2 Fewest coins and notes

For 121 rupees the same recipe gives 100 (21 left), then 20 (1 left), then 1. Three pieces. In code, for each value from the biggest to the smallest we take as many as fit: `amount // value` of them (integer division), and the leftover is `amount % value`.

This is exactly the problem _Fewest Coins and Notes_.

```python
def fewest_notes(amount):
    values = [2000, 500, 100, 50, 20, 10, 5, 2, 1]
    count = 0
    for v in values:
        count += amount // v     # how many of this value fit
        amount %= v              # what is left to pay
    return count


assert fewest_notes(70) == 2
assert fewest_notes(121) == 3
assert fewest_notes(0) == 0
assert fewest_notes(2000) == 1
```

```cpp
int fewest_notes(long long amount) {
    int values[] = {2000, 500, 100, 50, 20, 10, 5, 2, 1};
    long long count = 0;
    for (int v : values) {
        count += amount / v;     // how many of this value fit
        amount %= v;             // what is left to pay
    }
    return (int)count;
}
```

There are only nine values, so the time is $O(1)$ and the space is $O(1)$. For these particular values greedy is always right; in Chapter 2 we will see that it is not true for every set of coins.

## 1.3 Sort first, then be greedy

Many greedy algorithms begin with a sort, so that "the best choice" is easy to find. Let's take a story. Each child has a greed number: the smallest cookie size that will make them happy. Each cookie has a size. A cookie goes to one child at most, and a child gets one cookie at most. We want as many happy children as possible.

A good strategy: sort the children by greed and the cookies by size. Then look at the cookies from smallest to largest. If the current cookie is big enough for the _least greedy child still waiting_, give it to them. If not, this cookie is too small for everybody waiting (they are all at least as greedy), so throw it away and move on. We never waste a big cookie on a child who would have been happy with a small one.

For greed `[1, 2, 3]` and cookies `[1, 1]`: the first cookie (1) satisfies the child with greed 1. The second cookie (1) is too small for the child with greed 2. So the answer is 1.

This is exactly the problem _Assign Cookies_.

```python
def assign_cookies(greed, sizes):
    greed = sorted(greed)
    sizes = sorted(sizes)
    child = 0                       # the next child still waiting
    for s in sizes:
        if child < len(greed) and s >= greed[child]:
            child += 1              # this cookie makes that child happy
    return child


assert assign_cookies([1, 2, 3], [1, 1]) == 1
assert assign_cookies([1, 2], [1, 2, 3]) == 2
assert assign_cookies([5], []) == 0
```

```cpp
int assign_cookies(vector<int> greed, vector<int> sizes) {
    sort(greed.begin(), greed.end());
    sort(sizes.begin(), sizes.end());
    int child = 0;                  // the next child still waiting
    for (int s : sizes) {
        if (child < (int)greed.size() && s >= greed[child]) {
            child++;                // this cookie makes that child happy
        }
    }
    return child;
}
```

Sorting costs $O(n \log n + m \log m)$ for $n$ children and $m$ cookies, and the loop is $O(m)$. The space is $O(1)$ extra apart from the sorted copies.

## 1.4 Greedy with a small memory

Greedy choices sometimes depend on a little bit of state. A lemonade costs 5. Customers line up, each paying with a 5, 10 or 20 bill, and we start with no money. We must give correct change, using bills we have already received.

Handling a 5 needs no change. A 10 needs one 5 back. A 20 needs 15 back, and there are two ways: one 10 and one 5, or three 5s. Which is better? Fives are the more valuable bills, since they are the only ones that can make change for a 10, while a 10 is useful only for change on a 20. So greedily use the 10 first, and keep the 5s for later. If neither way works, we fail.

For `[5, 5, 10, 10, 20]`: we have two 5s, then take the 10 and give a 5 (one 5 left, one 10), take another 10 and give the last 5 (no 5s, two 10s), then a 20 needs 15: no 5s, so we fail. The answer is `False`.

This is exactly the problem _Lemonade Stand Change_.

```python
def lemonade_change(bills):
    fives = tens = 0
    for bill in bills:
        if bill == 5:
            fives += 1
        elif bill == 10:
            if fives == 0:
                return False
            fives -= 1
            tens += 1
        else:                                   # a 20 needs 15 back
            if tens > 0 and fives > 0:
                tens -= 1
                fives -= 1                      # prefer 10 + 5
            elif fives >= 3:
                fives -= 3
            else:
                return False
    return True


assert lemonade_change([5, 5, 5, 10, 20]) is True
assert lemonade_change([5, 5, 10, 10, 20]) is False
assert lemonade_change([10]) is False
```

```cpp
bool lemonade_change(const vector<int>& bills) {
    int fives = 0, tens = 0;
    for (int bill : bills) {
        if (bill == 5) {
            fives++;
        } else if (bill == 10) {
            if (fives == 0) return false;
            fives--;
            tens++;
        } else {                                // a 20 needs 15 back
            if (tens > 0 && fives > 0) {
                tens--;
                fives--;                        // prefer 10 + 5
            } else if (fives >= 3) {
                fives -= 3;
            } else {
                return false;
            }
        }
    }
    return true;
}
```

One pass: time $O(n)$ and space $O(1)$.

## 1.5 Check yourself

1. How many pieces does greedy use to pay 2763 rupees with the values from 1.2?
2. In _Assign Cookies_, why is it safe to throw away a cookie that is too small for the least greedy waiting child?
3. Why is it better to give a 10 and a 5, rather than three 5s, as change for a 20?
4. What are the two things a greedy algorithm never does?

# Chapter 2. When greedy works, and why

## 2.1 When greedy goes wrong

Now try the same coin recipe with a different set of coins: 1, 3 and 4, and pay 6. Greedy grabs the biggest piece that fits, 4, leaving 2, which needs two 1s. That is three coins: 4 + 1 + 1. But 3 + 3 is only two coins! Greedy was fooled: the best-looking first step (the 4) led to a worse total.

To be sure of the true best, we can use a slower method that tries everything cleverly (it is called dynamic programming; here it just computes, for every amount, the best count using the answers for smaller amounts).

```python
def greedy_coins(amount, coins):
    count = 0
    for c in sorted(coins, reverse=True):
        count += amount // c
        amount %= c
    return count


def best_coins(amount, coins):
    best = [0] + [10**9] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                best[a] = min(best[a], best[a - c] + 1)
    return best[amount]


assert greedy_coins(6, [1, 3, 4]) == 3
assert best_coins(6, [1, 3, 4]) == 2
assert greedy_coins(70, [1, 2, 5, 10, 20, 50, 100]) == best_coins(70, [1, 2, 5, 10, 20, 50, 100])
```

```cpp
int greedy_coins(int amount, vector<int> coins) {
    sort(coins.rbegin(), coins.rend());
    int count = 0;
    for (int c : coins) {
        count += amount / c;
        amount %= c;
    }
    return count;
}

int best_coins(int amount, const vector<int>& coins) {
    vector<int> best(amount + 1, 1000000000);
    best[0] = 0;
    for (int a = 1; a <= amount; a++) {
        for (int c : coins) {
            if (c <= a) best[a] = min(best[a], best[a - c] + 1);
        }
    }
    return best[amount];
}
```

The lesson is important: **a greedy idea is only a guess until you know why it is right**. Greedy is right for the Indian values because each value is large enough compared to the smaller ones that taking the biggest piece never hurts; with 1, 3, 4 it is not. Before trusting a greedy idea, try to break it with a small example, or compare it against a slow, obviously correct method on small inputs.

## 2.2 The exchange argument

How do we convince ourselves that a greedy choice is safe? The standard tool is the **exchange argument**, and it is simpler than it sounds. It goes like this:

Suppose some perfect (best possible) solution exists, one that does not start with our greedy choice. Look at what it does instead. Now _swap_ a piece of it for our greedy choice. If the swap never makes the solution worse, then there is also a perfect solution that starts with our greedy choice. So taking the greedy choice first loses nothing. After taking it, the rest of the problem is a smaller problem of the same kind, and we repeat the argument.

Let's try it on the cookies of Chapter 1. Our greedy choice: give the smallest cookie that satisfies the least greedy child $c$. Suppose a perfect solution does something else: say child $c$ gets a bigger cookie $B$, or no cookie. If $c$ gets a bigger cookie $B$, then swap: give $c$ our small cookie and give the other child (if there was one) cookie $B$. Cookie $B$ is at least as big as the small cookie, so whoever had the small cookie is still happy. Nobody got worse off, so our choice was safe.

You do not need to write such a proof in a contest, but being able to say it in your head ("if the best answer did it differently, I could swap and not lose") is what separates a real greedy solution from a lucky guess.

## 2.3 Take every rise

Let's use the same way of thinking on stock prices. Given the price on each day, you may buy and sell as often as you like but hold at most one share. What is the largest total profit?

The picture to hold in mind is a line chart. Any profit you make is a sum of upward steps of the line. Every day on which the price rises is an opportunity: you could have bought yesterday and sold today. Taking _all_ the rises gives the biggest possible total, because any single trade across several days just collects those same rises (a trade from day 2 to day 5 earns exactly the rises on day 3, 4 and 5 minus the falls in between, which is never more than the rises alone). A fall is never worth taking.

For `[7, 1, 5, 3, 6, 4]`, the steps are $-6, +4, -2, +3, -2$, and the rises are $4 + 3 = 7$.

This is exactly the problem _Buy and Sell Stock, Many Trades_.

```python
def max_profit_many(prices):
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit


assert max_profit_many([7, 1, 5, 3, 6, 4]) == 7
assert max_profit_many([1, 2, 3, 4, 5]) == 4
assert max_profit_many([5, 4, 3]) == 0
```

```cpp
int max_profit_many(const vector<int>& prices) {
    int profit = 0;
    for (size_t i = 1; i < prices.size(); i++) {
        if (prices[i] > prices[i - 1]) profit += prices[i] - prices[i - 1];
    }
    return profit;
}
```

One pass: time $O(n)$, space $O(1)$.

## 2.4 Best value per kilogram

Here is a classic: a bag holds a limited weight, and each item has a value and a weight. If you may take **fractions** of items (like sand or flour), what is the largest value you can carry?

Greedy choice: take items in order of **value per unit of weight**, best ratio first, and take as much of each as fits. The exchange argument is easy to see: if your bag holds a piece of a worse-ratio item while a better-ratio item is not used up, swap one kilogram of the first for one of the second and the value goes up. So in a perfect bag, no such pair exists.

For items `[value, weight] = [60, 10], [100, 20], [120, 30]` and capacity 50: the ratios are 6, 5 and 4. Take all of the first (weight 10), all of the second (weight 20), and 20 of the 30 kilograms of the third: value $60 + 100 + 120 \cdot \tfrac{20}{30} = 240$.

This is exactly the problem _Fractional Knapsack_.

```python
def fractional_knapsack(items, capacity):
    order = sorted(items, key=lambda it: it[0] / it[1], reverse=True)
    total = 0.0
    for value, weight in order:
        if capacity == 0:
            break
        take = min(weight, capacity)        # the part of this item that fits
        total += value * take / weight
        capacity -= take
    return total


assert fractional_knapsack([[60, 10], [100, 20], [120, 30]], 50) == 240.0
assert fractional_knapsack([[10, 5]], 2) == 4.0
assert fractional_knapsack([[10, 5]], 100) == 10.0
```

```cpp
double fractional_knapsack(vector<vector<int>> items, int capacity) {
    sort(items.begin(), items.end(), [](const vector<int>& a, const vector<int>& b) {
        return (double)a[0] / a[1] > (double)b[0] / b[1];
    });
    double total = 0.0;
    for (auto& it : items) {
        if (capacity == 0) break;
        int take = min(it[1], capacity);     // the part of this item that fits
        total += (double)it[0] * take / it[1];
        capacity -= take;
    }
    return total;
}
```

Sorting dominates: time $O(n \log n)$, space $O(1)$ beyond the copy. Careful: if items cannot be split (the "0/1 knapsack"), this greedy idea fails, for the same reason coins 1, 3, 4 failed. For example with capacity 50 and the same items, taking whole items by ratio gives 160, while the best whole-item choice (the second and third items) gives 220.

## 2.5 Check yourself

1. Give a set of coins and an amount where greedy uses more coins than necessary.
2. In words, what does an exchange argument show?
3. Why is "take every rise" at least as good as any buy-and-sell plan?
4. Why does fractional knapsack work but whole-item knapsack does not?

# Chapter 3. Choosing intervals

## 3.1 Activity selection

Many greedy problems are about **intervals**: a start time and an end time, such as meetings, trains or tasks. The first big one: you are given activities with start and end times, you can attend one at a time, and an activity that ends at time $t$ does not clash with one that starts at $t$. Attend as many as possible.

Which activity should we pick first? Tempting ideas: the shortest one, or the one that starts earliest. Both fail (a short activity in the middle of two long ones can block two good ones, and a very long early activity blocks everything). The idea that works: **pick the activity that ends first**. It leaves the most room for everything else. Then skip all activities that start before it ends, and repeat from the next one.

The exchange argument: if a perfect schedule begins with some other activity, replace that first activity by the one that ends earliest. It finishes no later, so it cannot collide with anything the schedule did afterwards.

In code: sort by end time, remember the end of the last chosen activity, and take an activity whenever it starts at or after that end. For starts `[1, 3, 0, 5, 8, 5]` and ends `[2, 4, 6, 7, 9, 9]`, the sorted-by-end activities are (1,2), (3,4), (0,6), (5,7), (8,9), (5,9). We take (1,2), then (3,4), skip (0,6), take (5,7), take (8,9), skip (5,9): four activities.

This is exactly the problem _Activity Selection_.

```python
def max_activities(starts, ends):
    acts = sorted(zip(starts, ends), key=lambda a: a[1])   # earliest end first
    count = 0
    last_end = float("-inf")
    for s, e in acts:
        if s >= last_end:
            count += 1
            last_end = e
    return count


assert max_activities([1, 3, 0, 5, 8, 5], [2, 4, 6, 7, 9, 9]) == 4
assert max_activities([1], [2]) == 1
assert max_activities([1, 2], [3, 4]) == 1     # they overlap
assert max_activities([1, 3], [3, 5]) == 2     # touching is allowed
```

```cpp
int max_activities(const vector<int>& starts, const vector<int>& ends) {
    int n = starts.size();
    vector<pair<int, int>> acts;                 // (end, start)
    for (int i = 0; i < n; i++) acts.push_back({ends[i], starts[i]});
    sort(acts.begin(), acts.end());              // earliest end first
    int count = 0;
    long long last_end = LLONG_MIN;
    for (auto [e, s] : acts) {
        if (s >= last_end) {
            count++;
            last_end = e;
        }
    }
    return count;
}
```

Sorting costs $O(n \log n)$ and the scan $O(n)$; extra space is $O(n)$.

## 3.2 Removing the fewest intervals

The same idea answers a "removal" question. Given intervals, remove the fewest so that the rest do not overlap (touching ends are fine). The number removed is simply the total minus the largest set that can stay, and the largest set that can stay is exactly what activity selection finds. So sort by end, keep an interval if it starts at or after the end of the last kept one, and otherwise count it as removed.

For `[[1, 2], [2, 3], [3, 4], [1, 3]]` sorted by end: [1,2] kept, [2,3] kept, [1,3] starts before 3 overlaps with the kept [2,3], it is removed (count 1), [3,4] kept. The answer is 1.

This is exactly the problem _Remove Overlapping Intervals_.

```python
def erase_overlap(intervals):
    removed = 0
    last_end = float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):
        if start >= last_end:
            last_end = end
        else:
            removed += 1
    return removed


assert erase_overlap([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
assert erase_overlap([[1, 2], [1, 2], [1, 2]]) == 2
assert erase_overlap([[1, 2], [2, 3]]) == 0
```

```cpp
int erase_overlap(vector<vector<int>> intervals) {
    sort(intervals.begin(), intervals.end(),
         [](const vector<int>& a, const vector<int>& b) { return a[1] < b[1]; });
    int removed = 0;
    long long last_end = LLONG_MIN;
    for (auto& iv : intervals) {
        if (iv[0] >= last_end) last_end = iv[1];
        else removed++;
    }
    return removed;
}
```

Time $O(n \log n)$, space $O(1)$ beyond the sort.

## 3.3 Fewest arrows for balloons

Balloons hang on a wall as horizontal segments, and an arrow shot straight up at position $x$ pops every balloon whose segment contains $x$. Fewest arrows to pop all? This is again an interval problem in disguise, but now overlapping is _good_: one arrow serves a whole group of overlapping balloons.

Sort the balloons by their right end. Shoot the first arrow at the right end of the first balloon, which is the furthest to the right you can aim and still pop it, so it pops as many later balloons as possible. Every later balloon whose start is at or before the arrow is already popped. The first balloon that starts after the arrow needs a new arrow at its own right end.

For `[[10, 16], [2, 8], [1, 6], [7, 12]]`, sorted by right end: [1,6], [2,8], [7,12], [10,16]. Arrow at 6 pops [1,6] and [2,8] (start 2 is at most 6). [7,12] starts after 6, so a second arrow at 12 pops [7,12] and [10,16]. Two arrows.

This is exactly the problem _Minimum Arrows to Burst Balloons_.

```python
def min_arrows(balloons):
    if not balloons:
        return 0
    balloons = sorted(balloons, key=lambda b: b[1])
    arrows = 1
    arrow = balloons[0][1]
    for start, end in balloons[1:]:
        if start > arrow:          # not popped by the last arrow
            arrows += 1
            arrow = end
    return arrows


assert min_arrows([[10, 16], [2, 8], [1, 6], [7, 12]]) == 2
assert min_arrows([[1, 2], [3, 4], [5, 6]]) == 3
assert min_arrows([[1, 2], [2, 3]]) == 1
```

```cpp
int min_arrows(vector<vector<int>> balloons) {
    if (balloons.empty()) return 0;
    sort(balloons.begin(), balloons.end(),
         [](const vector<int>& a, const vector<int>& b) { return a[1] < b[1]; });
    int arrows = 1;
    long long arrow = balloons[0][1];
    for (size_t i = 1; i < balloons.size(); i++) {
        if (balloons[i][0] > arrow) {      // not popped by the last arrow
            arrows++;
            arrow = balloons[i][1];
        }
    }
    return arrows;
}
```

Time $O(n \log n)$, space $O(1)$ beyond the sort.

## 3.4 Counting overlaps: platforms

Our last interval question asks for the **most overlap at one moment**. Trains arrive and depart; each train occupies a platform from arrival to departure, both ends included (a train that arrives exactly when another leaves needs a different platform). How many platforms are needed so that nobody waits?

The answer is the largest number of trains in the station at the same time. We do not need to know which train is which, only the number inside. So sort all arrival times, and separately sort all departure times. Walk through time with two pointers: if the next event is an arrival (arrival time at most the next departure time, so ties count the arrival first), one more train is inside; otherwise a train has left. Track the highest count seen.

For arrivals `[900, 940, 950, 1100, 1500, 1800]` and departures `[910, 1200, 1120, 1130, 1900, 2000]` (sorted: 910, 1120, 1130, 1200, 1900, 2000): at 900 one train, 910 one leaves, 940 one in, 950 two in, 1100 three in (the maximum), 1120 two, 1130 one... so the answer is 3.

This is exactly the problem _Minimum Platforms_.

```python
def min_platforms(arrivals, departures):
    arr = sorted(arrivals)
    dep = sorted(departures)
    i = j = 0
    inside = best = 0
    while i < len(arr):
        if arr[i] <= dep[j]:       # arrival first on ties
            inside += 1
            best = max(best, inside)
            i += 1
        else:
            inside -= 1
            j += 1
    return best


assert min_platforms([900, 940, 950, 1100, 1500, 1800],
                     [910, 1200, 1120, 1130, 1900, 2000]) == 3
assert min_platforms([1, 2], [2, 3]) == 2          # touching counts as overlapping
assert min_platforms([5], [6]) == 1
```

```cpp
int min_platforms(vector<int> arrivals, vector<int> departures) {
    sort(arrivals.begin(), arrivals.end());
    sort(departures.begin(), departures.end());
    size_t i = 0, j = 0;
    int inside = 0, best = 0;
    while (i < arrivals.size()) {
        if (arrivals[i] <= departures[j]) {    // arrival first on ties
            inside++;
            best = max(best, inside);
            i++;
        } else {
            inside--;
            j++;
        }
    }
    return best;
}
```

Sorting dominates: time $O(n \log n)$, space $O(1)$ beyond the sorted copies.

## 3.5 Check yourself

1. Why does "pick the activity that ends first" beat "pick the shortest activity"?
2. How is _Remove Overlapping Intervals_ related to _Activity Selection_?
3. In the balloon problem, why do we shoot at the right end of the first balloon, and not the left?
4. Why does _Minimum Platforms_ handle an arrival before a departure at the same time?

# Chapter 4. Going far along a line

## 4.1 Jump game

You stand at index 0 of a list. The number at index $i$ is the longest jump you can make from there (shorter jumps are fine as well). Can you reach the last index?

A recursive search that tries every jump is slow. Instead keep one number: `far`, the farthest index you could possibly reach so far. Walk through the list from left to right. If you are standing at an index that is beyond `far`, you can never get there, so you fail. Otherwise update `far = max(far, i + nums[i])`. Why do we only need `far`? Because every index up to `far` is reachable: you can land exactly on `far` by some jump, and shorter jumps land on everything in between.

Let's trace `[2, 3, 1, 1, 4]`: at index 0, far = 2; index 1, far = max(2, 1+3) = 4; the last index is 4, so reachable. For `[3, 2, 1, 0, 4]`: far stays at 3 (index 3 has jump 0), and when we arrive at index 4 it is beyond far: stuck.

This is exactly the problem _Jump Game_.

```python
def can_jump(nums):
    far = 0
    for i, x in enumerate(nums):
        if i > far:
            return False        # index i cannot be reached
        far = max(far, i + x)
    return True


assert can_jump([2, 3, 1, 1, 4]) is True
assert can_jump([3, 2, 1, 0, 4]) is False
assert can_jump([0]) is True
```

```cpp
bool can_jump(const vector<int>& nums) {
    int far = 0;
    for (int i = 0; i < (int)nums.size(); i++) {
        if (i > far) return false;      // index i cannot be reached
        far = max(far, i + nums[i]);
    }
    return true;
}
```

One pass: time $O(n)$, space $O(1)$.

## 4.2 Fewest jumps

Now we want the **fewest** jumps to reach the last index. Think of it in rounds, like waves spreading out. With 0 jumps you are at index 0. With 1 jump you can reach every index up to `0 + nums[0]`; call that the end of the current round. While scanning the indices of the current round, we track the farthest index any of them could reach with one more jump. When the scan arrives at the end of the current round, we must spend one more jump, and the next round extends up to that farthest point.

For `[2, 3, 1, 1, 4]`: round 0 is only index 0, whose jump reaches index 2. At the end of the round (index 0) we take jump 1, and the new round covers indices 1 to 2. While scanning index 1 the farthest becomes 4. At index 2, the end of that round, we take jump 2, and the round now reaches index 4, the last one. The answer is 2.

If at some index we are beyond `far`, or at the very end `far` has not reached the last index, the target is unreachable and we return -1.

This is exactly the problem _Fewest Jumps to the End_.

```python
def min_jumps(nums):
    n = len(nums)
    jumps = 0
    end = 0          # the last index covered with `jumps` jumps
    far = 0          # the farthest index reachable with one more jump
    for i in range(n - 1):
        if i > far:
            return -1
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            end = far
    return jumps if far >= n - 1 else -1


assert min_jumps([2, 3, 1, 1, 4]) == 2
assert min_jumps([1, 0, 1]) == -1
assert min_jumps([0]) == 0
assert min_jumps([1, 1, 1, 1]) == 3
```

```cpp
int min_jumps(const vector<int>& nums) {
    int n = nums.size();
    int jumps = 0;
    int end = 0;     // the last index covered with `jumps` jumps
    int far = 0;     // the farthest index reachable with one more jump
    for (int i = 0; i < n - 1; i++) {
        if (i > far) return -1;
        far = max(far, i + nums[i]);
        if (i == end) {
            jumps++;
            end = far;
        }
    }
    return far >= n - 1 ? jumps : -1;
}
```

One pass again: time $O(n)$, space $O(1)$. This is a breadth-first search over "how many jumps" levels, but because the reachable set is always an interval, a single running maximum is enough.

## 4.3 Gas station

A road is a circle with $n$ stations. Station $i$ gives `gas[i]` units of fuel and the trip from $i$ to the next costs `cost[i]`. The tank starts empty and is unlimited. From which station can you complete a full lap?

Let `gain[i] = gas[i] - cost[i]` be the net change after station $i$. Two facts make this easy. **Fact 1:** if the total of all gains is negative, there is not enough fuel overall, so no start works. **Fact 2:** if starting at station $s$ you run out of fuel for the first time while trying to leave station $k$, then no station between $s$ and $k$ can be a good start either: each of them would arrive at its own place with at most as much fuel as the one from $s$ did (the tank never went negative before $k$), so it would fail at $k$ too. So the next start to try is $k + 1$.

Combine them in one pass: keep the tank, and whenever it goes negative, reset it to 0 and move the candidate start to the next station. At the end, if the total is non-negative, the candidate is a valid start (and the smallest valid one).

For gas `[1, 2, 3, 4, 5]`, cost `[3, 4, 5, 1, 2]`: the gains are $-2, -2, -2, 3, 3$ and their total is 0. The tank goes negative at stations 0, 1 and 2 (each time restarting), so the candidate becomes 3. From station 3 the tank is 3 then 6, never negative. The answer is 3.

This is exactly the problem _Gas Station_.

```python
def can_complete_circuit(gas, cost):
    total = 0
    tank = 0
    start = 0
    for i in range(len(gas)):
        gain = gas[i] - cost[i]
        total += gain
        tank += gain
        if tank < 0:            # cannot continue from `start`
            start = i + 1
            tank = 0
    return start if total >= 0 else -1


assert can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
assert can_complete_circuit([2, 3, 4], [3, 4, 3]) == -1
assert can_complete_circuit([5], [4]) == 0
```

```cpp
int can_complete_circuit(const vector<int>& gas, const vector<int>& cost) {
    long long total = 0, tank = 0;
    int start = 0;
    for (int i = 0; i < (int)gas.size(); i++) {
        int gain = gas[i] - cost[i];
        total += gain;
        tank += gain;
        if (tank < 0) {          // cannot continue from `start`
            start = i + 1;
            tank = 0;
        }
    }
    return total >= 0 ? start : -1;
}
```

Time $O(n)$ and space $O(1)$.

## 4.4 Check yourself

1. In _Jump Game_, why is every index up to `far` reachable?
2. What does `end` stand for in the fewest-jumps loop, and when do we add a jump?
3. In _Gas Station_, why does a failure at station $k$ rule out all starts between $s$ and $k$?
4. What does a negative total gain tell us?

# Chapter 5. Scanning and fixing

## 5.1 Candy: two passes

Children stand in a line with ratings. Everyone gets at least one candy, and a child with a higher rating than a neighbour must get more candy than that neighbour. Fewest candies in total?

There are two kinds of rules: "more than the left neighbour" and "more than the right neighbour". Handling both at once is awkward, but handling each alone is easy. So do two passes. In a pass from **left to right**, if a child's rating is higher than the one before, give them one more candy than that child; otherwise they stay at 1. This satisfies all the left-neighbour rules and uses as few candies as possible for them. In a pass from **right to left**, do the same with the right neighbour, but never lower what a child already has: take the maximum of the two requirements.

For ratings `[1, 2, 87, 87, 87, 2, 1]`, the left pass gives candies `[1, 2, 3, 1, 1, 1, 1]`, and the right pass raises the last ones to `[1, 2, 3, 1, 3, 2, 1]`, for a total of 13.

This is exactly the problem _Distribute Candy_.

```python
def candy(ratings):
    n = len(ratings)
    give = [1] * n
    for i in range(1, n):                      # rule for the left neighbour
        if ratings[i] > ratings[i - 1]:
            give[i] = give[i - 1] + 1
    for i in range(n - 2, -1, -1):             # rule for the right neighbour
        if ratings[i] > ratings[i + 1]:
            give[i] = max(give[i], give[i + 1] + 1)
    return sum(give)


assert candy([1, 0, 2]) == 5
assert candy([1, 2, 87, 87, 87, 2, 1]) == 13
assert candy([1, 2, 2]) == 4
assert candy([5]) == 1
```

```cpp
int candy(const vector<int>& ratings) {
    int n = ratings.size();
    vector<int> give(n, 1);
    for (int i = 1; i < n; i++) {                  // rule for the left neighbour
        if (ratings[i] > ratings[i - 1]) give[i] = give[i - 1] + 1;
    }
    for (int i = n - 2; i >= 0; i--) {             // rule for the right neighbour
        if (ratings[i] > ratings[i + 1]) give[i] = max(give[i], give[i + 1] + 1);
    }
    int total = 0;
    for (int g : give) total += g;
    return total;
}
```

Time $O(n)$ and space $O(n)$. (A cleverer version keeps only the lengths of the current rising and falling runs and uses $O(1)$ space; the two-pass way is easier to trust.)

## 5.2 Partition labels

Cut a string into as many parts as possible so that every letter appears in only one part. The key observation: if a part contains the letter `a`, then it must reach all the way to the **last** occurrence of `a`. So first record the last position of every letter. Then scan: start a part at the current position and set `end` to the last position of the first letter. As you walk, every letter you meet might push `end` further right (its own last position). When your walking index reaches `end`, nothing in the part appears later, so this is a valid cut. The part is as short as possible, so there are as many parts as possible.

For `"ababcbacadefegdehijhklij"`, the letter `a` last appears at 8, but inside the first part, `b` reaches 5 and `c` reaches 7, so the part ends at index 8 (size 9). The rest give 7 and 8 characters.

This is exactly the problem _Partition Labels_.

```python
def partition_labels(s):
    last = {ch: i for i, ch in enumerate(s)}
    sizes = []
    start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])      # this part must reach at least here
        if i == end:                  # nothing in the part appears later
            sizes.append(end - start + 1)
            start = i + 1
    return sizes


assert partition_labels("ababcbacadefegdehijhklij") == [9, 7, 8]
assert partition_labels("eccbbbbdec") == [10]
assert partition_labels("abc") == [1, 1, 1]
```

```cpp
vector<int> partition_labels(const string& s) {
    int last[256];
    for (int i = 0; i < 256; i++) last[i] = -1;
    for (int i = 0; i < (int)s.size(); i++) last[(unsigned char)s[i]] = i;
    vector<int> sizes;
    int start = 0, end = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        end = max(end, last[(unsigned char)s[i]]);   // this part must reach at least here
        if (i == end) {                              // nothing in the part appears later
            sizes.push_back(end - start + 1);
            start = i + 1;
        }
    }
    return sizes;
}
```

Time $O(n)$, space $O(1)$ (one table for the alphabet).

## 5.3 Longest wiggle

A **wiggle** sequence goes up, then down, then up, and so on. We want the longest wiggling subsequence of a list (we may skip elements). The greedy view: only the turning points matter. In a long upward climb, we need just one number from it, ideally its peak, because a higher peak only helps the next down-step. In practice we do not need to find the peaks; we keep two counters: `up`, the longest wiggle so far that ends with a rise, and `down`, the longest that ends with a fall. When the next number is higher than the previous one, a rise can be added on to any wiggle ending in a fall: `up = down + 1`. When it is lower, `down = up + 1`. Equal numbers change nothing.

For `[1, 7, 4, 9, 2, 5]`, each step turns direction, so the answer is 6; for `[1, 2, 3]` there is only one climb, so the answer is 2.

This is exactly the problem _Longest Wiggle Subsequence_.

```python
def wiggle_max_length(nums):
    if len(nums) < 2:
        return len(nums)
    up = down = 1
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            up = down + 1
        elif nums[i] < nums[i - 1]:
            down = up + 1
    return max(up, down)


assert wiggle_max_length([1, 7, 4, 9, 2, 5]) == 6
assert wiggle_max_length([1, 17, 5, 10, 13, 15, 10, 5, 16, 8]) == 7
assert wiggle_max_length([1, 2, 3]) == 2
assert wiggle_max_length([4, 4]) == 1
```

```cpp
int wiggle_max_length(const vector<int>& nums) {
    int n = nums.size();
    if (n < 2) return n;
    int up = 1, down = 1;
    for (int i = 1; i < n; i++) {
        if (nums[i] > nums[i - 1]) up = down + 1;
        else if (nums[i] < nums[i - 1]) down = up + 1;
    }
    return max(up, down);
}
```

Time $O(n)$, space $O(1)$.

## 5.4 Largest number with rising digits

Given $n$, find the largest number at most $n$ whose digits never decrease from left to right. If $n$ already has that property, it is the answer. Otherwise some digit is bigger than the digit right after it; call that a **drop**. To fix a drop we must lower the bigger digit by 1 and then make everything after it as large as possible, which means all 9s.

For 332: the pair `3, 2` drops. Lower the second 3 to 2 and fill the rest with 9: 329. But now the first `3` is bigger than the new `2`: another drop, so lower it to 2 and fill with 9s: 299. That the first drop can trigger an earlier one is why we scan from the **right**: going from right to left, whenever a digit is bigger than the one to its right, lower it by 1 and remember that everything from the next place onward becomes 9. At the end, write 9s from the remembered place.

This is exactly the problem _Largest Number With Non-Decreasing Digits_.

```python
def monotone_increasing_digits(n):
    digits = list(str(n))
    mark = len(digits)                      # from here on, all digits become 9
    for i in range(len(digits) - 1, 0, -1):
        if digits[i - 1] > digits[i]:
            digits[i - 1] = str(int(digits[i - 1]) - 1)
            mark = i
    for i in range(mark, len(digits)):
        digits[i] = "9"
    return int("".join(digits))


assert monotone_increasing_digits(332) == 299
assert monotone_increasing_digits(1234) == 1234
assert monotone_increasing_digits(10) == 9
assert monotone_increasing_digits(120) == 119
```

```cpp
long long monotone_increasing_digits(long long n) {
    string d = to_string(n);
    int mark = d.size();                    // from here on, all digits become 9
    for (int i = (int)d.size() - 1; i > 0; i--) {
        if (d[i - 1] > d[i]) {
            d[i - 1]--;
            mark = i;
        }
    }
    for (int i = mark; i < (int)d.size(); i++) d[i] = '9';
    return stoll(d);
}
```

Time $O(d)$ for $d$ digits, i.e. $O(\log n)$, and space $O(d)$.

## 5.5 Check yourself

1. Why do the two passes in _Distribute Candy_ use a maximum in the second pass?
2. In _Partition Labels_, when is it safe to cut?
3. What do `up` and `down` mean in the wiggle algorithm?
4. Why do we scan the digits from the right in the last problem?

# Chapter 6. Counting, slack and deadlines

## 6.1 Parentheses with wildcards

A string has `(`, `)` and `*`, where each `*` may act as `(`, `)` or nothing. Can the brackets be made valid? Trying all choices is exponential. Instead, keep **a range** of what is possible. Let `lo` be the smallest number of unclosed `(` we could have after the characters seen so far, and `hi` the largest. A `(` raises both. A `)` lowers both. A `*` can be a `)` (lowering `lo`), or a `(` (raising `hi`), or nothing, so `lo` goes down by one and `hi` goes up by one, and every value in between is possible too.

Two rules finish it. If `hi` ever drops below 0, even the most generous choice of stars has more `)` than `(`, so it is invalid. And `lo` can never really be below 0 (a negative count of open brackets means we simply chose not to use that star as `)`), so clamp it up to 0. At the end the string is valid exactly when 0 is in the range, meaning `lo == 0`.

For `"(*))"`: after `(`: lo 1, hi 1. After `*`: lo 0, hi 2. After `)`: lo 0 (clamped from -1), hi 1. After `)`: lo 0 (clamped), hi 0. Final `lo == 0`: valid.

This is exactly the problem _Valid Parenthesis String With Wildcards_.

```python
def check_valid_string(s):
    lo = hi = 0
    for ch in s:
        if ch == "(":
            lo += 1
            hi += 1
        elif ch == ")":
            lo -= 1
            hi -= 1
        else:
            lo -= 1
            hi += 1
        if hi < 0:
            return False
        lo = max(lo, 0)
    return lo == 0


assert check_valid_string("(*)") is True
assert check_valid_string("(*))") is True
assert check_valid_string(")(") is False
assert check_valid_string("((*") is False
```

```cpp
bool check_valid_string(const string& s) {
    int lo = 0, hi = 0;
    for (char ch : s) {
        if (ch == '(') {
            lo++;
            hi++;
        } else if (ch == ')') {
            lo--;
            hi--;
        } else {
            lo--;
            hi++;
        }
        if (hi < 0) return false;
        lo = max(lo, 0);
    }
    return lo == 0;
}
```

Time $O(n)$, space $O(1)$.

## 6.2 Task scheduler

Tasks are letters, each takes one unit of time, and two equal letters must be at least $n$ other time units (tasks or idle) apart. What is the least total time?

The troublemaker is the letter with the highest count $m$. Its $m$ copies need $m-1$ gaps between them, and each gap must hold $n$ other slots. So picture a frame: the most frequent letter, then $n$ slots, then the letter again, and so on, ending with the letter. For `AAABBB` with $n = 2$: `A B _ A B _ A B`, a frame with $m - 1 = 2$ full blocks of length $n + 1 = 3$ followed by a final block with the letters that tie for the maximum count (here A and B, so 2 slots). The length is $(m-1)(n+1) + \text{ties} = 2 \cdot 3 + 2 = 8$.

Other tasks fit into the gaps of the frame for free. If there are so many other tasks that they overflow the gaps, no idle time is needed at all, and the answer is simply the number of tasks. So the answer is the larger of the two:

$$\max\bigl(\,|\text{tasks}|,\ (m-1)(n+1) + \text{ties}\,\bigr)$$

For `AAAABBC` with $n = 2$: $m = 4$, ties = 1, frame $3 \cdot 3 + 1 = 10$ which beats 7 tasks. For `AABCDE` with $n = 1$: frame $1 \cdot 2 + 1 = 3$, but there are 6 tasks, so the answer is 6.

This is exactly the problem _Task Scheduler_.

```python
def least_interval(tasks, n):
    if not tasks:
        return 0
    counts = {}
    for t in tasks:
        counts[t] = counts.get(t, 0) + 1
    m = max(counts.values())
    ties = sum(1 for c in counts.values() if c == m)
    return max(len(tasks), (m - 1) * (n + 1) + ties)


assert least_interval("AAABBB", 2) == 8
assert least_interval("AAAABBC", 2) == 10
assert least_interval("AABCDE", 1) == 6
assert least_interval("AAABBB", 0) == 6
```

```cpp
int least_interval(const string& tasks, int n) {
    if (tasks.empty()) return 0;
    map<char, int> counts;
    for (char t : tasks) counts[t]++;
    int m = 0;
    for (auto& [ch, c] : counts) m = max(m, c);
    int ties = 0;
    for (auto& [ch, c] : counts) if (c == m) ties++;
    return max((int)tasks.size(), (m - 1) * (n + 1) + ties);
}
```

Time $O(T)$ for $T$ tasks, and space $O(1)$ (at most as many counters as letters).

## 6.3 Job sequencing with deadlines

Each job takes one time unit, has a deadline $d$ (it must finish within time slots $1..d$) and a profit. One job per slot. Maximise the total profit.

Greedy choice: consider jobs from the **highest profit** down. Give each job the **latest free slot** that is still within its deadline; keeping early slots free leaves them for jobs with tight deadlines. If no free slot exists, skip the job. Exchange argument sketch: a more profitable job should never lose its place to a less profitable one, and putting it as late as allowed disturbs the fewest others.

For jobs `[deadline, profit]` = `[4, 20], [1, 10], [1, 40], [1, 30]`: sorted by profit: (1, 40), (1, 30), (1, 10), (4, 20). The job with profit 40 takes slot 1. The next two have deadline 1 and slot 1 is taken: skipped. The job with profit 20 takes slot 4. Total 60.

This is exactly the problem _Job Sequencing With Deadlines_.

```python
def job_profit(jobs):
    limit = min(max(d for d, p in jobs), len(jobs)) if jobs else 0
    taken = [False] * (limit + 1)
    total = 0
    for deadline, profit in sorted(jobs, key=lambda j: -j[1]):
        t = min(deadline, limit)
        while t > 0 and taken[t]:      # walk down to the latest free slot
            t -= 1
        if t > 0:
            taken[t] = True
            total += profit
    return total


assert job_profit([[4, 20], [1, 10], [1, 40], [1, 30]]) == 60
assert job_profit([[2, 100], [1, 19], [2, 27], [1, 25], [3, 15]]) == 142
assert job_profit([]) == 0
```

```cpp
long long job_profit(vector<vector<int>> jobs) {
    int limit = 0;
    for (auto& j : jobs) limit = max(limit, j[0]);
    limit = min(limit, (int)jobs.size());
    vector<bool> taken(limit + 1, false);
    sort(jobs.begin(), jobs.end(),
         [](const vector<int>& a, const vector<int>& b) { return a[1] > b[1]; });
    long long total = 0;
    for (auto& j : jobs) {
        int t = min(j[0], limit);
        while (t > 0 && taken[t]) t--;     // walk down to the latest free slot
        if (t > 0) {
            taken[t] = true;
            total += j[1];
        }
    }
    return total;
}
```

Walking down can be slow: time is $O(n \log n + n \cdot d)$ in the worst case. We can remember, for each slot, a pointer to "the latest free slot at or below me". When slot $s$ gets used, point it at $s - 1$. Following pointers (and shortcutting them as we go, a trick called path compression that is the heart of the union-find structure from the graphs chapter) makes each lookup almost $O(1)$.

```python
def job_profit_fast(jobs):
    limit = min(max(d for d, p in jobs), len(jobs)) if jobs else 0
    parent = list(range(limit + 1))        # parent[t] = a free slot <= t, or 0

    def find(t):
        while parent[t] != t:
            parent[t] = parent[parent[t]]  # shortcut
            t = parent[t]
        return t

    total = 0
    for deadline, profit in sorted(jobs, key=lambda j: -j[1]):
        slot = find(min(deadline, limit))
        if slot > 0:
            parent[slot] = slot - 1        # this slot is used now
            total += profit
    return total


assert job_profit_fast([[4, 20], [1, 10], [1, 40], [1, 30]]) == 60
assert job_profit_fast([[2, 100], [1, 19], [2, 27], [1, 25], [3, 15]]) == 142
assert job_profit_fast([]) == 0
```

```cpp
long long job_profit_fast(vector<vector<int>> jobs) {
    int limit = 0;
    for (auto& j : jobs) limit = max(limit, j[0]);
    limit = min(limit, (int)jobs.size());
    vector<int> parent(limit + 1);
    for (int t = 0; t <= limit; t++) parent[t] = t;   // parent[t] = a free slot <= t, or 0
    auto find = [&](int t) {
        while (parent[t] != t) {
            parent[t] = parent[parent[t]];            // shortcut
            t = parent[t];
        }
        return t;
    };
    sort(jobs.begin(), jobs.end(),
         [](const vector<int>& a, const vector<int>& b) { return a[1] > b[1]; });
    long long total = 0;
    for (auto& j : jobs) {
        int slot = find(min(j[0], limit));
        if (slot > 0) {
            parent[slot] = slot - 1;                  // this slot is used now
            total += j[1];
        }
    }
    return total;
}
```

Time $O(n \log n)$ for the sort plus almost-linear lookups, space $O(n)$.

## 6.4 Check yourself

1. In the wildcard-parentheses problem, what do `lo` and `hi` mean?
2. Why are the other tasks "free" inside the frame of the task scheduler?
3. Why give a job the latest free slot rather than the earliest?
4. When does the task scheduler need no idle time at all?

# Chapter 7. Greedy by custom order

## 7.1 Largest number from a list

Given non-negative integers, arrange them so that the number formed by writing them side by side is as large as possible: for `[3, 30, 34, 5, 9]` the answer is `9534330`. Sorting by plain value does not work: it would put 30 ahead of 3, but `330` beats `303`.

The right greedy idea is to **define our own order**. For two numbers written as strings $a$ and $b$, put $a$ first if $a + b$ is bigger than $b + a$ (concatenation, as text). For 3 and 30: `"330"` versus `"303"`, so 3 goes first. This is a valid ordering (if $a$ should go before $b$ and $b$ before $c$ then $a$ before $c$), and sorting with it is exactly the exchange argument: if two neighbours are in the wrong order, swapping them makes the number larger, so in the best answer no neighbours are swapped.

If the biggest piece after sorting is `"0"`, every number was zero, and we return `"0"` instead of a string of zeros.

This is exactly the problem _Largest Number_.

```python
from functools import cmp_to_key


def largest_number(nums):
    words = [str(x) for x in nums]

    def compare(a, b):
        if a + b > b + a:
            return -1            # a should come first
        if a + b < b + a:
            return 1
        return 0

    words.sort(key=cmp_to_key(compare))
    result = "".join(words)
    return "0" if result[0] == "0" else result


assert largest_number([3, 30, 34, 5, 9]) == "9534330"
assert largest_number([10, 2]) == "210"
assert largest_number([0, 0]) == "0"
```

```cpp
string largest_number(const vector<int>& nums) {
    vector<string> words;
    for (int x : nums) words.push_back(to_string(x));
    sort(words.begin(), words.end(),
         [](const string& a, const string& b) { return a + b > b + a; });
    string result;
    for (auto& w : words) result += w;
    return result[0] == '0' ? "0" : result;
}
```

Sorting $n$ numbers with comparisons of length $L$ costs $O(n \log n \cdot L)$ time, and the space is $O(n L)$ for the text.

## 7.2 Smallest string with each letter once

Remove letters from a string so that each letter appearing in it appears exactly once, the order of the survivors is unchanged, and the result is the smallest in dictionary order. For `"cbacdcbc"` the answer is `"acdb"`.

A **stack** (a pile where we only add and remove at the top) does it with a greedy rule. Walk through the letters and build the answer on the stack. For each new letter:

If it is already on the stack, skip it (keeping the earlier copy is never worse). Otherwise, while the top of the stack is **bigger** than the new letter **and** that top letter appears again later in the string, pop it: we can put it back later, and removing it now makes the front of the answer smaller. Then push the new letter.

To know whether a letter appears later, record the last position of every letter first. Trace for `"cbacdcbc"`: push c; `b` is smaller than c and c appears later, so pop c and push b; `a` is smaller than b and b appears later, so pop b and push a; stack `a`. Then `c` is pushed (`ac`), `d` is pushed (`acd`). The next `c` is already on the stack and is skipped. The next `b` is smaller than `d`, but `d` never appears again, so we cannot pop; push b (`acdb`). The last `c` is on the stack, skipped. Result: `acdb`.

This is exactly the problem _Smallest String With Each Letter Once_.

```python
def remove_duplicate_letters(s):
    last = {ch: i for i, ch in enumerate(s)}
    stack = []
    on_stack = set()
    for i, ch in enumerate(s):
        if ch in on_stack:
            continue
        while stack and stack[-1] > ch and last[stack[-1]] > i:
            on_stack.discard(stack.pop())    # it will come again later
        stack.append(ch)
        on_stack.add(ch)
    return "".join(stack)


assert remove_duplicate_letters("bcabc") == "abc"
assert remove_duplicate_letters("cbacdcbc") == "acdb"
assert remove_duplicate_letters("aaa") == "a"
```

```cpp
string remove_duplicate_letters(const string& s) {
    int last[256];
    for (int i = 0; i < 256; i++) last[i] = -1;
    for (int i = 0; i < (int)s.size(); i++) last[(unsigned char)s[i]] = i;
    string stack;
    bool on_stack[256] = {false};
    for (int i = 0; i < (int)s.size(); i++) {
        unsigned char ch = s[i];
        if (on_stack[ch]) continue;
        while (!stack.empty() && (unsigned char)stack.back() > ch &&
               last[(unsigned char)stack.back()] > i) {
            on_stack[(unsigned char)stack.back()] = false;   // it will come again later
            stack.pop_back();
        }
        stack.push_back(ch);
        on_stack[ch] = true;
    }
    return stack;
}
```

Every letter is pushed and popped at most once: time $O(n)$ and space $O(1)$ for the alphabet (the stack holds at most one copy of each letter).

## 7.3 A checklist for greedy problems

When a new problem smells greedy, go through four questions. What is the choice I make at each step (the earliest end, the best ratio, the largest profit)? What order should I process things in, and do I need to sort first? Why can I never regret the choice, which is the exchange argument in your head? And can I find a tiny counterexample, such as coins 1, 3, 4, that breaks it? If you cannot break the idea on small inputs and you can say why a swap never hurts, trust it.

Also keep in mind the common shapes you met here: sort by one key and sweep (cookies, intervals, knapsack, job sequencing); keep one running number (`far`, `end`, `tank`); scan from both sides (candy); and define an order or maintain a stack (largest number, smallest letters). A lot of problems in interviews are one of these in disguise.

## 7.4 Check yourself

1. Why is plain numeric sorting wrong for _Largest Number_?
2. In _Smallest String With Each Letter Once_, why must the popped letter appear again later?
3. What does "the last position of each letter" give us in that problem?
4. Name one problem from this page that needs a sort, and one that needs only a single pass.
