> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Bit manipulation)

This page teaches bit manipulation: working directly with the 0s and 1s that a computer uses to store every number. Once you can see a number as a row of switches that are either off or on, a surprising number of problems become short and fast: counting, checking, swapping, adding, and even finding the best pair in a list.

The page is a staircase. **Chapter 1 is gentle**: it only explains what binary numbers are and how to read them, with no special tricks. Each next chapter adds one new idea (the basic operators, the famous `n & (n - 1)` trick, XOR magic, adding without a plus sign, and finally counting bit by bit and a trie of bits). Every chapter uses only what came before. Every code example is shown in Python and in C++, so pick whichever you like.

# Chapter 1. Numbers as rows of switches

## 1.1 What binary means

In everyday life we write numbers with ten digits, 0 to 9, and each place is worth ten times the place to its right. In 405, the 5 is worth 5, the 0 is worth 0 tens, and the 4 is worth 4 hundreds.

Computers use only two digits, 0 and 1, so each place is worth **two** times the place to its right. A single 0 or 1 is called a **bit** (short for "binary digit"). Reading from the right, the places are worth 1, 2, 4, 8, 16, 32 and so on, the powers of two. To read a binary number, add up the place values wherever there is a 1.

```
binary   1    1    0    1
place    8    4    2    1
value    8 +  4 +  0 +  1  = 13
```

So `1101` in binary is the number 13. We call the rightmost bit **bit 0**, the next one **bit 1**, and so on, so bit $i$ is worth $2^i$. Bit 0 is also called the **lowest** bit (or least significant bit); the leftmost 1 is the **highest** bit.

## 1.2 Turning a number into bits

To go the other way, repeatedly ask "is the number odd or even?" and then cut it in half. The remainder when dividing by 2 is the next bit, starting from the lowest. For 13: it is odd (bit 1), half of it rounded down is 6; 6 is even (bit 0), half is 3; 3 is odd (bit 1), half is 1; 1 is odd (bit 1), half is 0, and we stop. The bits we collected, lowest first, are 1, 0, 1, 1, so reading them back to front gives `1101`.

```python
def to_binary(n):
    if n == 0:
        return "0"
    bits = []
    while n > 0:
        bits.append(str(n % 2))   # the lowest bit
        n = n // 2                # drop that bit
    return "".join(reversed(bits))


assert to_binary(13) == "1101"
assert to_binary(8) == "1000"
assert to_binary(0) == "0"
```

```cpp
string to_binary(long long n) {
    if (n == 0) return "0";
    string bits;
    while (n > 0) {
        bits.push_back(char('0' + n % 2));   // the lowest bit
        n /= 2;                              // drop that bit
    }
    reverse(bits.begin(), bits.end());
    return bits;
}
```

The loop runs once per bit, which is about $\log_2 n$ times, so the time is $O(\log n)$ and the space is $O(\log n)$ for the string. Python also has the built-in `bin(13)`, which gives `'0b1101'`.

## 1.3 Counting the ones by hand

A bit that equals 1 is called a **set** bit. The first real question of this page is: how many set bits does a number have? The idea from the previous section already answers it. Every time the number is odd, its lowest bit is 1, so we count it. Then we cut the number in half to move on to the next bit.

```python
def count_set_bits_slow(n):
    count = 0
    while n > 0:
        count += n % 2     # 1 if the lowest bit is set
        n //= 2
    return count


assert count_set_bits_slow(13) == 3
assert count_set_bits_slow(0) == 0
assert count_set_bits_slow(255) == 8
```

```cpp
int count_set_bits_slow(long long n) {
    int count = 0;
    while (n > 0) {
        count += n % 2;    // 1 if the lowest bit is set
        n /= 2;
    }
    return count;
}
```

This takes one round per bit of the number, $O(\log n)$ time and $O(1)$ extra space. It is correct, and later we will make it faster when a number has few set bits. This is the starting point of the sheet problem _Count the Set Bits_, which we will finish properly in Chapter 3.

## 1.4 Check yourself

1. What number is `10110` in binary?
2. What is the binary form of 20?
3. Which place value does bit 5 stand for?
4. How many set bits does 255 have, and why?

# Chapter 2. The bit operators

## 2.1 AND, OR and XOR

Dividing by two works, but computers can look at all the bits of two numbers at once with **bitwise operators**. Each one compares the numbers bit by bit: the bits at position 0 are compared with each other, then the bits at position 1, and so on.

**AND** (written `&`) gives 1 only if both bits are 1. **OR** (written `|`) gives 1 if at least one bit is 1. **XOR** (written `^`, short for "exclusive or") gives 1 if the two bits are different.

```
 a  b | a&b  a|b  a^b
 0  0 |  0    0    0
 0  1 |  0    1    1
 1  0 |  0    1    1
 1  1 |  1    1    0
```

Take 5 (`101`) and 6 (`110`) and line them up:

```
  101   (5)
  110   (6)
  ---
  100   5 & 6 = 4
  111   5 | 6 = 7
  011   5 ^ 6 = 3
```

A good way to remember them: AND is "both", OR is "either", and XOR is "exactly one" (or "they differ"). A last operator, **NOT** (`~` in both languages), flips every bit; we will meet it when we talk about negative numbers.

## 2.2 Shifts

A **shift** slides all the bits sideways. `x << k` moves every bit $k$ places to the left and fills the right with zeros, which multiplies the number by $2^k$. `x >> k` moves the bits right and the lowest $k$ bits fall off, which divides by $2^k$ and rounds down.

```
 5       = 101
 5 << 1  = 1010   (10)
 5 << 2  = 10100  (20)
 5 >> 1  = 10     (2)
```

