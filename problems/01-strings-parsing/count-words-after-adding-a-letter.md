# Count Words Obtained After Adding a Letter

> **LeetCode:** 2135. Count Words Obtained After Adding a Letter · **Difficulty:** 🟡 Medium · **Pattern:** Bitmask / Hash Set · **Google frequency:** ⭐ high

---

## Problem

You're given two arrays of lowercase words, `startWords` and `targetWords`. A target word is **obtainable** if you can pick some word from `startWords`, **add exactly one new letter** that isn't already in it, then **rearrange** the letters in any order to spell the target. Return how many words in `targetWords` are obtainable. A crucial given: **every word has all-distinct letters** — no repeats inside a single word.

**Example:** `startWords = ["ant","act","tack"]`, `targetWords = ["tack","act","acti"]` → `2`

- `"tack"` — take `"act"` (a,c,t), add `k`, rearrange → `tack`. ✅
- `"act"` — you'd need a 2-letter start word to add one letter to; there isn't one. ❌
- `"acti"` — take `"act"`, add `i`, rearrange → `acti`. ✅

**Constraints that matter:** both arrays can be up to `5·10⁴` long, and each word up to length `26`. A pairwise check — every target against every start — is `O(|target|·|start|·26)` ≈ `10¹⁰`. That's a hard timeout. We need to make each target a **constant-ish lookup**, not a scan over all start words.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** for each target word, loop over every start word and ask *"is this start word one added-letter away from the target?"* That means: the start's letters are all inside the target, and the target has exactly one extra letter. Correct — but it's a nested loop over two arrays of 50k. It times out.
- **Where it hurts:** for every single target you re-scan the *entire* start list. All that work — comparing letter sets over and over — is the waste. You're asking "does a matching start exist?" the slow way, by looking at all of them, when a **membership test** would answer it instantly.
- **The leap:** two facts in the problem hand you a superpower. **(1) Rearranging is allowed** → the *order* of letters is irrelevant; only the *set* of letters matters. **(2) Every word has distinct letters** → that set is exactly the identity of the word — nothing is lost by throwing order away. So represent each word as the **set of letters it contains**. Since there are only 26 lowercase letters, that set is a **26-bit bitmask** — one integer per word. Now "add exactly one new letter" becomes "flip on exactly one bit," and its inverse — "remove exactly one letter" — is "flip *off* one bit." A target (mask `T`) is obtainable **iff** turning off one of its set bits lands on a mask that's in the start set.
- **Pattern trigger:** **"order doesn't matter + small fixed alphabet + distinct elements"** → **bitmask as a set**, and **"does a matching thing exist?"** → **hash set membership**. The transferable move: when rearrangement is free and letters are unique, stop thinking *strings* and start thinking *sets of bits*.

---

## ① Brute Force

For every target, scan every start word: it qualifies if the start has exactly one fewer letter and all its letters live in the target.

```python
def wordCount_brute(startWords, targetWords):
    count = 0
    for t in targetWords:
        tset = set(t)
        for s in startWords:
            # add exactly one new letter → start is one shorter and a subset
            if len(s) + 1 == len(t) and set(s) <= tset:
                count += 1
                break          # this target is obtainable; stop scanning
    return count
```

**Why it's the natural first attempt:** it's a direct translation of the rules — "one shorter, all letters contained." It reads cleanly and passes the tiny example.

**Why it's not enough:** it re-scans all of `startWords` for *every* target. With both arrays at 50k and rebuilding `set(s)` inside the inner loop, you're looking at ~`10¹⁰` character comparisons. It's not wrong — it's the version that goes green on the example and then hits Time Limit Exceeded on the big test.

**Complexity:** Time `O(|target| · |start| · L)` where `L ≤ 26`, Space `O(L)` per set.

---

## ② Optimised Solution

Turn every word into a **26-bit mask** (bit `i` on = letter `i` present). Put all start masks in a hash **set**. For each target mask `T`, try removing each of its set bits — `T ^ (1 << b)` — and ask if that mask is a start. One hit means obtainable.

```python
def wordCount(startWords, targetWords):
    def mask(word):
        m = 0
        for ch in word:
            m |= 1 << (ord(ch) - ord('a'))   # switch on this letter's bit
        return m

    starts = {mask(w) for w in startWords}    # O(1) membership on start masks

    count = 0
    for w in targetWords:
        t = mask(w)
        for ch in w:                          # try removing each letter of the target
            b = 1 << (ord(ch) - ord('a'))
            if (t ^ b) in starts:             # removing this letter yields a start word?
                count += 1
                break                         # obtainable — stop, don't double-count
    return count
```

**Walk the example** `startWords = ["ant","act","tack"]`, `targetWords = ["tack","act","acti"]`:

First, the start masks (bit per letter, `a`=bit 0 … `z`=bit 25):

| Word | Letters | Mask (which bits) |
|---|---|---|
| `ant` | a, n, t | {a, n, t} |
| `act` | a, c, t | {a, c, t} |
| `tack` | t, a, c, k | {a, c, t, k} |

