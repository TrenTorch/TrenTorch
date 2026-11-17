> Every code block has a Python and a C++ version; use the switch above a block to pick one. Your choice is remembered.

# Introduction (Linked lists)

This page teaches linked lists: the humble chain of boxes that sits behind a surprising number of interview questions. We start with what a node is and how to walk along a list, then learn the handful of tricks that solve almost every problem: dummy nodes, reversing, fast and slow pointers, merging, cycle detection, sorting, and finally two famous "boss" problems, merging many lists and reversing in groups.

The page is a staircase. **Chapter 1 is deliberately gentle**: pictures, tiny loops, no clever tricks. Each later chapter adds one idea and uses the ones before it. By the last chapter you will be comfortable rewiring pointers in your head and can solve every question in the linked-list step. Every code example is shown in Python and in C++, so pick whichever you like.

# Chapter 1. Nodes and pointers

## 1.1 A chain of boxes

Imagine a treasure hunt. Each clue is written on a card, and each card also says where to find the next card. You cannot jump to clue number 7 directly; you must start at clue 1 and follow the trail. That is a **linked list**.

Each card is called a **node**. A node holds two things: a **value** (the data we care about) and a **pointer** to the next node. A pointer is just "the address of another node", an arrow that says _the next one is over there_. The last node's arrow points at nothing, which we write as `None` in Python and `nullptr` in C++. The first node is called the **head**, and we only ever keep hold of the head; every other node is reached by following arrows from it.

```
head
 |
 v
[ 1 | * ]--->[ 2 | * ]--->[ 3 | * ]--->None
```

Compare this with an array. In an array, element 7 is found instantly because the elements sit side by side in memory. In a linked list the nodes can be anywhere in memory, so finding the 7th node means following 6 arrows. The reward is that **changing the shape is cheap**: to remove a node or insert a new one we only redirect a couple of arrows, and nothing else has to shift. Almost every linked-list problem is about redirecting arrows correctly.

## 1.2 The node in code

A node is a tiny class (a struct in C++) with a `val` and a `next`. To keep the examples readable we also write two helpers: `build` turns an ordinary list of numbers into a linked list, and `to_list` turns a linked list back into an ordinary list so we can compare it in a test.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


assert to_list(build([1, 2, 3])) == [1, 2, 3]
assert build([]) is None
```

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

ListNode* build(const vector<int>& values) {
    ListNode* head = nullptr;
    for (int i = (int)values.size() - 1; i >= 0; i--) {
        head = new ListNode(values[i], head);
    }
    return head;
}

vector<int> toList(ListNode* head) {
    vector<int> out;
    while (head != nullptr) {
        out.push_back(head->val);
        head = head->next;
    }
    return out;
}
```

Notice how `build` works: it goes through the values from the back, and each time it creates a new node whose `next` is the list built so far. Building from the back means the new node automatically becomes the new head.

## 1.3 Walking along a list

To visit every node we use a moving pointer, usually called `cur` (for "current"). We start it at the head, and as long as it is not `None` we do something with the node and then step to `cur.next`. Here is the walk that counts the nodes.

```python
def length(head):
    count = 0
    cur = head
    while cur is not None:
        count += 1
        cur = cur.next
    return count


assert length(build([4, 7, 9])) == 3
assert length(None) == 0
```

```cpp
int length(ListNode* head) {
    int count = 0;
    ListNode* cur = head;
    while (cur != nullptr) {
        count++;
        cur = cur->next;
    }
    return count;
}
```

Two habits will save you from most bugs. First, the loop condition is `cur is not None`: if you step past the end and then ask for `cur.next`, the program crashes because `None` has no `next`. Second, we walk with a copy (`cur`) and keep `head` untouched, because the head is the only way back to the start of the list. Walking costs $O(n)$ time for $n$ nodes and $O(1)$ extra space, since we only keep one pointer.

## 1.4 Changing the arrows

Now the interesting part. Suppose `node` is a node somewhere in the list, and we want to put a new value right after it. Two arrows change: the new node must point at what `node` used to point at, and `node` must point at the new node. The order matters. If you first make `node` point at the new node, you have lost the only reference to the rest of the list.

```
before:   node ---> B ---> C
after:    node ---> NEW ---> B ---> C
```

Deleting the node after `node` is even simpler: make `node` skip over it, `node.next = node.next.next`. The skipped node is now unreachable and simply disappears. Both operations take $O(1)$ time, as long as we already hold `node`. (Finding `node` in the first place may cost $O(n)$.)

```python
def push_front(head, val):
    return ListNode(val, head)


def insert_after(node, val):
    node.next = ListNode(val, node.next)


def delete_after(node):
    if node.next is not None:
        node.next = node.next.next


head = build([1, 2, 4])
insert_after(head.next, 3)
assert to_list(head) == [1, 2, 3, 4]
delete_after(head)
assert to_list(head) == [1, 3, 4]
head = push_front(head, 0)
assert to_list(head) == [0, 1, 3, 4]
```

```cpp
ListNode* pushFront(ListNode* head, int val) {
    return new ListNode(val, head);
}

void insertAfter(ListNode* node, int val) {
    node->next = new ListNode(val, node->next);
}

void deleteAfter(ListNode* node) {
    if (node->next != nullptr) {
        node->next = node->next->next;
    }
}
```

Inserting at the very front is a special case that does not need a node before it: the new node simply points at the old head, and becomes the new head. That is why `push_front` returns a head. Keep this in mind, because the front of the list is where most bugs hide, and the next chapter gives a neat trick for it.

## 1.5 Check yourself

1. Why can we not jump straight to the 5th node of a linked list the way we can with an array?
2. What would go wrong if `length` used `while cur.next is not None` and the list were empty?
3. In `insert_after`, why must the new node be given the old `node.next` before `node.next` is changed?
4. What does it cost to delete a node when you already hold the node just before it?

# Chapter 2. The dummy node and clean removal

## 2.1 Trouble at the front

Let us delete the first node whose value equals a target. If the match is somewhere in the middle, we need the node _before_ it, so that we can redirect that node's arrow. We walk with a pointer `prev` and look at `prev.next`.

But what if the match is the head itself? Then there is no node before it, and the head variable must change. That needs a separate `if` at the start, and then a second piece of code for the normal case. Two code paths for one idea is how bugs breed.

The cure is a tiny trick used all over linked-list problems: put a **dummy node** (also called a sentinel) in front of the real head. The dummy holds a useless value, and its `next` is the head. Now every real node, even the head, has a node before it, so one code path handles everything. At the end we return `dummy.next`, which is the (possibly new) head.

```
dummy ---> 5 ---> 6 ---> 7
  ^
 prev starts here
```

## 2.2 Delete the first match

Here is the dummy node in action. We keep `prev` on the node before the one we are testing. If `prev.next` is the target we skip over it and stop; otherwise we step `prev` forward.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def delete_first(head, target):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next is not None:
        if prev.next.val == target:
            prev.next = prev.next.next
            break
        prev = prev.next
    return dummy.next


assert to_list(delete_first(build([1, 2, 3, 2]), 2)) == [1, 3, 2]
assert to_list(delete_first(build([5, 6]), 5)) == [6]
assert to_list(delete_first(build([5, 6]), 9)) == [5, 6]
```

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

ListNode* build(const vector<int>& values) {
    ListNode* head = nullptr;
    for (int i = (int)values.size() - 1; i >= 0; i--) {
        head = new ListNode(values[i], head);
    }
    return head;
}

vector<int> toList(ListNode* head) {
    vector<int> out;
    while (head != nullptr) {
        out.push_back(head->val);
        head = head->next;
    }
    return out;
}

ListNode* deleteFirst(ListNode* head, int target) {
    ListNode dummy(0, head);
    ListNode* prev = &dummy;
    while (prev->next != nullptr) {
        if (prev->next->val == target) {
            prev->next = prev->next->next;
            break;
        }
        prev = prev->next;
    }
    return dummy.next;
}
```

(The first block of each chapter restates the node and the two helpers, so every chapter can be read on its own.) In C++ the dummy can live on the stack, which is why it is written `ListNode dummy(0, head);` and used through `&dummy`.