The expression `1 << i` is the most useful one of all: it is a number with a single 1 at position $i$ (the value $2^i$). Such a number is called a **mask**, because we can lay it over another number to look at just one bit.

## 2.3 Reading and changing one bit

With a mask we can do four small jobs on bit $i$ of a number $x$. To **get** the bit, shift $x$ right by $i$ so the wanted bit lands at position 0, and AND with 1 to throw the rest away. To **set** it to 1, OR with the mask. To **clear** it to 0, AND with the opposite of the mask (`~mask` has every bit set except bit $i$). To **toggle** it, XOR with the mask, which flips that bit and leaves the others alone.

```python
def get_bit(x, i):
    return (x >> i) & 1


def set_bit(x, i):
    return x | (1 << i)


def clear_bit(x, i):
    return x & ~(1 << i)


def toggle_bit(x, i):
    return x ^ (1 << i)


assert get_bit(13, 0) == 1 and get_bit(13, 1) == 0     # 1101
assert set_bit(13, 1) == 15                             # 1101 -> 1111
assert clear_bit(13, 2) == 9                            # 1101 -> 1001
assert toggle_bit(13, 3) == 5                           # 1101 -> 0101
```

```cpp
int get_bit(long long x, int i) {
    return (x >> i) & 1;
}

long long set_bit(long long x, int i) {
    return x | (1LL << i);
}

long long clear_bit(long long x, int i) {
    return x & ~(1LL << i);
}

long long toggle_bit(long long x, int i) {
    return x ^ (1LL << i);
}
```

In C++ write `1LL << i` (a 64-bit one) whenever $i$ could reach 31 or more; a plain `1 << 31` overflows an `int`. Each function is a few machine instructions, $O(1)$ time and space.

## 2.4 Odd, even and halving

Bit 0 decides whether a number is odd, so `x & 1` is 1 for odd numbers and 0 for even numbers, a faster way to write `x % 2`. In the same spirit, `x >> 1` is `x // 2`, and `x << 1` is `x * 2`. Our slow bit counter from Chapter 1 can now be written with operators; it does exactly the same work.

```python
def count_set_bits_shift(n):
    count = 0
    while n > 0:
        count += n & 1
        n >>= 1
    return count


assert count_set_bits_shift(13) == 3
assert count_set_bits_shift(7) == 3
assert count_set_bits_shift(64) == 1
```

```cpp
int count_set_bits_shift(long long n) {
    int count = 0;
    while (n > 0) {
        count += n & 1;
        n >>= 1;
    }
    return count;
}
```

## 2.5 Check yourself

1. What are `12 & 10`, `12 | 10` and `12 ^ 10`?
2. What does `1 << 4` equal?
3. Which operator and mask do you use to turn bit 3 of a number off?
4. What is `37 >> 2`?

# Chapter 3. Clearing the lowest bit

## 3.1 The n and n minus one trick

Here is one of the best-known tricks in programming. Look at what happens to the bits when you subtract 1 from a number. Subtracting 1 turns the lowest set bit into 0 and turns all the zeros _below_ it into 1s, because of borrowing, just like 1000 - 1 = 999 in decimal. Everything above the lowest set bit stays as it was.

```
n      = 101000   (40)
n - 1  = 100111   (39)
n&(n-1)= 100000   (32)
```

Now AND the two: the part above the lowest set bit is the same in both, so it survives. The lowest set bit itself is 1 in $n$ but 0 in $n-1$, and the zeros below it are 0 in $n$ but 1 in $n-1$. So all of those disappear. The result is $n$ with **its lowest set bit removed**. In one operation, `n & (n - 1)` removes exactly one set bit.

## 3.2 Counting set bits faster

If each `n & (n - 1)` removes one set bit, we can count how many times we need it until the number reaches 0. That count is exactly the number of set bits. This is called **Kernighan's method**. For 12 (`1100`): $12 \,\&\, 11 = 8$ (`1000`), then $8 \,\&\, 7 = 0$. Two rounds, and 12 indeed has two set bits.

This is exactly the problem _Count the Set Bits_.

```python
def count_set_bits(n):
    count = 0
    while n:
        n &= n - 1     # remove the lowest set bit
        count += 1
    return count


assert count_set_bits(13) == 3
assert count_set_bits(12) == 2
assert count_set_bits(0) == 0
assert count_set_bits(2**61) == 1
```

```cpp
int count_set_bits(long long n) {
    int count = 0;
    while (n) {
        n &= n - 1;    // remove the lowest set bit
        count++;
    }
    return count;
}
```

Unlike the shifting loop, this one runs once per _set_ bit instead of once per bit: time is $O(s)$ where $s$ is the number of set bits, and space is $O(1)$. For a number like $2^{60}$ that is one round instead of sixty-one.

## 3.3 Is it a power of two?

A power of two (1, 2, 4, 8, ...) has exactly **one** set bit: 8 is `1000`. Removing that single bit with `n & (n - 1)` must leave 0. For any positive number with two or more set bits, one set bit survives, so the result is not 0. We only need to rule out zero and negatives first, because 0 also gives `0 & -1 == 0`.

This is exactly the problem _Is It a Power of Two?_.

```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0


assert is_power_of_two(16)
assert not is_power_of_two(6)
assert not is_power_of_two(0)
assert not is_power_of_two(-8)
```

```cpp
bool is_power_of_two(long long n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```

Time and space are both $O(1)$.

## 3.4 Is it a power of four?

Powers of four are 1, 4, 16, 64, ..., which in binary are `1`, `100`, `10000`, `1000000`. They are powers of two whose single set bit sits at an **even** position (0, 2, 4, 6, ...). A power of two like 8 (`1000`) has its bit at position 3, which is odd, so it is not a power of four.