`starts = { {a,n,t}, {a,c,t}, {a,c,t,k} }`. Now each target:

| Target | Mask `T` | Remove each letter → check `T ^ bit` | Hit? | Count |
|---|---|---|---|---|
| `tack` | {a,c,t,k} | −a→{c,t,k}, −c→{a,t,k}, −t→{a,c,k}, **−k→{a,c,t}** ✓ in starts | yes (`act`) | 1 |
| `act` | {a,c,t} | −a→{c,t}, −c→{a,t}, −t→{a,c} — none in starts | no | 1 |
| `acti` | {a,c,t,i} | −a→{c,t,i}, −c→{a,t,i}, −t→{a,c,i}, **−i→{a,c,t}** ✓ in starts | yes (`act`) | 2 |

Answer: **2**. ✅

**Why it's correct:** "add exactly one new letter, then rearrange" means the target's letter-set equals the start's letter-set plus one letter the start didn't have. Because rearranging is free, order is irrelevant — the mask captures everything. Because letters are distinct, the mask loses no information. So the operation is exactly *"set one bit that was off."* Its inverse is *"clear one bit that's on,"* which is precisely `T ^ (1 << b)` for each set bit `b` of `T`. If any of those `T`-minus-one-bit masks is a start mask, a valid start word exists; if none is, no start word can reach `T`. The `break` counts each target at most once.

**Complexity:** Time `O((|start| + |target|) · L)` to build masks + `O(|target| · L)` for the removals — `O((|start| + |target|) · 26)` overall. Space `O(|start|)` for the set.

---

## ③ Space Optimization

**Already optimal — and here's why.** You have to remember *something* about every start word to answer targets, and the leanest possible memory of a start word is its single-integer mask. The set holds up to `|start|` of those integers, so `O(|start|)` isn't overhead you can trim — it *is* the lookup table the algorithm queries. Each individual word already collapsed from a string to **one 32-bit int**, which is as compressed as a 26-letter set gets.

```python
# No leaner variant: we must store one mask per start word to answer queries in O(1).
# Each word is already a single int (26 bits), and the set is the query structure itself.
# You could sort the masks and binary-search instead of hashing — still O(|start|) space,
# and O(log) per query instead of O(1). No asymptotic memory win exists.
```

**Complexity:** Time `O((|start| + |target|) · 26)`, Space `O(|start|)`.

> Say it out loud: *"Space is O(|start|) and that's the floor — I need one mask per start word to make lookups O(1), and a mask is already the most compact form of a distinct-letter word. There's no rolling trick; the set of masks is the algorithm."*

---

## Java (for Java interviewers)

```java
public int wordCount(String[] startWords, String[] targetWords) {
    Set<Integer> starts = new HashSet<>();
    for (String w : startWords) {
        int m = 0;
        for (char ch : w.toCharArray()) m |= 1 << (ch - 'a');  // switch on the bit
        starts.add(m);
    }

    int count = 0;
    for (String w : targetWords) {
        int t = 0;
        for (char ch : w.toCharArray()) t |= 1 << (ch - 'a');
        for (char ch : w.toCharArray()) {                       // try removing each letter
            if (starts.contains(t ^ (1 << (ch - 'a')))) {       // yields a start word?
                count++;
                break;                                          // obtainable — stop
            }
        }
    }
    return count;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (pairwise subset check) | O(\|target\| · \|start\| · 26) | O(26) |
| Optimised (bitmask + hash set) | O((\|start\| + \|target\|) · 26) | O(\|start\|) |
| Space-optimised | — (none exists) | O(\|start\|) — the mask set *is* the algorithm |

---

## Say it out loud (interview narration)

> *"The brute force is: for each target, scan every start word and check if it's one letter short and a subset. That's `|target|·|start|` — 50k times 50k, it'll time out. So here's my leap: rearranging is allowed, which means order doesn't matter, and every word has distinct letters, which means a word is fully described by its **set of letters**. Twenty-six lowercase letters → I encode each word as a 26-bit integer. I dump all start masks into a hash set. Then adding one new letter is 'set one bit'; so a target is reachable iff clearing one of its set bits — `T XOR (1<<b)` — lands on a start mask. One hash lookup per set bit. That drops it to `O((|start|+|target|)·26)` time, `O(|start|)` space, and the space is the floor because I need one mask per start word to keep lookups constant."*

Before coding, ask the clarifying question that proves you caught the key premise: *"Every word has all-distinct letters, right? — that's what lets me treat a word as a bitset instead of a multiset."* Naming that assumption out loud is exactly the General Cognitive Ability signal Google rewards.

## Related / follow-ups
- **Number of Wonderful Substrings (LC 1915)** — parity bitmask over a fixed alphabet; same "letters → bits" collapse.
- **Find the Difference (LC 389) / Single Number (LC 136)** — XOR to isolate exactly one added/odd element.
- **Maximum Product of Word Lengths (LC 318)** — 26-bit masks + bitwise AND to test disjoint letter sets.
- **Group Anagrams (LC 49)** — the sibling idea when letters *can* repeat: sort or count instead of a plain bitmask.