## 2.3 Delete every match

To remove all the nodes with a given value we change one thing: after deleting we do **not** move `prev`. Why? Because the node that slid into the place of the deleted one might be a match too. Only when `prev.next` is safe do we step forward. Look at `[7, 7, 1, 7]` with target 7: after the first deletion, the new `prev.next` is another 7 that also has to go, and if we had already stepped forward we would have skipped it.

This is exactly the problem _Remove Matching Nodes_. The dummy node is what makes removing a run of matches at the head work without any special case.

```python
def remove_all(head, target):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next is not None:
        if prev.next.val == target:
            prev.next = prev.next.next
        else:
            prev = prev.next
    return dummy.next


assert to_list(remove_all(build([7, 7, 1, 7, 2, 7]), 7)) == [1, 2]
assert to_list(remove_all(build([3, 3, 3]), 3)) == []
```

```cpp
ListNode* removeAll(ListNode* head, int target) {
    ListNode dummy(0, head);
    ListNode* prev = &dummy;
    while (prev->next != nullptr) {
        if (prev->next->val == target) {
            prev->next = prev->next->next;
        } else {
            prev = prev->next;
        }
    }
    return dummy.next;
}
```

This runs in $O(n)$ time with $O(1)$ extra space: every iteration either deletes a node or moves forward, and both can happen at most $n$ times.

## 2.4 Sorted lists and duplicates

When a list is sorted, equal values sit next to each other. That makes duplicates easy to spot: just compare a node with the one after it. To keep one copy of each value, stand on a node and look at `cur.next`. If it has the same value, skip it and stay put (there might be a third copy); otherwise move on. The head never disappears here, because the first copy of every value is kept, so no dummy is needed.

This is exactly the problem _Remove Duplicates From a Sorted List_.

```python
def dedupe_keep_one(head):
    cur = head
    while cur is not None and cur.next is not None:
        if cur.next.val == cur.val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head


assert to_list(dedupe_keep_one(build([1, 1, 2, 3, 3, 3]))) == [1, 2, 3]
assert to_list(dedupe_keep_one(build([]))) == []
```

```cpp
ListNode* dedupeKeepOne(ListNode* head) {
    ListNode* cur = head;
    while (cur != nullptr && cur->next != nullptr) {
        if (cur->next->val == cur->val) {
            cur->next = cur->next->next;
        } else {
            cur = cur->next;
        }
    }
    return head;
}
```

## 2.5 Removing every repeated value

A harder twist: delete **all** copies of any value that appears more than once, keeping only values that were alone. For `1, 2, 2, 3` the answer is `1, 3`. Now the head itself can vanish (think of `1, 1, 2`, where the answer starts with 2), so the dummy node is back.

Stand `prev` on the last node known to be safe. Look at `cur = prev.next`. If `cur` and the node after it have the same value, we have found a repeated run. Remember the value, run `cur` forward past every node with that value, and hook `prev.next` to whatever comes after the run. Note that we do not move `prev`, since the next node is still unchecked. If `cur` is not repeated, it is safe and `prev` moves onto it.

This is exactly the problem _Remove Every Repeated Value_.

```python
def drop_all_repeated(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next is not None:
        cur = prev.next
        if cur.next is not None and cur.next.val == cur.val:
            dup = cur.val
            while cur is not None and cur.val == dup:
                cur = cur.next
            prev.next = cur
        else:
            prev = cur
    return dummy.next


assert to_list(drop_all_repeated(build([1, 2, 2, 3]))) == [1, 3]
assert to_list(drop_all_repeated(build([1, 1, 2]))) == [2]
assert to_list(drop_all_repeated(build([4, 4, 4]))) == []
```

```cpp
ListNode* dropAllRepeated(ListNode* head) {
    ListNode dummy(0, head);
    ListNode* prev = &dummy;
    while (prev->next != nullptr) {
        ListNode* cur = prev->next;
        if (cur->next != nullptr && cur->next->val == cur->val) {
            int dup = cur->val;
            while (cur != nullptr && cur->val == dup) {
                cur = cur->next;
            }
            prev->next = cur;
        } else {
            prev = cur;
        }
    }
    return dummy.next;
}
```

Time is $O(n)$ since each node is passed over at most twice, and space is $O(1)$.

## 2.6 Check yourself

1. What problem does the dummy node remove, and what do we return at the end?
2. In `remove_all`, why do we leave `prev` where it is after a deletion?
3. Why does `dedupe_keep_one` not need a dummy node but `drop_all_repeated` does?
4. What would `drop_all_repeated` return for `[1, 1, 1, 2, 2]`?

# Chapter 3. Reversing

## 3.1 Flipping all the arrows

Reversing a list is the most famous linked-list exercise, and a building block for many harder ones. The picture is simple: the list `1 -> 2 -> 3` must become `3 -> 2 -> 1`. The nodes stay where they are in memory; only the arrows turn around.

Before the clever way, here is the slow-but-easy way: make a **new** list by pushing each value to the front. Visiting `1, 2, 3` and pushing each to the front gives `1`, then `2 -> 1`, then `3 -> 2 -> 1`. It works, but it builds new nodes and uses $O(n)$ extra memory. We would like to reuse the nodes we have.

## 3.2 Reversing in place

Walk through the list with `cur`, and keep a second pointer `prev` on the node just behind it (at first there is none, so `prev` is `None`). At each node do three things: remember the next node, point `cur` backwards at `prev`, and then slide both pointers forward. Remembering the next node first is essential; once the arrow is flipped, the way forward is lost.

Here is the walk on `1 -> 2 -> 3`:

```
start:   prev=None  cur=1    1->2->3
step 1:  1 now points to None;    prev=1  cur=2
step 2:  2 now points to 1;       prev=2  cur=3
step 3:  3 now points to 2;       prev=3  cur=None   stop
```

When `cur` falls off the end, `prev` is sitting on the old last node, which is the new head. This is exactly the problem _Reverse a Linked List_.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def flip_arrows(head):
    prev = None
    cur = head
    while cur is not None:
        after = cur.next
        cur.next = prev
        prev = cur
        cur = after
    return prev