So we ask two questions: is it a power of two, and does its one bit sit in an even place? To test the second we use a mask that has 1s at all the even positions: `0101 0101 ...` in binary, which is `0x5555555555555555` in hexadecimal (hex is a compact way of writing four bits per digit; `5` is `0101`). If `n & mask` is not zero, the single bit of $n$ is at an even position.

This is exactly the problem _Is It a Power of Four?_.

```python
EVEN_MASK = 0x5555555555555555


def is_power_of_four(n):
    return n > 0 and (n & (n - 1)) == 0 and (n & EVEN_MASK) != 0


assert is_power_of_four(1)
assert is_power_of_four(64)
assert not is_power_of_four(8)
assert not is_power_of_four(12)
```

```cpp
bool is_power_of_four(long long n) {
    const long long EVEN_MASK = 0x5555555555555555LL;
    return n > 0 && (n & (n - 1)) == 0 && (n & EVEN_MASK) != 0;
}
```

This is $O(1)$ in time and space.

## 3.5 Isolating the lowest set bit

Sometimes we want to _keep_ the lowest set bit instead of removing it. Computers store negative numbers with a scheme called **two's complement**: to get $-n$ you flip every bit of $n$ and add 1. Let's see what that does with $n = 12$ written in 8 bits:

```
n       = 00001100   (12)
~n      = 11110011   (flip every bit)
-n      = 11110100   (add 1: the trailing 1s carry out)
n & -n  = 00000100   (4)
```

Adding 1 to the flipped number turns the low zeros back into zeros and puts a 1 exactly where the lowest set bit of $n$ was. Above that spot, $-n$ is the exact opposite of $n$, so the AND is 0. The result is a number with only the lowest set bit left: `n & -n`. For $n = 0$ the answer is 0.

This is exactly the problem _The Lowest Set Bit_.

```python
def lowest_set_bit(n):
    return n & -n


assert lowest_set_bit(12) == 4
assert lowest_set_bit(40) == 8
assert lowest_set_bit(7) == 1
assert lowest_set_bit(0) == 0
```

```cpp
long long lowest_set_bit(long long n) {
    return n & -n;
}
```

Time and space are $O(1)$. We will use this exact trick again in Chapter 5.

## 3.6 Check yourself

1. What is `40 & 39`, and which bit disappeared?
2. How many rounds does Kernighan's loop take for 1000 (`1111101000`)?
3. Why must `is_power_of_two` check `n > 0`?
4. What is `20 & -20`?

# Chapter 4. Counting and moving bits

## 4.1 Counting bits for every number

Suppose we need the set-bit count for every number from 0 to $n$. Counting each one from scratch would be wasteful, because the numbers are related. The number `i >> 1` is `i` with its lowest bit chopped off, and it is smaller than `i`, so its answer is already in our table. The only thing missing is the chopped bit, which is `i & 1`. So

$$\text{bits}[i] = \text{bits}[i \gg 1] + (i \,\&\, 1)$$

For $i = 6$ (`110`): `6 >> 1` is 3 (`11`) which has 2 set bits, and the lowest bit of 6 is 0, so 6 has 2 set bits. The table for 0 to 7 is 0, 1, 1, 2, 1, 2, 2, 3.

This is exactly the problem _Count Bits for Every Number_.

```python
def count_bits_up_to(n):
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits


assert count_bits_up_to(5) == [0, 1, 1, 2, 1, 2]
assert count_bits_up_to(7) == [0, 1, 1, 2, 1, 2, 2, 3]
assert count_bits_up_to(0) == [0]
```

```cpp
vector<int> count_bits_up_to(int n) {
    vector<int> bits(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        bits[i] = bits[i >> 1] + (i & 1);
    }
    return bits;
}
```

Each entry costs $O(1)$, so the total time is $O(n)$ and the space is $O(n)$ for the answer. This is a tiny example of dynamic programming: reuse smaller answers.

## 4.2 How many bits differ

Two numbers differ at position $i$ exactly when XOR gives a 1 there. So `a ^ b` is a number whose set bits mark every position where $a$ and $b$ disagree. To convert $a$ to $b$ we must flip each of those, so the number of flips is the number of set bits of `a ^ b`. For 10 (`1010`) and 7 (`0111`): the XOR is `1101`, which has 3 set bits, so 3 flips. We can reuse Kernighan's loop.

This is exactly the problem _Bit Flips to Convert_.

```python
def bit_flips(a, b):
    diff = a ^ b
    count = 0
    while diff:
        diff &= diff - 1
        count += 1
    return count


assert bit_flips(10, 7) == 3
assert bit_flips(5, 5) == 0
assert bit_flips(0, 255) == 8
```

```cpp
int bit_flips(long long a, long long b) {
    long long diff = a ^ b;
    int count = 0;
    while (diff) {
        diff &= diff - 1;
        count++;
    }
    return count;
}
```

The count of differing positions between two numbers is called their **Hamming distance**. Time is $O(d)$ for $d$ differing bits, space $O(1)$.

## 4.3 Reversing the bits

To reverse the bits of a 32-bit number, we build the answer one bit at a time. We read the lowest bit of $n$, and push it onto the _bottom_ of the result while sliding the earlier bits of the result up by one place. The first bit we read is pushed up 31 times in total, so it ends at the top. The last bit we read ends at the bottom.

Here is the same idea with only 8 bits to keep it short. Reversing `00010110` (22) gives `01101000` (104):

```
n = 00010110  read bit: 0, result = 0
              read bit: 1, result = 01
              read bit: 1, result = 011
              read bit: 0, result = 0110
              read bit: 1, result = 01101
              read bit: 0, result = 011010
              read bit: 0, result = 0110100
              read bit: 0, result = 01101000
```

