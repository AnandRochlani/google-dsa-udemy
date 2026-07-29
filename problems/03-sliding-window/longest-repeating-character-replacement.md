# Longest Repeating Character Replacement

> **LeetCode:** 424. Longest Repeating Character Replacement · **Difficulty:** 🟡 Medium · **Pattern:** Sliding Window · **Google frequency:** medium

---

## Problem

You're given a string `s` (uppercase English letters) and an integer `k`. You may **change at most `k` characters** to any other uppercase letter. Return the length of the **longest substring that can be made of a single repeated character** after those changes.

**Example:** `s = "AABABBA"`, `k = 1` → `4` *(take `"ABAB"`... no — take `"AABA"` and change the one `B`, or the window `"ABBA"` and change one letter, giving a run of 4 identical characters).* Simpler: `s = "ABAB"`, `k = 2` → `4` (change both `A`s to `B`, or both `B`s to `A`).

**Constraints that matter:** `n` up to ~10⁵ → we need `O(n)`. Alphabet is fixed at 26 uppercase letters, which makes "count of each character in the window" cheap. The core quantity: **a window of length `L` is achievable if the characters we'd need to replace — everything except the most common letter — is `≤ k`.**

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For every substring, find its most frequent character. The rest are the ones I'd have to change. If that count of 'others' is `≤ k`, this substring is achievable — track the longest." Checking every substring is the brute force.
- **The key reframe:** For any window, the cheapest way to make it all one letter is to **keep the most frequent letter** and replace everyone else. So the number of replacements needed = `window_length − count_of_most_frequent_char`. The window is **valid** exactly when that value is `≤ k`.
- **Where brute force hurts:** you recompute character frequencies for every one of the `O(n²)` substrings from scratch — massive overlap between neighbouring windows, all recomputed.
- **The leap:** Use a **dynamic window** and keep a running **count array of the 26 letters currently inside it**. Grow `right`, update the count. If the window becomes invalid — `window_length − max_count > k` — **shrink from the left by one** (you slide rather than collapse). Track the best window length seen.
- **The clever bit (why we never shrink more than needed):** we only ever need the window to *grow or stay the same size*, because we're after the **maximum**. So instead of a `while` shrink loop, a single `if` that slides `left` forward by one keeps the window at its best-so-far size. We also don't bother recomputing `max_count` downward — a stale (possibly too-high) `max_count` can only make us *think* a window is valid when it's the same size as a genuinely valid earlier one, and since we only care about the maximum length, that never produces a wrong (too-long) answer. This is the subtle trick interviewers love to hear explained.
- **Pattern trigger:** **"longest window where (window size − dominant element count) ≤ budget"** → **dynamic Sliding Window + frequency count.**

---

## ① Brute Force

Check every substring; for each, count letters and test whether `len − maxfreq ≤ k`.

```python
def character_replacement_brute(s, k):
    n = len(s)
    best = 0
    for start in range(n):
        count = {}
        max_freq = 0
        for end in range(start, n):
            count[s[end]] = count.get(s[end], 0) + 1
            max_freq = max(max_freq, count[s[end]])
            length = end - start + 1
            if length - max_freq <= k:      # replacements needed fit budget
                best = max(best, length)
    return best
```

**Why it's the natural first attempt:** it directly encodes the definition — for each substring, "others = length − most common", check against `k`.

**Why it's not enough:** `n` starts × up to `n` extensions = `O(n²)`, and neighbouring windows recompute nearly identical frequency counts. At `n = 10⁵` that's ~10¹⁰ operations → **Time Limit Exceeded.**

**Complexity:** Time `O(n²)`, Space `O(Σ)` (Σ = 26).

---

## ② Optimised Solution

One dynamic window with a 26-length count array. Slide `left` forward whenever the window would need more than `k` replacements.

