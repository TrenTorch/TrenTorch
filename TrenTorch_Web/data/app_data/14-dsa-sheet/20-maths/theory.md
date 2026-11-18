> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Number theory)

This page teaches the number tricks that keep showing up in coding interviews: primes, divisors, remainders, powers, and counting with huge numbers. It assumes only that you can write a loop and a simple function. You do not need to know any advanced mathematics.

The page is a staircase. **Chapter 1 is deliberately gentle**: what a factor is, what a prime is and what a remainder is, with small examples. Each later chapter adds one new tool, and the mathematics gets a little heavier. By the last chapters you will be able to test whether a huge number is prime and combine remainders from different moduli. If a later chapter looks hard, do not worry; every chapter only uses what came before.

Every code example is shown in Python and in C++, so pick whichever language you like.

# Chapter 1. Numbers, factors and primes

## 1.1 Factors and multiples

A **factor** (or **divisor**) of a number is a whole number that divides it with nothing left over. The factors of 12 are 1, 2, 3, 4, 6 and 12, because $12 = 1 \cdot 12 = 2 \cdot 6 = 3 \cdot 4$. A **multiple** of a number is what you get when you multiply it by 1, 2, 3 and so on, so the multiples of 4 are 4, 8, 12, 16, and so on.

To check whether $d$ is a factor of $n$ we look at the **remainder** of the division. In Python and C++ the remainder is written `n % d`. For example `12 % 5` is 2, because 5 goes into 12 twice and 2 is left. A number $d$ divides $n$ exactly when `n % d == 0`.

Listing all factors of $n$ the slow way means trying every number from 1 to $n$. That works for small numbers, but there is a neat shortcut. Factors come in pairs: if $d$ is a factor, then so is $n/d$. In the pair $(3, 4)$ for 12, one of the two is always at most $\sqrt{n}$, so we only need to try numbers up to $\sqrt{n}$ and record both members of each pair.

```python
def divisors(n):
    small, large = [], []
    d = 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d != n // d:
                large.append(n // d)
        d += 1
    return small + large[::-1]

assert divisors(12) == [1, 2, 3, 4, 6, 12]
assert divisors(36) == [1, 2, 3, 4, 6, 9, 12, 18, 36]
assert divisors(1) == [1]
```

```cpp
vector<long long> divisors(long long n) {
    vector<long long> small, large;
    for (long long d = 1; d * d <= n; d++) {
        if (n % d == 0) {
            small.push_back(d);
            if (d != n / d) large.push_back(n / d);
        }
    }
    reverse(large.begin(), large.end());
    small.insert(small.end(), large.begin(), large.end());
    return small;
}
```

The loop runs about $\sqrt{n}$ times, so the cost is $O(\sqrt{n})$. For $n = 10^{12}$ that is about a million steps, which is fast. The check `d != n // d` handles perfect squares such as 36, where the pair $(6, 6)$ must be counted only once.

## 1.2 Prime numbers

A **prime number** is a number greater than 1 whose only factors are 1 and itself. The first primes are 2, 3, 5, 7, 11, 13. A number greater than 1 that is not prime is called **composite**; it can be split into smaller factors, like $12 = 3 \cdot 4$. The number 1 is neither prime nor composite.

Primes are the building blocks of all numbers. This is the **fundamental theorem of arithmetic**: every whole number greater than 1 can be written as a product of primes in exactly one way, apart from the order. For instance $360 = 2^3 \cdot 3^2 \cdot 5$. We will use this fact again and again.

To test whether $n$ is prime, we can use the same square-root shortcut. If $n$ had a factor larger than $\sqrt{n}$, it would also have a matching factor smaller than $\sqrt{n}$. So if no number from 2 up to $\sqrt{n}$ divides $n$, then $n$ is prime.

```python
def is_prime_slow(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True

assert [p for p in range(20) if is_prime_slow(p)] == [2, 3, 5, 7, 11, 13, 17, 19]
assert is_prime_slow(1_000_000_007)
```

```cpp
bool is_prime_slow(long long n) {
    if (n < 2) return false;
    for (long long d = 2; d * d <= n; d++)
        if (n % d == 0) return false;
    return true;
}
```

This costs $O(\sqrt{n})$ time and constant space. It is perfect when $n$ is up to about $10^{12}$ and you test only a few numbers. Later chapters show faster ways for many numbers or for enormous ones.

## 1.3 What the remainder tells us

The remainder operation is more powerful than it looks. If you look at a clock, after 12 comes 1 again; the hour is the remainder of the total hours when divided by 12. This idea of "wrapping around" is called **modular arithmetic**. We write $a \bmod m$ for the remainder of $a$ divided by $m$, and it is always between 0 and $m-1$.

Two numbers $a$ and $b$ are called **congruent modulo $m$** if they have the same remainder, which we write $a \equiv b \pmod m$. For example $17 \equiv 5 \pmod{12}$, because both leave remainder 5.

The most useful property is that adding, subtracting and multiplying can be done on the remainders. If you want the last digit of $4237 \cdot 8951$, you only need $7 \cdot 1 = 7$. Formally:

$$(a + b) \bmod m = \big((a \bmod m) + (b \bmod m)\big) \bmod m,$$

$$(a \cdot b) \bmod m = \big((a \bmod m) \cdot (b \bmod m)\big) \bmod m.$$

This lets us keep numbers small while computing with huge ones, which is the heart of the later chapters. One warning: in Python the result of `%` with a positive modulus is never negative, but in C++ `(-7) % 5` is $-2$. When subtracting in C++, write `((a - b) % m + m) % m`.

```python
def add_mod(a, b, m):
    return (a % m + b % m) % m

def sub_mod(a, b, m):
    return ((a - b) % m + m) % m

def mul_mod(a, b, m):
    return (a % m) * (b % m) % m

assert add_mod(10, 5, 12) == 3
assert sub_mod(3, 10, 12) == 5
assert mul_mod(4237, 8951, 10) == 7
```

```cpp
long long add_mod(long long a, long long b, long long m) {
    return (a % m + b % m) % m;
}

long long sub_mod(long long a, long long b, long long m) {
    return ((a - b) % m + m) % m;
}

long long mul_mod(long long a, long long b, long long m) {
    return (a % m) * (b % m) % m;
}
```

## 1.4 Check yourself

1. Why is it enough to test divisors up to $\sqrt{n}$ when listing the factors of $n$?
2. Is 1 a prime number? Is 91 a prime number? Give a reason in one sentence each.
3. What is $(23 \cdot 47) \bmod 10$, computed using only the last digits?
4. Why does `(-7) % 5` need care in C++ but not in Python?

