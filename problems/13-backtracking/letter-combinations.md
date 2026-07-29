# Letter Combinations of a Phone Number

> **LeetCode:** 17. Letter Combinations of a Phone Number · **Difficulty:** 🟡 Medium · **Pattern:** Subsets & Backtracking · **Google frequency:** ⭐ high

---

## Problem

Given a string `digits` containing digits `2`–`9`, return **all possible letter combinations** the number could spell, using the classic phone keypad mapping (`2`→`abc`, `3`→`def`, ..., `9`→`wxyz`). Return them in any order. If `digits` is empty, return an empty list.

**Example:** `digits = "23"` → `["ad","ae","af","bd","be","bf","cd","ce","cf"]` *(each of `abc` paired with each of `def` → 3 × 3 = 9 strings).*

**Constraints that matter:** `0 ≤ digits.length ≤ 4`, each digit is `2`–`9`. With up to 4 digits and up to 4 letters each (`7` and `9` map to 4 letters), the output is at most `4⁴ = 256` strings. The **output is exponential in the number of digits** — `∏ len(letters[d])` — which is inherent: you're asked for *every* combination.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For the first digit, try each of its letters; for each of those, try each letter of the second digit; and so on." That's a nested product — one loop per digit. When the number of loops depends on the *input length*, you can't hand-write them, so you recurse: this is the **Cartesian product**, and backtracking builds it naturally.

- **The decision tree mental model:** level `i` of the tree corresponds to digit `i`. At that level you branch once per letter that digit maps to. A **path from root to a leaf at depth `len(digits)`** spells one combination. Every leaf is an answer; internal nodes are partial strings.

- **The difference from Subsets/Permutations:** there's no `start` index and no `used` set. The branching set at each level is fixed by *which digit* you're on. You advance strictly by *position* (`index`), and at each position you iterate over that digit's letters.

- **The backtracking skeleton — same rhythm:** **CHOOSE** a letter for the current digit (append to `path`), **RECURSE** to the next digit (`index + 1`), then **UN-CHOOSE** (pop the letter) to try the next letter for this digit. When `index == len(digits)`, the `path` is a full combination — record it.

- **No real pruning here:** every branch reaches a valid leaf (any letter choice is legal), so there's nothing to prune. This problem is the *pure enumeration* member of the family — it shows the skeleton with the pruning muscle relaxed.

- **Pattern trigger:** **"generate all combinations from a per-position set of choices"** (Cartesian product) → backtracking that advances by index and loops over each position's options.

---

## ① Brute Force

The "iterative product" framing: build the result set by repeatedly appending each next digit's letters to every string so far. (Equivalent to `itertools.product`.)

```python
def letter_combinations_iter(digits):
    if not digits:
        return []
    mapping = {'2':'abc','3':'def','4':'ghi','5':'jkl',
               '6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
    result = ['']
    for d in digits:
        result = [prefix + ch for prefix in result for ch in mapping[d]]
    return result
```

**Why it's the natural first attempt:** it directly mirrors "combine every string-so-far with every letter of the next digit," and it's correct and compact.

**Why we look further:** it rebuilds a full list of prefix strings at every step (lots of intermediate string copies), and it doesn't showcase the recursive skeleton the interviewer is usually probing for. Backtracking uses one mutable buffer and only materializes a string at the leaves.

**Complexity:** Time `O(4ⁿ · n)` where `n = len(digits)` (up to `4ⁿ` combinations, each length `n`), Space `O(4ⁿ · n)` output plus intermediate lists.

---

## ② Optimised Solution

Recursive backtracking with a single character buffer, materialized only at leaves.

```python
def letter_combinations(digits):
    if not digits:
        return []
    mapping = {'2':'abc','3':'def','4':'ghi','5':'jkl',
               '6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
    result = []
    path = []

    def backtrack(index):
        if index == len(digits):              # leaf: one full combination
            result.append(''.join(path))      # materialize the string
            return
        for ch in mapping[digits[index]]:     # options for THIS digit
            path.append(ch)                   # CHOOSE
            backtrack(index + 1)              # RECURSE to next digit
            path.pop()                        # UN-CHOOSE

    backtrack(0)
    return result
```

