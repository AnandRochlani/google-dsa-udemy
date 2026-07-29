# Minimum Window Substring

> **LeetCode:** 76. Minimum Window Substring · **Difficulty:** 🔴 Hard · **Pattern:** Sliding Window · **Google frequency:** ⭐ high

---

## Problem

Given strings `s` and `t`, return the **shortest substring of `s`** that contains **every character of `t`, including duplicates**. If no such window exists, return `""`. The answer is guaranteed unique when it exists.

**Example:** `s = "ADOBECODEBANC"`, `t = "ABC"` → `"BANC"` *(it contains A, B, and C, and no shorter window of `s` does).*

**Constraints that matter:** `|s|` up to ~10⁵ → we need `O(|s|)` (or `O(|s| + |t|)`). `t` can have **repeats** (e.g. `t = "AABC"` needs *two* A's), so this is about matching **counts**, not just presence. This is the canonical *variable-size window with need/have counts* problem — the template that unlocks a whole family.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Generate every substring of `s`, and for each one check whether it contains all of `t`'s characters (with the right multiplicities). Keep the shortest that passes." That's the brute force — and it's `O(n²)` substrings times an `O(n)` check.
- **Where it hurts:** enormous overlap. Checking substring `[i..j]` and then `[i..j+1]` re-scans almost the same characters. You're recomputing "does this window cover `t`?" from scratch every time.
- **The leap — a dynamic window that grows to become valid, then shrinks to get minimal:**
  - **`need`**: a count of how many of each character `t` requires. **`required`** = number of *distinct* characters we must satisfy.
  - Move `right` to **expand** the window, updating a `window` count. Each time a character's window-count reaches its `need`, we've fully satisfied one required character → bump a `formed` counter.
  - When `formed == required`, the window is **valid** (covers all of `t`). Now **contract** from the `left` as far as possible while it *stays* valid, recording the smallest valid window as we go. The moment removing a character would break coverage, stop shrinking and go back to expanding.
- **Why grow-then-shrink is the right shape:** expanding fixes "not enough characters yet"; shrinking fixes "more than needed / wasted length." Every character enters once (via `right`) and leaves once (via `left`), so despite the nested loop it's linear.
- **Pattern trigger:** **"smallest / shortest window that *covers* a target multiset"** → **dynamic Sliding Window with need/have (`formed`/`required`) counts.** This is *the* template; memorise its shape.

---

## ① Brute Force

Try every substring; for each, check whether it covers all of `t`'s characters with multiplicity.

```python
from collections import Counter

def min_window_brute(s, t):
    if not t or not s:
        return ""
    need = Counter(t)
    n = len(s)
    best = ""
    for i in range(n):
        for j in range(i, n):
            window = Counter(s[i:j + 1])
            # window covers t if every needed char count is met
            if all(window[c] >= need[c] for c in need):
                if best == "" or (j - i + 1) < len(best):
                    best = s[i:j + 1]
                break        # extending this start only gets longer
    return best
```

**Why it's the natural first attempt:** it's the definition made literal — check every window for coverage, keep the shortest.

**Why it's not enough:** `O(n²)` substrings, and each coverage check is `O(n)` (or `O(|t|)` amortised) — building `Counter` objects repeatedly over overlapping ranges. Overall around `O(n²)` or worse → far too slow at `n = 10⁵`.

**Complexity:** Time `O(n²·Σ)` in the worst case, Space `O(Σ)`.

---

## ② Optimised Solution

One dynamic window. Expand `right` until valid, contract `left` while it stays valid, tracking the minimum.

```python
from collections import Counter

def min_window(s, t):
    if not s or not t:
        return ""

    need = Counter(t)
    required = len(need)          # distinct chars we must satisfy
    window = {}
    formed = 0                    # how many distinct chars are fully satisfied

    best_len = float("inf")
    best_left = 0
    left = 0

    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            formed += 1           # this character just became fully covered

        # contract while the window is valid
        while formed == required:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_left = left
            lch = s[left]
            window[lch] -= 1
            if lch in need and window[lch] < need[lch]:
                formed -= 1       # dropped below required → no longer valid
            left += 1

    return "" if best_len == float("inf") else s[best_left:best_left + best_len]
```

**Walk the example** `s = "ADOBECODEBANC"`, `t = "ABC"`. `need = {A:1, B:1, C:1}`, `required = 3`.

| right | ch | window covers ABC? (formed) | action | best so far |
|---|---|---|---|---|
| 5 | C | first time formed=3 at window `"ADOBEC"` | contract: drop A,D,O until invalid → `"OBEC"`? loses A → stop; window `"ADOBEC"` recorded | `"ADOBEC"` (len 6) |
| 10 | B | formed=3 again at `"CODEBA..."` region → window `"CODEBANC"`? | contract to `"BANC"`-ish, record shorter windows | shrinks toward `"BANC"` |
| 12 | C | formed=3 at window ending in `"BANC"` | contract: `"BANC"` is valid, dropping `B` loses B → stop | **`"BANC"`** (len 4) |

The shortest valid window found is `"BANC"`. ✅ *(The table compresses several steps; the mechanism is: every time `formed == required`, shrink from the left and record if smaller.)*

**Why it's correct:** `formed == required` holds **exactly when** every distinct character of `t` has its full required count inside the window — i.e. the window covers `t`. We only record a candidate while valid, and we shrink to the tightest valid window for each `right`, so across all `right` positions we consider every minimal-for-its-right window — the global minimum is among them. `formed` is maintained precisely: it rises when a character *reaches* its needed count and falls only when a character drops *below* it.

**Complexity:** Time `O(|s| + |t|)` — each character of `s` is added once by `right` and removed once by `left` (amortised O(1) per step); building `need` is `O(|t|)`. Space `O(Σ)` for the two count maps (bounded by the alphabet).

---

## ③ Space Optimization

Already essentially optimal. The `need` and `window` maps hold at most one entry per **distinct character**, so space is `O(min(|s|, Σ))` — bounded by the alphabet (≤ 128 for ASCII, ≤ 52 for mixed-case letters), effectively `O(1)` for a fixed alphabet. You genuinely can't drop the counts: matching multiplicities *requires* remembering how many of each character you need and have.

> **Micro-optimisation for large strings with a small `t`:** filter `s` down to only the indices whose characters appear in `t`, and slide over *that* shorter list. It doesn't change the asymptotic bound but can be much faster when `t`'s alphabet is tiny relative to `s`. Worth naming as a follow-up; the core algorithm is already `O(|s|)` time.

**Complexity:** Time `O(|s| + |t|)`, Space `O(min(|s|, Σ))`.

---

## Java (for Java interviewers)

```java
public String minWindow(String s, String t) {
    if (s.isEmpty() || t.isEmpty()) return "";

    int[] need = new int[128];
    int required = 0;
    for (char c : t.toCharArray()) {
        if (need[c]++ == 0) required++;   // new distinct char to satisfy
    }

    int[] window = new int[128];
    int formed = 0, left = 0;
    int bestLen = Integer.MAX_VALUE, bestLeft = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        window[c]++;
        if (need[c] > 0 && window[c] == need[c]) formed++;

        while (formed == required) {
            if (right - left + 1 < bestLen) {
                bestLen = right - left + 1;
                bestLeft = left;
            }
            char lc = s.charAt(left);
            window[lc]--;
            if (need[lc] > 0 && window[lc] < need[lc]) formed--;
            left++;
        }
    }
    return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestLeft, bestLeft + bestLen);
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n²·Σ) | O(Σ) |
| Optimised (dynamic window, need/have) | O(\|s\| + \|t\|) | O(min(\|s\|, Σ)) |

---

## Say it out loud (interview narration)

> *"Brute force checks every substring for coverage — O(n²), way too slow. Instead I use a dynamic window with need/have counts. I count what t requires, and 'required' is the number of distinct characters to satisfy. I expand right, and each time a character reaches its needed count I bump 'formed'. When formed equals required the window covers t, so I contract from the left as far as it stays valid, recording the smallest window. Every character enters once and leaves once, so it's linear — O(|s| + |t|) time, O(alphabet) space. This need/have template also solves Find All Anagrams and Permutation in String."*

## Related / follow-ups
- **Permutation in String** (LC 567) and **Find All Anagrams in a String** (LC 438) — same need/have machinery, fixed window
- **Longest Substring Without Repeating Characters** (LC 3 — dynamic window, shrink on a violation)
- **Substring with Concatenation of All Words** (LC 30 — window over word-sized chunks)
- **Minimum Size Subarray Sum** (LC 209 — grow/shrink on a numeric sum instead of counts)
