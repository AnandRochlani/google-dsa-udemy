# Happy Number

> **LeetCode:** 202. Happy Number · **Difficulty:** 🟢 Easy · **Pattern:** Fast & Slow Pointers · **Google frequency:** medium

---

## Problem

A number is **happy** if you repeatedly replace it with the **sum of the squares of its digits**, and this process eventually reaches `1`. If instead it falls into a loop that never reaches `1`, it's not happy. Return `True` if `n` is happy.

**Example:** `n = 19` → `1² + 9² = 82` → `8² + 2² = 68` → `6² + 8² = 100` → `1² + 0² + 0² = 1` → **`True`**.

`n = 2` → `4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 → …` — it cycles back to `4` and never hits `1` → **`False`**.

**Constraints that matter:** `1 ≤ n ≤ 2³¹ − 1`. The key fact: the digit-square process is **deterministic**, so it either reaches `1` or **repeats a value forever** — there's no third option (the values are bounded, so it can't run off to infinity). "Reaches 1 or cycles" is literally cycle detection in disguise.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** simulate the process. Keep computing the next number. If you hit `1`, it's happy. But how do you know when to give up? "I'll remember every number I've already produced — if one repeats, I'm in a loop and it'll never reach 1." That's a **hash set of seen values**. Correct and clean.
- **Where it hurts:** the set grows with however many distinct values appear before repeating — **O(k) extra space**. And here's the reframe: this sequence is exactly a **linked list**. Each number "points to" the next number (the digit-square sum). "Does it reach 1, or loop?" is precisely "does this list terminate, or does it have a cycle?"
- **The leap:** if it's a linked list with a possible cycle, you already own the O(1)-space tool — **Floyd's tortoise and hare**. Run a slow pointer (one step of the process) and a fast pointer (two steps). If they meet at `1`, happy. If they meet at anything else, that's the cycle — not happy. No set needed.
- **Pattern trigger:** **"repeat a deterministic step; does it terminate or cycle?"** → treat the value sequence as a linked list and apply **Fast & Slow Pointers**. Recognising an *implicit* linked list is the transferable skill.

---

## ① Brute Force

Simulate, storing every value seen in a set; a repeat means a non-terminating loop.

```python
def is_happy_bruteforce(n):
    def next_num(x):
        total = 0
        while x:
            x, d = divmod(x, 10)
            total += d * d
        return total

    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = next_num(n)
    return n == 1
```

**Why it's the natural first attempt:** "keep going until I hit 1 or see a repeat" is the direct simulation, and a set is the obvious way to detect a repeat.

**Why it's not enough:** the set uses **O(k) space** for the values visited before a cycle. It's a great answer — but the O(1)-space version demonstrates you recognised the hidden linked-list structure.

**Complexity:** Time `O(log n)` per step over `O(k)` steps, Space `O(k)`.

---

## ② Optimised Solution

Same `next_num`, but detect the cycle with fast/slow pointers instead of a set.

```python
def is_happy(n):
    def next_num(x):
        total = 0
        while x:
            x, d = divmod(x, 10)
            total += d * d
        return total

    slow = n
    fast = next_num(n)
    while fast != 1 and slow != fast:
        slow = next_num(slow)             # +1 step
        fast = next_num(next_num(fast))   # +2 steps
    return fast == 1
```

**Walk `n = 19` (happy):** the fast pointer races ahead through `82 → 100 → …` and reaches `1`; the loop exits with `fast == 1` → **True** ✅.

**Walk `n = 2` (unhappy):** the sequence is `4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 → …`. Fast and slow both circle this loop and eventually land on the same value (`slow == fast`) without ever hitting `1` → loop exits, `fast != 1` → **False** ✅.

**Why it's correct:** the value sequence is a linked list where `next` = `next_num`. If it reaches `1`, `1`'s successor is `1` (a self-loop), so fast gets stuck at `1` and we detect happiness. Otherwise there's a genuine cycle of other values, and by Floyd's guarantee the fast pointer laps and collides with slow.

**Complexity:** Time `O(log n)` per step, `O(k)` steps → effectively `O(log n)` amortised bounds, Space `O(1)`.

---

## ③ Space Optimization

This is the point of using the pattern here:

- **Hash set:** stores every value before the cycle → **O(k) space**.
- **Fast & slow:** two integer variables → **O(1) space**.

Nothing about the sequence needs to be *remembered* — the second, faster pointer discovers the loop on its own. Recognising the numeric sequence as a linked list is what unlocks the constant-space solution.

> *"The digit-square sequence is really a linked list, so instead of a hash set I'll run tortoise and hare on it — O(1) space. If the fast pointer reaches 1 it's happy; if the two pointers meet elsewhere, it's a cycle and it's not."*

---

## Java (for Java interviewers)

```java
public boolean isHappy(int n) {
    int slow = n, fast = next(n);
    while (fast != 1 && slow != fast) {
        slow = next(slow);
        fast = next(next(fast));
    }
    return fast == 1;
}

private int next(int x) {
    int total = 0;
    while (x > 0) {
        int d = x % 10;
        total += d * d;
        x /= 10;
    }
    return total;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (hash set) | O(log n) per step | O(k) |
| Optimised (fast & slow) | O(log n) per step | O(1) |

---

## Say it out loud (interview narration)

> *"The digit-square process is deterministic, so it either reaches 1 or loops forever — that's cycle detection. The easy version stores seen values in a set, O(k) space. But the sequence is really a linked list where each number points to its digit-square sum, so I'll run Floyd's tortoise and hare: fast reaching 1 means happy, fast and slow meeting anywhere else means an unhappy cycle. O(1) space."*

## Related / follow-ups
- **Linked List Cycle** (the same tortoise-and-hare on an explicit list)
- **Find the Duplicate Number** (another "implicit linked list" + Floyd problem)
- **Add Digits** / digit-manipulation warmups
