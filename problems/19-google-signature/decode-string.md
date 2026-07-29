# Decode String

> **LeetCode:** 394. Decode String · **Difficulty:** 🟡 Medium · **Pattern:** Stack · **Google frequency:** ⭐ high

---

## Problem

You're given an encoded string where a chunk in the form `k[encoded]` means "repeat `encoded` exactly `k` times." The brackets can **nest** — a repeated chunk can contain more repeated chunks. Decode it into the plain string. `k` is always a positive integer, and there are no stray digits outside the `k[...]` form.

**Example:** `3[a2[c]]` → `accaccacc` *(inner `2[c]` = `cc`, so `a2[c]` = `acc`, then `3[...]` repeats that → `accaccacc`).*

**Constraints that matter:** the string length is small (up to ~30 chars encoded), but the **decoded output can blow up** — nesting multiplies. `10[10[10[a]]]` is only 12 characters in but a thousand `a`s out. So the real cost is the size of the *output*, not the input, and you must build that output somewhere.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Scan left to right and expand each `k[...]` as I go." That feels fine until you hit a nested bracket. When you're standing at the outer `3[`, you don't yet know what the inside decodes to — there's another `2[c]` buried in there. You can't multiply by 3 until the inside is finished.
- **Where it hurts:** the moment you try to "expand as you go," you realize you have to **pause** the outer count, go finish the inner part first, then come back and apply the outer 3. That "pause the outer, finish the inner, resume" is the tell.
- **The leap:** *most-recently-opened bracket must be resolved first.* That's Last-In-First-Out — a **stack**. Every time you see `[`, you push what you've built so far plus the repeat count, and start a fresh buffer for the inside. When you see `]`, you pop and stitch: `previous_string + count × current_buffer`.
- **Pattern trigger:** **nested / bracketed structure that resolves innermost-first** → **Stack**. Same instinct as matching parentheses or evaluating nested expressions. When you catch yourself saying "I need to finish the inside before I can finish the outside," reach for a stack.

---

## ① Brute Force

Recursively decode: find a `k[...]`, recurse on its contents, expand, and splice it back into the string — repeat until no brackets remain.

```python
# brute force: rebuild the string via repeated scan-and-recurse
def decode_brute(s):
    def helper(i):
        # returns (decoded_string, next_index)
        result = []
        num = 0
        while i < len(s):
            c = s[i]
            if c.isdigit():
                num = num * 10 + int(c)
            elif c == '[':
                inner, i = helper(i + 1)   # decode the inside first
                result.append(inner * num)
                num = 0
            elif c == ']':
                return ''.join(result), i
            else:
                result.append(c)
            i += 1
        return ''.join(result), i

    return helper(0)[0]
```

**Why it's the natural first attempt:** it mirrors the definition literally — a `k[...]` *is* `k` copies of its decoded inside, so recursion reads like the spec.

**Why it's not enough:** honestly, it's *not* wrong and it's not even slow here — recursion is a perfectly good solution. The trap is the *other* brute force people try first: expanding the outer count before the inner is done ("expand as you go"), which forces re-scanning and re-expanding the same inner region once per outer copy, and loses the outer count while you chase the inner. The recursion above sidesteps that — but it hides the same LIFO idea inside the call stack. The iterative stack version makes that idea explicit and avoids deep recursion on pathological nesting.

**Complexity:** Time `O(output length)`, Space `O(output length + nesting depth)` (recursion frames).

---

## ② Optimised Solution

Walk the string once with an **explicit stack of `(previous_string, repeat_count)`**. Keep a running `current` buffer and a running `num`:

- **digit** → build the number: `num = num * 10 + int(c)` (handles multi-digit like `12[a]`).
- **`[`** → push `(current, num)` onto the stack, then reset `current = ""` and `num = 0`. You're stepping *inside* a new bracket.
- **`]`** → pop `(prev, k)`, and set `current = prev + k * current`. You just closed a bracket: repeat the inside `k` times and glue it after whatever came before.
- **letter** → append it to `current`.

```python
def decode_string(s):
    stack = []          # holds (previous_string, repeat_count)
    current = ""
    num = 0
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)      # multi-digit safe
        elif c == '[':
            stack.append((current, num)) # save context, then dive in
            current = ""
            num = 0
        elif c == ']':
            prev, k = stack.pop()
            current = prev + k * current # stitch inside back into outside
        else:
            current += c                 # ordinary letter
    return current
```

