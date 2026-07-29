# Generate Parentheses

> **LeetCode:** 22. Generate Parentheses · **Difficulty:** 🟡 Medium · **Pattern:** Subsets & Backtracking · **Google frequency:** ⭐ high

---

## Problem

Given `n` pairs of parentheses, generate **all combinations of well-formed (balanced) parentheses**. Return them in any order.

**Example:** `n = 3` → `["((()))","(()())","(())()","()(())","()()()"]` *(all 5 valid arrangements of 3 pairs).*

**Constraints that matter:** `1 ≤ n ≤ 8`. The count of valid strings is the **Catalan number** `C(n) = (2n)! / ((n+1)! · n!)` (for `n = 8`, that's `1430`). The **output is exponential** — inherent to "generate all valid combinations." The whole game is to **prune invalid branches early** so we never build a string that can't become balanced.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "A string of `2n` characters where each position is `(` or `)`. Generate all `2²ⁿ` of them and keep the balanced ones." That's the brute force — build every binary string, filter by validity.

- **Where it hurts:** most of those `2²ⁿ` strings are invalid, and we only find out *after* building the whole thing. Building `")..."` is pointless — it's dead from the first character. We're doing exponential work to throw most of it away.

- **The leap — prune with two counters:** track how many `(` (`open`) and `)` (`close`) we've placed. A partial string can still become valid **only if**:
  1. `open < n` — we may add another `(` (haven't used all our opens), and
  2. `close < open` — we may add a `)` (there's an unmatched `(` to close).
  These two rules mean we *never even create* an invalid prefix. Every leaf we reach at length `2n` is guaranteed balanced — **the pruning is so tight there's no final validity check at all.**

- **The decision tree mental model:** each node is a partial string with counts `(open, close)`. It branches at most two ways: add `(` (if `open < n`) or add `)` (if `close < open`). Leaves at depth `2n` are complete valid strings. Whole invalid subtrees are chopped off by the two conditions.

- **The backtracking skeleton — same rhythm:** **CHOOSE** a bracket (append), **RECURSE** with the updated count, then **UN-CHOOSE** (pop) to try the other bracket. The `open`/`close` counts are passed by value, so they auto-restore — but the shared `path` buffer still needs the explicit pop.

- **Pattern trigger:** **"generate all valid sequences under a structural rule"** → backtracking where the *prune condition encodes the rule* (here: balance). Contrast with Subsets (no rule) — the rule is what turns brute force into an efficient search.

---

## ① Brute Force

Generate **every** `2n`-length string of `(`/`)`, then filter with a validity check.

```python
def generate_brute(n):
    result = []
    path = []

    def valid(s):
        bal = 0
        for ch in s:
            bal += 1 if ch == '(' else -1
            if bal < 0:                       # a ')' with no matching '('
                return False
        return bal == 0

    def build(length):
        if length == 2 * n:
            if valid(path):                   # filter AFTER building
                result.append(''.join(path))
            return
        for ch in '()':
            path.append(ch)                   # CHOOSE (no constraint)
            build(length + 1)                 # RECURSE
            path.pop()                        # UN-CHOOSE
    build(0)
    return result
```

**Why it's the natural first attempt:** "list all bracket strings, keep the balanced ones" is the most literal reading.

**Why it's not enough:** it explores all `2²ⁿ` strings and validates each in `O(n)` → `O(2²ⁿ · n)`, even though only Catalan-many are valid. It builds `)(((...` fully before rejecting it. We can reject the instant a prefix goes invalid.

**Complexity:** Time `O(2²ⁿ · n)`, Space `O(n)` auxiliary + output.

---

## ② Optimised Solution

Carry `open` and `close` counts; only branch where the prefix can still become valid.

```python
def generate_parenthesis(n):
    result = []
    path = []

    def backtrack(open_count, close_count):
        if len(path) == 2 * n:                # leaf: guaranteed balanced
            result.append(''.join(path))
            return
        if open_count < n:                    # can we add '('?
            path.append('(')                  # CHOOSE
            backtrack(open_count + 1, close_count)   # RECURSE
            path.pop()                        # UN-CHOOSE
        if close_count < open_count:          # can we add ')'?
            path.append(')')                  # CHOOSE
            backtrack(open_count, close_count + 1)   # RECURSE
            path.pop()                        # UN-CHOOSE

    backtrack(0, 0)
    return result
```

**Walk part of the decision tree** for `n = 2` (need 2 pairs):

```
backtrack(0,0) path=""
  add '(' -> backtrack(1,0) path="("
    add '(' -> backtrack(2,0) path="(("
      open==n, so no more '('; close<open -> add ')' -> "(()"
        add ')' -> "(())"  LEAF record ✅
    close<open -> add ')' -> backtrack(1,1) path="()"
      add '(' -> backtrack(2,1) path="()("
        add ')' -> "()()"  LEAF record ✅
      close==open, no ')' 
  (close<open is false at root, so root never starts with ')')
```

Result for `n=2`: `["(())", "()()"]`. Notice the root never even *considers* starting with `)` — `close < open` is `0 < 0`, false. That whole invalid half of the tree is pruned before it exists.

**Why it's correct:** the two conditions are exactly the invariant of a balanced-prefix: never place more than `n` opens, never close more than you've opened. Any string reaching length `2n` under these rules has `open == close == n` and never dipped below zero balance → valid. And every valid string is reachable, since the conditions only forbid *impossible* extensions.

**Complexity:** Time `O(4ⁿ / √n)` (Catalan number × `O(n)` per string to build), Space `O(n)` auxiliary. Vastly fewer nodes than brute force.

---

## ③ Space Optimization

The output holds Catalan-many strings of length `2n` → inherent, that's the answer.

**Output vs auxiliary space:** we keep one `path` buffer (length ≤ `2n`) and the recursion stack (depth ≤ `2n`) → **auxiliary space `O(n)`**. Already optimal. The `open`/`close` counters are two integers passed by value — free.

There's nothing to trim: unlike Subsets where you *could* argue about copies, here the buffer is a single shared list mutated in place with choose/un-choose, and the counters ride along on the call stack. Say it: *"Auxiliary space is O(n) — one buffer plus the call stack — and the balance counters are just two ints on the stack. The exponential part is only the required output."*

---

## Java (for Java interviewers)

```java
public List<String> generateParenthesis(int n) {
    List<String> result = new ArrayList<>();
    backtrack(new StringBuilder(), 0, 0, n, result);
    return result;
}

private void backtrack(StringBuilder path, int open, int close, int n, List<String> result) {
    if (path.length() == 2 * n) {
        result.add(path.toString());                  // balanced leaf
        return;
    }
    if (open < n) {                                   // can add '('
        path.append('(');                             // CHOOSE
        backtrack(path, open + 1, close, n, result);  // RECURSE
        path.deleteCharAt(path.length() - 1);         // UN-CHOOSE
    }
    if (close < open) {                               // can add ')'
        path.append(')');                             // CHOOSE
        backtrack(path, open, close + 1, n, result);  // RECURSE
        path.deleteCharAt(path.length() - 1);         // UN-CHOOSE
    }
}
```

---

## Complexity Summary

| Approach | Time | Space (aux) | Space (output) |
|---|---|---|---|
| Brute force + filter | O(2²ⁿ · n) | O(n) | O(Catalan · n) |
| Pruned backtracking | O(4ⁿ / √n) | O(n) | O(Catalan · n) |

---

## Say it out loud (interview narration)

> *"Brute force builds all 2²ⁿ bracket strings and filters the balanced ones — wasteful, since most are invalid. Instead I backtrack while tracking two counts: opens placed and closes placed. I add a `(` only while opens are below n, and a `)` only while closes are below opens. Those two rules mean every prefix stays valid, so any string I reach at length 2n is balanced — no final check needed. Choose a bracket, recurse with the updated count, pop to try the other. Time drops from 2²ⁿ to Catalan-many; auxiliary space is O(n) for the buffer and stack, the two counters are free."*

## Related / follow-ups
- **Valid Parentheses** (LC 20 — *check* balance with a stack; the invariant behind the prune)
- **Letter Combinations** (LC 17 — per-position choices, but no validity prune)
- **Remove Invalid Parentheses** (LC 301 — backtracking + BFS pruning)
- **Different Ways to Add Parentheses** (LC 241 — divide & conquer on operators)