In code, each round does `result = (result << 1) | (n & 1)` and then drops the bit with `n >>= 1`. We run exactly 32 rounds even if $n$ is small, so that the leading zeros are also moved.

This is exactly the problem _Reverse the Bits_.

```python
def reverse_bits(n, width=32):
    result = 0
    for _ in range(width):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


assert reverse_bits(1) == 2147483648
assert reverse_bits(0b00010110, 8) == 0b01101000
assert reverse_bits(0) == 0
```

```cpp
unsigned int reverse_bits(unsigned int n) {
    unsigned int result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);
        n >>= 1;
    }
    return result;
}
```

In C++ we use `unsigned int` because shifting a signed value left into the sign bit is a trap. The loop runs a fixed 32 times, so time is $O(1)$ (or $O(w)$ for width $w$) and space is $O(1)$.

## 4.4 Masks that pick out many bits

A **mask** can have many 1s, not just one. ANDing with it keeps only the bits you chose. To swap each pair of neighbouring bits we need two masks: one that picks the _even_ positions (0, 2, 4, ...) and one that picks the _odd_ positions (1, 3, 5, ...). In hexadecimal, `0x55555555` is `0101 ... 0101` (the even positions) and `0xAAAAAAAA` is `1010 ... 1010` (the odd positions).

We take the even bits and shift them up by one, take the odd bits and shift them down by one, and OR the two halves together. They cannot collide, because each half lands on the positions the other half vacated. With 8 bits, `10110100` becomes `01111000`:

```
n          = 10110100
n & 0xAA   = 10100000  -> >> 1 = 01010000
n & 0x55   = 00010100  -> << 1 = 00101000
OR         =                     01111000
```

This is exactly the problem _Swap Odd and Even Bits_.

```python
def swap_odd_even_bits(n):
    even = n & 0x55555555
    odd = n & 0xAAAAAAAA
    return (even << 1) | (odd >> 1)


assert swap_odd_even_bits(10) == 5          # 1010 -> 0101
assert swap_odd_even_bits(0b10110100) == 0b01111000
assert swap_odd_even_bits(1) == 2
```

```cpp
unsigned int swap_odd_even_bits(unsigned int n) {
    unsigned int even = n & 0x55555555u;
    unsigned int odd = n & 0xAAAAAAAAu;
    return (even << 1) | (odd >> 1);
}
```

Time and space are $O(1)$: a handful of operations, no loop.

## 4.5 Check yourself

1. What is the table of set-bit counts for 0 to 4?
2. How many flips turn 8 into 7?
3. Why do we run exactly 32 rounds when reversing, even for $n = 1$?
4. What does `x & 0xAAAAAAAA` keep?

# Chapter 5. The magic of XOR

## 5.1 Four facts about XOR

XOR has a few properties that look strange at first but are very handy. Check each one against the table in Chapter 2:

First, $x \oplus 0 = x$: XOR with zero changes nothing (a bit that differs from 0 is just itself). Second, $x \oplus x = 0$: a number never differs from itself, so any number XORed with itself disappears. Third, the order does not matter: $a \oplus b = b \oplus a$ and $(a \oplus b) \oplus c = a \oplus (b \oplus c)$. Fourth, therefore, if we XOR a long list in any order, every number that appears an even number of times cancels itself out.

For example, $5 \oplus 7 \oplus 5 = 7 \oplus (5 \oplus 5) = 7 \oplus 0 = 7$. In code the symbol is `^` and we write the math symbol as $\oplus$.

## 5.2 The single number

Suppose every number in a list appears twice, except one that appears once. XOR the whole list. All the pairs cancel to 0 and only the lonely number is left, no matter where it was. For `[4, 1, 2, 1, 2]` we get $4 \oplus 1 \oplus 2 \oplus 1 \oplus 2 = 4$. No dictionary needed: one pass and one variable.

```python
def single_number(nums):
    result = 0
    for x in nums:
        result ^= x
    return result


assert single_number([4, 1, 2, 1, 2]) == 4
assert single_number([7]) == 7
assert single_number([-3, 5, 5]) == -3
```

```cpp
int single_number(const vector<int>& nums) {
    int result = 0;
    for (int x : nums) result ^= x;
    return result;
}
```

Time is $O(n)$ and space is $O(1)$. This warm-up is the base for the next two questions.

## 5.3 Two single numbers

Now suppose two different numbers $a$ and $b$ appear once and all others appear twice. XORing everything gives $a \oplus b$, which mixes both together, so we cannot read them off yet. But $a \ne b$, so $a \oplus b$ is not zero, which means it has at least one set bit, and at that bit position $a$ and $b$ **differ**: one has a 0 there and the other a 1.

Pick one such bit, the easiest being the lowest set bit `x & -x` from Chapter 3. Now split the whole list into two groups: numbers that have that bit set, and numbers that do not. The numbers of each pair are equal, so they land in the _same_ group and cancel there. The lonely $a$ goes in one group and $b$ in the other. XOR each group separately and out come $a$ and $b$.

For `[1, 2, 1, 3, 2, 5]`: the XOR of all is $3 \oplus 5 = 6$ (`110`), whose lowest set bit is 2 (`010`). Numbers with that bit: 2, 3, 2, which XOR to 3. Numbers without: 1, 1, 5, which XOR to 5.

This is exactly the problem _Two Single Numbers_.

```python
def two_single_numbers(nums):
    xor_all = 0
    for x in nums:
        xor_all ^= x
    low = xor_all & -xor_all      # a bit where the two answers differ
    a = b = 0
    for x in nums:
        if x & low:
            a ^= x
        else:
            b ^= x
    return sorted([a, b])


assert two_single_numbers([1, 2, 1, 3, 2, 5]) == [3, 5]
assert two_single_numbers([-1, 0]) == [-1, 0]
assert two_single_numbers([4, 4, 7, 9]) == [7, 9]
```

