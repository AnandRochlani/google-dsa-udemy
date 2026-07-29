# Strings Differ by One Character

> **LeetCode:** 1554. Strings Differ by One Character · **Difficulty:** 🟡 Medium · **Pattern:** Hashing / Masking · **Google frequency:** ⭐ high

---

## Problem

You're given a list `dict` of strings that are **all the same length**. Return `true` if there exist **two** strings in the list that differ in **exactly one position** — same length (guaranteed), identical at every index except one, where they hold different characters. Otherwise return `false`.

"Differ by one character" means *positional*: `"abc"` and `"adc"` differ only at index 1 → yes. `"abc"` and `"cba"` differ at indices 0 and 2 → no. Anagrams don't count; only same-slot, single-slot differences do.

**Example:** `dict = ["abcd","acbd","aacd"]` → `true` — `"abcd"` vs `"aacd"` are identical except index 1 (`b` vs `a`).

**Example (false):** `dict = ["ab","cd","yz"]` → `false` — every pair differs at *both* positions.

**Constraints that matter:** up to `n = 10^5` strings, each of length up to `m`, and `n · m ≤ 6 · 10^4` in the original limits — but treat `n` and `m` as independently large for the interview. A pairwise `O(n² · m)` scan is the obvious answer and the one that times out. The whole game is getting the pair-finding *below* `n²`.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** compare every pair of strings, character by character, and count the mismatches. If any pair has a mismatch count of exactly 1, return true. Correct, dead simple — and `O(n²)` pairs, each costing `O(m)`. On `10^5` strings that's `10^{10}` character comparisons. Dead on arrival.
- **Where it hurts:** the `n²` is the wound. We're re-comparing the same strings against each other from scratch, learning nothing reusable between pairs. Comparing `A` to `B` teaches us nothing that helps compare `A` to `C`. Every pair is a fresh full scan.
- **The leap:** flip the question. Instead of *"which pairs differ by one?"* ask *"what do two strings that differ only at index `i` have in common?"* Answer: **everything except index `i`.** So if I take a string and **blank out** one position — replace it with a wildcard `*` — then any two strings that collapse to the **same** blanked-out form must be identical everywhere else and differ (or match) only at that blanked slot. Blank out each position in turn, and let a hash set do the "have I seen this shape before?" lookup in `O(1)`. That trades the `n²` pair loop for a single pass that *remembers*.
- **Pattern trigger:** **"find a near-duplicate under one allowed edit"** → **masking + hashing.** The transferable move: when you're hunting pairs that match *except* for one controlled difference, **erase the difference and hash the rest.** Two things that agree on the un-erased part land in the same bucket. You've seen the cousin of this in group-anagrams (sort/erase order, hash the rest) — same DNA, different mask.

---

## ① Brute Force

Compare every pair; count positional mismatches; return true the moment a pair hits exactly one.

```python
def differ_by_one_brute(dict):
    n = len(dict)
    for i in range(n):
        for j in range(i + 1, n):          # every unordered pair once
            diff = 0
            for a, b in zip(dict[i], dict[j]):
                if a != b:
                    diff += 1
                    if diff > 1:           # early exit: 2 mismatches → not our pair
                        break
            if diff == 1:
                return True
    return False
```

**Why it's the natural first attempt:** it's the literal reading of the problem — "are there two strings that differ by one char?" So check all twos.

**Why it's not enough:** `O(n²)` pairs is the killer. With `n = 10^5` you're looking at ~`5 · 10^9` pairs before you even touch the `O(m)` inner compare. It passes the tiny examples and times out on the real test. The wasted work is structural: nothing learned from pair `(i, j)` is reused for pair `(i, k)`.

**Complexity:** Time `O(n² · m)`, Space `O(1)` (beyond the input).

---

## ② Optimised Solution

**Mask one position at a time, hash the rest.** For each string, generate `m` "wildcard" keys — the string with position `i` replaced by `*`, for every `i`. If a wildcard key has been seen before, two different strings collapsed to the same shape → they match everywhere except that one slot → return true. Store keys in a set as you go.

```python
def differ_by_one(dict):
    seen = set()
    for word in dict:
        for i in range(len(word)):
            # blank out position i with a char that can't appear in the input
            key = word[:i] + '*' + word[i + 1:]
            if key in seen:
                return True          # someone else already collapsed to this shape
            seen.add(key)
    return False
```

*(`'*'` is safe because inputs are lowercase letters. If the alphabet could include `*`, use a tuple `(i, word[:i], word[i+1:])` or a sentinel outside the alphabet.)*

**Walk the example** `dict = ["abcd","acbd","aacd"]`:

| String | Wildcard keys generated | Any key already in `seen`? | Action |
|---|---|---|---|
| `abcd` | `*bcd`, `a*cd`, `ab*d`, `abc*` | no (set empty) | add all four |
| `acbd` | `*cbd`, `a*bd`, `ac*d`, `acb*` | no — none match the four above | add all four |
| `aacd` | `*acd`, **`a*cd`**, `aa*d`, `aac*` | **yes — `a*cd`** was left by `abcd` | **return `true`** |

`a*cd` is the shape of both `abcd` (blank index 1: `b→*`) and `aacd` (blank index 1: `a→*`). They share `a_cd` and differ only at index 1. ✅

