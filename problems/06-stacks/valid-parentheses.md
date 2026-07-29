# Valid Parentheses

> **LeetCode:** 20. Valid Parentheses · **Difficulty:** 🟢 Easy · **Pattern:** Stacks · **Google frequency:** ⭐ high

---

## Problem

Given a string `s` containing just the characters `(`, `)`, `{`, `}`, `[` and `]`, decide whether the string is **valid**. Valid means: every open bracket is closed by the **same type** of bracket, and brackets are closed in the **correct order** (the most recently opened is the first one closed).

**Example:** `s = "([{}])"` → `true`. But `s = "([)]"` → `false` *(the `)` tries to close a `[`, wrong type / wrong order).*

**Constraints that matter:** `1 ≤ s.length ≤ 10⁴`, and the string contains only those six bracket characters. The length isn't what forces the technique here — the **nesting/ordering rule** is. You can't just count brackets; `"]["` has one of each and is still invalid.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Just count — same number of `(` as `)`, etc." That fails immediately on `")("`: equal counts, still invalid. So counting is dead; **order matters**.
- **Next instinct:** "Repeatedly find an adjacent matched pair like `()` or `{}`, delete it, and repeat until nothing's left." That actually *works* — `([{}])` → `([])` → `()` → `""` → valid. But each deletion re-scans the string, so it's O(n²), and it's fiddly to implement with string slicing.
- **Where it hurts:** The re-scanning repeats work. Notice *what* you're always looking for: a closing bracket right next to **the most recently opened, still-unclosed bracket**. "Most recently added, first to be resolved" is exactly Last-In-First-Out.
- **The leap:** Walk left to right. Push every opening bracket onto a **stack**. When you hit a closing bracket, the only thing it's allowed to close is whatever is on **top** of the stack. If the top is the matching opener, pop it and move on; otherwise it's invalid. At the end the stack must be empty.
- **Pattern trigger:** **"match things in nested / most-recent-first order"** → **Stack**. Balanced-brackets is the canonical example; the same shape appears in expression parsing, path simplification, and undo history.

---

## ① Brute Force

Repeatedly remove adjacent matched pairs until the string stops changing; valid iff it collapses to empty.

```python
def is_valid_brute(s):
    prev = None
    while prev != s:                 # keep going until nothing changes
        prev = s
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""
```

**Why it's the natural first attempt:** it mirrors how you'd cancel matched pairs by hand, and `str.replace` makes it a few lines.

**Why it's not enough:** each pass over the string removes at most a layer of pairs, and each `replace` rebuilds the whole string. In the worst case (deep nesting like `"(((…)))"`) that's O(n) passes of O(n) work → **O(n²)** time, plus O(n) new strings churned every pass.

**Complexity:** Time `O(n²)`, Space `O(n)`.

---

## ② Optimised Solution

Single pass with a stack. Push openers; on a closer, check the top.

```python
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}   # closer -> its opener
    stack = []
    for ch in s:
        if ch in pairs:                       # ch is a closing bracket
            # top must be the matching opener; if stack empty, use a
            # sentinel that can never match
            top = stack.pop() if stack else "#"
            if pairs[ch] != top:
                return False
        else:                                 # ch is an opening bracket
            stack.append(ch)
    return not stack                          # valid only if nothing left open
```

**Walk the example** `s = "([{}])"` — stack shown left (bottom) to right (top):

| char | action | stack after |
|---|---|---|
| `(` | opener → push | `[ (`  |
| `[` | opener → push | `[ ( [` |
| `{` | opener → push | `[ ( [ {` |
| `}` | closer → pop `{`, matches `{` ✅ | `[ ( [` |
| `]` | closer → pop `[`, matches `[` ✅ | `[ (` |
| `)` | closer → pop `(`, matches `(` ✅ | `[ ]` (empty) |

Stack is empty at the end → **`true`**. Contrast `"([)]"`: at the `)` the top is `[`, which doesn't match → **`false`** immediately.

**Why it's correct:** a closing bracket can only legally close the *most recently opened* unmatched bracket — precisely the stack top. Popping enforces both rules at once (right **type** via the `pairs` lookup, right **order** via LIFO). A leftover non-empty stack means some opener was never closed; hitting a closer on an empty stack means a closer had no opener. The sentinel `"#"` cleanly handles that empty case.

**Complexity:** Time `O(n)` — each character is pushed and popped at most once. Space `O(n)` for the stack.

---

## ③ Space Optimization

The O(n) stack is **inherent** here. In the worst case the input is all openers (`"((((("`) — you genuinely have to remember every one of them until its matching closer shows up, so there's no way to use less than O(n) space in the general case.

```python
# No meaningful space win for arbitrary bracket strings — the stack is required.
```

Two honest half-measures worth naming out loud:

- If the string used **only one** bracket type (just `(` and `)`), you could replace the stack with a single **counter** — increment on `(`, decrement on `)`, fail if it goes negative, and it must end at 0. That's O(1) space. The moment you have *three* types, a counter can't tell `[` from `{`, so you're back to the stack.
- The input string itself is O(n), so O(n) auxiliary space doesn't change the overall memory class.

> Say it plainly: *"With one bracket type I'd use an O(1) counter, but with three types I need the stack to remember which kind is open — that's O(n) and it's unavoidable."*

**Complexity:** Time `O(n)`, Space `O(n)` (or `O(1)` in the single-bracket-type special case).

---

## Java (for Java interviewers)

```java
public boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();   // ArrayDeque as a stack
    for (char c : s.toCharArray()) {
        if (c == '(') stack.push(')');
        else if (c == '[') stack.push(']');
        else if (c == '{') stack.push('}');
        // for a closer: it must equal what we expect on top
        else if (stack.isEmpty() || stack.pop() != c) return false;
    }
    return stack.isEmpty();
}
```

*(Neat trick: push the **expected closer** when you see an opener, so the closing check is a single equality.)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (repeated replace) | O(n²) | O(n) |
| Optimised (stack) | O(n) | O(n) |
| Single-bracket-type special case | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"Counting won't work because order matters — `)(` has equal counts but is invalid. The rule is that a closer must match the most recently opened bracket, which is a last-in-first-out relationship, so I'll use a stack. I push every opener; when I hit a closer I pop and check the top is the matching opener, failing fast on a mismatch or an empty stack. At the end the stack must be empty. That's one pass, O(n) time and O(n) space — and the space is inherent because a string of all openers must all be remembered."*

## Related / follow-ups
- **Min Stack** (LC 155) — augmenting a stack to answer O(1) min
- **Longest Valid Parentheses** (LC 32) — stack of indices for the longest balanced run
- **Simplify Path** (LC 71) — stack of path components
- **Remove All Adjacent Duplicates in String** (LC 1047) — same "cancel with the top" idea
- **Basic Calculator** (LC 224) — stack-based expression evaluation