**Walk the example** `3[a2[c]]`:

| char | num | current | stack | note |
|---|---|---|---|---|
| `3` | 3 | `""` | `[]` | build count |
| `[` | 0 | `""` | `[("", 3)]` | push, reset |
| `a` | 0 | `"a"` | `[("", 3)]` | append letter |
| `2` | 2 | `"a"` | `[("", 3)]` | build count |
| `[` | 0 | `""` | `[("", 3), ("a", 2)]` | push, reset |
| `c` | 0 | `"c"` | `[("", 3), ("a", 2)]` | append letter |
| `]` | 0 | `"acc"` | `[("", 3)]` | pop `("a",2)` → `"a" + 2*"c"` |
| `]` | 0 | `"accaccacc"` | `[]` | pop `("", 3)` → `"" + 3*"acc"` |

Result: `accaccacc` ✅

**Why it's correct:** every `[` opens a scope; the stack remembers exactly what was built *before* that scope and how many times the scope should repeat. When the matching `]` arrives, the innermost (top of stack) context is the one we resolve — LIFO guarantees we always close the most-recent bracket first, which is precisely the nesting rule. Nothing is ever expanded before its inside is complete.

**Complexity:** Time `O(output length)`, Space `O(output length)`.

---

## ③ Space Optimization

**Already optimal — and it's worth saying why out loud.** The output itself can be exponentially larger than the input (`10[10[10[a]]]` → 1000 chars from 12), and the problem *demands* we return that full decoded string. So we must materialize `O(output length)` characters no matter what — that space is **inherent to the problem**, not waste we introduced.

What we *can* talk about is the **recursion-stack vs explicit-stack tradeoff**:

- The recursive brute force uses the **call stack**, whose depth equals the **nesting depth**. Deeply nested input (`1[1[1[...]]]`) can blow the recursion limit / stack.
- The iterative version uses an **explicit stack on the heap** of the same depth — no recursion-limit risk, and the intent (LIFO) is visible in the code.

> *"The output space is unavoidable — we're required to build the decoded string. Beyond that, I'd pick the iterative stack over recursion so deep nesting can't overflow the call stack."*

Naming that the O(output) space is *inherent* — not a flaw — is the strong signal here.

---

## Java (for Java interviewers)

```java
public String decodeString(String s) {
    Deque<String> strStack = new ArrayDeque<>();
    Deque<Integer> numStack = new ArrayDeque<>();
    StringBuilder current = new StringBuilder();
    int num = 0;
    for (char c : s.toCharArray()) {
        if (Character.isDigit(c)) {
            num = num * 10 + (c - '0');
        } else if (c == '[') {
            numStack.push(num);
            strStack.push(current.toString());
            current = new StringBuilder();
            num = 0;
        } else if (c == ']') {
            int k = numStack.pop();
            StringBuilder decoded = new StringBuilder(strStack.pop());
            for (int i = 0; i < k; i++) decoded.append(current);
            current = decoded;
        } else {
            current.append(c);
        }
    }
    return current.toString();
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (recursion) | O(output length) | O(output length + depth) |
| Optimised (explicit stack) | O(output length) | O(output length) |
| Space-optimised | O(output length) | O(output length) — inherent, output must be built |

---

## Say it out loud (interview narration)

> *"The moment I hit a nested bracket I realize I can't apply the outer count until the inside is decoded — I have to finish the innermost bracket first. That's last-in-first-out, so it's a stack. I keep a running string and a running number; on `[` I push the string-so-far and the count and reset, on `]` I pop and set current = previous + count × current, and letters just append. One pass, O(output length) time. Space is O(output length) too — but that's inherent, since the problem requires me to build the whole decoded string. I'd use an explicit stack over recursion so deep nesting can't overflow the call stack."*

## Related / follow-ups
- **Basic Calculator / Basic Calculator II** (stack to resolve nested expressions)
- **Valid Parentheses** (the canonical match-innermost-first stack)
- **Number of Atoms** (parse nested `k[...]`-style chemical formulas)
- **Flatten Nested List Iterator** (stack over nested structure)