# Chapter 2. Sieve, factorisation and counting divisors

## 2.1 Counting primes with the sieve

Testing every number below $n$ with trial division would be slow. A much faster idea was found by the Greek mathematician Eratosthenes more than two thousand years ago. Write down all the numbers from 2 to $n-1$. Take the first number that is not crossed out, 2, and cross out all of its multiples (4, 6, 8, and so on). The next number not crossed out, 3, must be prime; cross out its multiples. Repeat. Every number that is never crossed out is prime. This is called the **sieve of Eratosthenes**, and it is exactly the idea of the problem _Count Primes_.

Here is the sieve for numbers below 30. After crossing out the multiples of 2, 3 and 5, only the primes remain: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29. We can stop crossing out once the prime $p$ satisfies $p \cdot p \ge n$, because any composite number below $n$ already has a factor at most $\sqrt{n}$. And for a prime $p$ we may begin crossing out at $p \cdot p$, since smaller multiples such as $2p$ and $3p$ were removed earlier.

```python
def count_primes(n):
    if n < 3:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    p = 2
    while p * p < n:
        if is_prime[p]:
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False
        p += 1
    return sum(is_prime)

assert count_primes(30) == 10
assert count_primes(10) == 4
assert count_primes(2) == 0
assert count_primes(100) == 25
```

```cpp
int count_primes(int n) {
    if (n < 3) return 0;
    vector<bool> is_prime(n, true);
    is_prime[0] = is_prime[1] = false;
    for (long long p = 2; p * p < n; p++) {
        if (is_prime[p]) {
            for (long long m = p * p; m < n; m += p) is_prime[m] = false;
        }
    }
    return count(is_prime.begin(), is_prime.end(), true);
}
```

The sieve takes about $O(n \log \log n)$ time, which is almost linear, and $O(n)$ memory. For $n = 10^7$ it runs in well under a second in C++.

## 2.2 Writing a number as a product of primes

By the fundamental theorem of arithmetic, every $n > 1$ equals a product of primes in exactly one way. We write it as $n = p_1^{e_1} p_2^{e_2} \cdots p_k^{e_k}$, where each $p_i$ is a prime and each $e_i$ says how many times it appears. For example $360 = 2^3 \cdot 3^2 \cdot 5^1$. This is the problem _Prime Factorization_.

To find the factors we do trial division, but with a trick: divide out each factor completely as soon as we find it. We start with $d = 2$. While $d$ divides $n$, we divide and count. Then we move on to $d = 3$, and so on. Because we divide out the small primes first, whenever $d$ divides the current $n$, $d$ is guaranteed to be prime. We can stop when $d \cdot d > n$, because what is left over is either 1 or a single prime.

```python
def prime_factors(n):
    result = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            exponent = 0
            while n % d == 0:
                n //= d
                exponent += 1
            result.append([d, exponent])
        d += 1
    if n > 1:
        result.append([n, 1])
    return result

assert prime_factors(360) == [[2, 3], [3, 2], [5, 1]]
assert prime_factors(97) == [[97, 1]]
assert prime_factors(1) == []
assert prime_factors(1001) == [[7, 1], [11, 1], [13, 1]]
```

```cpp
vector<pair<long long, int>> prime_factors(long long n) {
    vector<pair<long long, int>> result;
    for (long long d = 2; d * d <= n; d++) {
        if (n % d == 0) {
            int exponent = 0;
            while (n % d == 0) {
                n /= d;
                exponent++;
            }
            result.push_back({d, exponent});
        }
    }
    if (n > 1) result.push_back({n, 1});
    return result;
}
```

The time is $O(\sqrt{n})$, because $d$ never needs to go above $\sqrt{n}$. After the loop, if $n > 1$, the remaining value is a prime larger than every $d$ we tried, so we add it with exponent 1.

## 2.3 Counting the divisors from the factors

Once we know $n = p_1^{e_1} \cdots p_k^{e_k}$, counting the divisors is easy. A divisor picks, for each prime $p_i$, how many copies to use: anywhere from 0 up to $e_i$, which is $e_i + 1$ choices. Choices for different primes are independent, so we multiply:

$$d(n) = (e_1 + 1)(e_2 + 1) \cdots (e_k + 1).$$

For $360 = 2^3 \cdot 3^2 \cdot 5$ we get $(3+1)(2+1)(1+1) = 24$ divisors. This is the problem _Count Divisors_. Likewise the sum of all divisors is $\prod \frac{p_i^{e_i+1} - 1}{p_i - 1}$, because each prime contributes $1 + p + p^2 + \cdots + p^{e}$.

```python
def count_divisors(n):
    total = 1
    for _, exponent in prime_factors(n):
        total *= exponent + 1
    return total

def sum_divisors(n):
    total = 1
    for p, exponent in prime_factors(n):
        total *= (p ** (exponent + 1) - 1) // (p - 1)
    return total

assert count_divisors(360) == 24
assert count_divisors(1) == 1
assert count_divisors(97) == 2
assert sum_divisors(12) == 28
```

```cpp
long long count_divisors(long long n) {
    long long total = 1;
    for (auto [p, exponent] : prime_factors(n)) total *= exponent + 1;
    return total;
}

long long sum_divisors(long long n) {
    long long total = 1;
    for (auto [p, exponent] : prime_factors(n)) {
        long long term = 1, power = 1;
        for (int i = 0; i < exponent; i++) {
            power *= p;
            term += power;
        }
        total *= term;
    }
    return total;
}
```

## 2.4 Check yourself

1. In the sieve, why can the inner loop start at $p \cdot p$ instead of $2p$?
2. What are the prime factors of 1001, and how many divisors does it have?
3. After the factorisation loop finishes with $n > 1$, why is the leftover $n$ a prime?
4. How many divisors does $2^{10}$ have, and how many does $2^5 \cdot 3^5$ have?

# Chapter 3. The GCD and the Euclidean algorithm

## 3.1 Greatest common divisor

The **greatest common divisor** of two numbers, written $\gcd(a, b)$, is the largest number that divides both. For 12 and 18 the common divisors are 1, 2, 3 and 6, so $\gcd(12, 18) = 6$. Two numbers whose gcd is 1 are called **coprime**: they share no prime factor. For instance 8 and 15 are coprime.

We could find the gcd by comparing the prime factorisations, but there is a far faster method, found by Euclid. It rests on one observation: any number that divides both $a$ and $b$ also divides $a - b$, and also divides the remainder of $a$ divided by $b$. So $\gcd(a, b) = \gcd(b, a \bmod b)$. We repeat this until the second number becomes 0, and then the answer is the first number, because $\gcd(a, 0) = a$.

