# Word Break

> **LeetCode:** 139. Word Break · **Difficulty:** 🟡 Medium · **Pattern:** Dynamic Programming (over string prefixes) · **Google frequency:** ⭐ high

---

## Problem

Given a string `s` and a dictionary `wordDict`, return `true` if `s` can be segmented into a **space-separated sequence of one or more dictionary words** (each word reusable any number of times).

**Example:** `s = "leetcode"`, `wordDict = ["leet", "code"]` → `true` (`"leet code"`).

**Example:** `s = "applepenapple"`, `wordDict = ["apple", "pen"]` → `true` (`"apple pen apple"`).

**Example:** `s = "catsandog"`, `wordDict = ["cats","dog","sand","and","cat"]` → `false`.

**Constraints that matter:** `1 ≤ s.length ≤ 300`, `wordDict.length ≤ 1000`. The naive "try every split point recursively" is exponential; DP over prefix boundaries is `O(n²)` (or `O(n² · L)` counting comparisons). Put the dictionary in a **set** for O(1) lookups.

---

## 🧠 Intuition — how you'd actually arrive at this

**(a) Find the decision at each step.** Segment from the front: pick a **first word** — some prefix `s[0:k]` that's in the dictionary — then recursively ask whether the **remainder** `s[k:]` can also be segmented.

> **canBreak(start)** = true if for some `end > start`, `s[start:end]` is in the dict AND `canBreak(end)` is true.

Base: `canBreak(len(s)) = True` (an empty remainder is trivially segmentable).

**(b) Notice overlapping subproblems.** Different first-word choices land on the same `start` index later — e.g. splitting `"aaaa"` many ways all bottleneck on the same suffixes. The recursion recomputes `canBreak(start)` for the same `start` exponentially. DP signal — the state is just a **single index** into the string.

**(c) Memoize on `start`** → only `n+1` distinct states.

**(d) Bottom-up table.** Define `dp[i]` = "can `s[:i]` (the first `i` chars) be fully segmented?" `dp[0] = True` (empty string). For each end `i`, look for a split point `j < i` where `dp[j]` is true **and** `s[j:i]` is a dictionary word:

> **dp[i] = OR over j in [0, i) of ( dp[j] AND s[j:i] in wordSet )**

Answer: `dp[n]`.

**(e) Space.** `dp` is a 1-D boolean array of size `n+1`, and `dp[i]` can depend on *any* earlier `dp[j]` (a word can be up to length `n`), so you can't collapse it to O(1) — `O(n)` is the floor. A real optimization: only try split lengths that match an actual dictionary word length, or only `j` such that `i - j ≤ maxWordLen`. That trims work without changing the O(n) space.

**State & recurrence (memorize this):**
- **State:** `dp[i]` = can the prefix `s[:i]` be segmented into dictionary words.
- **Recurrence:** `dp[i] = any(dp[j] and s[j:i] in wordSet for j in range(i))`.
- **Base:** `dp[0] = True`. **Answer:** `dp[n]`.

---

## ① Brute Force

Recurse from the front: try every prefix as the first word, recurse on the rest. No caching.

```python
def word_break_brute(s, wordDict):
    words = set(wordDict)

    def helper(start):
        if start == len(s):
            return True
        for end in range(start + 1, len(s) + 1):
            if s[start:end] in words and helper(end):
                return True
        return False

    return helper(0)
```

**Why it's the natural first attempt:** "peel off a valid first word, then solve the remainder the same way" — the direct recursive segmentation.

**Why it's not enough:** with strings like `"aaaaaaa…b"` and dict `["a","aa","aaa",…]`, the same suffix positions are re-explored through countless split combinations — exponential, ~`O(2ⁿ)`.

**Complexity:** Time `O(2ⁿ)`, Space `O(n)` (stack).

---

## ② Optimised Solution — bottom-up DP

`dp[i]` = prefix `s[:i]` is segmentable.

```python
def word_break(s, wordDict):
    words = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True                       # empty prefix
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break                  # one valid split is enough
    return dp[n]
```

**A small filled table** for `s = "leetcode"`, dict `{"leet", "code"}`:

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| prefix | "" | l | le | lee | leet | leetc | … | … | leetcode |
| dp[i] | T | F | F | F | T | F | F | F | **T** |

`dp[4] = True` because `dp[0]` is true and `s[0:4] = "leet"` is a word. `dp[8] = True` because `dp[4]` is true and `s[4:8] = "code"` is a word. Answer `dp[8] = True`. ✅

**Why it's correct:** `dp[i]` is true iff *some* boundary `j` splits the prefix into an already-segmentable part `s[:j]` and a single dictionary word `s[j:i]`. That covers every possible last word, so no valid segmentation is missed.

**Complexity:** Time `O(n²)` split points × `O(L)` substring/lookup = `O(n²·L)`, Space `O(n)` (plus the word set).

---

## ③ Space Optimization

**Honest answer: `dp` is already at the O(n) space floor — say so and explain.** `dp[i]` can depend on any `dp[j]` with `0 ≤ j < i`, because a dictionary word can be as long as the whole string. There's no fixed-size window to slide (unlike Climbing Stairs), so you can't reduce below `O(n)`.

> *"Space is O(n) and that's the floor — a word can span from position j all the way to i for any earlier j, so dp[i] may reference any previous entry. No constant-size rolling window applies."*

What you *can* optimize is **time**, by only checking split lengths that correspond to real word lengths (bound the inner loop by the max word length, or iterate over dictionary words at each `i`):

```python
def word_break(s, wordDict):
    words = set(wordDict)
    max_len = max((len(w) for w in words), default=0)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        # only look back as far as the longest word
        for j in range(max(0, i - max_len), i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[n]
```

**Complexity:** Time `O(n · max_len · L)`, Space `O(n)` (still the floor).

---

## Java (for Java interviewers)

```java
public boolean wordBreak(String s, List<String> wordDict) {
    Set<String> words = new HashSet<>(wordDict);
    int n = s.length();
    boolean[] dp = new boolean[n + 1];
    dp[0] = true;
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < i; j++) {
            if (dp[j] && words.contains(s.substring(j, i))) {
                dp[i] = true;
                break;
            }
        }
    }
    return dp[n];
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (recursion) | O(2ⁿ) | O(n) |
| Memoized (top-down) | O(n²·L) | O(n) |
| Tabulated (bottom-up) | O(n²·L) | O(n) |
| Time-optimised (bound by max word len) | O(n · maxLen · L) | O(n) — already the floor |

*(L = cost of a substring build + set lookup.)*

---

## Say it out loud (interview narration)

> *"I put the dictionary in a set, then define dp[i] = can the first i characters be segmented. dp[0] is true, and dp[i] is true if there's a split point j where dp[j] is true and s[j:i] is a word. Naive recursion re-explores the same suffixes exponentially, so this O(n²) DP with memoization is the fix. Space is O(n) and that's the floor — a word can reach back to any earlier boundary, so there's no constant-size window to roll."*

## Related / follow-ups
- **Word Break II** (return *all* segmentations — DP/memo that stores the actual sentences, backtracking)
- **Concatenated Words** (word breakable using *other* dictionary words)
- **Palindrome Partitioning** (same split-point DP, predicate is "is palindrome")
- **Trie**-backed lookups to speed the substring checks
