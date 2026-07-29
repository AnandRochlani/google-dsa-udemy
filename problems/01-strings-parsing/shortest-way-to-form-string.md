# Shortest Way to Form String

> **LeetCode:** 1055. Shortest Way to Form String · **Difficulty:** 🟡 Medium · **Pattern:** Greedy / Two Pointers · **Google frequency:** ⭐ high

---

## Problem

You're given two strings, `source` and `target`. A **subsequence** of `source` is any string you get by deleting zero or more characters from `source` without reordering the rest. You want to build `target` by **concatenating** subsequences of `source`. Return the **minimum number** of such subsequences you need, or `-1` if it's impossible.

**Example:** `source = "abc"`, `target = "abcbc"` → `2` — take `"abc"` then `"bc"`, both subsequences of `"abc"`, and glued together they spell `"abcbc"`.

**Constraints that matter:** `source` and `target` are up to `~1000` lowercase letters, so an `O(|source| · |target|)` scan is comfortably fine — but there's a cleaner near-linear version worth knowing. The two facts that shape everything: (1) if `target` contains any character that never appears in `source`, the answer is instantly `-1` — no amount of concatenation invents a new letter; (2) every subsequence you take can be as long as you can greedily stretch it, so **taking the longest possible bite each pass is never wrong.**

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "I need to cover `target` using pieces of `source`. Let me match `target` left to right, and every time I run out of `source`, I grab a fresh copy of it." That instinct is exactly right — the only question is *how much* of `target` one copy of `source` can absorb.
- **Where it hurts:** the worry is greed. "If I gobble as many `target` characters as I can with this one pass of `source`, could I regret it later and wish I'd stopped earlier?" With subsequence matching the answer is **no** — and seeing *why* is the whole problem.
- **The leap:** picture one pointer `j` sitting on `target`, and sweep `source` left to right once. Every time a `source` character equals `target[j]`, consume it — advance `j`. One full sweep of `source` = one subsequence used. The key insight: **a later subsequence can never reach further into `target` than an earlier greedy one could have.** Advancing `j` as far as possible now leaves the *most* room for the passes that follow. Greedy is optimal because subsequences don't interfere — each character you match only helps.
- **Pattern trigger:** **"cover one string using repeated left-to-right passes of another"** → **greedy two-pointer**. The transferable move: when matching is monotonic (you only ever move forward), *take the longest bite every time* and count the bites. No backtracking, no DP over choices.

---

## ① Brute Force

Match `target` with a pointer `j`. Repeatedly sweep the whole `source` from the left; each sweep advances `j` past every character it can match. Each sweep costs one subsequence. Stop when `j` reaches the end of `target` (success) — or when a full sweep of `source` advances `j` by **zero** (stuck → impossible).

```python
def shortestWay_brute(source: str, target: str) -> int:
    # Fast reject: any char in target that source lacks makes it impossible.
    if set(target) - set(source):
        return -1

    count = 0
    j = 0                       # pointer into target
    n = len(target)
    while j < n:
        prev = j                # remember where this sweep started
        # one left-to-right sweep of source = one subsequence
        for ch in source:
            if j < n and ch == target[j]:
                j += 1          # greedily consume this target char
        count += 1
        if j == prev:           # a whole sweep matched nothing → stuck
            return -1
    return count
```

**Why it's the natural first attempt:** it's literally the definition in code — "keep laying down copies of `source` until `target` is covered." You can explain it to the interviewer in one breath.

**Why it's not enough:** it's actually *good enough* for the given limits — but each subsequence re-scans all of `source`, so the cost is `O(|source| · answer)`, and in the worst case `answer ≈ |target|`, giving `O(|source| · |target|)`. When `source` is long and each pass only picks up one or two characters, you re-walk the entire `source` for almost nothing. That's the wasted work an interviewer will poke at.

**Complexity:** Time `O(|source| · |target|)` worst case, Space `O(1)` (the two sets are `O(26)`).

---

## ② Optimised Solution

Keep the greedy idea — but stop re-scanning `source`. Precompute a jump table: for every position `i` in `source` and every letter `c`, store **the next index `≥ i` where `c` appears** (or `n = len(source)` meaning "not found from here on"). Now matching one `target` character is a single lookup instead of a scan, and each subsequence pass jumps straight from letter to letter.

```python
def shortestWay(source: str, target: str) -> int:
    if set(target) - set(source):
        return -1

    n = len(source)
    # nxt[i][c] = smallest index k >= i with source[k] == c, else n ("not found")
    nxt = [[n] * 26 for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        nxt[i] = nxt[i + 1][:]              # inherit the "further right" answers
        nxt[i][ord(source[i]) - 97] = i     # this position is the nearest for its own char

    count = 1                               # we've started our first subsequence
    src = 0                                 # current cursor inside source
    for ch in target:
        c = ord(ch) - 97
        if nxt[src][c] == n:                # can't finish this char in the current pass
            count += 1                      # start a fresh subsequence
            src = nxt[0][c] + 1             # match this char from the top of source
        else:
            src = nxt[src][c] + 1           # consume it, move just past it
    return count
```

**Walk one example** — `source = "abc"`, `target = "abcbc"`. The jump table (indices `a,b,c` = the columns; `n = 3`):

| `i` | source[i] | next `a` | next `b` | next `c` |
|---|---|---|---|---|
| 0 | a | 0 | 1 | 2 |
| 1 | b | 3 | 1 | 2 |
| 2 | c | 3 | 3 | 2 |
| 3 | — | 3 | 3 | 3 |

Now sweep `target = "abcbc"` with `count = 1`, `src = 0`:

| target char | `nxt[src][c]` | action | new `src` | `count` |
|---|---|---|---|---|
| a | `nxt[0][a] = 0` | consume | 1 | 1 |
| b | `nxt[1][b] = 1` | consume | 2 | 1 |
| c | `nxt[2][c] = 2` | consume | 3 | 1 |
| b | `nxt[3][b] = 3 = n` | **new pass**, match from top: `nxt[0][b]=1` | 2 | **2** |
| c | `nxt[2][c] = 2` | consume | 3 | 2 |

Answer: **2** — exactly `"abc"` + `"bc"`. And try `source="xyz"`, `target="xzyxz"` by hand the same way: pass 1 grabs `x,z`, pass 2 grabs `y`, pass 3 grabs `x,z` → **3**.

**Why it's correct:** the greedy invariant is that after processing each `target` character, `src` sits at the **earliest** possible position in `source` that still leaves us able to match everything matched so far. Earliest cursor = most `source` remaining for the current pass = we only ever open a new subsequence when the current one *genuinely* can't continue (`nxt[src][c] == n`). You can never do better than "extend the current piece as far as it physically goes," so the count of pieces is minimal. The `set` pre-check guarantees `nxt[0][c]` is never `n` after a reset, so the reset is always safe.

**Complexity:** Time `O((|source| + |target|) · 26)` — building the table is `O(|source| · 26)`, matching is `O(|target|)` lookups. Space `O(|source| · 26)` for the table.

---

## ③ Space Optimization

The two versions trade space against time, so pick by what the constraints demand.

- The **brute-force two-pointer** is already `O(1)` auxiliary space — it holds only two indices and a counter, nothing that grows with the input (the character sets are a fixed `O(26)`). For `|source|, |target| ≤ 1000` this is the version I'd write in the room: dead simple, impossible to get subtly wrong, and fast enough.
- The **`nxt` table** buys speed by spending `O(|source| · 26)` memory. You reach for it only when `source` is large *and* you're doing many queries (e.g., the same `source` against many `targets`) — then the table is built once and amortized.

```python
# Space-optimal version = the brute-force two-pointer itself.
# Two indices + a counter → O(1) auxiliary. Nothing scales with input length.
def shortestWay_min_space(source: str, target: str) -> int:
    if set(target) - set(source):
        return -1
    count, j, n = 0, 0, len(target)
    while j < n:
        prev = j
        for ch in source:
            if j < n and ch == target[j]:
                j += 1
        count += 1
        if j == prev:
            return -1
    return count
```

**Complexity:** Time `O(|source| · |target|)`, Space `O(1)` auxiliary.

> Say it out loud: *"There's a genuine time-vs-space fork here. The two-pointer sweep is O(1) space; the next-array is O(|source|·26) space but shaves the matching down to near-linear. At n ≤ 1000 I'd ship the O(1) one for clarity, and mention the table as the scale-up."* Naming the trade-off — instead of defaulting to one — is the strong-hire move.

---

## Java (for Java interviewers)

```java
public int shortestWay(String source, String target) {
    // Fast reject: any target char missing from source → impossible.
    boolean[] inSource = new boolean[26];
    for (char ch : source.toCharArray()) inSource[ch - 'a'] = true;
    for (char ch : target.toCharArray())
        if (!inSource[ch - 'a']) return -1;

    int n = source.length();
    // nxt[i][c] = next index >= i where char c appears in source, else n.
    int[][] nxt = new int[n + 1][26];
    java.util.Arrays.fill(nxt[n], n);
    for (int i = n - 1; i >= 0; i--) {
        nxt[i] = nxt[i + 1].clone();          // inherit answers to the right
        nxt[i][source.charAt(i) - 'a'] = i;   // this index is nearest for its own char
    }

    int count = 1, src = 0;                   // one subsequence started, cursor at 0
    for (char ch : target.toCharArray()) {
        int c = ch - 'a';
        if (nxt[src][c] == n) {               // can't continue this pass
            count++;                          // open a fresh subsequence
            src = nxt[0][c] + 1;              // match from the top of source
        } else {
            src = nxt[src][c] + 1;            // consume, step just past it
        }
    }
    return count;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (greedy two-pointer, re-sweep) | O(\|source\| · \|target\|) | O(1) |
| Optimised (next-index jump table) | O((\|source\| + \|target\|) · 26) | O(\|source\| · 26) |
| Space-optimised (= the two-pointer) | O(\|source\| · \|target\|) | O(1) |

---

## Say it out loud (interview narration)

> *"First a clarifying check: characters are lowercase letters, and I can reuse `source` as many times as I want, right? Good. My very first move is a feasibility test — if `target` has any letter `source` lacks, it's `-1` immediately. Then it's a greedy two-pointer: I walk `target` with one pointer, and I sweep `source` left to right, consuming target characters as they match. Each full sweep of `source` is one subsequence, so I count the sweeps. Greedy is safe because extending the current piece as far as it goes never hurts a later piece — subsequences don't compete. That's O(|source|·|target|) time, O(1) space. If `source` were huge or reused across many targets, I'd precompute a next-index table so each match is a single lookup — that's O((|source|+|target|)·26) time for O(|source|·26) space. At these limits I'd ship the simple O(1) one and mention the table as the scale-up."*

## Related / follow-ups
- **Is Subsequence (LC 392)** — the atom this problem is built from: does one string appear as a subsequence of another? (And its "many queries" follow-up is exactly the `nxt` table.)
- **Number of Matching Subsequences (LC 792)** — count how many words are subsequences of `s`; same next-pointer / bucketing toolkit.
- **Shortest Common Supersequence (LC 1092)** — the DP cousin when you can *interleave* rather than concatenate whole passes.
- **Longest Common Subsequence (LC 1143)** — the DP baseline for "subsequence matching" reasoning.