Let us trace $\gcd(252, 105)$. We have $252 = 2 \cdot 105 + 42$, so we continue with $(105, 42)$. Then $105 = 2 \cdot 42 + 21$, so we continue with $(42, 21)$. Then $42 = 2 \cdot 21 + 0$, so we continue with $(21, 0)$, and the answer is 21.

```python
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a // gcd(a, b) * b

assert gcd(252, 105) == 21
assert gcd(8, 15) == 1
assert gcd(0, 7) == 7
assert lcm(4, 6) == 12
```

```cpp
long long gcd_euclid(long long a, long long b) {
    while (b != 0) {
        long long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

long long lcm_euclid(long long a, long long b) {
    return a / gcd_euclid(a, b) * b;
}
```

Each step makes the numbers much smaller (the remainder is less than half of the larger number after two steps), so the loop runs only $O(\log \min(a, b))$ times. The **least common multiple** of $a$ and $b$ is the smallest number that both divide, and it satisfies $\gcd(a, b) \cdot \operatorname{lcm}(a, b) = a \cdot b$. We divide before multiplying in `lcm` to keep the numbers small.

## 3.2 Extended Euclid: finding the coefficients

There is a beautiful fact called **Bézout's identity**: for any two numbers $a$ and $b$ there are whole numbers $x$ and $y$ (they may be negative) such that

$$a x + b y = \gcd(a, b).$$

For example, with $a = 252$ and $b = 105$ the gcd is 21, and $252 \cdot (-2) + 105 \cdot 5 = -504 + 525 = 21$. The **extended Euclidean algorithm** finds $x$ and $y$ together with the gcd by remembering the steps of Euclid's algorithm. The idea is recursive. Suppose we already know $x'$ and $y'$ with $b x' + (a \bmod b) y' = g$. Since $a \bmod b = a - \lfloor a / b \rfloor b$, we can rewrite this as $a y' + b (x' - \lfloor a/b \rfloor y') = g$. So $x = y'$ and $y = x' - \lfloor a/b \rfloor y'$.

```python
def ext_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = ext_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

g, x, y = ext_gcd(252, 105)
assert g == 21 and 252 * x + 105 * y == 21
g, x, y = ext_gcd(3, 7)
assert g == 1 and 3 * x + 7 * y == 1
```

```cpp
long long ext_gcd(long long a, long long b, long long& x, long long& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    long long x1, y1;
    long long g = ext_gcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}
```

The extended algorithm has the same $O(\log \min(a, b))$ cost. We need it in Chapter 5 to compute modular inverses and in Chapter 7 to combine remainder conditions.

## 3.3 Check yourself

1. Why is $\gcd(a, b) = \gcd(b, a \bmod b)$?
2. Compute $\gcd(84, 36)$ and $\operatorname{lcm}(84, 36)$ by hand.
3. If $\gcd(a, b) = 1$, what does Bézout's identity say about $x$ and $y$?
4. Why does `lcm` divide by the gcd first and then multiply?

# Chapter 4. Powers with remainders

## 4.1 Why we need fast powers

Suppose we want $3^{1000000} \bmod 1000$. The number $3^{1000000}$ has almost half a million digits, so we cannot write it down. We could multiply by 3 one million times and take the remainder each time (we may, by the rule from Chapter 1), but a million steps is wasteful, and for exponents like $10^{18}$ it is impossible.

The trick is **fast exponentiation**, also called **binary exponentiation** or **square and multiply**. The idea is that squaring doubles the exponent in one step. We know $a^{2k} = (a^k)^2$ and $a^{2k+1} = a \cdot (a^k)^2$. So to compute $a^n$ we compute $a^{\lfloor n/2 \rfloor}$ once, square it, and multiply by one extra $a$ if $n$ is odd. The exponent halves each time, so we need only about $\log_2 n$ steps.

Let us trace $3^{13}$. Since $13 = 1101$ in binary, we have $3^{13} = 3^8 \cdot 3^4 \cdot 3^1$. We compute the squares $3^1 = 3$, $3^2 = 9$, $3^4 = 81$, $3^8 = 6561$ and multiply together those whose bit in 13 is 1: $6561 \cdot 81 \cdot 3 = 1594323$.

```python
def power_mod(a, n, m):
    result = 1 % m
    a %= m
    while n > 0:
        if n & 1:
            result = result * a % m
        a = a * a % m
        n >>= 1
    return result

assert power_mod(3, 13, 10**9) == 1594323
assert power_mod(2, 10, 1000) == 24
assert power_mod(5, 0, 7) == 1
assert power_mod(3, 10**18, 1000) == pow(3, 10**18, 1000)
```

```cpp
long long power_mod(long long a, long long n, long long m) {
    long long result = 1 % m;
    a %= m;
    while (n > 0) {
        if (n & 1) result = result * a % m;
        a = a * a % m;
        n >>= 1;
    }
    return result;
}
```

The loop runs $O(\log n)$ times. In C++, the products stay below $m^2$, so they fit in a 64-bit integer when $m$ is below about $3 \cdot 10^9$. In Python there is also the built-in `pow(a, n, m)`, which does the same thing.

## 4.2 Powers with a huge exponent given as digits

Sometimes the exponent itself is too large to store, and we get it as a list of its decimal digits. This is the problem _Super Pow_: compute $a^b \bmod 1337$, where $b$ is given as a list of digits, such as `[1, 0]` for 10.

We can use the rule $a^{10 x + d} = (a^x)^{10} \cdot a^d$. So we process the digits from left to right, keeping the value of $a^{\text{(digits read so far)}} \bmod m$. When a new digit $d$ arrives, the old exponent $x$ becomes $10x + d$, so the new answer is $(\text{old})^{10} \cdot a^d$. Each of these small powers is computed with `power_mod`, so no huge number ever appears.

```python
def super_pow(a, digits, m=1337):
    result = 1
    for d in digits:
        result = power_mod(result, 10, m) * power_mod(a, d, m) % m
    return result

assert super_pow(2, [1, 0]) == pow(2, 10, 1337)
assert super_pow(2, [3]) == 8
assert super_pow(2147483647, [2, 0, 0]) == pow(2147483647, 200, 1337)
```

```cpp
long long super_pow(long long a, const vector<int>& digits, long long m = 1337) {
    long long result = 1;
    for (int d : digits)
        result = power_mod(result, 10, m) * power_mod(a, d, m) % m;
    return result;
}
```

For a list of $L$ digits this takes $O(L)$ steps, each costing a constant number of small fast powers.

## 4.3 Check yourself

