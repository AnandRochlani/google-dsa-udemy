# RLE Iterator

> **LeetCode:** 900. RLE Iterator · **Difficulty:** 🟡 Medium · **Pattern:** Design / pointer over run-length encoding · **Google frequency:** medium

---

## Problem

You're given a sequence stored in **run-length encoding**: a flat list `encoding = [count, value, count, value, ...]`. Each pair means *"`count` copies of `value`"*. So `[3, 8, 0, 9, 2, 5]` decodes to `8, 8, 8, 5, 5` (three 8s, zero 9s, two 5s).

Design an iterator with one method:

- `next(n)` — **exhaust** the next `n` elements of the decoded sequence and **return the last one exhausted**. If fewer than `n` elements remain, exhaust everything that's left and return `-1`.

"Exhaust" means consume — those elements are gone; a later `next` continues after them.

**Example:** `RLEIterator([3, 8, 0, 9, 2, 5])` → decoded stream is `8, 8, 8, 5, 5`

```
next(2) -> 8    // consume 8,8 ; last consumed is 8
next(1) -> 8    // consume the 3rd 8 ; last is 8
next(1) -> 5    // the 8s are gone (and 0 nines) ; consume first 5 ; last is 5
next(2) -> -1   // only one 5 left, need 2 → exhaust it and return -1
```

**Constraints that matter:** counts go up to **10⁹**, and the encoding can hold up to `1000` pairs. That single number — `10⁹` — is the whole problem. A run can say *"one billion copies of 8"*. If your first move is to decode the stream into an actual list, you allocate a **billion-element array** and time out (or run out of memory) before you answer a single query. The design must **never materialize the decoded sequence** — it has to skip through runs arithmetically.

---

## 🧠 Intuition — how you'd actually arrive at this

> This is a "don't take the problem literally" design question. The naive reading — "decode it, then walk it" — is a trap the constraints are built to punish.

- **First instinct:** decode `encoding` into a real list `[8,8,8,5,5]`, keep an index, and `next(n)` just advances the index by `n` and returns the element there. Clean, obvious, correct… on small inputs.
- **Where it hurts:** a run can be `10⁹` copies. Decoding blows up memory and time on a *single* run. You're expanding data you never actually need to see element-by-element — you only ever need the **value** of a run and **how many** are left in it.
- **The leap:** don't expand the runs — **walk over the runs themselves.** Keep a pointer `i` at the current run's `count` slot. Each run is a bucket with a value (`encoding[i+1]`) and a remaining quantity (`encoding[i]`). To consume `n`: if the current bucket has enough, just subtract `n` from its remaining count and you're done — the answer is that bucket's value. If it doesn't, drain the bucket (subtract what it had from `n`), step the pointer forward by 2 to the next run, and repeat. A billion-copy run is handled by **one subtraction**, not a billion steps.
- **Pattern trigger:** *"the input is a compressed/encoded form and the naive move is to decompress it"* → **operate on the compressed form directly, with a pointer + a running remainder.** The transferable lesson: when a count can be astronomically large, the count is a *number to do arithmetic on*, never a length to loop over.

---

## ① Brute Force

Decode the whole encoding into a flat list, keep a read index, and serve `next(n)` by jumping the index.

```python
class RLEIteratorBrute:
    def __init__(self, encoding):
        self.seq = []
        for i in range(0, len(encoding), 2):
            count, value = encoding[i], encoding[i + 1]
            self.seq.extend([value] * count)   # ← expands 10^9 copies into memory
        self.pos = 0

    def next(self, n: int) -> int:
        self.pos += n                          # consume n elements
        if self.pos > len(self.seq):           # ran past the end?
            self.pos = len(self.seq)
            return -1
        return self.seq[self.pos - 1]          # last one consumed
```

**Why it's the natural first attempt:** it's a direct translation of the words — "the sequence is these values repeated, and next skips ahead." If counts were small it would be perfect.

**Why it's not enough:** `self.seq.extend([value] * count)` with `count = 10⁹` tries to build a billion-element list. That's gigabytes of memory and a huge up-front loop — it dies in the constructor, before any `next` call runs. The elements inside a run are all identical, so materializing them one by one is pure waste.

**Complexity:** Time O(total decoded length) to build — up to ~10⁹ per run. Space O(total decoded length). Both unusable.

---

## ② Optimised Solution

Keep the encoding as-is and walk over **runs**, not elements. A pointer `i` marks the current run's count slot; we decrement that count in place as we consume, and step forward by 2 when a run is drained.

```python
class RLEIterator:
    def __init__(self, encoding):
        self.enc = encoding    # store as-is; enc[i] = remaining count, enc[i+1] = value
        self.i = 0             # index of the current run's *count*

    def next(self, n: int) -> int:
        # walk forward through runs until we've consumed n elements
        while self.i < len(self.enc):
            if self.enc[self.i] >= n:          # this run alone covers the request
                self.enc[self.i] -= n          # consume n from it (arithmetic, not a loop)
                return self.enc[self.i + 1]    # its value is the last one exhausted
            # otherwise drain this whole run and move on
            n -= self.enc[self.i]              # subtract what this run had left
            self.enc[self.i] = 0               # mark it empty
            self.i += 2                        # advance to the next run's count
        return -1                              # fell off the end → not enough left
```

**Walk the example** `RLEIterator([3, 8, 0, 9, 2, 5])` — the encoding array *is* our state; watch `enc` and `i` mutate:

