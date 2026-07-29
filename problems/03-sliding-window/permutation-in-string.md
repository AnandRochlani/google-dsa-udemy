# Permutation in String

> **LeetCode:** 567. Permutation in String · **Difficulty:** 🟡 Medium · **Pattern:** Sliding Window · **Google frequency:** medium

---

## Problem

Given two strings `s1` and `s2`, return `True` if `s2` contains a **permutation of `s1`** as a substring — i.e. some contiguous window of `s2` is an anagram of `s1`.

**Example:** `s1 = "ab"`, `s2 = "eidbaooo"` → `True` *(the substring `"ba"` is a permutation of `"ab"`).* For `s1 = "ab"`, `s2 = "eidboaoo"` → `False` (no window equals a rearrangement of `"ab"`).

**Constraints that matter:** lengths up to ~10⁴, lowercase English letters only. A permutation of `s1` has **exactly `len(s1)` characters**, so we only ever look at windows of `s2` of that **fixed size**. Two strings are permutations of each other **iff their character frequency counts are identical** — that's the whole engine.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "A permutation of `s1` is any string with the same letters in the same quantities. So slide a window of length `len(s1)` across `s2`, and for each window check: does it have the exact same character counts as `s1`?" That's the brute force skeleton, and the check is the expensive part.
- **Where it hurts:** the window size is fixed at `m = len(s1)`. Building a fresh frequency count for each of the ~`n` windows costs `O(m)` each → `O(n·m)`. And neighbouring windows differ by only **one character out and one character in** — yet brute force recounts all `m` from scratch. Classic overlap waste.
- **The leap (the sliding part):** keep one **running frequency count of the current window** and update it incrementally — when the window slides one step, **decrement the count of the char that left** and **increment the char that entered**. Then compare to `s1`'s count. Two updates instead of `m`.
- **The leap (the comparison part):** comparing two 26-length arrays each step is `O(26)` — fine, but we can do better. Track a single number `matches` = how many of the 26 letters currently have **equal** counts in the window and in `s1`. When `matches == 26`, the window *is* a permutation. Each slide only touches two letters, so we only re-check those two — `O(1)` per step.
- **Pattern trigger:** **"find a window that's an anagram / permutation" + fixed window size** → **fixed-size Sliding Window + frequency-count match.** The tell is that the target length is known and constant.

---

## ① Brute Force

For each window of length `m = len(s1)`, rebuild its frequency count and compare to `s1`'s.

```python
from collections import Counter

def check_inclusion_brute(s1, s2):
    m, n = len(s1), len(s2)
    if m > n:
        return False
    need = Counter(s1)
    for start in range(n - m + 1):
        window = Counter(s2[start:start + m])   # rebuild count each time
        if window == need:
            return True
    return False
```

**Why it's the natural first attempt:** it's the definition made literal — every fixed-size window, check if its letter counts match `s1`'s.

**Why it's not enough:** slicing and counting each window is `O(m)`, done for ~`n` windows → `O(n·m)`. Consecutive windows overlap in `m−1` characters that get recounted from scratch. Slow when both strings are large.

**Complexity:** Time `O(n·m)`, Space `O(Σ)` (Σ = 26).

---

## ② Optimised Solution

One fixed-size window with an incrementally-updated count and a `matches` counter of how many letters already agree with `s1`.

```python
def check_inclusion(s1, s2):
    m, n = len(s1), len(s2)
    if m > n:
        return False

    need = [0] * 26
    window = [0] * 26
    for ch in s1:
        need[ord(ch) - ord("a")] += 1

    matches = 0
    for i in range(26):
        if need[i] == window[i]:      # both zero initially → they agree
            matches += 1

    for right in range(n):
        # add the entering character
        r = ord(s2[right]) - ord("a")
        if window[r] == need[r]:
            matches -= 1              # was equal, about to break
        window[r] += 1
        if window[r] == need[r]:
            matches += 1              # became equal

        # remove the leaving character once window exceeds size m
        if right >= m:
            l = ord(s2[right - m]) - ord("a")
            if window[l] == need[l]:
                matches -= 1
            window[l] -= 1
            if window[l] == need[l]:
                matches += 1

        if matches == 26:
            return True
    return False
```

**Walk the example** `s1 = "ab"`, `s2 = "eidbaooo"` (`m = 2`). `need = {a:1, b:1}`. We look at windows of size 2 as `right` advances:

| right (ch) | window contents | counts vs need | all 26 match? |
|---|---|---|---|
| 1 (i) | `"ei"` | a:0 b:0 → both short | no |
| 2 (d) | `"id"` | still no a/b | no |
| 3 (b) | `"db"` | b:1 ✓ but a:0 | no |
| 4 (a) | `"ba"` | a:1 ✓ b:1 ✓ | **yes → return True** ✅ |

**Why it's correct:** the window always holds exactly `m` consecutive characters of `s2` (we start removing the left char once `right >= m`). `window` is kept as the true frequency count of that window via one increment and one decrement per slide. `matches` counts letters whose window-count equals need-count; it's updated only for the two touched letters, using the "was it equal before / is it equal after" bookkeeping. When all 26 letters agree, every count matches exactly, so the window is a permutation of `s1`.

**Complexity:** Time `O(n)` (Σ = 26 setup is constant, then O(1) per character), Space `O(Σ) = O(1)`.

---

## ③ Space Optimization

Already optimal — **and here's why.** Two fixed 26-length arrays (`need`, `window`) plus a few scalars: `O(26) = O(1)` space, independent of input length. You fundamentally need per-letter counts to compare frequencies, and there are only 26 letters.

> A simpler-to-write variant drops `matches` and instead compares the two arrays (`window == need`) each step — that's still `O(n·26) = O(n)` time and the same `O(1)` space, just with a bigger constant. Mention it as the "readable but slightly slower" version; the `matches` counter is the tightening.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## Java (for Java interviewers)

```java
public boolean checkInclusion(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    if (m > n) return false;

    int[] need = new int[26], window = new int[26];
    for (char c : s1.toCharArray()) need[c - 'a']++;

    int matches = 0;
    for (int i = 0; i < 26; i++) if (need[i] == window[i]) matches++;

    for (int right = 0; right < n; right++) {
        int r = s2.charAt(right) - 'a';
        if (window[r] == need[r]) matches--;
        window[r]++;
        if (window[r] == need[r]) matches++;

        if (right >= m) {
            int l = s2.charAt(right - m) - 'a';
            if (window[l] == need[l]) matches--;
            window[l]--;
            if (window[l] == need[l]) matches++;
        }
        if (matches == 26) return true;
    }
    return false;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n·m) | O(Σ) = O(1) |
| Optimised (window + matches counter) | O(n) | O(Σ) = O(1) |
| Window + array compare each step | O(n·Σ) = O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"A permutation of s1 has exactly s1's letter counts and exactly s1's length, so I only look at fixed-size windows of length len(s1). Brute force recounts each window from scratch — O(n·m). Instead I keep one running count and slide: decrement the char leaving, increment the char entering. To avoid comparing 26 counts each step, I track a single 'matches' number — how many letters already agree with s1 — updating only the two touched letters per slide. When matches hits 26, the window is an anagram. That's O(n) time and O(1) space since the alphabet is fixed at 26."*

## Related / follow-ups
- **Find All Anagrams in a String** (LC 438 — same machinery, collect *all* start indices instead of returning on the first)
- **Longest Repeating Character Replacement** (LC 424 — window + frequency, different condition)
- **Minimum Window Substring** (LC 76 — variable window with need/have counts)
- **Group Anagrams** (LC 49 — frequency signatures as hash keys)