1. How many multiplications does fast exponentiation need for $a^{1000}$, roughly?
2. Why do we write `result = 1 % m` and not just `1`?
3. Why can we keep taking remainders in the middle of the computation?
4. In Super Pow, why is the old answer raised to the power 10 when a new digit arrives?

# Chapter 5. Modular inverses and Euler's totient function

## 5.1 Dividing in a world of remainders

We can add, subtract and multiply remainders freely, but division is trickier. If we know $a \bmod m$, we cannot just divide by $b$ and take the remainder, because the result of a division is usually not a whole number. Instead of dividing by $b$, we **multiply by the modular inverse** of $b$.

The **modular inverse** of $a$ modulo $m$ is a number $x$ with $0 \le x < m$ such that $a \cdot x \equiv 1 \pmod m$. For example, modulo 7 the inverse of 3 is 5, because $3 \cdot 5 = 15 = 2 \cdot 7 + 1$. Multiplying by 5 modulo 7 acts exactly like dividing by 3. This is the problem _Modular Inverse_.

An inverse exists exactly when $\gcd(a, m) = 1$. If $a$ and $m$ share a factor, every multiple of $a$ shares that factor with $m$ and can never leave remainder 1. When the gcd is 1, Bézout's identity from Chapter 3 gives numbers $x$ and $y$ with $a x + m y = 1$. Looking at this equation modulo $m$, the term $m y$ disappears, so $a x \equiv 1$, and $x$ is the inverse. We only need to bring $x$ into the range 0 to $m-1$.

```python
def mod_inverse(a, m):
    g, x, _ = ext_gcd(a % m, m)
    if g != 1:
        return -1
    return x % m

def ext_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = ext_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

assert mod_inverse(3, 7) == 5
assert mod_inverse(2, 4) == -1
assert mod_inverse(10, 17) * 10 % 17 == 1
assert mod_inverse(5, 1) == 0
```

```cpp
long long mod_inverse(long long a, long long m) {
    long long x, y;
    long long g = ext_gcd(((a % m) + m) % m, m, x, y);
    if (g != 1) return -1;
    return ((x % m) + m) % m;
}
```

(The helper `ext_gcd` is the one from Chapter 3. The Python version above defines it again so that this block runs on its own.) The cost is $O(\log m)$. For $m = 1$ every number is congruent to 0, and the answer is 0, which the code handles because $x \bmod 1 = 0$.

## 5.2 Euler's totient function

How many numbers between 1 and $n$ are coprime to $n$? The count is called **Euler's totient function** and is written $\varphi(n)$. For $n = 12$ the numbers coprime to 12 are 1, 5, 7, 11, so $\varphi(12) = 4$. This is the problem _Euler Totient_.

We could test every number with gcd, but there is a formula that uses only the prime factors of $n$. Take the numbers from 1 to $n$ and remove those that share a prime factor $p$ with $n$: a fraction $1/p$ of all numbers are multiples of $p$, so a fraction $(1 - 1/p)$ survives. Doing this for every distinct prime factor gives

$$\varphi(n) = n \prod_{p \mid n} \left(1 - \frac{1}{p}\right).$$

For $12 = 2^2 \cdot 3$ we get $12 \cdot \frac12 \cdot \frac23 = 4$. To avoid fractions, we compute it by starting with $n$ and, for each prime $p$ of $n$, replacing the value by `value - value // p`.

```python
def euler_phi(n):
    result = n
    d = 2
    while d * d <= n:
        if n % d == 0:
            while n % d == 0:
                n //= d
            result -= result // d
        d += 1
    if n > 1:
        result -= result // n
    return result

assert euler_phi(12) == 4
assert euler_phi(1) == 1
assert euler_phi(13) == 12
assert euler_phi(36) == 12
```

```cpp
long long euler_phi(long long n) {
    long long result = n;
    for (long long d = 2; d * d <= n; d++) {
        if (n % d == 0) {
            while (n % d == 0) n /= d;
            result -= result / d;
        }
    }
    if (n > 1) result -= result / n;
    return result;
}
```

This is the same loop as prime factorisation, so it costs $O(\sqrt{n})$.

## 5.3 Fermat's little theorem: a shortcut for prime moduli

If $p$ is a prime and $a$ is not a multiple of $p$, then

$$a^{p-1} \equiv 1 \pmod p.$$

This is **Fermat's little theorem**. For example $2^6 = 64 = 9 \cdot 7 + 1$, so $2^6 \equiv 1 \pmod 7$. Multiplying both sides by $a^{-1}$ gives $a^{p-2} \equiv a^{-1}$. So when the modulus is prime, the inverse of $a$ is simply $a^{p-2} \bmod p$, which we can compute with fast exponentiation. This is the usual way to divide modulo $10^9 + 7$, which is a prime.

Euler generalised the theorem to any modulus: if $\gcd(a, m) = 1$ then $a^{\varphi(m)} \equiv 1 \pmod m$.

```python
def inverse_prime(a, p):
    return pow(a, p - 2, p)

P = 10**9 + 7
assert inverse_prime(3, 7) == 5
assert 12345 * inverse_prime(12345, P) % P == 1
assert inverse_prime(2, P) == (P + 1) // 2
```

```cpp
long long inverse_prime(long long a, long long p) {
    return power_mod(a, p - 2, p);
}
```

## 5.4 Check yourself

1. For which $a$ does $a$ have an inverse modulo 12?
2. What is $\varphi(30)$? What is $\varphi(p)$ for a prime $p$?
3. Why does Fermat's theorem give the inverse $a^{p-2}$?
4. Why can we not use Fermat's trick when the modulus is 12?

# Chapter 6. Counting under a modulus

## 6.1 Factorials and binomial coefficients

Counting problems often ask for a huge number "modulo $10^9 + 7$". A very common one is the **binomial coefficient** $\binom{n}{k}$, the number of ways to choose $k$ items out of $n$. It equals

$$\binom{n}{k} = \frac{n!}{k!\,(n-k)!}.$$

The division is the problem: $n!$ is gigantic, and we only keep remainders. Because $10^9 + 7$ is prime, we can divide by multiplying with the modular inverse from Chapter 5. We precompute all factorials $0!, 1!, \dots, n!$ modulo $p$, then the inverse of each factorial, and every $\binom{n}{k}$ becomes three multiplications. This is the problem _Binomial Coefficient Modulo_.

A neat way to get all inverse factorials cheaply is to compute only the last one, $(n!)^{-1}$, with Fermat's trick, and then walk backwards using $(k-1)!^{-1} = k! ^{-1} \cdot k$.