| Call | start `i`, `enc` | what happens | returns | end `i`, `enc` |
|---|---|---|---|---|
| `next(2)` | `i=0`, `[3,8,0,9,2,5]` | `enc[0]=3 ≥ 2` → `enc[0] -= 2` | **8** (`enc[1]`) | `i=0`, `[1,8,0,9,2,5]` |
| `next(1)` | `i=0`, `[1,8,0,9,2,5]` | `enc[0]=1 ≥ 1` → `enc[0] -= 1` | **8** | `i=0`, `[0,8,0,9,2,5]` |
| `next(1)` | `i=0`, `[0,8,0,9,2,5]` | `enc[0]=0 < 1` → drain, `i→2`; `enc[2]=0 < 1` → drain, `i→4`; `enc[4]=2 ≥ 1` → `enc[4] -= 1` | **5** (`enc[5]`) | `i=4`, `[0,8,0,9,1,5]` |
| `next(2)` | `i=4`, `[0,8,0,9,1,5]` | `enc[4]=1 < 2` → `n=1`, drain, `i→6`; `i=6 ≥ len` → loop ends | **-1** | `i=6`, `[0,8,0,9,0,5]` |

Notice the third call skipped the empty `0,9` run (zero copies of 9) in a single step, and the fourth call fell off the end and returned `-1` exactly as required.

**Why it's correct:** the invariant is that `enc[i]` always holds *how many elements of the current run remain unconsumed*, and everything before index `i` is fully drained. When a run has `≥ n` left, the `n`-th element we consume lands inside it, so its value `enc[i+1]` is the last one exhausted — and subtracting `n` keeps the remaining-count invariant. When a run has fewer than `n`, we consume all of it (`n -= enc[i]`) and move on; the value we ultimately return is whichever run finally absorbs the last unit. If we run past the final run, there weren't `n` elements left, so `-1` is correct. Crucially, a run of a billion is consumed with **one subtraction**, never a loop.

**Complexity (per `next` call):** Time **O(number of runs consumed in this call)** — at worst O(pairs), but the pointer only ever moves forward across the whole object's lifetime, so it's **amortized O(1) per run** overall. Space **O(len(encoding))** — we store the encoding and two integers, nothing that scales with the counts.

---

## ③ Space Optimization

**Already optimal — and here's why there's nothing to cut.** We keep only the input encoding plus a single index `i`. Nothing grows with the *counts* (the dangerous `10⁹`) — a billion-copy run costs the same one slot as a one-copy run. The extra working memory beyond the input is a single integer, i.e. **O(1) auxiliary**.

```python
# No leaner variant exists. The state is: the encoding array + one pointer.
# We mutate the encoding in place (decrementing the current run's count),
# so we don't even allocate a copy. Auxiliary space beyond the input is O(1).
```

If mutating the caller's array bothers you, the only tweak is to track the current run's *consumed* amount in a separate variable instead of editing `enc[i]` in place — same asymptotic space, just non-destructive.

**Complexity:** Time amortized O(1) per run over the object's life; Space O(len(encoding)) for the stored encoding, **O(1) auxiliary**.

> Say it out loud: *"There's no memory trick to chase here — the point is what I refuse to allocate. I never decode the runs, so nothing in my state scales with the counts, only with the number of pairs. That's the whole win."* Naming *why* it's already optimal — and pinning it to the `10⁹` constraint — is the strong-hire move.

---

## Java (for Java interviewers)

```java
class RLEIterator {
    private final long[] enc;   // long: counts can be up to 10^9 and n can sum high
    private int i = 0;          // index of the current run's remaining count

    public RLEIterator(int[] encoding) {
        enc = new long[encoding.length];
        for (int k = 0; k < encoding.length; k++) enc[k] = encoding[k];
    }

    public int next(int n) {
        while (i < enc.length) {
            if (enc[i] >= n) {            // this run covers the whole request
                enc[i] -= n;             // consume n by arithmetic, no loop
                return (int) enc[i + 1]; // its value is the last exhausted
            }
            n -= enc[i];                 // drain this run
            enc[i] = 0;
            i += 2;                      // step to the next run
        }
        return -1;                       // not enough elements left
    }
}
```

*(Note the `long`: values fit in `int`, but keeping counts as `long` avoids any overflow worry when a run holds ~10⁹ and `n` is subtracted against it.)*

---

## Complexity Summary

| Approach | `next(n)` | Space |
|---|---|---|
| Brute force (decode to a list) | O(decoded length) to build; O(1) per call after | O(decoded length) — up to ~10⁹, unusable |
| Pointer over runs | O(runs consumed); amortized O(1) per run | O(len(encoding)), O(1) auxiliary |

---

## Say it out loud (interview narration)

> *"First clarifying instinct: the counts go to a billion, so the trap is decoding the sequence — that's a billion-element array and an instant timeout. I'll refuse to expand it. Instead I keep the encoding as-is and hold a pointer at the current run's count. For next(n): if the current run has at least n left, I subtract n and return that run's value — one arithmetic step even for a billion-copy run. If it doesn't, I drain it, subtract what it had from n, jump the pointer to the next pair, and repeat. Fall off the end and I return -1. The pointer only moves forward, so it's amortized O(1) per run, and my space is just the encoding plus one index — nothing scales with the counts, which is the entire point."*

Lead with the clarifying observation about `10⁹` before you write anything — spotting that decoding is a trap is exactly the General Cognitive Ability signal Google's rubric rewards.

## Related / follow-ups
- **Design Compressed String Iterator** (604) — nearly the same idea: iterate a run-length string with `next()`/`hasNext()` without decompressing.
- **Iterator for Combination / Peeking Iterator** (1286 / 284) — design an iterator that computes on demand instead of materializing.
- **Decode String** (394) — the opposite temptation: here you *do* expand, but nested, so watch the blow-up.
- **Flatten Nested List Iterator** (341) — iterator design with lazy traversal over a compressed/nested structure.