assert to_list(flip_arrows(build([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
assert to_list(flip_arrows(build([]))) == []
```

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

ListNode* build(const vector<int>& values) {
    ListNode* head = nullptr;
    for (int i = (int)values.size() - 1; i >= 0; i--) {
        head = new ListNode(values[i], head);
    }
    return head;
}

vector<int> toList(ListNode* head) {
    vector<int> out;
    while (head != nullptr) {
        out.push_back(head->val);
        head = head->next;
    }
    return out;
}

ListNode* flipArrows(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* cur = head;
    while (cur != nullptr) {
        ListNode* after = cur->next;
        cur->next = prev;
        prev = cur;
        cur = after;
    }
    return prev;
}
```

Time $O(n)$, extra space $O(1)$. If you ever need to reverse a list inside another algorithm, this four-line loop is the tool.

## 3.3 The recursive view

There is a second way to think about reversal that many people find elegant. Suppose a magic helper reverses everything _after_ the head. Then `1 -> 2 -> 3` becomes `1 -> (3 -> 2)`, where node 2 is now the tail of the reversed rest and still has a stale arrow from 1 pointing at it. To finish, we make node 2 point back at node 1 (`head.next.next = head`) and cut the old arrow (`head.next = None`).

```python
def reverse_recursive(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


assert to_list(reverse_recursive(build([1, 2, 3]))) == [3, 2, 1]
```

```cpp
ListNode* reverseRecursive(ListNode* head) {
    if (head == nullptr || head->next == nullptr) {
        return head;
    }
    ListNode* newHead = reverseRecursive(head->next);
    head->next->next = head;
    head->next = nullptr;
    return newHead;
}
```

This also takes $O(n)$ time, but the recursion uses $O(n)$ stack space, so for long lists the loop version is safer.

## 3.4 Reversing only a piece

Often we must reverse just a stretch in the middle, say the nodes at positions 2 to 4 of `1 -> 2 -> 3 -> 4 -> 5`. First we turn the flipping loop into a helper that reverses exactly `k` nodes starting at `start`. It returns two things: the new front of the reversed piece, and `rest`, the first node after the piece (where `cur` stops).

Then three steps finish the job. Find `before`, the node just ahead of the piece (a dummy node helps if the piece starts at position 1). Reverse the piece. Finally reconnect both ends: `before.next` must point at the new front, and the old first node of the piece, which is now its last, must point at `rest`.

```
before   first                 rest
   1 --> 2 --> 3 --> 4 --> 5       reverse 3 nodes starting at 2
   1 --> 4 --> 3 --> 2 --> 5
```

This is exactly the problem _Reverse Part of a Linked List_. We assume, as the problem does, that the piece lies inside the list.

```python
def reverse_k(start, k):
    prev = None
    cur = start
    for _ in range(k):
        after = cur.next
        cur.next = prev
        prev = cur
        cur = after
    return prev, cur


def reverse_part(head, left, size):
    dummy = ListNode(0, head)
    before = dummy
    for _ in range(left - 1):
        before = before.next
    first = before.next
    new_front, rest = reverse_k(first, size)
    before.next = new_front
    first.next = rest
    return dummy.next


assert to_list(reverse_part(build([1, 2, 3, 4, 5]), 2, 3)) == [1, 4, 3, 2, 5]
assert to_list(reverse_part(build([1, 2, 3, 4, 5]), 1, 5)) == [5, 4, 3, 2, 1]
assert to_list(reverse_part(build([1, 2, 3]), 3, 1)) == [1, 2, 3]
```

```cpp
pair<ListNode*, ListNode*> reverseK(ListNode* start, int k) {
    ListNode* prev = nullptr;
    ListNode* cur = start;
    for (int i = 0; i < k; i++) {
        ListNode* after = cur->next;
        cur->next = prev;
        prev = cur;
        cur = after;
    }
    return {prev, cur};
}

ListNode* reversePart(ListNode* head, int left, int size) {
    ListNode dummy(0, head);
    ListNode* before = &dummy;
    for (int i = 0; i < left - 1; i++) {
        before = before->next;
    }
    ListNode* first = before->next;
    auto [newFront, rest] = reverseK(first, size);
    before->next = newFront;
    first->next = rest;
    return dummy.next;
}
```

The cost is $O(n)$ time in the worst case (walking to position `left`) and $O(1)$ space. We will meet `reverse_k` again in the last chapter.

## 3.5 Swapping neighbours

Swapping each pair of neighbours (`1 2 3 4` becomes `2 1 4 3`) means moving the nodes, not the values stored inside them. Stand `prev` on the node before a pair. Call the pair `a` (first) and `b` (second). Three arrows change: `prev` must point at `b`, `b` must point at `a`, and `a` must point at whatever followed `b`. Do them in an order that never loses a node: first `a.next = b.next`, then `b.next = a`, then `prev.next = b`. Finally `prev` jumps onto `a`, which is now the second of the pair and the node before the next pair.

```
prev --> a --> b --> rest        becomes        prev --> b --> a --> rest
```

If only one node is left over (or none), we stop, and the odd one out stays where it is. This is exactly the problem _Swap Nodes in Pairs_.

```python
def swap_pairs(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next is not None and prev.next.next is not None:
        a = prev.next
        b = a.next
        a.next = b.next
        b.next = a
        prev.next = b
        prev = a
    return dummy.next


assert to_list(swap_pairs(build([1, 2, 3, 4]))) == [2, 1, 4, 3]
assert to_list(swap_pairs(build([1, 2, 3]))) == [2, 1, 3]
assert to_list(swap_pairs(build([1]))) == [1]
```

```cpp
ListNode* swapPairs(ListNode* head) {
    ListNode dummy(0, head);
    ListNode* prev = &dummy;
    while (prev->next != nullptr && prev->next->next != nullptr) {
        ListNode* a = prev->next;
        ListNode* b = a->next;
        a->next = b->next;
        b->next = a;
        prev->next = b;
        prev = a;
    }
    return dummy.next;
}
```

Time $O(n)$, space $O(1)$.

## 3.6 Check yourself

1. In the flipping loop, why must we save `cur.next` before changing `cur.next`?
2. After the loop ends, which pointer holds the new head, and why?
3. In `reverse_part`, which two arrows must be repaired after reversing the piece?
4. In `swap_pairs`, why does `prev` move to `a` and not to `b`?

# Chapter 4. Fast and slow pointers

## 4.1 Two runners

Here is a question that sounds hard for a linked list: where is the middle? An array would answer instantly with `n // 2`, but a list does not know its own length. One answer is to count the nodes first and then walk half that far, which takes two passes. There is a neater trick that needs only one.

Send out two runners from the head. The **slow** one takes one step at a time. The **fast** one takes two steps at a time. When the fast runner reaches the end, the slow runner has covered exactly half the distance, so it is standing in the middle.

On `1 -> 2 -> 3 -> 4 -> 5`: slow visits 1, 2, 3 while fast visits 1, 3, 5. Fast cannot step further, so slow is on 3, the middle. On `1 -> 2 -> 3 -> 4` there are two middles; slow visits 1, 2, 3 and fast visits 1, 3, then falls off the end (it moved from 3 to `None`), so slow stops on the second middle, 3. The stopping rule is "while fast and fast.next exist".

This is exactly the problem _Middle of a Linked List_.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def middle(head):
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


assert to_list(middle(build([1, 2, 3, 4, 5]))) == [3, 4, 5]
assert to_list(middle(build([1, 2, 3, 4]))) == [3, 4]
assert to_list(middle(build([9]))) == [9]
```

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

ListNode* build(const vector<int>& values) {
    ListNode* head = nullptr;
    for (int i = (int)values.size() - 1; i >= 0; i--) {
        head = new ListNode(values[i], head);
    }
    return head;
}

vector<int> toList(ListNode* head) {
    vector<int> out;
    while (head != nullptr) {
        out.push_back(head->val);
        head = head->next;
    }
    return out;
}

ListNode* middle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}
```

One pass, time $O(n)$, space $O(1)$. The order of the two tests in the `while` matters: check `fast is not None` first, because asking for `fast.next` on `None` would crash.

## 4.2 Two runners with a gap

A second use of two pointers: keep them a fixed distance apart. Suppose we want the value of the node that is 2nd from the end (the last node counts as 1st). Put `fast` one step ahead of `slow`. Now move both together, one step each. When `fast` stands on the last node, `slow` is one step behind it, so it stands on the 2nd node from the end. The gap never changes, so reaching the end of the list carries the second pointer to the right place. For the $n$-th node from the end, the head start is $n - 1$ steps.

```
[a] -> [b] -> [c] -> [d] -> [e]
                      slow   fast       slow is the 2nd from the end
```

```python
def value_from_end(head, n):
    slow = head
    fast = head
    for _ in range(n - 1):
        fast = fast.next
    while fast.next is not None:
        fast = fast.next
        slow = slow.next
    return slow.val


assert value_from_end(build([10, 20, 30, 40, 50]), 1) == 50
assert value_from_end(build([10, 20, 30, 40, 50]), 2) == 40
assert value_from_end(build([10, 20, 30, 40, 50]), 5) == 10
```

```cpp
int valueFromEnd(ListNode* head, int n) {
    ListNode* slow = head;
    ListNode* fast = head;
    for (int i = 0; i < n - 1; i++) {
        fast = fast->next;
    }
    while (fast->next != nullptr) {
        fast = fast->next;
        slow = slow->next;
    }
    return slow->val;
}
```

To **remove** that node we need the node just _before_ it. So we let both pointers begin on a dummy node placed in front of the head, give `fast` a head start of `n` steps, and then move both until `fast` is on the last node. At that moment `slow` is the node just before the one to delete. The dummy also takes care of deleting the head itself. We do it in one pass, as the problem asks.

This is exactly the problem _Remove the Nth Node From the End_.

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next is not None:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next


assert to_list(remove_nth_from_end(build([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
assert to_list(remove_nth_from_end(build([1, 2]), 2)) == [2]
assert to_list(remove_nth_from_end(build([7]), 1)) == []
```

```cpp
ListNode* removeNthFromEnd(ListNode* head, int n) {
    ListNode dummy(0, head);
    ListNode* slow = &dummy;
    ListNode* fast = &dummy;
    for (int i = 0; i < n; i++) {
        fast = fast->next;
    }
    while (fast->next != nullptr) {
        fast = fast->next;
        slow = slow->next;
    }
    slow->next = slow->next->next;
    return dummy.next;
}
```

Time $O(n)$, space $O(1)$.

## 4.3 Rotating with a ring

To rotate a list right by $k$ places, the last $k$ nodes must jump to the front. For `1 -> 2 -> 3 -> 4 -> 5` and $k = 2$ the answer is `4 -> 5 -> 1 -> 2 -> 3`.

A lovely way to see it: join the tail back to the head so the list becomes a ring. Rotating is then only a matter of choosing where to cut the ring. With $n$ nodes, the new tail is the node at position $n - k$ (counting the head as position 1), and the new head is the node after it. Cut the ring right there.

Two details. We need $n$, so one walk to the last node counts the length and finds the tail. And rotating by $n$ places brings the list back to itself, so $k$ can be replaced by $k \bmod n$. That is what makes huge values of $k$ harmless.

```
ring:  1 -> 2 -> 3 -> 4 -> 5 -+
       ^----------------------+      n = 5, k = 2: new tail is position 3
cut after 3:  4 -> 5 -> 1 -> 2 -> 3
```

This is exactly the problem _Rotate a Linked List_.

```python
def rotate_right(head, k):
    if head is None or head.next is None:
        return head
    n = 1
    tail = head
    while tail.next is not None:
        tail = tail.next
        n += 1
    k %= n
    if k == 0:
        return head
    tail.next = head
    new_tail = head
    for _ in range(n - k - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return new_head


assert to_list(rotate_right(build([1, 2, 3, 4, 5]), 2)) == [4, 5, 1, 2, 3]
assert to_list(rotate_right(build([1, 2, 3, 4, 5]), 7)) == [4, 5, 1, 2, 3]
assert to_list(rotate_right(build([1, 2, 3]), 3)) == [1, 2, 3]
```

```cpp
ListNode* rotateRight(ListNode* head, int k) {
    if (head == nullptr || head->next == nullptr) {
        return head;
    }
    int n = 1;
    ListNode* tail = head;
    while (tail->next != nullptr) {
        tail = tail->next;
        n++;
    }
    k %= n;
    if (k == 0) {
        return head;
    }
    tail->next = head;
    ListNode* newTail = head;
    for (int i = 0; i < n - k - 1; i++) {
        newTail = newTail->next;
    }
    ListNode* newHead = newTail->next;
    newTail->next = nullptr;
    return newHead;
}
```

Time $O(n)$, space $O(1)$.

## 4.4 Halve, reverse, compare

Is a list a palindrome, meaning it reads the same forwards and backwards? With an array you would compare the two ends and move inwards. A singly linked list cannot walk backwards, but we can fix that by reversing the second half.

The plan combines two tools we already own. Use fast and slow pointers to find the end of the first half. Reverse everything after it. Now walk one pointer from the head and another from the start of the reversed half, comparing values. If the list has an odd length, the centre node is skipped, which is fine: it equals itself. As a courtesy we reverse the second half back afterwards, so the caller gets the list unchanged.

For `1 -> 2 -> 2 -> 1` the first half is `1 -> 2`, the reversed second half is `1 -> 2`, and they match. For `1 -> 2` we compare `1` with `2` and say no.

This is exactly the problem _Palindrome Linked List_.

```python
def reverse_list(head):
    prev = None
    cur = head
    while cur is not None:
        after = cur.next
        cur.next = prev
        prev = cur
        cur = after
    return prev


def is_palindrome(head):
    if head is None or head.next is None:
        return True
    slow = head
    fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
    second = reverse_list(slow.next)
    a = head
    b = second
    ok = True
    while b is not None:
        if a.val != b.val:
            ok = False
            break
        a = a.next
        b = b.next
    slow.next = reverse_list(second)
    return ok


assert is_palindrome(build([1, 2, 2, 1])) is True
assert is_palindrome(build([1, 2, 1])) is True
assert is_palindrome(build([1, 2])) is False
lst = build([1, 2, 3, 4])
is_palindrome(lst)
assert to_list(lst) == [1, 2, 3, 4]
```

```cpp
ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* cur = head;
    while (cur != nullptr) {
        ListNode* after = cur->next;
        cur->next = prev;
        prev = cur;
        cur = after;
    }
    return prev;
}

bool isPalindrome(ListNode* head) {
    if (head == nullptr || head->next == nullptr) {
        return true;
    }
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast->next != nullptr && fast->next->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode* second = reverseList(slow->next);
    ListNode* a = head;
    ListNode* b = second;
    bool ok = true;
    while (b != nullptr) {
        if (a->val != b->val) {
            ok = false;
            break;
        }
        a = a->next;
        b = b->next;
    }
    slow->next = reverseList(second);
    return ok;
}
```

Notice the slightly different stopping rule: here `slow` must end on the _last node of the first half_, not on the middle. Time $O(n)$ and space $O(1)$, because we only rearrange arrows.

## 4.5 Halve, reverse, weave

One more combination of the same pieces. The task: turn `L0, L1, ..., Ln` into `L0, Ln, L1, Ln-1, L2, ...` (first, last, second, second to last, and so on). For `1 -> 2 -> 3 -> 4` the answer is `1 -> 4 -> 2 -> 3`.

Look at what is being asked: it alternates between the front half read forwards and the back half read backwards. We can do exactly that. Find the end of the first half, cut the list there, reverse the second half, and then **weave** the two lists together, taking one node from each in turn. For `1 -> 2 -> 3 -> 4` the halves are `1 -> 2` and, after reversing, `4 -> 3`; weaving gives `1, 4, 2, 3`.

When weaving, save both followers before touching any arrow: `a` is what follows the first-half node, and `b` is what follows the second-half node. Then link `first -> second -> a` and move on to `a` and `b`.

This is exactly the problem _Reorder a Linked List_.

```python
def reorder(head):
    if head is None or head.next is None:
        return head
    slow = head
    fast = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
    second = reverse_list(slow.next)
    slow.next = None
    first = head
    while second is not None:
        a = first.next
        b = second.next
        first.next = second
        second.next = a
        first = a
        second = b
    return head


assert to_list(reorder(build([1, 2, 3, 4]))) == [1, 4, 2, 3]
assert to_list(reorder(build([1, 2, 3, 4, 5]))) == [1, 5, 2, 4, 3]
assert to_list(reorder(build([1]))) == [1]
```

```cpp
ListNode* reorder(ListNode* head) {
    if (head == nullptr || head->next == nullptr) {
        return head;
    }
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast->next != nullptr && fast->next->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode* second = reverseList(slow->next);
    slow->next = nullptr;
    ListNode* first = head;
    while (second != nullptr) {
        ListNode* a = first->next;
        ListNode* b = second->next;
        first->next = second;
        second->next = a;
        first = a;
        second = b;
    }
    return head;
}
```

Again $O(n)$ time and $O(1)$ space. (Here `reverse_list` is defined in the section before, in the same chapter.)

## 4.6 Check yourself

1. When the fast runner moves two steps per slow step, why is the slow runner in the middle when fast finishes?
2. In `remove_nth_from_end`, why do both pointers start on the dummy node and not on the head?
3. What is the new tail after rotating a 6-node list right by 8 places?
4. Why is reversing the second half useful for both the palindrome and the reorder problems?

# Chapter 5. Building lists with a tail pointer

## 5.1 Merging two sorted lists

Think of two queues of people, each sorted by height, that must be combined into one sorted queue. Look at the two front people, send the shorter one to the new queue, and repeat. When one queue is empty, the rest of the other simply follows.

For lists, we build the answer by appending to a **tail** pointer that always sits on the last node of the new list. The dummy node is back as the very first "last node", so appending the first element needs no special case. We never create new nodes: we simply re-aim `tail.next` at nodes from either list. When one list runs out, a single assignment attaches the entire remainder of the other.

```
a: 1 -> 4 -> 6          b: 2 -> 3
dummy -> 1 -> 2 -> 3 -> 4 -> 6
```

This is exactly the problem _Merge Two Sorted Lists_.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def merge_sorted(a, b):
    dummy = ListNode()
    tail = dummy
    while a is not None and b is not None:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next


assert to_list(merge_sorted(build([1, 4, 6]), build([2, 3]))) == [1, 2, 3, 4, 6]
assert to_list(merge_sorted(build([]), build([5]))) == [5]
assert to_list(merge_sorted(build([]), build([]))) == []
```

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

ListNode* build(const vector<int>& values) {
    ListNode* head = nullptr;
    for (int i = (int)values.size() - 1; i >= 0; i--) {
        head = new ListNode(values[i], head);
    }
    return head;
}

vector<int> toList(ListNode* head) {
    vector<int> out;
    while (head != nullptr) {
        out.push_back(head->val);
        head = head->next;
    }
    return out;
}

ListNode* mergeSorted(ListNode* a, ListNode* b) {
    ListNode dummy;
    ListNode* tail = &dummy;
    while (a != nullptr && b != nullptr) {
        if (a->val <= b->val) {
            tail->next = a;
            a = a->next;
        } else {
            tail->next = b;
            b = b->next;
        }
        tail = tail->next;
    }
    tail->next = (a != nullptr) ? a : b;
    return dummy.next;
}
```

Merging lists of lengths $m$ and $n$ costs $O(m + n)$ time and $O(1)$ extra space. Using `<=` keeps equal values in their original order, which matters when sorting later.

## 5.2 Adding numbers digit by digit

Here is a use of the same "append to the tail" idea. Two numbers are stored as lists of digits with the **ones digit first**: `2 -> 4 -> 3` means 342. That odd-looking order is a gift, because it is exactly the order in which we add on paper: start at the ones column, add the two digits, write the last digit of the total, and **carry** the rest to the next column.

For `342 + 465`: the ones column gives $2 + 5 = 7$, no carry. The tens give $4 + 6 = 10$: write 0, carry 1. The hundreds give $3 + 4 + 1 = 8$. The answer list is `7 -> 0 -> 8`, which is 807.

The loop continues while either list still has digits **or** a carry is left over. That last condition handles the case `99 + 1`, which ends with a brand-new digit: `0 -> 0 -> 1`. Python's `divmod(total, 10)` gives the carry and the digit in one go.

This is exactly the problem _Add Two Numbers_.

```python
def add_digits(a, b):
    dummy = ListNode()
    tail = dummy
    carry = 0
    while a is not None or b is not None or carry:
        total = carry
        if a is not None:
            total += a.val
            a = a.next
        if b is not None:
            total += b.val
            b = b.next
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next


assert to_list(add_digits(build([2, 4, 3]), build([5, 6, 4]))) == [7, 0, 8]
assert to_list(add_digits(build([9, 9]), build([1]))) == [0, 0, 1]
assert to_list(add_digits(build([0]), build([0]))) == [0]
```

```cpp
ListNode* addDigits(ListNode* a, ListNode* b) {
    ListNode dummy;
    ListNode* tail = &dummy;
    int carry = 0;
    while (a != nullptr || b != nullptr || carry != 0) {
        int total = carry;
        if (a != nullptr) {
            total += a->val;
            a = a->next;
        }
        if (b != nullptr) {
            total += b->val;
            b = b->next;
        }
        carry = total / 10;
        tail->next = new ListNode(total % 10);
        tail = tail->next;
    }
    return dummy.next;
}
```

Time $O(\max(m, n))$, and the answer list is the only extra memory.

## 5.3 Two chains: odd and even places

We are asked to put the nodes in odd positions (1st, 3rd, 5th, ...) first, then the ones in even positions, keeping each group's order. The idea is to grow two chains at once. Let `odd` stand on the head and `even` on the second node, and remember where the even chain starts. Then repeat: the odd node skips over the even one to the next odd node, and the even node skips over that odd node to the next even node. When the chains cannot grow any more, join them: the last odd node points at the start of the even chain.

```
1 -> 2 -> 3 -> 4 -> 5
odd chain:  1 -> 3 -> 5
even chain: 2 -> 4
joined:     1 -> 3 -> 5 -> 2 -> 4
```

Notice that this relies on position, not value. This is exactly the problem _Odd Even Linked List_.

```python
def odd_even(head):
    if head is None or head.next is None:
        return head
    odd = head
    even = head.next
    even_head = even
    while even is not None and even.next is not None:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    return head


assert to_list(odd_even(build([1, 2, 3, 4, 5]))) == [1, 3, 5, 2, 4]
assert to_list(odd_even(build([2, 1, 3, 5, 6, 4, 7]))) == [2, 3, 6, 7, 1, 5, 4]
assert to_list(odd_even(build([1, 2]))) == [1, 2]
```

```cpp
ListNode* oddEven(ListNode* head) {
    if (head == nullptr || head->next == nullptr) {
        return head;
    }
    ListNode* odd = head;
    ListNode* even = head->next;
    ListNode* evenHead = even;
    while (even != nullptr && even->next != nullptr) {
        odd->next = even->next;
        odd = odd->next;
        even->next = odd->next;
        even = even->next;
    }
    odd->next = evenHead;
    return head;
}
```

Time $O(n)$ and space $O(1)$.

## 5.4 Two dummy lists: partition

The same "two chains" idea works when the rule is about values. To put all values smaller than $x$ before the rest while keeping the original order inside each group, deal the nodes into two new lists like a card dealer: a `small` list and a `big` list, each with its own dummy node and tail pointer. Walk through the original list once and append each node to the matching tail. At the end, connect the tail of `small` to the head of `big`, and make sure `big`'s tail points to `None`. Without that last step the old arrows could create a cycle, a bug we will look at in the next chapter.

This is exactly the problem _Partition a Linked List_.

```python
def partition(head, x):
    small_dummy = ListNode()
    big_dummy = ListNode()
    small = small_dummy
    big = big_dummy
    cur = head
    while cur is not None:
        if cur.val < x:
            small.next = cur
            small = cur
        else:
            big.next = cur
            big = cur
        cur = cur.next
    big.next = None
    small.next = big_dummy.next
    return small_dummy.next


assert to_list(partition(build([1, 4, 3, 2, 5, 2]), 3)) == [1, 2, 2, 4, 3, 5]
assert to_list(partition(build([2, 1]), 2)) == [1, 2]
assert to_list(partition(build([]), 3)) == []
```

```cpp
ListNode* partition(ListNode* head, int x) {
    ListNode smallDummy, bigDummy;
    ListNode* small = &smallDummy;
    ListNode* big = &bigDummy;
    ListNode* cur = head;
    while (cur != nullptr) {
        if (cur->val < x) {
            small->next = cur;
            small = cur;
        } else {
            big->next = cur;
            big = cur;
        }
        cur = cur->next;
    }
    big->next = nullptr;
    small->next = bigDummy.next;
    return smallDummy.next;
}
```

Time $O(n)$, space $O(1)$: we only move existing nodes.

## 5.5 Check yourself

1. Why does `merge_sorted` use `<=` and not `<` when comparing the two front values?
2. In `add_digits`, why must the loop also continue while `carry` is not zero?
3. In `odd_even`, why do we remember `even_head` before the loop?
4. In `partition`, why do we set `big.next = None` at the end?

# Chapter 6. Cycles and meeting points

## 6.1 A list that loops

So far every list ended in `None`. But arrows are just pointers, and nothing stops the last node from pointing back at an earlier node. Then the list has a **cycle**: following `next` goes round and round forever, and a loop like `while cur is not None` never ends. This can happen by accident (for example by forgetting to cut a tail after rearranging nodes), and it is also a classic puzzle.

```
1 -> 2 -> 3 -> 4
          ^    |
          +----+       node 4 points back at node 3
```

To test our code we need a helper that builds such lists: `build_cycle(values, k)` creates the nodes and, when `k >= 0`, makes the last node point back to node number `k` (counting from 0). It also returns the list of nodes so tests can ask which node was found.

The obvious way to detect a cycle is to keep a set of every node already seen. If we step onto a node that is in the set, we have looped. It is correct, but it uses $O(n)$ memory. Can we do it with $O(1)$?

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_cycle(values, k):
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if k >= 0 and nodes:
        nodes[-1].next = nodes[k]
    head = nodes[0] if nodes else None
    return head, nodes


def has_cycle_with_set(head):
    seen = set()
    cur = head
    while cur is not None:
        if cur in seen:
            return True
        seen.add(cur)
        cur = cur.next
    return False


head, _ = build_cycle([3, 2, 0, -4], 1)
assert has_cycle_with_set(head) is True
head, _ = build_cycle([3, 2, 0, -4], -1)
assert has_cycle_with_set(head) is False
```

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

ListNode* buildCycle(const vector<int>& values, int k, vector<ListNode*>& nodes) {
    nodes.clear();
    for (int v : values) {
        nodes.push_back(new ListNode(v));
    }
    for (int i = 0; i + 1 < (int)nodes.size(); i++) {
        nodes[i]->next = nodes[i + 1];
    }
    if (k >= 0 && !nodes.empty()) {
        nodes.back()->next = nodes[k];
    }
    return nodes.empty() ? nullptr : nodes[0];
}

bool hasCycleWithSet(ListNode* head) {
    unordered_set<ListNode*> seen;
    ListNode* cur = head;
    while (cur != nullptr) {
        if (seen.count(cur)) {
            return true;
        }
        seen.insert(cur);
        cur = cur->next;
    }
    return false;
}
```

Two pieces of vocabulary for later: the **tail** (the stretch before the cycle begins) has length $a$, and the cycle has length $c$.

## 6.2 The tortoise and the hare

Picture two runners on a circular track. If one runs faster than the other, the fast runner will eventually lap the slow one and they meet. On a straight road, by contrast, the fast runner just reaches the end. That difference is the whole idea: run a slow pointer (one step at a time) and a fast pointer (two steps at a time) from the head. If the fast pointer reaches `None`, there is no cycle. If the two pointers ever land on the same node, there is a cycle. This is **Floyd's cycle detection**, nicknamed the tortoise and the hare.

Why must they meet? Once both are inside the cycle, look at the gap between them (measured along the cycle, from slow forward to fast). Each round, fast moves 2 and slow moves 1, so the gap shrinks by exactly 1. A gap that shrinks by 1 each round cannot jump over 0, so it hits 0 and they stand on the same node. They cannot skip past each other.

Let us watch it on a list of five nodes, numbered 0 to 4, where node 4 points back at node 1. After round 1, slow is on node 1 and fast on node 2. After round 2: slow on 2, fast on 4. After round 3: slow on 3, fast on 2. After round 4: slow on 4 and fast on 4. They meet.

This is exactly the problem _Does the List Have a Cycle?_. It takes $O(n)$ time and just $O(1)$ extra space.

```python
def has_cycle(head):
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


head, _ = build_cycle([3, 2, 0, -4, 7], 1)
assert has_cycle(head) is True
head, _ = build_cycle([1, 2, 3], -1)
assert has_cycle(head) is False
head, _ = build_cycle([5], 0)
assert has_cycle(head) is True
assert has_cycle(None) is False
```

```cpp
bool hasCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            return true;
        }
    }
    return false;
}
```

Note that we compare nodes with `is` (identity), never values. Two different nodes can easily hold the same value.

## 6.3 How long is the loop?

Once the pointers have met, both are standing inside the cycle. To measure its length, freeze one pointer and walk the other around until it returns to the frozen one, counting steps. If the list has no cycle, the answer is 0.

In our five-node example the meeting node is node 4. Walking from there goes to node 1, then 2, 3 and back to 4: four steps, so the cycle has four nodes (nodes 1, 2, 3, 4).

This is exactly the problem _Length of the Cycle_.

```python
def cycle_length(head):
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            count = 1
            walker = slow.next
            while walker is not slow:
                walker = walker.next
                count += 1
            return count
    return 0


head, _ = build_cycle([3, 2, 0, -4, 7], 1)
assert cycle_length(head) == 4
head, _ = build_cycle([1, 2, 3], 0)
assert cycle_length(head) == 3
head, _ = build_cycle([1, 2, 3], -1)
assert cycle_length(head) == 0
```

```cpp
int cycleLength(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            int count = 1;
            ListNode* walker = slow->next;
            while (walker != slow) {
                walker = walker->next;
                count++;
            }
            return count;
        }
    }
    return 0;
}
```

## 6.4 Where does the loop begin?

Now the clever one. Let $a$ be the number of steps from the head to the first node of the cycle, and let $c$ be the cycle length. Suppose slow and fast meet after slow has walked $a + b$ steps, where $b$ is how far into the cycle it is. Fast has walked twice as much: $2(a + b)$ steps. Fast has gone around the cycle some whole number $m$ of extra times, so the difference between the two walks is a multiple of $c$:

$$2(a + b) - (a + b) = m \cdot c \quad\Longrightarrow\quad a + b = m \cdot c.$$

Rearrange: $a = m \cdot c - b$. In words: from the meeting point, walking $a$ more steps takes us around the cycle $m$ times minus $b$ steps, which lands exactly on the start of the cycle (the meeting point is already $b$ steps past it). And walking $a$ steps from the head also lands on the start. So put one pointer at the head and keep the other at the meeting point, move them one step at a time, and **they meet exactly at the cycle start**.

In our example $a = 1$, the meeting node is node 4 and $b = 3$, $c = 4$, so $a + b = 4 = c$. One step from node 4 leads to node 1, and one step from the head (node 0) also leads to node 1.

This is exactly the problem _Where Does the Cycle Start?_. Time $O(n)$, space $O(1)$.

```python
def cycle_start(head):
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            finder = head
            while finder is not slow:
                finder = finder.next
                slow = slow.next
            return finder
    return None


head, nodes = build_cycle([3, 2, 0, -4, 7], 1)
assert cycle_start(head) is nodes[1]
head, nodes = build_cycle([1, 2, 3], 0)
assert cycle_start(head) is nodes[0]
head, nodes = build_cycle([1, 2, 3], -1)
assert cycle_start(head) is None
```

```cpp
ListNode* cycleStart(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            ListNode* finder = head;
            while (finder != slow) {
                finder = finder->next;
                slow = slow->next;
            }
            return finder;
        }
    }
    return nullptr;
}
```

## 6.5 Two lists that join

A cousin of the cycle problem: two lists start separately but may merge into one shared tail (the very same nodes, not merely equal values). Where do they first share a node?

The elegant answer uses no extra memory. Walk one pointer `p` along list A and another `q` along list B. When a pointer falls off the end of its list, send it to the **head of the other list**. Let the private part of A have length $x$, the private part of B have length $y$, and the shared tail have length $z$. Pointer `p` walks all of A ($x + z$ steps), jumps to the head of B, and walks B's private part ($y$ steps), so it stands on the first shared node after $x + z + y$ steps in total. Pointer `q` does the mirror image: $y + z + x$ steps. The totals are equal, so both pointers reach the first shared node at the same moment. If there is no shared part, both pointers fall off the end of their second list together after $x + y$ steps, both become `None`, and `None` is the right answer.

This is exactly the problem _Intersection of Two Lists_. Time $O(x + y + z)$, space $O(1)$.

```python
def join_lists(a_head, b_head_chain):
    cur = a_head
    while cur.next is not None:
        cur = cur.next
    cur.next = b_head_chain


def intersection(a, b):
    p = a
    q = b
    while p is not q:
        p = p.next if p is not None else b
        q = q.next if q is not None else a
    return p


shared = ListNode(8, ListNode(9))
list_a = ListNode(1, ListNode(2))
list_b = ListNode(5)
join_lists(list_a, shared)
join_lists(list_b, shared)
assert intersection(list_a, list_b) is shared
assert intersection(ListNode(1), ListNode(2)) is None
```

```cpp
ListNode* intersection(ListNode* a, ListNode* b) {
    ListNode* p = a;
    ListNode* q = b;
    while (p != q) {
        p = (p != nullptr) ? p->next : b;
        q = (q != nullptr) ? q->next : a;
    }
    return p;
}
```

(`join_lists` is only a test helper that attaches a chain to the end of a list.)

## 6.6 Check yourself

1. Why can the fast pointer never jump over the slow pointer once both are inside the cycle?
2. After the pointers meet, how do we measure the cycle length?
3. In the proof for the cycle start, what does the equation $a + b = m \cdot c$ tell us?
4. In the intersection trick, why do the two pointers walk the same total distance?

# Chapter 7. Sorting a list

## 7.1 Why not sort like an array?

Sorting an array can use random access: quicksort jumps around, and heapsort indexes into the middle. A linked list has no jumping, so those methods are awkward. The simple method that does work, insertion sort (take each node and walk through the sorted part to find where it belongs), costs $O(n^2)$ time and is too slow for long lists.

The method that suits linked lists perfectly is **merge sort**, for two reasons. Splitting a list in half is cheap (we have just seen how to find the middle). And merging two sorted lists needs no extra space: we did it in Chapter 5 by only re-aiming arrows.

## 7.2 Merge sort on a list

Merge sort works by divide and conquer, which means: split the problem in two halves, solve each half by calling yourself, and combine the answers. For a list: if it has 0 or 1 node, it is already sorted. Otherwise cut it in the middle into two lists, sort each with the same function, and merge the two sorted halves.

To cut, we find the last node of the first half with slow and fast pointers (here `fast` starts one step ahead, at `head.next`, so that `slow` ends on the last node of the first half), set `second = slow.next`, and cut with `slow.next = None`. Forgetting that cut means the first half still leads into the second, and the recursion never shrinks.

```
4 -> 2 -> 5 -> 1          split:   4 -> 2     5 -> 1
sort halves:                        2 -> 4     1 -> 5
merge:                         1 -> 2 -> 4 -> 5
```

How long does it take? Each level of splitting halves the lists, so there are about $\log_2 n$ levels, and at every level the merges together touch all $n$ nodes once. That gives $O(n \log n)$ time. The recursion is $O(\log n)$ deep, so the extra space is $O(\log n)$ for the call stack (a bottom-up version that merges small pieces into bigger ones needs only $O(1)$, but the recursive one is easier to get right).

This is exactly the problem _Sort a Linked List_.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def merge_sorted(a, b):
    dummy = ListNode()
    tail = dummy
    while a is not None and b is not None:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next


def merge_sort(head):
    if head is None or head.next is None:
        return head
    slow = head
    fast = head.next
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None
    return merge_sorted(merge_sort(head), merge_sort(second))


assert to_list(merge_sort(build([4, 2, 5, 1]))) == [1, 2, 4, 5]
assert to_list(merge_sort(build([3, 1, 2]))) == [1, 2, 3]
assert to_list(merge_sort(build([2, 2, 1, 1]))) == [1, 1, 2, 2]
assert to_list(merge_sort(build([]))) == []
```

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

ListNode* build(const vector<int>& values) {
    ListNode* head = nullptr;
    for (int i = (int)values.size() - 1; i >= 0; i--) {
        head = new ListNode(values[i], head);
    }
    return head;
}

vector<int> toList(ListNode* head) {
    vector<int> out;
    while (head != nullptr) {
        out.push_back(head->val);
        head = head->next;
    }
    return out;
}

ListNode* mergeSorted(ListNode* a, ListNode* b) {
    ListNode dummy;
    ListNode* tail = &dummy;
    while (a != nullptr && b != nullptr) {
        if (a->val <= b->val) {
            tail->next = a;
            a = a->next;
        } else {
            tail->next = b;
            b = b->next;
        }
        tail = tail->next;
    }
    tail->next = (a != nullptr) ? a : b;
    return dummy.next;
}

ListNode* mergeSort(ListNode* head) {
    if (head == nullptr || head->next == nullptr) {
        return head;
    }
    ListNode* slow = head;
    ListNode* fast = head->next;
    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
    }
    ListNode* second = slow->next;
    slow->next = nullptr;
    return mergeSorted(mergeSort(head), mergeSort(second));
}
```

Check the split on the smallest cases: a two-node list `4 -> 2` has `slow` on 4 and `fast` on 2 (whose `next` is empty), so the loop does not run, the halves are `4` and `2`, and each is a single node. A three-node list splits 2 and 1. Both halves are always strictly smaller than the whole, so the recursion ends.

## 7.3 Check yourself

1. Why does merge sort suit linked lists better than quicksort?
2. What goes wrong if we forget `slow.next = None` before recursing?
3. Why does merging two sorted lists cost no extra memory?
4. About how many levels of splitting does a list of 1000 nodes need?

# Chapter 8. Merging many lists

## 8.1 Why merge one after another is slow

Now we have $k$ sorted lists and want one sorted list. The first idea: merge list 1 with list 2, then merge the result with list 3, and so on. It works, but think about the cost. If each list has $m$ nodes, the first merge touches $2m$ nodes, the second $3m$, then $4m$, and the last $k m$. The total is about $m(2 + 3 + \dots + k)$, which is of order $k^2 m / 2 = N k / 2$ when $N = k m$ is the total number of nodes. With many lists that is far too slow. The early nodes get copied around again and again.

## 8.2 Always take the smallest front

Look at merging two lists again: we compare the two front nodes and take the smaller one. With $k$ lists, the idea extends naturally: look at the $k$ front nodes, take the smallest, and then the list it came from offers its next node. We need a structure that quickly gives "the smallest of these $k$ items" and lets us replace it with another. That is a **heap** (also called a priority queue): a container where pushing and removing the smallest item each cost $O(\log k)$ for $k$ items.

So: put the head of every non-empty list in a min-heap. Repeat: pop the smallest node, append it to the answer's tail, and push that node's `next` if it exists. The heap never holds more than $k$ nodes, so each of the $N$ pops and pushes costs $O(\log k)$. The total is $O(N \log k)$ time and $O(k)$ extra space.

In Python we store tuples `(value, list_index, node)`. The list index matters: if two values are equal Python would otherwise try to compare two `ListNode` objects, which cannot be ordered and would crash. Because the index is different for every entry in the heap, the tuples never tie on both of the first two items. In C++ we give the priority queue a comparison that looks at `val`.

This is exactly the problem _Merge K Sorted Lists_.

```python
import heapq


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def merge_k_heap(lists):
    heap = []
    for i, node in enumerate(lists):
        if node is not None:
            heap.append((node.val, i, node))
    heapq.heapify(heap)
    dummy = ListNode()
    tail = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next is not None:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next