```python
MOD = 10**9 + 7

def make_factorials(n):
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv = [1] * (n + 1)
    inv[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % MOD
    return fact, inv

def binomial_mod(n, k, fact, inv):
    if k < 0 or k > n:
        return 0
    return fact[n] * inv[k] % MOD * inv[n - k] % MOD

fact, inv = make_factorials(1000)
assert binomial_mod(5, 2, fact, inv) == 10
assert binomial_mod(10, 0, fact, inv) == 1
assert binomial_mod(5, 7, fact, inv) == 0
assert binomial_mod(1000, 500, fact, inv) == 159835829
```

```cpp
const long long MOD = 1000000007;

pair<vector<long long>, vector<long long>> make_factorials(int n) {
    vector<long long> fact(n + 1, 1), inv(n + 1, 1);
    for (int i = 1; i <= n; i++) fact[i] = fact[i - 1] * i % MOD;
    inv[n] = power_mod(fact[n], MOD - 2, MOD);
    for (int i = n; i > 0; i--) inv[i - 1] = inv[i] * i % MOD;
    return {fact, inv};
}

long long binomial_mod(int n, int k, const vector<long long>& fact, const vector<long long>& inv) {
    if (k < 0 || k > n) return 0;
    return fact[n] * inv[k] % MOD * inv[n - k] % MOD;
}
```

Precomputing costs $O(n + \log p)$, and each query then costs $O(1)$. If you need only one value for a huge $n$ and a small $k$, you can use the product $\frac{n (n-1) \cdots (n-k+1)}{k!}$ with a single inverse.

## 6.2 Zeros at the end of a factorial

How many zeros does $n!$ end with? A zero at the end comes from a factor of 10, and $10 = 2 \cdot 5$. In $n!$ the number 2 appears far more often than 5, so the number of trailing zeros equals the number of times 5 divides $n!$. This is the problem _Trailing Zeros of Factorial_.

Counting how many times 5 divides $n!$ works like this. Among the numbers $1, \dots, n$ there are $\lfloor n/5 \rfloor$ multiples of 5, and each contributes one factor 5. But multiples of 25 contribute a second one, and there are $\lfloor n/25 \rfloor$ of them. Multiples of 125 contribute a third, and so on:

$$\text{zeros}(n) = \left\lfloor \frac{n}{5} \right\rfloor + \left\lfloor \frac{n}{25} \right\rfloor + \left\lfloor \frac{n}{125} \right\rfloor + \cdots$$

For $n = 100$ this is $20 + 4 = 24$ zeros. The same idea, called **Legendre's formula**, counts how often any prime $p$ divides $n!$.

```python
def trailing_zeros(n):
    count = 0
    power = 5
    while power <= n:
        count += n // power
        power *= 5
    return count

assert trailing_zeros(5) == 1
assert trailing_zeros(100) == 24
assert trailing_zeros(0) == 0
assert trailing_zeros(25) == 6
```

```cpp
long long trailing_zeros(long long n) {
    long long count = 0;
    for (long long power = 5; power <= n; power *= 5) count += n / power;
    return count;
}
```

The loop runs $\log_5 n$ times, so it is $O(\log n)$.

## 6.3 Huge Fibonacci numbers

The Fibonacci numbers are $F_0 = 0$, $F_1 = 1$ and $F_k = F_{k-1} + F_{k-2}$. For $n$ up to $10^{18}$ we cannot loop $n$ times. This is the problem _Fibonacci Modulo_. Here is a fast method called **fast doubling**. From the Fibonacci recurrence one can show

$$F_{2k} = F_k \bigl(2F_{k+1} - F_k\bigr), \qquad F_{2k+1} = F_k^2 + F_{k+1}^2.$$

These formulas let us jump from $(F_k, F_{k+1})$ to $(F_{2k}, F_{2k+1})$ in one step, and then move to $2k+1$ by adding one more step if needed. As with fast exponentiation, the index halves each time, so we need only $O(\log n)$ steps. For example, $F_5 = F_2^2 + F_3^2 = 1 + 4 = 5$ and $F_6 = F_3(2F_4 - F_3) = 2 \cdot (6 - 2) = 8$.

```python
MOD = 10**9 + 7

def fib_pair(n):
    if n == 0:
        return 0, 1
    a, b = fib_pair(n // 2)
    c = a * ((2 * b - a) % MOD) % MOD
    d = (a * a + b * b) % MOD
    if n % 2 == 0:
        return c, d
    return d, (c + d) % MOD

def fib_mod(n):
    return fib_pair(n)[0]

assert [fib_mod(i) for i in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
assert fib_mod(50) == 12586269025 % MOD
assert fib_mod(10**18) == 209783453
```

```cpp
pair<long long, long long> fib_pair(long long n) {
    if (n == 0) return {0, 1};
    auto [a, b] = fib_pair(n / 2);
    long long c = a * ((2 * b - a + MOD) % MOD) % MOD;
    long long d = (a * a + b * b) % MOD;
    if (n % 2 == 0) return {c, d};
    return {d, (c + d) % MOD};
}

long long fib_mod(long long n) {
    return fib_pair(n).first;
}
```

The recursion goes about $\log_2 n$ levels deep, and each level does a few multiplications, so the cost is $O(\log n)$.

## 6.4 Check yourself

1. Why must the modulus be prime for the inverse-factorial method to work?
2. How many zeros does $200!$ end with?
3. Why do trailing zeros of $n!$ depend only on the factor 5, not on 2?
4. Use fast doubling to find $F_{10}$ from $F_5$ and $F_6$.

# Chapter 7. Combining remainder conditions

## 7.1 The Chinese remainder idea

Here is an old puzzle. A number leaves remainder 2 when divided by 3, and remainder 3 when divided by 5. What could it be? We are looking for $x$ with $x \equiv 2 \pmod 3$ and $x \equiv 3 \pmod 5$. Listing numbers that leave remainder 2 modulo 3 gives 2, 5, 8, 11, 14, 17, and so on; the first one that leaves remainder 3 modulo 5 is 8. The next solution is $8 + 15 = 23$, because adding $3 \cdot 5 = 15$ changes neither remainder. So the solutions are $8, 23, 38, \dots$, all congruent to 8 modulo 15.

This is the **Chinese remainder theorem**, or **CRT**: when the moduli are coprime, a system of remainder conditions always has a solution, and it is unique modulo the product of the moduli. The problem _Chinese Remainder Theorem_ asks for the smallest non-negative solution, and it allows moduli that are **not** coprime, in which case there may be no solution at all. For example $x \equiv 1 \pmod 4$ and $x \equiv 2 \pmod 6$ is impossible: the first says $x$ is odd and the second says $x$ is even.

## 7.2 Merging two conditions at a time

