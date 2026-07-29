# Longest Palindromic Substring

> **LeetCode:** 5. Longest Palindromic Substring · **Difficulty:** 🟡 Medium · **Pattern:** Expand Around Center (Two Pointers on strings) · **Google frequency:** ⭐ high

---

## Problem

Given a string `s`, return the **longest contiguous substring that reads the same forwards and backwards.** If several answers tie in length, returning any one of them is fine.

**Example:** `"babad"` → `"bab"` *(and `"aba"` is an equally valid answer — both are length 3).*

**Example:** `"cbbd"` → `"bb"` *(the only palindrome longer than one character).*

**Constraints that matter:** `n` can be up to ~1000. That's small enough that an `O(n²)` scan (~10⁶ operations) sails through, but the naive `O(n³)` (~10⁹) is right on the edge of too slow. So the target is `O(n²)` time — and, as we'll see, we can hit it with `O(1)` extra space.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "A palindrome is a property of a substring, so let me look at *every* substring, check if it's a palindrome, and keep the longest." There are `O(n²)` substrings and checking each one is `O(n)` — that's the brute force, and it's `O(n³)`.
- **Where it hurts:** the checking work is enormously redundant. To test whether `"abcba"` is a palindrome you compare the outer pair, then the inner pair — but you threw all of that away when you moved on to test `"abcb"`. You keep re-deriving facts you already knew about shorter palindromes sitting inside longer ones.
- **The leap:** stop thinking about *substrings* and start thinking about *centers*. Every palindrome has a middle. Stand on that middle and walk two pointers outward — as long as the characters on the left and right match, you're still inside a palindrome; the moment they differ (or you fall off the edge), you've found the largest palindrome for that center. You build outward from the answer instead of guessing substrings and verifying them.
- **The subtle bit:** a center isn't always a single character. `"aba"` has a character in the middle (odd length), but `"bb"` has its center *between* two characters (even length). So there are **two kinds of centers**, and `2n − 1` of them total: `n` single-character centers plus `n − 1` between-character gaps. Check them all.
- **Pattern trigger:** **"longest palindrome / palindromic property + a string"** → **Expand Around Center** (two pointers walking *outward* instead of inward). Burn in the `2n − 1` count — forgetting the even-length centers is the classic bug.

---

## ① Brute Force

Try every substring; check each one for the palindrome property; track the longest that passes.

```python
def longest_palindrome_brute(s):
    def is_palindrome(lo, hi):
        while lo < hi:
            if s[lo] != s[hi]:
                return False
            lo += 1
            hi -= 1
        return True

    best = ""
    n = len(s)
    for i in range(n):
        for j in range(i, n):
            if j - i + 1 > len(best) and is_palindrome(i, j):
                best = s[i:j + 1]
    return best
```

**Why it's the natural first attempt:** it's the literal reading of the problem — "find the longest substring that is a palindrome," so enumerate substrings and test the property.

**Why it's not enough:** `O(n²)` substrings, each verified in `O(n)` → `O(n³)`. At `n = 1000` that's ~10⁹ comparisons, and you're re-checking inner pairs you already confirmed a hundred times. Wasteful.

**Complexity:** Time `O(n³)`, Space `O(1)`.

---

## ② Optimised Solution

Flip the direction: don't verify substrings, **grow** them. For each of the `2n − 1` centers, push two pointers outward while the characters match.

```python
def longest_palindrome(s):
    if not s:
        return ""

    start, end = 0, 0  # best palindrome found so far, as [start, end]

    def expand(left, right):
        # walk outward while it's still a palindrome; return the widest [l, r]
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1  # step back to the last valid pair

    for i in range(len(s)):
        l1, r1 = expand(i, i)        # odd-length center: single char i
        if r1 - l1 > end - start:
            start, end = l1, r1
        l2, r2 = expand(i, i + 1)    # even-length center: gap between i and i+1
        if r2 - l2 > end - start:
            start, end = l2, r2

    return s[start:end + 1]
```

**Walk the example** `"babad"`:

| center | expand from | grows to | palindrome | length |
|---|---|---|---|---|
| `i=0` odd (`b`) | (0,0) | (0,0) | `"b"` | 1 |
| `i=1` odd (`a`) | (1,1) → (0,2) | `s[0]==s[2]` (`b==b`) ✓, then off edge | `"bab"` | **3** |
| `i=1` even (`ba`) | (1,2) | `a != b` immediately | `"a"` | 1 |
| `i=2` odd (`b`) | (2,2) → (1,3) | `a==a` ✓ → (0,4) `b != d` ✗ | `"aba"` | 3 |
| … | … | nothing beats length 3 | | |

First palindrome of length 3 found is `"bab"` → that's our answer. *(If the scan had recorded `"aba"` first it would be equally correct.)*

**Why it's correct:** every palindrome is uniquely determined by its center, and we try **every** center — all `n` single-char centers and all `n − 1` gaps. For each center we expand to the maximal matching radius, so we never miss the longest palindrome anchored there. The overall longest must be anchored at *some* center, and we checked them all.

**Complexity:** Time `O(n²)` — `2n − 1` centers, each expanding up to `O(n)`. Space `O(1)`.

---

## ③ Space Optimization

Already optimal on space — **and that's worth saying out loud in the room.** Expand-around-center carries no auxiliary data structure at all: two integer pointers walking outward and four integers (`start`, `end`, `left`, `right`) tracking the best answer. Nothing grows with the input.

```python
# nothing to add — the optimised solution is already O(1) extra space.
```

> *"Expand-around-center is already O(1) extra space — I'm only holding a couple of indices, nothing scales with n. The DP table solution I could write instead would be O(n²) space, so this is strictly leaner."*

Naming the absence of a trick is itself a signal: you know *why* there's nothing left to cut, and you know the alternative you deliberately avoided.

---

## Java (for Java interviewers)

```java
public String longestPalindrome(String s) {
    if (s == null || s.isEmpty()) return "";
    int start = 0, end = 0;
    for (int i = 0; i < s.length(); i++) {
        int[] odd = expand(s, i, i);       // odd-length center
        if (odd[1] - odd[0] > end - start) { start = odd[0]; end = odd[1]; }
        int[] even = expand(s, i, i + 1);  // even-length center
        if (even[1] - even[0] > end - start) { start = even[0]; end = even[1]; }
    }
    return s.substring(start, end + 1);
}

private int[] expand(String s, int left, int right) {
    while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
        left--;
        right++;
    }
    return new int[]{left + 1, right - 1};  // step back to last valid pair
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (check every substring) | O(n³) | O(1) |
| Expand around center | O(n²) | O(1) |
| DP table | O(n²) | O(n²) |
| Manacher's | O(n) | O(n) |

---

## Say it out loud (interview narration)

> *"Brute force is every substring times an O(n) palindrome check — O(n³), and it re-verifies pairs it already confirmed. Instead of testing substrings, I'll grow them: every palindrome has a center, so I stand on each center and expand two pointers outward while the characters match. There are 2n−1 centers — n single characters for odd-length palindromes, and n−1 gaps between characters for even-length ones — and each expands up to O(n), so it's O(n²) time. And it's O(1) space, since I'm only carrying a few indices. If you want better than O(n²), the DP table is same time but O(n²) space, and Manacher's algorithm gets it down to true O(n) — but expand-around-center is the one I'd actually write here."*

## Related / follow-ups
- **Palindromic Substrings (LC 647)** — same expand-around-center, just *count* them instead of tracking the longest.
- **Longest Palindromic Subsequence (LC 516)** — subsequence, not substring → this is the classic 2-D DP (`O(n²)` space) they may push you toward.
- **Valid Palindrome (LC 125)** — two pointers walking *inward* to verify a single palindrome.
- **Manacher's algorithm** — the `O(n)` answer if the interviewer asks "can you beat O(n²)?"; transforms the string with separators and reuses mirror information so each center's radius is computed in amortized O(1).