lists = [build([1, 4, 5]), build([1, 3, 4]), build([2, 6])]
assert to_list(merge_k_heap(lists)) == [1, 1, 2, 3, 4, 4, 5, 6]
assert to_list(merge_k_heap([])) == []
assert to_list(merge_k_heap([None, build([7])])) == [7]
```

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

ListNode* build(const vector<int>& values) {
    ListNode* head = nullptr;
    for (int i = (int)values.size() - 1; i >= 0; i--) {
        head = new ListNode(values[i], head);
    }
    return head;
}

vector<int> toList(ListNode* head) {
    vector<int> out;
    while (head != nullptr) {
        out.push_back(head->val);
        head = head->next;
    }
    return out;
}

ListNode* mergeKHeap(vector<ListNode*>& lists) {
    auto cmp = [](ListNode* a, ListNode* b) { return a->val > b->val; };
    priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> heap(cmp);
    for (ListNode* node : lists) {
        if (node != nullptr) {
            heap.push(node);
        }
    }
    ListNode dummy;
    ListNode* tail = &dummy;
    while (!heap.empty()) {
        ListNode* node = heap.top();
        heap.pop();
        tail->next = node;
        tail = node;
        if (node->next != nullptr) {
            heap.push(node->next);
        }
    }
    return dummy.next;
}
```

