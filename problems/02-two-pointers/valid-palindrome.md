# Valid Palindrome

> **LeetCode:** 125. Valid Palindrome · **Difficulty:** 🟢 Easy · **Pattern:** Two Pointers · **Google frequency:** ⭐ high

---

## Problem

Given a string `s`, return `True` if it reads the same forwards and backwards **after** you (a) drop everything that isn't a letter or digit, and (b) lowercase the rest. Otherwise return `False`.

**Example:** `s = "A man, a plan, a canal: Panama"` → `True` *(cleaned up it's `"amanaplanacanalpanama"`, which mirrors itself).*
`s = "race a car"` → `False` *(cleaned it's `"raceacar"` — `r…r`, `a…a`, then `c` vs `e` breaks).*

**Constraints that matter:** `s` can be up to ~2×10⁵ characters. So an O(n) scan is fine, but building a reversed *copy* costs O(n) extra memory — and the whole point of this problem is to show you can do it in O(1) space.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** "A palindrome reads the same reversed. So clean the string, reverse it, compare." That works and it's honest — write it first. It's the brute force.
- **Where it hurts:** you built a **second full string** (the cleaned version) and often a **third** (its reverse). That's two extra O(n) allocations to answer a yes/no question. You're also comparing the whole thing when the *first mismatch* already settles it.
- **The leap:** you don't need a reversed copy to compare front-to-back. Put one pointer at the **start**, one at the **end**, and walk them toward each other. A palindrome is exactly the statement "the character `i` steps from the front equals the character `i` steps from the back." Skip non-alphanumerics as you go, and the moment two compared characters differ, you can bail immediately.
- **Pattern trigger:** **compare a sequence against its own reverse / symmetry from both ends** → **Two Pointers** from opposite ends. Any "is it a mirror?" question is a two-pointer question.

---

## ① Brute Force

Filter to lowercase alphanumerics, then check the cleaned string against its reverse.

```python
def is_palindrome_brute(s):
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]
```

**Why it's the natural first attempt:** it's the literal definition of a palindrome — "same as its reverse" — typed straight out.

**Why it's not enough:** `cleaned` is a new O(n) list and `cleaned[::-1]` is *another* O(n) list. You allocate two arrays and scan the whole thing even when character 1 already disagrees. Correct, but wasteful on memory.

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ② Optimised Solution

Two pointers from both ends. Skip junk characters, compare, converge.

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        # skip non-alphanumerics from the left
        while left < right and not s[left].isalnum():
            left += 1
        # skip non-alphanumerics from the right
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

**Walk the example** `"A man, a plan..."` — start `left=0 ('A')`, `right=last ('a')`:

| left (char) | right (char) | compare | action |
|---|---|---|---|
| 0 (`A`) | 29 (`a`) | `a == a` | move both in |
| 1 (` `) | 28 (`m`) | left is space | skip left++ |
| 2 (`m`) | 28 (`m`) | `m == m` | move both in |
| ... | ... | keep matching | ... |
| meet in middle | | never mismatched | **return True** ✅ |

For `"race a car"`: pointers eventually line up `c` (from `...car`) against `e` (from `race...`) → `c != e` → **return False** on the spot.

**Why it's correct:** the invariant is "everything already passed (outside `left..right`) is a confirmed mirror." Skipping non-alphanumerics honors the "letters and digits only" rule without materializing a cleaned string. If we reach `left >= right` with no mismatch, every symmetric pair matched → palindrome.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## ③ Space Optimization

Already O(1) space — and that's the whole upgrade over brute force. The two-pointer version never builds the cleaned string or its reverse; it just carries **two integer indices** and reads `s` in place. Nothing grows with the input.

> Say it out loud: *"I don't need a reversed copy — two pointers from both ends compare in place, so I drop from O(n) space to O(1)."*

Naming that you eliminated the extra allocation is the senior signal here. The brute force wasn't *wrong*, it was *memory-hungry*, and you fixed exactly that.

---

## Java (for Java interviewers)

```java
public boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        while (left < right && !Character.isLetterOrDigit(s.charAt(left))) left++;
        while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;
        if (Character.toLowerCase(s.charAt(left)) != Character.toLowerCase(s.charAt(right)))
            return false;
        left++;
        right--;
    }
    return true;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (clean + reverse) | O(n) | O(n) |
| Optimised (two pointers) | O(n) | O(1) |
| Space-optimised | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"Simplest version: strip out punctuation, lowercase, and compare the string to its reverse — O(n) time but O(n) space for the copies. I can skip the copies: put a pointer at each end, skip anything that isn't a letter or digit, and compare inward. First mismatch means it's not a palindrome; if they cross cleanly, it is. Same O(n) time, but now O(1) space because I only carry two indices."*

## Related / follow-ups
- **Pair with Target Sum / Two Sum II** (two pointers converging from both ends)
- **Valid Palindrome II** (allowed to delete at most one character)
- **Reverse String** (in-place two-pointer swap)
- **Palindromic Substrings** (expand around center — pointers moving *outward*)