**Walk part of the decision tree** for `digits = "23"` (`2`→`abc`, `3`→`def`):

```
backtrack(0), path=[]
  choose 'a' -> path=['a']
    backtrack(1)
      choose 'd' -> "ad"  record; pop
      choose 'e' -> "ae"  record; pop
      choose 'f' -> "af"  record; pop
    pop 'a'
  choose 'b' -> path=['b']  -> "bd","be","bf"
  choose 'c' -> path=['c']  -> "cd","ce","cf"
```

Each `path.append(ch)` / `path.pop()` pair lets one buffer serve every branch: after finishing all of `a`'s children we pop `a` and push `b`.

**Why it's correct:** the recursion visits digits left to right; at each it tries *every* mapped letter, so no combination is skipped, and because each digit contributes exactly one letter per path, every leaf has length `len(digits)` — a complete, valid combination. No duplicates because each path is a distinct sequence of choices.

**Complexity:** Time `O(4ⁿ · n)` — up to `4ⁿ` leaves, each an `O(n)` join. Space `O(n)` auxiliary.

---

## ③ Space Optimization

The output holds up to `4ⁿ` strings of length `n` → `O(4ⁿ · n)`, **inherent** (it's the answer).

**Output vs auxiliary space:** the backtracking version keeps only one `path` buffer (length ≤ `n`) plus recursion depth ≤ `n` → **auxiliary space `O(n)`**. That's already optimal — you can't do better than storing the current partial string plus the call stack.

Contrast with the iterative product version, which holds a full *frontier* of partial strings (up to `4ⁿ⁻¹` of them) in memory at once — that's `O(4ⁿ · n)` *working* space, not just output. So backtracking is strictly leaner on auxiliary memory. Say it: *"The iterative product keeps a whole layer of partial strings alive; my recursion keeps just one buffer and the O(n) call stack."*

---

## Java (for Java interviewers)

```java
private static final String[] MAP = {
    "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
};

public List<String> letterCombinations(String digits) {
    List<String> result = new ArrayList<>();
    if (digits == null || digits.isEmpty()) return result;
    backtrack(digits, 0, new StringBuilder(), result);
    return result;
}

private void backtrack(String digits, int index, StringBuilder path, List<String> result) {
    if (index == digits.length()) {
        result.add(path.toString());                  // materialize at leaf
        return;
    }
    String letters = MAP[digits.charAt(index) - '0'];
    for (char ch : letters.toCharArray()) {
        path.append(ch);                              // CHOOSE
        backtrack(digits, index + 1, path, result);   // RECURSE
        path.deleteCharAt(path.length() - 1);         // UN-CHOOSE
    }
}
```

---

## Complexity Summary

| Approach | Time | Space (aux) | Space (output) |
|---|---|---|---|
| Iterative product | O(4ⁿ · n) | O(4ⁿ · n) frontier | O(4ⁿ · n) |
| Backtracking | O(4ⁿ · n) | O(n) | O(4ⁿ · n) |

*(n = number of digits; 4 is the max letters per digit.)*

---

## Say it out loud (interview narration)

> *"This is a Cartesian product: each digit contributes one letter, so the total is the product of the letter-counts — exponential in the number of digits, which is inherent. I'll backtrack, advancing by digit index. At each digit I loop over its letters: append one, recurse to the next digit, then pop it and try the next. When the index reaches the end I join the buffer into a string and record it. No pruning is needed since every choice is valid. Time is O(4ⁿ·n) dominated by the output; auxiliary space is just O(n) — one buffer and the call stack — which is leaner than building a whole frontier of partial strings iteratively."*

## Related / follow-ups
- **Subsets** (LC 78 — same choose/recurse/un-choose, but `start`-indexed)
- **Generate Parentheses** (LC 22 — per-position choices with a validity prune)
- **Combinations** (LC 77 — fixed-size selection)
- **Word Search** (LC 79 — backtracking over a grid)