```python
def character_replacement(s, k):
    count = [0] * 26
    left = 0
    max_count = 0          # highest single-letter frequency seen in any window
    best = 0
    for right in range(len(s)):
        count[ord(s[right]) - ord("A")] += 1
        max_count = max(max_count, count[ord(s[right]) - ord("A")])
        # replacements needed = window_len - max_count; if > k, shrink by one
        if (right - left + 1) - max_count > k:
            count[ord(s[left]) - ord("A")] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
```

**Walk the example** `s = "AABABBA"`, `k = 1`:

| right (ch) | count (A,B) | max_count | window len | len − max_count | > k? shrink | best |
|---|---|---|---|---|---|---|
| 0 (A) | A1 | 1 | 1 | 0 | no | 1 |
| 1 (A) | A2 | 2 | 2 | 0 | no | 2 |
| 2 (B) | A2 B1 | 2 | 3 | 1 | no (≤1) | 3 |
| 3 (A) | A3 B1 | 3 | 4 | 1 | no | 4 |
| 4 (B) | A3 B2 | 3 | 5 | 2 | yes → drop `A` at 0, left=1 | 4 |
| 5 (B) | A2 B3 | 3 | 5 | 2 | yes → drop `A` at 1, left=2 | 4 |
| 6 (A) | A2... B3 (window `BABBA`→ slides) | 3 | 5 | 2 | yes → drop `B` at 2, left=3 | 4 |

Answer: `4`. ✅

**Why it's correct:** `best` only ever takes a window whose replacement cost `(len − max_count)` was `≤ k` at the moment we measured it — a genuinely achievable window. The window never shrinks below its best size (single `if`, not a loop), so once we've found a length-4 valid window, we only accept a longer one if a *truly* valid longer one appears — which requires `max_count` to actually rise. A stale-high `max_count` can't invent a longer valid window out of thin air; it can only fail to shrink for a *same-length* window, which doesn't change the maximum. So the returned `best` is exactly the longest achievable length.

**Complexity:** Time `O(n)` (one pass, O(1) per step — the count array is fixed size 26), Space `O(Σ) = O(26) = O(1)`.

---

## ③ Space Optimization

Already optimal — **and here's why.** The count array is a fixed 26 slots regardless of how long `s` is, so space is `O(1)` (constant). There's nothing to trim: you need per-letter counts to know the dominant character, and there are only 26 letters.

> If the alphabet were arbitrary Unicode you'd swap the array for a hash map, making space `O(min(n, Σ))` — but for this problem's fixed A–Z alphabet, the array is both simpler and strictly constant space.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## Java (for Java interviewers)

```java
public int characterReplacement(String s, int k) {
    int[] count = new int[26];
    int left = 0, maxCount = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        int idx = s.charAt(right) - 'A';
        count[idx]++;
        maxCount = Math.max(maxCount, count[idx]);
        if ((right - left + 1) - maxCount > k) {   // too many replacements
            count[s.charAt(left) - 'A']--;
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(n²) | O(Σ) = O(1) |
| Optimised (window + freq count) | O(n) | O(Σ) = O(1) |

---

## Say it out loud (interview narration)

> *"The trick is reframing: a window can become all-one-letter if the number of characters that aren't its most common letter — that's length minus the max frequency — is within k. Brute force checks every substring, O(n²). Instead I slide a window, keeping a count of the 26 letters and the max frequency. When length minus max-count exceeds k, I slide left forward by one. Because I only care about the longest window, I never shrink below my best size, and I don't need to decrement max-count — a stale value can't fabricate a longer valid window. One pass, O(n) time, and the count array is fixed at 26 so O(1) space."*

## Related / follow-ups
- **Longest Substring Without Repeating Characters** (LC 3 — window + last-seen map)
- **Max Consecutive Ones III** (LC 1004 — flip at most k zeros; same "budget of changes" idea)
- **Longest Substring with At Most K Distinct Characters** (LC 340)
- **Permutation in String** (LC 567 — fixed window + exact frequency match)