The easiest way to solve a whole list of conditions is to merge them two at a time. Suppose we already know $x \equiv r_1 \pmod{m_1}$ and we add $x \equiv r_2 \pmod{m_2}$. Every solution of the first condition has the form $x = r_1 + m_1 t$ for some whole number $t$. Putting this into the second condition gives

$$m_1 t \equiv r_2 - r_1 \pmod{m_2}.$$

Let $g = \gcd(m_1, m_2)$. This equation has a solution only if $g$ divides $r_2 - r_1$; otherwise the conditions contradict each other, like the odd and even example above. If it does divide, we can divide the whole equation by $g$ to get $\frac{m_1}{g} t \equiv \frac{r_2 - r_1}{g} \pmod{\frac{m_2}{g}}$. Now $\frac{m_1}{g}$ and $\frac{m_2}{g}$ are coprime, so $\frac{m_1}{g}$ has an inverse modulo $\frac{m_2}{g}$ (Chapter 5), and we can solve for $t$. The merged condition is $x \equiv r_1 + m_1 t$ modulo $\operatorname{lcm}(m_1, m_2) = \frac{m_1 m_2}{g}$.

Starting from the empty condition $x \equiv 0 \pmod 1$ and merging every condition in turn, we get the final answer. The result, in the range 0 to the final modulus minus 1, is the smallest non-negative $x$.

```python
def ext_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = ext_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def solve_congruences(remainders, moduli):
    r, m = 0, 1
    for r2, m2 in zip(remainders, moduli):
        r2 %= m2
        g, p, _ = ext_gcd(m, m2)
        if (r2 - r) % g != 0:
            return -1
        step = m2 // g
        t = ((r2 - r) // g) * p % step
        r = r + m * t
        m = m // g * m2
        r %= m
    return r

assert solve_congruences([2, 3], [3, 5]) == 8
assert solve_congruences([1, 2], [4, 6]) == -1
assert solve_congruences([2, 3, 2], [3, 5, 7]) == 23
assert solve_congruences([], []) == 0
assert solve_congruences([1, 3], [4, 6]) == 9
```

```cpp
long long ext_gcd(long long a, long long b, long long& x, long long& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    long long x1, y1;
    long long g = ext_gcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

long long solve_congruences(const vector<long long>& remainders, const vector<long long>& moduli) {
    long long r = 0, m = 1;
    for (size_t i = 0; i < remainders.size(); i++) {
        long long m2 = moduli[i];
        long long r2 = ((remainders[i] % m2) + m2) % m2;
        long long p, q;
        long long g = ext_gcd(m, m2, p, q);
        if ((r2 - r) % g != 0) return -1;
        long long step = m2 / g;
        long long t = (((r2 - r) / g) % step * (p % step)) % step;
        if (t < 0) t += step;
        r = r + m * t;
        m = m / g * m2;
        r %= m;
    }
    return r;
}
```

Each merge costs $O(\log m)$, so a list of $k$ conditions costs $O(k \log m)$. A warning for C++: the numbers $m$ can grow up to the lcm of all moduli, so the products must fit in 64 bits; the contest versions of this problem promise that they do. In Python, integers never overflow.

## 7.3 Check yourself

1. Find the smallest $x$ with $x \equiv 1 \pmod 3$ and $x \equiv 2 \pmod 4$.
2. Why do $x \equiv 1 \pmod 4$ and $x \equiv 2 \pmod 6$ have no solution?
3. After merging two conditions, what is the new modulus?
4. What happens in the merging step if the moduli are coprime?

# Chapter 8. Testing huge numbers for primality

## 8.1 Why trial division is not enough

Trial division needs about $\sqrt{n}$ steps. For a 18-digit number that is a billion steps, which is far too slow if we have many numbers to test. We need a test that takes time proportional to the number of digits, not to the number itself. The tool is the **Miller–Rabin test**, and it is the topic of the problem _Miller Rabin Primality_.

The starting point is Fermat's little theorem from Chapter 5: if $n$ is prime and $a$ is not a multiple of $n$, then $a^{n-1} \equiv 1 \pmod n$. We can run this as a test: pick $a$, compute $a^{n-1} \bmod n$ with fast exponentiation, and if the answer is not 1, then $n$ is certainly composite. Unfortunately some composite numbers, such as 561, pass the test for every $a$ (they are called Carmichael numbers). Miller and Rabin strengthened the test to remove this weakness.

## 8.2 The stronger test

Write $n - 1 = d \cdot 2^s$ with $d$ odd, by pulling out all factors of 2. For a prime $n$, consider the sequence

$$a^d,\; a^{2d},\; a^{4d},\; \dots,\; a^{2^s d} = a^{n-1} \pmod n.$$

Each term is the square of the previous one. The last term is 1 by Fermat. For a prime modulus, the only numbers whose square is 1 are 1 and $n - 1$ (the only square roots of 1). So going backwards, the sequence must either start with $a^d \equiv 1$, or contain $n - 1$ somewhere before it reaches 1. If neither happens, $n$ is composite, and $a$ is called a **witness** of its compositeness.

One witness is enough to prove a number composite. And a handful of fixed bases is enough to be certain for every number below $2^{64}$: it is known that testing the twelve bases $2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37$ gives the correct answer for all 64-bit numbers. So this version is not random at all; it is exact.

```python
def is_prime(n):
    if n < 2:
        return False
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

assert [p for p in range(30) if is_prime(p)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
assert not is_prime(561)
assert not is_prime(3215031751)
assert is_prime(1_000_000_007)
assert is_prime(2**61 - 1)
assert not is_prime(2**61 + 1)
```

```cpp
long long mul_mod_big(long long a, long long b, long long m) {
    return (__int128)a * b % m;
}

long long power_mod_big(long long a, long long n, long long m) {
    long long result = 1;
    a %= m;
    while (n > 0) {
        if (n & 1) result = mul_mod_big(result, a, m);
        a = mul_mod_big(a, a, m);
        n >>= 1;
    }
    return result;
}

bool is_prime(long long n) {
    if (n < 2) return false;
    long long small[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    for (long long p : small) {
        if (n % p == 0) return n == p;
    }
    long long d = n - 1;
    int s = 0;
    while (d % 2 == 0) {
        d /= 2;
        s++;
    }
    for (long long a : small) {
        long long x = power_mod_big(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool composite = true;
        for (int i = 0; i < s - 1; i++) {
            x = mul_mod_big(x, x, n);
            if (x == n - 1) {
                composite = false;
                break;
            }
        }
        if (composite) return false;
    }
    return true;
}
```