**Why it's correct:** two strings differ by *exactly one* position **iff** blanking that one position makes them identical. The masking generates every possible "blank one slot" shape for every string, so if such a pair exists, both members will produce that shared wildcard key — and because we check-then-add in a single pass, the second one to arrive finds the first already in the set. We never miss a valid pair, and a collision on wildcard key `k` at slot `i` *guarantees* the two source strings agree on all `m−1` other slots (that's literally what `k` encodes). *(One caveat: if the list can contain exact duplicates, two identical strings also share every wildcard key — but they differ by **zero**, not one. LC 1554's data is distinct; if yours isn't, dedupe first or store the original string alongside the key and confirm it's actually different.)*

**Complexity:** Time `O(n · m²)` — `n · m` keys, and slicing each key costs `O(m)`. Space `O(n · m²)` in characters if you store the full sliced strings (`n · m` keys × length `m`). See ③ for how to knock both the slicing and the space down.

---

## ③ Space Optimization

The `O(m)`-per-key slicing is doing double duty as our time *and* space cost. Kill it with a **rolling / polynomial hash**: precompute the hash of each full string, then a single-slot wildcard hash is *arithmetic* — subtract the masked character's contribution — computed in `O(1)` instead of rebuilt in `O(m)`.

```python
def differ_by_one_hash(dict):
    MOD = (1 << 61) - 1                    # big prime → few collisions
    BASE = 131
    seen = set()

    for word in dict:
        m = len(word)
        # full polynomial hash of the word
        h = 0
        for ch in word:
            h = (h * BASE + (ord(ch) - 96)) % MOD   # 'a'..'z' → 1..26

        # powers of BASE, so we can subtract one position's contribution
        power = 1
        # position i contributes (char_i) * BASE^(m-1-i); walk right→left
        for i in range(m - 1, -1, -1):
            ch_val = ord(word[i]) - 96
            # hash of the word with position i "zeroed out" (its char removed)
            masked = (h - ch_val * power) % MOD
            key = (i, masked)                        # tag with the slot i
            if key in seen:
                return True
            seen.add(key)
            power = (power * BASE) % MOD
    return False
```

**Why tag the key with `i`?** Two strings only truly share a blank if they blanked the **same** position. `(i, masked)` bakes the slot into the key so a slot-2 blank can't accidentally match a slot-5 blank that happens to hash equal.

**The honest catch — and the interview-scoring move:** a hash *collision* means two different masked strings could produce the same `masked` value. So on a match, the strictly-correct version doesn't trust the hash alone — it **verifies** by comparing the two actual source strings at that slot before returning true. Store the original string with each key and confirm they differ by exactly one char. With a 61-bit prime the collision odds are astronomically low, but *saying* "I'd verify on a hash hit to be safe" is exactly the rigor Google's rubric rewards.

**Complexity:** Time `O(n · m)` (each string hashed once, then `O(1)` per slot), Space `O(n · m)` — `n · m` integer keys, each `O(1)` instead of an `O(m)` string.

---

## Java (for Java interviewers)

```java
public boolean differByOne(String[] dict) {
    Set<String> seen = new HashSet<>();
    for (String word : dict) {
        char[] chars = word.toCharArray();
        for (int i = 0; i < chars.length; i++) {
            char original = chars[i];
            chars[i] = '*';                 // blank position i in place
            String key = new String(chars);
            if (!seen.add(key)) {           // add returns false if already present
                return true;                // collision → differ by exactly one slot
            }
            chars[i] = original;            // restore for the next position
        }
    }
    return false;
}
```

*(Straightforward masking version. For the `O(n·m)` rolling-hash variant, store `Long` keys tagged with the slot index and verify equality on a hash hit — same idea as the Python `differ_by_one_hash`.)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (all pairs) | O(n² · m) | O(1) |
| Masking + set (string slices) | O(n · m²) | O(n · m²) chars |
| Masking + rolling hash (verify on hit) | O(n · m) | O(n · m) |

*(n = number of strings, m = string length.)*

---

## Say it out loud (interview narration)

> *"Brute force is compare-every-pair and count mismatches — `O(n²·m)`, which times out. So I'll flip it: two strings differ by exactly one position iff blanking that position makes them identical. For each string I generate `m` wildcard keys — the string with one slot replaced by `*` — and drop them in a hash set. The first time a wildcard key repeats, I've found two strings that collapse to the same shape, so they differ in only that one slot. That's one pass, `O(n·m²)` with plain slicing. If `m` is large I'd swap the slicing for a polynomial rolling hash so each masked key is `O(1)` arithmetic instead of an `O(m)` rebuild — that gets me to `O(n·m)` time and space. One honesty point: a rolling hash can collide, so on a match I'd verify the two actual strings differ by exactly one char before returning true."*

Before coding, ask the clarifying question that proves you read the spec: *"Differ by one means same length and one differing index, right — not anagrams or edit distance?"* That one question steers you away from the wrong pattern and is precisely the GCA signal Google scores.

## Related / follow-ups
- **Group Anagrams (LC 49)** — same "erase the noise, hash the rest" move; here you erase order instead of one slot.
- **Longest Word With All Prefixes / Implement Trie** — another "share a common shape" structure, tries instead of masks.
- **One Edit Distance (LC 161)** — the two-string version: differ by one *edit* (insert/delete/replace), a superset of this problem's replace-only case.
- **Repeated DNA Sequences (LC 187)** — rolling-hash a sliding window and detect repeats with a set — same hashing-for-duplicates reflex.