```cpp
vector<int> two_single_numbers(const vector<int>& nums) {
    long long xor_all = 0;
    for (int x : nums) xor_all ^= x;
    long long low = xor_all & -xor_all;   // a bit where the two answers differ
    int a = 0, b = 0;
    for (int x : nums) {
        if (x & low) a ^= x;
        else b ^= x;
    }
    if (a > b) swap(a, b);
    return {a, b};
}
```

We use `long long` for `xor_all` so that negating an extreme value such as the smallest `int` cannot overflow. Time is $O(n)$ and space is $O(1)$.

## 5.4 Everything else appears three times

XOR cancels pairs, but not triples: $x \oplus x \oplus x = x$. So we need a different idea. Look at one bit position at a time. For a value that appears three times, it contributes either 0 or 3 ones to that column. So if we count the ones in each column across the whole list, the count is a multiple of 3 from the tripled values, plus 1 more if the single number has a 1 in that column. So **count mod 3** in each column gives exactly the single number's bit.

We do this for all 32 columns. Negative numbers are stored in 32 bits too; if the top bit (bit 31) of the result is set, then the number is negative, and we subtract $2^{32}$ to get its real value. For `[2, 2, 3, 2]`: 2 is `10` and 3 is `11`. Column 0 sees only the 3: count 1. Column 1 sees 2, 2, 3, 2: count 4, and $4 \bmod 3 = 1$. So the answer is `11` = 3.

This is exactly the problem _Single Number, Others Three Times_.

```python
def single_number_three(nums):
    result = 0
    for bit in range(32):
        ones = 0
        for x in nums:
            ones += (x >> bit) & 1
        if ones % 3:
            result |= 1 << bit
    if result >= 1 << 31:          # the sign bit is set: negative number
        result -= 1 << 32
    return result


assert single_number_three([2, 2, 3, 2]) == 3
assert single_number_three([0, 1, 0, 1, 0, 1, 99]) == 99
assert single_number_three([-2, -2, 1, -2]) == 1
assert single_number_three([-5, 4, 4, 4]) == -5
```

```cpp
int single_number_three(const vector<int>& nums) {
    unsigned int result = 0;
    for (int bit = 0; bit < 32; bit++) {
        int ones = 0;
        for (int x : nums) ones += ((unsigned int)x >> bit) & 1;
        if (ones % 3) result |= 1u << bit;
    }
    return (int)result;     // reinterprets bit 31 as the sign
}
```

Time is $O(32 \cdot n)$, which is $O(n)$, and space is $O(1)$. The cast to `unsigned` before shifting avoids trouble with the sign bit.

There is also a famous one-pass version with two variables, `ones` and `twos`. Think of the pair as a tiny counter _per bit_ that counts 0, 1, 2 and then back to 0. `ones` holds the bits seen once (mod 3) and `twos` the bits seen twice. Each new number $x$ first flips into `ones` unless the bit is already in `twos`, then into `twos` unless it ended up in `ones`. When a bit has been seen three times, it is in neither variable, so it vanishes. The code is only two lines, but the column-counting version above is easier to trust.

```python
def single_number_three_fast(nums):
    ones = twos = 0
    for x in nums:
        ones = (ones ^ x) & ~twos
        twos = (twos ^ x) & ~ones
    return ones


assert single_number_three_fast([2, 2, 3, 2]) == 3
assert single_number_three_fast([-2, -2, 1, -2]) == 1
assert single_number_three_fast([0, 1, 0, 1, 0, 1, 99]) == 99
```

```cpp
int single_number_three_fast(const vector<int>& nums) {
    int ones = 0, twos = 0;
    for (int x : nums) {
        ones = (ones ^ x) & ~twos;
        twos = (twos ^ x) & ~ones;
    }
    return ones;
}
```

Both are $O(n)$ time and $O(1)$ space; this one does a single pass.

## 5.5 XOR of a whole range

How would you XOR all the numbers from `left` to `right`? Looping works but is slow for ranges of billions. Let $f(n) = 0 \oplus 1 \oplus \dots \oplus n$ be the running XOR from 0. Write it out:

```
n      : 0 1 2 3 4 5 6 7 8 9
f(n)   : 0 1 3 0 4 1 7 0 8 1
```

A pattern appears every four numbers. When $n \bmod 4 = 0$ we get $n$, when it is 1 we get 1, when it is 2 we get $n+1$, and when it is 3 we get 0. (Why: any four consecutive numbers starting at a multiple of 4 XOR to 0, because their upper bits cancel in pairs and the low two bits are `00 ^ 01 ^ 10 ^ 11 = 00`.)

Then the range from `left` to `right` is $f(\text{right}) \oplus f(\text{left}-1)$: the numbers below `left` appear in both parts and cancel, the same trick as in 5.1.

This is exactly the problem _XOR of a Range_.

```python
def xor_up_to(n):
    if n < 0:
        return 0
    return (n, 1, n + 1, 0)[n % 4]


def xor_of_range(left, right):
    return xor_up_to(right) ^ xor_up_to(left - 1)


assert xor_up_to(6) == 7
assert xor_of_range(3, 9) == 3 ^ 4 ^ 5 ^ 6 ^ 7 ^ 8 ^ 9
assert xor_of_range(5, 5) == 5
assert xor_of_range(0, 0) == 0
```

```cpp
long long xor_up_to(long long n) {
    if (n < 0) return 0;
    switch (n % 4) {
        case 0: return n;
        case 1: return 1;
        case 2: return n + 1;
        default: return 0;
    }
}

long long xor_of_range(long long left, long long right) {
    return xor_up_to(right) ^ xor_up_to(left - 1);
}
```