Each base costs $O(\log n)$ multiplications, and there are twelve bases, so one test takes $O(\log n)$ time, a few microseconds even for 18-digit numbers. In C++ the product of two 64-bit numbers can overflow, so we multiply in 128 bits (`__int128`) before taking the remainder.

## 8.3 Check yourself

1. Write $n - 1 = d \cdot 2^s$ for $n = 97$: what are $d$ and $s$?
2. Why does one witness prove that a number is composite?
3. Why is the number 561 a good example of why plain Fermat testing is not enough?
4. Why do we use `__int128` in the C++ version?

# Chapter 9. Counting with digits

## 9.1 Counting the digit one

How many times does the digit 1 appear when we write all numbers from 1 to $n$? For $n = 13$ the numbers 1, 10, 11, 12, 13 contain six 1s (11 contains two). This is the problem _Count Digit One_. Writing out every number takes too long for $n$ up to $10^9$, so we count position by position instead.

Take one position at a time, say the tens position, of the numbers from 1 to $n$. Split $n$ around that position into three parts: the digits above it (**high**), the digit at it (**cur**), and the digits below it (**low**). For $n = 314$ and the tens position, high is 3, cur is 1 and low is 4. The tens digit cycles through 0 to 9 in blocks of length 100. Every complete block (the high part counts how many there are) has exactly 10 numbers with tens digit 1. So complete blocks contribute $\text{high} \cdot 10$. In the last, incomplete block, the numbers with tens digit 1 are: none if cur is 0; all of them (that is, $\text{low} + 1$) if cur is 1; or a full ten if cur is above 1.

For a position with value $p$ (1, 10, 100, and so on), the count is

$$\text{high} \cdot p + \begin{cases} 0 & \text{cur} = 0 \\ \text{low} + 1 & \text{cur} = 1 \\ p & \text{cur} > 1. \end{cases}$$

Adding this up over all positions gives the answer, in $O(\log n)$ time.

```python
def count_digit_one(n):
    total = 0
    p = 1
    while p <= n:
        high = n // (p * 10)
        cur = (n // p) % 10
        low = n % p
        total += high * p
        if cur > 1:
            total += p
        elif cur == 1:
            total += low + 1
        p *= 10
    return total

assert count_digit_one(13) == 6
assert count_digit_one(0) == 0
assert count_digit_one(100) == 21
assert count_digit_one(314) == sum(str(i).count("1") for i in range(1, 315))
```

```cpp
long long count_digit_one(long long n) {
    long long total = 0;
    for (long long p = 1; p <= n; p *= 10) {
        long long high = n / (p * 10);
        long long cur = (n / p) % 10;
        long long low = n % p;
        total += high * p;
        if (cur > 1) total += p;
        else if (cur == 1) total += low + 1;
    }
    return total;
}
```

## 9.2 The nth digit of an endless string

Write all positive numbers one after another: 123456789101112... We want the $n$-th digit. This is the problem _Nth Digit_. We first find which number the digit belongs to, then which digit of that number.

The 1-digit numbers 1 to 9 give 9 digits. The 2-digit numbers 10 to 99 give $90 \cdot 2 = 180$ digits, the 3-digit numbers give $900 \cdot 3$, and in general the $L$-digit numbers give $9 \cdot 10^{L-1} \cdot L$ digits. We subtract these block sizes from $n$ until the remaining $n$ falls inside a block. Then, inside the block of length-$L$ numbers, the number we want is $10^{L-1} + (n-1) \,//\, L$, and the digit we want is the $((n-1) \bmod L)$-th digit of it, counting from 0 on the left.

For $n = 11$: subtract 9 to get 2, so we are in the 2-digit block. The number is $10 + (2-1) // 2 = 10$ and the digit index is $(2-1) \bmod 2 = 1$, the second digit of 10, which is 0.

```python
def nth_digit(n):
    length, count, start = 1, 9, 1
    while n > length * count:
        n -= length * count
        length += 1
        count *= 10
        start *= 10
    number = start + (n - 1) // length
    return int(str(number)[(n - 1) % length])

assert nth_digit(11) == 0
assert nth_digit(3) == 3
assert nth_digit(10) == 1
assert nth_digit(190) == 1
assert nth_digit(1000) == int("".join(str(i) for i in range(1, 400))[999])
```

```cpp
int nth_digit(long long n) {
    long long length = 1, count = 9, start = 1;
    while (n > length * count) {
        n -= length * count;
        length++;
        count *= 10;
        start *= 10;
    }
    long long number = start + (n - 1) / length;
    string s = to_string(number);
    return s[(n - 1) % length] - '0';
}
```

The loop runs once per digit length, so it is $O(\log n)$.

## 9.3 Check yourself

1. In the digit-one count, what are high, cur and low for $n = 5207$ and the hundreds position?
2. How many 1s appear in the numbers from 1 to 99?
3. How many digits do all the numbers from 1 to 999 have in total?
4. Which number holds the 15th digit of 123456789101112...?

# Chapter 10. Sums over divisors

## 10.1 Counting pairs instead of divisors

Let $d(k)$ be the number of divisors of $k$. The problem _Sum of Divisor Counts_ asks for $d(1) + d(2) + \cdots + d(n)$. Computing $d(k)$ for every $k$ by factorisation would work for moderate $n$, but there is a much simpler view.

The sum counts pairs $(k, j)$ where $j$ divides $k$ and $k \le n$. Instead of fixing $k$ and counting its divisors $j$, fix the divisor $j$ and count how many numbers up to $n$ it divides: those are $j, 2j, 3j, \dots$, and there are $\lfloor n/j \rfloor$ of them. So

$$\sum_{k=1}^{n} d(k) = \sum_{j=1}^{n} \left\lfloor \frac{n}{j} \right\rfloor.$$

For $n = 6$ the terms are $6, 3, 2, 1, 1, 1$, which add up to 14, and indeed $d(1..6) = 1, 2, 2, 3, 2, 4$ also adds up to 14.

```python
def sum_divisor_counts_slow(n):
    return sum(n // j for j in range(1, n + 1))

assert sum_divisor_counts_slow(6) == 14
assert sum_divisor_counts_slow(1) == 1
```

```cpp
long long sum_divisor_counts_slow(long long n) {
    long long total = 0;
    for (long long j = 1; j <= n; j++) total += n / j;
    return total;
}
```

This costs $O(n)$, which is fine for $n$ up to about $10^7$ but too slow for $n = 10^{12}$.

## 10.2 Grouping equal quotients

