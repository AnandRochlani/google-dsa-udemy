# <Problem Title>

> **LeetCode:** <#number. Name> · **Difficulty:** 🟢/🟡/🔴 · **Pattern:** <Pattern> · **Google frequency:** ⭐ (high) / medium

---

## Problem

<Plain-English restatement of the problem. Inputs, outputs, constraints. One worked example: input → output.>

**Example:** `input` → `output` *(one line of why)*

**Constraints that matter:** <the constraint that decides the target complexity, e.g. n up to 10^5 → O(n²) is too slow>

---

## 🧠 Intuition — how you'd actually arrive at this

> This is the heart of the file. Walk the *thought process*, not just the answer.

- **First instinct:** what's the most obvious thing a person tries? (This becomes the brute force.)
- **Where it hurts:** what work is being repeated / wasted? Point at the exact inefficiency.
- **The leap:** what observation removes that waste? *(e.g. "the array is sorted, so I don't need to re-scan" / "I've seen this value before, so store it" / "I only care about the top K, not the full order".)*
- **Pattern trigger:** which signal in the problem maps to which pattern — the transferable lesson.

---

## ① Brute Force

<One sentence describing the naive approach.>

```python
# brute force
```

**Why it's the natural first attempt:** <...>
**Why it's not enough:** <the timeout / the wasted work>
**Complexity:** Time `O(...)`, Space `O(...)`.

---

## ② Optimised Solution

<How the intuition above turns into a better approach. Name the pattern and the key move.>

```python
# optimised
```

**Walk one example** step by step so the mechanism is concrete.

**Why it's correct:** <the invariant / why we never miss a valid answer>
**Complexity:** Time `O(...)`, Space `O(...)`.

---

## ③ Space Optimization

<If the optimised solution uses extra memory, can we cut it? in-place, rolling variables, two pointers instead of a copy, 1-D DP instead of 2-D, etc.>

```python
# space-optimised (if applicable)
```

**Complexity:** Time `O(...)`, Space `O(...)`.

> If space is already optimal: **say so and explain why.** "Already O(1) — only two indices, nothing grows with the input." Naming the absence is as strong as finding the trick.

---

## Java (optional, for Java interviewers)

```java
// optimised solution in Java
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force | O(...) | O(...) |
| Optimised | O(...) | O(...) |
| Space-optimised | O(...) | O(...) |

---

## Say it out loud (interview narration)

> One paragraph: how you'd narrate brute-force → optimise → space to the interviewer.

## Related / follow-ups
- <near-twin problems that use the same pattern>