Time and space are $O(1)$, however large the range is.

## 5.6 Check yourself

1. What is $9 \oplus 9 \oplus 4$?
2. Why does the lowest set bit of $a \oplus b$ tell us where $a$ and $b$ differ?
3. Why does XOR alone fail when every other number appears three times?
4. What is $f(11)$, the XOR of 0 to 11?

# Chapter 6. Adding with bits, and ranges

## 6.1 Adding without the plus sign

How does a computer add? Let's add 5 and 3 the way you did in school, but in binary, column by column. In one column, two bits add to 0 (0+0), 1 (0+1 or 1+0) or 2 (1+1, which is `10`: write 0 and carry 1). So the _sum bit_ is the XOR of the two bits and the _carry_ is their AND. Doing this for every column at once: the sum without carries is `a ^ b` and the carries are `(a & b) << 1` (shifted one column left, because a carry goes to the next column).

Now add those two together. That is the same kind of problem, so repeat until there is no carry left. For $5 + 3$:

```
a=5 (101)  b=3 (011)  sum bits a^b=6 (110)  carry (a&b)<<1=2 (010)
a=6 (110)  b=2 (010)  sum bits a^b=4 (100)  carry (a&b)<<1=4 (100)
a=4 (100)  b=4 (100)  sum bits a^b=0 (000)  carry (a&b)<<1=8 (1000)
a=0        b=8        sum bits a^b=8        carry 0
```

The carry is now 0, so the answer is 8. In Python numbers never overflow, and negative numbers have infinitely many leading 1s, so the loop would never end for them. We mask to 32 bits with `& 0xFFFFFFFF` so every value is treated as a 32-bit number, and at the end convert back: if bit 31 is set the number is negative, so we subtract $2^{32}$.

This is exactly the problem _Add Without the Plus Sign_.

```python
def bit_add(a, b):
    mask = 0xFFFFFFFF
    a &= mask
    b &= mask
    while b:
        a, b = (a ^ b) & mask, ((a & b) << 1) & mask
    return a - (1 << 32) if a >= 1 << 31 else a


assert bit_add(5, 3) == 8
assert bit_add(-1, 1) == 0
assert bit_add(-7, 3) == -4
assert bit_add(2**31 - 1, 1) == -(2**31)       # wraps around like a 32-bit register
```

```cpp
int bit_add(int a, int b) {
    unsigned int x = a, y = b;
    while (y) {
        unsigned int carry = (x & y) << 1;
        x = x ^ y;
        y = carry;
    }
    return (int)x;
}
```

In C++ unsigned arithmetic already wraps around at 32 bits, so no explicit mask is needed. Each round pushes the carries at least one column to the left, so there are at most 32 rounds: $O(1)$ time and space.

## 6.2 AND of a range of numbers

What is `left & (left+1) & ... & right`? A bit survives an AND only if it is 1 in _every_ number. Think about the range 26 to 30:

```
26 = 11010
27 = 11011
28 = 11100
29 = 11101
30 = 11110
```

The top two bits `11` are the same in every number; they survive. Below that, once the range goes through 28 (`11100`), the third bit changes from 0 to 1. And as soon as a bit position flips somewhere in the range, then the range contains some number with a 0 there, so that bit and all those below it become 0 in the AND. Hence the answer is the **common prefix** of `left` and `right` (the leading bits that are equal), followed by zeros: `11000` = 24.

A neat way to find the prefix: keep shifting both numbers right until they are equal, counting the shifts, and then shift back left by that count.

This is exactly the problem _Bitwise AND of a Range_.

```python
def range_and(left, right):
    shift = 0
    while left != right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift


assert range_and(26, 30) == 24
assert range_and(5, 7) == 4
assert range_and(8, 8) == 8
assert range_and(0, 1) == 0
```

```cpp
long long range_and(long long left, long long right) {
    int shift = 0;
    while (left != right) {
        left >>= 1;
        right >>= 1;
        shift++;
    }
    return left << shift;
}
```

Time is $O(\log n)$ and space $O(1)$.

## 6.3 Flips needed so a OR b equals c

Because bits do not talk to each other in AND, OR and XOR, we can solve a bit problem **column by column** and add up the costs. Here we want `a | b == c` with the fewest single-bit flips in `a` and `b`. Look at one column, with the bits $x$ of `a`, $y$ of `b` and $z$ of `c`:

If $z = 0$, then both $x$ and $y$ must be 0, so we flip each of them that is 1: the cost is $x + y$. If $z = 1$, we need at least one of $x, y$ to be 1. If one of them already is, the cost is 0. If both are 0, one flip fixes it: the cost is 1.

For $a = 2$ (`010`), $b = 6$ (`110`), $c = 5$ (`101`): column 0 has $z = 1$ and $x = y = 0$, cost 1; column 1 has $z = 0$ and $x = y = 1$, cost 2; column 2 has $z = 1$ with $y = 1$, cost 0. The total is 3.

This is exactly the problem _Minimum Flips to Make a OR b Equal c_.

```python
def min_flips(a, b, c):
    flips = 0
    for i in range(31):
        x, y, z = (a >> i) & 1, (b >> i) & 1, (c >> i) & 1
        if z == 0:
            flips += x + y
        elif x == 0 and y == 0:
            flips += 1
    return flips


assert min_flips(2, 6, 5) == 3
assert min_flips(4, 2, 7) == 1
assert min_flips(1, 2, 3) == 0
```