Look at the values of $\lfloor n/j \rfloor$ for $n = 100$: for $j = 1, 2, 3, \dots$ they are 100, 50, 33, 25, 20, 16, 14, 12, 11, 10, and for large $j$ the same value repeats many times (all $j$ from 51 to 100 give 1). The number of **different** values of $\lfloor n/j \rfloor$ is only about $2\sqrt{n}$: for $j \le \sqrt{n}$ there are at most $\sqrt{n}$ different values, and for $j > \sqrt{n}$ the quotient is below $\sqrt{n}$, so it takes at most $\sqrt{n}$ different values.

So we can jump over whole runs of equal quotients. If the current $j$ has quotient $q = \lfloor n/j \rfloor$, the run of equal quotients ends at $j' = \lfloor n/q \rfloor$. We add $q \cdot (j' - j + 1)$ and continue from $j' + 1$. This **quotient grouping** cuts the work to $O(\sqrt{n})$.

```python
def sum_divisor_counts(n):
    total = 0
    j = 1
    while j <= n:
        q = n // j
        last = n // q
        total += q * (last - j + 1)
        j = last + 1
    return total

assert sum_divisor_counts(6) == 14
assert sum_divisor_counts(100) == sum_divisor_counts_slow(100)
assert sum_divisor_counts(10**5) == sum_divisor_counts_slow(10**5)
assert sum_divisor_counts(1) == 1
```

```cpp
long long sum_divisor_counts(long long n) {
    long long total = 0;
    for (long long j = 1; j <= n;) {
        long long q = n / j;
        long long last = n / q;
        total += q * (last - j + 1);
        j = last + 1;
    }
    return total;
}
```

Quotient grouping is a handy trick whenever a formula contains $\lfloor n / j \rfloor$, for example in sums of divisors and in counting coprime pairs.

## 10.3 Check yourself

1. Why does $\sum d(k)$ equal $\sum \lfloor n/j \rfloor$?
2. For $n = 10$, list the runs of equal $\lfloor 10/j \rfloor$ and the jumps the grouping loop makes.
3. Why are there only about $2\sqrt{n}$ different quotient values?
4. How would you count the pairs $(a, b)$ with $a b \le n$?

# Chapter 11. Counting with geometry and the gcd

## 11.1 Points on one line

Given points on a plane, find the largest number of points that lie on one straight line. This is the problem _Max Points on a Line_. A direct approach checks every triple of points, costing $O(n^3)$. A better idea is to fix one point $P$ and look at the **direction** from $P$ to every other point. All points on one line through $P$ have the same direction (the same slope), so we count how many other points share each direction and take the biggest group, plus $P$ itself. Doing this for every choice of $P$ costs $O(n^2)$.

The trap is how to compare slopes. The slope $dy / dx$ as a decimal number can be wrong because of rounding. Instead we keep it as a pair of whole numbers $(dy, dx)$ and **reduce it with the gcd** so that, for example, $(2, 4)$ and $(1, 2)$ become the same pair. We also fix the sign (so that $(-1, 2)$ and $(1, -2)$ are equal) and handle vertical lines, where $dx = 0$, by the pair $(1, 0)$.

```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def max_points(points):
    n = len(points)
    best = min(n, 2)
    for i in range(n):
        counts = {}
        for j in range(i + 1, n):
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            g = gcd(abs(dx), abs(dy))
            dx, dy = dx // g, dy // g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            counts[(dx, dy)] = counts.get((dx, dy), 0) + 1
            best = max(best, counts[(dx, dy)] + 1)
    return best

assert max_points([[1, 1], [2, 2], [3, 3]]) == 3
assert max_points([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]) == 4
assert max_points([[0, 0]]) == 1
assert max_points([[0, 0], [0, 5], [0, 9]]) == 3
```

```cpp
int max_points(const vector<vector<int>>& points) {
    int n = points.size();
    int best = min(n, 2);
    for (int i = 0; i < n; i++) {
        map<pair<int, int>, int> counts;
        for (int j = i + 1; j < n; j++) {
            int dx = points[j][0] - points[i][0];
            int dy = points[j][1] - points[i][1];
            int g = __gcd(abs(dx), abs(dy));
            dx /= g;
            dy /= g;
            if (dx < 0 || (dx == 0 && dy < 0)) {
                dx = -dx;
                dy = -dy;
            }
            best = max(best, ++counts[{dx, dy}] + 1);
        }
    }
    return best;
}
```

The points in the problem are all different, so the gcd is never 0 (if both $dx$ and $dy$ were 0, the points would coincide). The cost is $O(n^2)$ pairs, each doing one gcd and one dictionary update.

## 11.2 Check yourself

1. Why is comparing slopes as decimal numbers risky?
2. After reducing by the gcd, why do we also fix the sign of the pair?
3. Why do we add 1 to the biggest group count?
4. What is the cost of the method for 1000 points?

# Chapter 12. Putting the tools together

## 12.1 Choosing the right tool

When a number problem appears, ask what it is really about. If you must test or list primes below a limit that you can store, use the sieve. If you must factor or analyse a single number up to about $10^{12}$, use trial division up to $\sqrt{n}$. If the number is enormous, up to $10^{18}$, use Miller–Rabin. If an answer is asked "modulo $10^9 + 7$" and involves division, multiply by a modular inverse. If an exponent is huge, use fast exponentiation, and if an index is huge, think of fast doubling. If remainders from different moduli must be combined, merge them with CRT. And if a sum contains $\lfloor n/j \rfloor$, group equal quotients.

## 12.2 Common mistakes

The usual slips are all small. Forgetting to take the remainder after each multiplication makes numbers overflow in C++. Subtracting in C++ without adding the modulus gives negative remainders. Using the inverse trick with a modulus that is not prime breaks it; use extended Euclid instead. Looping up to $n$ where $\sqrt{n}$ is enough turns a fast solution into a timeout. Writing `d * d <= n` with `int` overflows for large $n$, so use `long long`. And when a problem says "return $-1$ if impossible", remember to check the gcd condition before dividing.

## 12.3 Check yourself

1. Which tool counts the primes below $10^7$, and which tests a single 18-digit number?
2. When can you use Fermat's trick for an inverse, and what do you use otherwise?
3. What do you do when an answer needs $\binom{n}{k}$ modulo $10^9 + 7$ for many queries?
4. Name two places where $\sqrt{n}$ (and not $n$) is the right loop limit.

# Sources and credit

Several chapters adapt ideas from articles on [cp-algorithms.com](https://cp-algorithms.com), including the sieve of Eratosthenes, the Euclidean algorithm, binary exponentiation, the modular inverse, Euler's totient function, the Chinese remainder theorem, primality tests, binomial coefficients, Fibonacci numbers and factorials modulo a prime. The text here is rewritten for beginners. Like the original, it is shared under the Creative Commons Attribution-ShareAlike 4.0 licence.