(C++'s `priority_queue` is a max-heap by default, so the comparison `a->val > b->val` flips it into a min-heap.)

## 8.3 Merging in pairs

There is a second way to reach $O(N \log k)$ using only the two-list merge. Instead of folding lists into one growing result, merge them **in pairs**: lists 1 and 2, lists 3 and 4, and so on. This halves the number of lists. Repeat on the results until one list is left. There are about $\log_2 k$ rounds, and in each round every node is touched once, so the cost is $O(N \log k)$ again, without a heap.

```
[A] [B] [C] [D] [E]
  [AB]   [CD]   [E]
     [ABCD]     [E]
          [ABCDE]
```

```python
def merge_sorted(a, b):
    dummy = ListNode()
    tail = dummy
    while a is not None and b is not None:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next


def merge_k_pairs(lists):
    if not lists:
        return None
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            a = lists[i]
            b = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_sorted(a, b))
        lists = merged
    return lists[0]


lists = [build([1, 4, 5]), build([1, 3, 4]), build([2, 6]), build([0, 9]), build([7])]
assert to_list(merge_k_pairs(lists)) == [0, 1, 1, 2, 3, 4, 4, 5, 6, 7, 9]
assert merge_k_pairs([]) is None
```

```cpp
ListNode* mergeSorted(ListNode* a, ListNode* b) {
    ListNode dummy;
    ListNode* tail = &dummy;
    while (a != nullptr && b != nullptr) {
        if (a->val <= b->val) {
            tail->next = a;
            a = a->next;
        } else {
            tail->next = b;
            b = b->next;
        }
        tail = tail->next;
    }
    tail->next = (a != nullptr) ? a : b;
    return dummy.next;
}

ListNode* mergeKPairs(vector<ListNode*> lists) {
    if (lists.empty()) {
        return nullptr;
    }
    while (lists.size() > 1) {
        vector<ListNode*> merged;
        for (size_t i = 0; i < lists.size(); i += 2) {
            ListNode* a = lists[i];
            ListNode* b = (i + 1 < lists.size()) ? lists[i + 1] : nullptr;
            merged.push_back(mergeSorted(a, b));
        }
        lists = merged;
    }
    return lists[0];
}
```

Either method is fine. The heap version is shorter to write; the pairing version reuses code you already have. In the C++ version the vector is passed by value so the caller's vector is not changed.

## 8.4 Check yourself

1. Why does merging the lists one after another cost about $N k / 2$?
2. Why does the Python heap store the list index next to the value?
3. How large can the heap get when we merge $k$ lists?
4. Roughly how many rounds of pairing are needed for 16 lists?

# Chapter 9. Reversing in groups of k

## 9.1 The plan

We finish with a problem that uses almost everything above: reverse the list $k$ nodes at a time. For `1 -> 2 -> 3 -> 4 -> 5 -> 6` and $k = 3$ we want `3 -> 2 -> 1 -> 6 -> 5 -> 4`. The recipe is a loop over groups, and in each round we do what Chapter 3 taught:

1. Keep a pointer `before` on the node just in front of the current group (a dummy node at the start).
2. Reverse the group of $k$ nodes with the `reverse_k` helper, which gives the new front and `rest`, the first node after the group.
3. Reconnect: `before.next` points at the new front, and the old first node of the group (now its last) points at `rest`.
4. Move `before` onto that old first node, which is the last node of the group just finished, and repeat.

## 9.2 Reversing every group, even the short one

Let us first solve an easier cousin: reverse every group of $k$, **including** a short group at the end. We only need a version of `reverse_k` that politely stops when the list ends. For `1 -> 2 -> 3 -> 4 -> 5` and $k = 3$ it yields `3 -> 2 -> 1 -> 5 -> 4`.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def reverse_up_to(start, k):
    prev = None
    cur = start
    for _ in range(k):
        if cur is None:
            break
        after = cur.next
        cur.next = prev
        prev = cur
        cur = after
    return prev, cur


def reverse_every_k(head, k):
    dummy = ListNode(0, head)
    before = dummy
    while before.next is not None:
        first = before.next
        new_front, rest = reverse_up_to(first, k)
        before.next = new_front
        first.next = rest
        before = first
    return dummy.next


assert to_list(reverse_every_k(build([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 5, 4]
assert to_list(reverse_every_k(build([1, 2, 3, 4, 5, 6]), 3)) == [3, 2, 1, 6, 5, 4]
assert to_list(reverse_every_k(build([1, 2, 3]), 1)) == [1, 2, 3]
```

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v = 0, ListNode* n = nullptr) : val(v), next(n) {}
};

ListNode* build(const vector<int>& values) {
    ListNode* head = nullptr;
    for (int i = (int)values.size() - 1; i >= 0; i--) {
        head = new ListNode(values[i], head);
    }
    return head;
}

vector<int> toList(ListNode* head) {
    vector<int> out;
    while (head != nullptr) {
        out.push_back(head->val);
        head = head->next;
    }
    return out;
}

pair<ListNode*, ListNode*> reverseUpTo(ListNode* start, int k) {
    ListNode* prev = nullptr;
    ListNode* cur = start;
    for (int i = 0; i < k; i++) {
        if (cur == nullptr) {
            break;
        }
        ListNode* after = cur->next;
        cur->next = prev;
        prev = cur;
        cur = after;
    }
    return {prev, cur};
}

ListNode* reverseEveryK(ListNode* head, int k) {
    ListNode dummy(0, head);
    ListNode* before = &dummy;
    while (before->next != nullptr) {
        ListNode* first = before->next;
        auto [newFront, rest] = reverseUpTo(first, k);
        before->next = newFront;
        first->next = rest;
        before = first;
    }
    return dummy.next;
}
```

## 9.3 Leaving a short group alone

The real problem says a final group with fewer than $k$ nodes must stay as it is. The only change: before reversing a group, check that $k$ nodes are really there. We do that with a small helper that walks $k - 1$ steps from the group's first node; if it falls off the end, the group is too short and we stop the whole loop. Everything else is unchanged, and we can use the same helper, since once we know the group is complete it reverses exactly $k$ nodes.

Take `1 -> 2 -> 3 -> 4 -> 5` with $k = 2$. Group `1, 2` is complete and becomes `2 -> 1`. Group `3, 4` becomes `4 -> 3`. Group `5` has only one node and stays. The result is `2 -> 1 -> 4 -> 3 -> 5`.

This is exactly the problem _Reverse Nodes in K-Groups_. Each node is visited a constant number of times, so time is $O(n)$ and extra space is $O(1)$.

```python
def has_k_nodes(start, k):
    cur = start
    for _ in range(k):
        if cur is None:
            return False
        cur = cur.next
    return True


def reverse_k_groups(head, k):
    dummy = ListNode(0, head)
    before = dummy
    while has_k_nodes(before.next, k):
        first = before.next
        new_front, rest = reverse_up_to(first, k)
        before.next = new_front
        first.next = rest
        before = first
    return dummy.next


assert to_list(reverse_k_groups(build([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
assert to_list(reverse_k_groups(build([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5]
assert to_list(reverse_k_groups(build([1, 2, 3]), 4)) == [1, 2, 3]
```

```cpp
bool hasKNodes(ListNode* start, int k) {
    ListNode* cur = start;
    for (int i = 0; i < k; i++) {
        if (cur == nullptr) {
            return false;
        }
        cur = cur->next;
    }
    return true;
}

ListNode* reverseKGroups(ListNode* head, int k) {
    ListNode dummy(0, head);
    ListNode* before = &dummy;
    while (hasKNodes(before->next, k)) {
        ListNode* first = before->next;
        auto [newFront, rest] = reverseUpTo(first, k);
        before->next = newFront;
        first->next = rest;
        before = first;
    }
    return dummy.next;
}
```

If you can explain why `before` moves onto `first` and why `has_k_nodes` is called on `before.next`, you have understood the whole page: every hard linked-list problem is a few arrows redirected in a careful order, usually with a dummy node at the front.

## 9.4 Check yourself

1. Why must `before` move onto the old first node of the group after each round?
2. What does `has_k_nodes` return for a group that is one node short?
3. For a list of 7 nodes and $k = 3$, how many groups get reversed?
4. Why is the total work $O(n)$ even though there are two nested loops?