```cpp
int min_flips(int a, int b, int c) {
    int flips = 0;
    for (int i = 0; i < 31; i++) {
        int x = (a >> i) & 1, y = (b >> i) & 1, z = (c >> i) & 1;
        if (z == 0) flips += x + y;
        else if (x == 0 && y == 0) flips += 1;
    }
    return flips;
}
```

Time is $O(31)$, which is $O(1)$, and space is $O(1)$.

## 6.4 The longest run of ones after one flip

Here we may flip one 0 into a 1 in a 32-bit number and want the longest block of consecutive 1s. Scan the bits from the lowest one up, remembering two run lengths: `current`, the run of ones we are in right now, and `previous`, the run of ones just before the last 0. If we flip that last zero, we glue `previous`, the flipped bit and `current` into a single run of length `previous + 1 + current`. When we meet a 0 the old `current` becomes the new `previous` and `current` restarts at 0. When we meet a 1, `current` grows.

For $1775$ (`11011101111`), reading from the bottom: four ones, a zero, three ones, a zero, two ones. Flipping the first zero joins 4 and 3 into $4 + 1 + 3 = 8$. Flipping the second zero joins 3 and 2 into 6. The best is 8.

We cap the answer at 32 because a number with no zero bit at all has no bit to flip, and the formula would count one bit that does not exist.

This is exactly the problem _Longest Run of Ones After One Flip_.

```python
def longest_ones_after_flip(n):
    best = current = previous = 0
    for i in range(32):
        if (n >> i) & 1:
            current += 1
        else:
            previous = current
            current = 0
        best = max(best, previous + current + 1)
    return min(best, 32)


assert longest_ones_after_flip(1775) == 8
assert longest_ones_after_flip(0) == 1
assert longest_ones_after_flip(0xFFFFFFFF) == 32
assert longest_ones_after_flip(0b101) == 3
```

```cpp
int longest_ones_after_flip(unsigned int n) {
    int best = 0, current = 0, previous = 0;
    for (int i = 0; i < 32; i++) {
        if ((n >> i) & 1) {
            current++;
        } else {
            previous = current;
            current = 0;
        }
        best = max(best, previous + current + 1);
    }
    return min(best, 32);
}
```

Time is $O(32)$, i.e. $O(1)$, and space is $O(1)$.

## 6.5 Check yourself

1. In binary addition, which operator gives the sum without carry, and which gives the carry?
2. What is `12 & 13 & 14 & 15`?
3. If $c$'s bit is 0 and both bits of $a$ and $b$ are 1, how many flips does that column cost?
4. For the number `0111`, what is the longest run of ones after flipping one zero (consider only these 4 bits)?

# Chapter 7. Counting bit by bit, and bitmasks

## 7.1 Total Hamming distance

Given a list of numbers, we want the sum of Hamming distances (Chapter 4) over all pairs. Trying every pair costs $O(n^2)$ comparisons, far too many for long lists. The trick: because columns are independent, we can add up the contribution of **each column** separately.

Take one column, and say $k$ of the $n$ numbers have a 1 there. A pair differs in this column exactly when one of the two has a 1 and the other a 0. There are $k$ choices for the one with 1 and $n-k$ choices for the one with 0, so this column adds $k \cdot (n-k)$ to the total. Add the columns up. For `[4, 14, 2]` (`0100`, `1110`, `0010`): column 1 has ones for 14 and 2, $k=2$, so $2 \cdot 1 = 2$; column 2 has ones for 4 and 14, $2 \cdot 1 = 2$; column 3 has a one for 14 only, $1 \cdot 2 = 2$. The total is 6.

This is exactly the problem _Total Hamming Distance_.

```python
def total_hamming_distance(nums):
    n = len(nums)
    total = 0
    for bit in range(32):
        k = sum((x >> bit) & 1 for x in nums)
        total += k * (n - k)
    return total


assert total_hamming_distance([4, 14, 2]) == 6
assert total_hamming_distance([5, 5]) == 0
assert total_hamming_distance([0, 1]) == 1
```

```cpp
long long total_hamming_distance(const vector<int>& nums) {
    long long n = nums.size();
    long long total = 0;
    for (int bit = 0; bit < 32; bit++) {
        long long k = 0;
        for (int x : nums) k += ((unsigned int)x >> bit) & 1;
        total += k * (n - k);
    }
    return total;
}
```

Time is $O(32 \cdot n)$, i.e. $O(n)$, and space is $O(1)$. (Negative numbers also work since all 32 bits are counted, and the answer needs a 64-bit total in C++.)

## 7.2 A number as a small set

A number can also be a **set**. Take a list of $m$ items. Give item $i$ the place $i$. A number whose bit $i$ is 1 means "item $i$ is in the set". Such a number is called a **bitmask**. The empty set is 0, the whole set is `(1 << m) - 1`, and the numbers $0, 1, \dots, 2^m - 1$ are all subsets, each exactly once. Adding an item is `|`, removing is `& ~`, testing membership is `(mask >> i) & 1`.

So we can walk through every subset with a plain loop. For example, here are the sums of all subsets of a list:

```python
def subset_sums(items):
    m = len(items)
    sums = []
    for mask in range(1 << m):
        total = 0
        for i in range(m):
            if (mask >> i) & 1:
                total += items[i]
        sums.append(total)
    return sums


assert subset_sums([1, 2]) == [0, 1, 2, 3]
assert sorted(subset_sums([1, 2, 4])) == [0, 1, 2, 3, 4, 5, 6, 7]
assert subset_sums([]) == [0]
```

```cpp
vector<int> subset_sums(const vector<int>& items) {
    int m = items.size();
    vector<int> sums;
    for (int mask = 0; mask < (1 << m); mask++) {
        int total = 0;
        for (int i = 0; i < m; i++) {
            if ((mask >> i) & 1) total += items[i];
        }
        sums.push_back(total);
    }
    return sums;
}
```

