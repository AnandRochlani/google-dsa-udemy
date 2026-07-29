# Longest Substring Without Repeating Characters

> **LeetCode:** 3. Longest Substring Without Repeating Characters · **Difficulty:** 🟡 Medium · **Pattern:** Sliding Window · **Google frequency:** ⭐ high

---

## Problem

Given a string `s`, return the **length of the longest substring with no repeating characters**. A *substring* is contiguous (not a subsequence).

**Example:** `s = "abcabcbb"` → `3` *(the answer is `"abc"`; after that you always hit a repeat within 3).* For `s = "bbbbb"` → `1` (`"b"`). For `s = "pwwkew"` → `3` (`"wke"`).

**Constraints that matter:** `n` up to ~5·10⁴, characters from the full ASCII/Unicode range. `O(n²)` re-checking is borderline-to-slow; the clean target is `O(n)`. The key structural fact: the answer is a **window that must stay free of duplicates** — the moment a duplicate enters, the window is invalid.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For every starting index, extend to the right as far as I can while all characters stay unique — the moment I'd repeat a character, stop and record the length. Then try the next start." That's the brute force.
- **Where it hurts:** Suppose from start `0` you build `"abc"` and then hit the repeated `a` at index 3. Brute force now restarts at index 1 and rebuilds `"bca"` from scratch — re-scanning characters it *just* verified were unique. That overlapping re-check is the wasted work, and it's `O(n²)` (or worse if the uniqueness check itself is a scan).
- **The leap:** Keep a **dynamic window** `[left, right]` that is *always* duplicate-free, plus a **set (or map) of the characters currently inside it**. Advance `right` one char at a time. If the new char isn't in the window, great — extend and update the best length. If it *is* a duplicate, **shrink from the left**, removing characters until the duplicate is gone. Then continue. You never rebuild — you slide.
- **The upgrade (map instead of set):** with a plain set you shrink one char at a time. But if you store **the last index where each character was seen**, then on a duplicate you can **jump `left` directly** past the previous occurrence in one step, instead of walking it forward. Same O(n), fewer moves, cleaner code.
- **Pattern trigger:** **"longest substring where a condition holds" + the condition is about the window's contents** → **dynamic Sliding Window backed by a hash set/map.** The map answers "have I seen this char, and where?" in O(1).

---

## ① Brute Force

For every start, extend right while characters stay unique (tracked in a set).

```python
def length_of_longest_brute(s):
    n = len(s)
    best = 0
    for start in range(n):
        seen = set()
        for end in range(start, n):
            if s[end] in seen:
                break           # duplicate → this start is done
            seen.add(s[end])
            best = max(best, end - start + 1)
    return best
```

**Why it's the natural first attempt:** it's the literal "check every substring for uniqueness and keep the longest valid one."

**Why it's not enough:** the outer loop tries `n` starts, the inner loop can run up to `n`, and each new start rebuilds a `seen` set over characters the previous start already validated. That's `O(n²)` time (and `O(min(n, alphabet))` space per start). On tens of thousands of characters it's slow and wasteful.

**Complexity:** Time `O(n²)`, Space `O(min(n, Σ))` where Σ is the alphabet size.

---

## ② Optimised Solution

One dynamic window. Store each character's **most recent index**; when a duplicate appears *inside* the window, jump `left` past it.

```python
def length_of_longest(s):
    last_seen = {}          # char -> most recent index
    left = 0
    best = 0
    for right, ch in enumerate(s):
        # if ch was seen and its last position is inside the window,
        # move left just past that position
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

**Walk the example** `s = "abcabcbb"`:

| right (ch) | seen before & in window? | left after | window | best |
|---|---|---|---|---|
| 0 (a) | no | 0 | `a` | 1 |
| 1 (b) | no | 0 | `ab` | 2 |
| 2 (c) | no | 0 | `abc` | 3 |
| 3 (a) | yes (idx 0 ≥ 0) → left = 1 | 1 | `bca` | 3 |
| 4 (b) | yes (idx 1 ≥ 1) → left = 2 | 2 | `cab` | 3 |
| 5 (c) | yes (idx 2 ≥ 2) → left = 3 | 3 | `abc` | 3 |
| 6 (b) | yes (idx 4 ≥ 3) → left = 5 | 5 | `cb` | 3 |
| 7 (b) | yes (idx 6 ≥ 5) → left = 7 | 7 | `b` | 3 |

Answer: `3`. ✅

**Why it's correct:** the window `[left, right]` is invariantly duplicate-free. When `right` brings in a character last seen at index `p`, there are two cases: if `p < left` the earlier copy is already *outside* the window, so nothing to do; if `p ≥ left` the copy is *inside*, so moving `left` to `p + 1` evicts it (and only it) and restores uniqueness. We update `best` at every step, so we never miss the longest valid window. The `last_seen[ch] >= left` guard is what prevents `left` from ever moving *backwards*.

**Complexity:** Time `O(n)` (each character processed once, O(1) map ops), Space `O(min(n, Σ))` for the map.

---

## ③ Space Optimization

The map holds at most one entry per **distinct character**, so space is `O(min(n, Σ))` — bounded by the alphabet, not the string length. For an input restricted to lowercase English letters, that's `≤ 26`; for ASCII, `≤ 128`. In those cases it's effectively `O(1)`.

> You can swap the hash map for a **fixed-size array** indexed by character code (e.g. `int[128]` storing last-seen index, initialised to −1). Same asymptotic space but a tighter constant and faster lookups — a nice touch to mention when the alphabet is known and small. You genuinely can't drop below `O(Σ)`: you must remember where each distinct in-window character last appeared.

**Complexity:** Time `O(n)`, Space `O(min(n, Σ))`.

---

## Java (for Java interviewers)

```java
public int lengthOfLongestSubstring(String s) {
    int[] lastSeen = new int[128];      // ASCII; last index of each char
    java.util.Arrays.fill(lastSeen, -1);
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        char ch = s.charAt(right);
        if (lastSeen[ch] >= left) {
            left = lastSeen[ch] + 1;    // jump past the previous copy
        }
        lastSeen[ch] = right;
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(min(n, Σ)) |
| Optimised (window + last-seen map) | O(n) | O(min(n, Σ)) |
| Window + fixed array | O(n) | O(Σ) |

---

## Say it out loud (interview narration)

> *"Brute force checks every substring for uniqueness — O(n²) and it re-verifies characters it already saw. Instead I keep one duplicate-free window with two pointers and a map of each character's last index. As I move right, if the new char's last position is inside my window I jump left just past it — that evicts the duplicate in one move. Update the best length each step. Each char is touched once, so it's O(n) time, and the map is bounded by the alphabet, so O(min(n, Σ)) space — effectively O(1) for a fixed alphabet."*

## Related / follow-ups
- **Longest Substring with At Most K Distinct Characters** (LC 340 — window + count of distinct)
- **Longest Repeating Character Replacement** (LC 424 — window + most-frequent-char count)
- **Minimum Window Substring** (LC 76 — window + need/have counts)
- **Permutation in String** (LC 567 — fixed window + frequency match)