There are $2^m$ subsets and each costs $O(m)$ to read, so time is $O(m \cdot 2^m)$; this is only practical for $m$ up to about 20. It is the doorway to a whole family of "bitmask" problems, in which a mask records which items are already used.

## 7.3 Maximum XOR of two numbers

Now the hardest problem of the step: from a list of numbers, find the largest $a \oplus b$ over two of them. Trying every pair is $O(n^2)$.

Think about how to make an XOR big: bits at the top are worth more than all the lower bits together. So we want a 1 at the highest bit, and among those choices a 1 at the next bit, and so on. This is a **greedy** idea (take the best at the top first). To build the best partner for a number $a$ we walk its bits from the top; at each position we would love a partner with the _opposite_ bit, if one exists.

To find such partners quickly we store all numbers in a **trie** (a tree where every step down chooses the next bit, 0 or 1; see the tries chapter of the course for the general idea). Each number is a path of 30 steps. For each number $a$ we walk down from the top and at each level try to go to the child with the opposite bit; if it does not exist we take the same-bit child.

```python
def max_xor_trie(nums, bits=30):
    root = [None, None]                    # a node is [child0, child1]
    for x in nums:
        node = root
        for i in range(bits - 1, -1, -1):
            b = (x >> i) & 1
            if node[b] is None:
                node[b] = [None, None]
            node = node[b]
    best = 0
    for x in nums:
        node = root
        total = 0
        for i in range(bits - 1, -1, -1):
            b = (x >> i) & 1
            if node[1 - b] is not None:    # an opposite bit exists: take it
                total |= 1 << i
                node = node[1 - b]
            else:
                node = node[b]
        best = max(best, total)
    return best


assert max_xor_trie([3, 10, 5, 25, 2, 8]) == 28      # 5 ^ 25
assert max_xor_trie([7]) == 0
assert max_xor_trie([1, 2]) == 3
```

```cpp
int max_xor_trie(const vector<int>& nums) {
    const int BITS = 30;
    vector<array<int, 2>> trie(1, {-1, -1});     // node 0 is the root
    for (int x : nums) {
        int node = 0;
        for (int i = BITS - 1; i >= 0; i--) {
            int b = (x >> i) & 1;
            if (trie[node][b] == -1) {
                trie[node][b] = trie.size();
                trie.push_back({-1, -1});
            }
            node = trie[node][b];
        }
    }
    int best = 0;
    for (int x : nums) {
        int node = 0, total = 0;
        for (int i = BITS - 1; i >= 0; i--) {
            int b = (x >> i) & 1;
            if (trie[node][1 - b] != -1) {
                total |= 1 << i;
                node = trie[node][1 - b];
            } else {
                node = trie[node][b];
            }
        }
        best = max(best, total);
    }
    return best;
}
```

Building the trie costs $O(30 \cdot n)$, and each query costs $O(30)$, so the time is $O(30 \cdot n) = O(n)$ and the space is $O(30 \cdot n)$ for the nodes.

## 7.4 The same idea with a set of prefixes

There is a trie-free way to do the same thing, which needs only a set. We decide the answer one bit at a time from the top. After handling the top bits, we know the best possible XOR _prefix_ `best` (the top bits of the answer). To test whether the next bit of the answer can be 1, set `candidate = best * 2 + 1` (the best prefix with a 1 appended). The candidate is achievable if two numbers' prefixes `p` and `q` (their numbers shifted right so only the bits examined so far remain) satisfy `p ^ q == candidate`. Rather than checking all pairs, we use XOR's own property: `p ^ q == candidate` exactly when `q == p ^ candidate`, so we put all prefixes in a set and, for each `p`, look up `p ^ candidate`.

If some pair works, `best` becomes `candidate`; otherwise the new bit is 0 and `best = best * 2`.

This is exactly the problem _Maximum XOR of Two Numbers_.

```python
def max_xor_pair(nums):
    best = 0
    for bit in range(29, -1, -1):
        prefixes = {x >> bit for x in nums}
        candidate = (best << 1) | 1
        best <<= 1
        for p in prefixes:
            if (p ^ candidate) in prefixes:
                best = candidate
                break
    return best


assert max_xor_pair([3, 10, 5, 25, 2, 8]) == 28
assert max_xor_pair([7]) == 0
assert max_xor_pair([14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70]) == 127
```

```cpp
int max_xor_pair(const vector<int>& nums) {
    int best = 0;
    for (int bit = 29; bit >= 0; bit--) {
        unordered_set<int> prefixes;
        for (int x : nums) prefixes.insert(x >> bit);
        int candidate = (best << 1) | 1;
        best <<= 1;
        for (int p : prefixes) {
            if (prefixes.count(p ^ candidate)) {
                best = candidate;
                break;
            }
        }
    }
    return best;
}
```

Each of the 30 rounds touches every number once, so the time is $O(30 \cdot n)$ on average and the space is $O(n)$ for the set.

## 7.5 Check yourself

1. If 3 of 5 numbers have a 1 in a column, how much does that column add to the total Hamming distance?
2. How many subsets does a list of 5 items have, and which mask is the full set?
3. Why is it better to decide the high bits of an XOR first?
4. In the prefix-set method, what does `p ^ candidate` look up?

# Sources and credit

Some of the ideas on this page (clearing and isolating the lowest set bit, the two's complement view of `-n`, counting bits, and the general toolbox of bit tricks) are adapted from the cp-algorithms.com article on bit manipulation (https://cp-algorithms.com). The text has been rewritten for beginners with new examples, and it is shared under the Creative Commons Attribution-ShareAlike 4.0 licence, like the original.
