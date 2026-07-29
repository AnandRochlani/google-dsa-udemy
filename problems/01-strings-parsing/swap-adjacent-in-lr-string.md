# Swap Adjacent in LR String

> **LeetCode:** 777. Swap Adjacent in LR String · **Difficulty:** 🟡 Medium · **Pattern:** Two Pointers / Invariants · **Google frequency:** ⭐ high

---

## Problem

You're given two strings `start` and `end` of the **same length**, each made of only `'L'`, `'R'`, and `'X'`. In one move you may replace an occurrence of `"XL"` with `"LX"` — which slides an `L` one step to the **left** — or replace `"RX"` with `"XR"` — which slides an `R` one step to the **right**. Return `true` if you can turn `start` into `end` using any number of moves.

Read the two moves again and notice what they really mean: an `L` can only ever walk **left**, an `R` can only ever walk **right**, and they walk by swapping past `X`s. An `L` and an `R` can never pass through each other — the only thing either can swap with is an `X`.

**Example:** `start = "RXXLRXRXL"`, `end = "XRLXXRRLX"` → `true` *(every L slid left, every R slid right, and the L/R order never changed)*

**Constraints that matter:** `start` and `end` can be up to `10^4` long. That kills any brute-force search over reachable strings — the number of arrangements is exponential. You want a **single linear pass**. The whole problem is spotting the *invariants* that a linear pass can check.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Simulate. Start from `start`, apply every legal swap, BFS outward, and see if I ever hit `end`." That's a correct mental model and it'll pass the tiny examples — but it explores an exponential cloud of strings. It times out instantly on a long input.
- **Where it hurts:** you're generating millions of intermediate strings to answer a yes/no question. That's a mountain of wasted work. The reachable set is huge, but the *question* is tiny. There must be a property that separates reachable from unreachable without ever building the path.
- **The leap:** stare at the moves. `L` only moves left. `R` only moves right. Neither can jump over the other — they only ever swap with `X`. So two things can **never** change: **(1)** the left-to-right *order* of the non-`X` letters, and **(2)** the fact that each `L` can only end up at the same spot or further **left**, and each `R` at the same spot or further **right**. Delete the `X`s from both strings — if the remaining `L`/`R` sequences differ, it's hopeless. If they match, line up the letters pairwise and check each one only moved in its legal direction.
- **Pattern trigger:** **"a transformation with a strict directional rule"** → **look for the invariant, then two-pointer-verify it.** When elements can only move one way and can't cross, you don't simulate the motion — you check start-vs-end positions directly. That's the transferable move: *find what the operation can't change, and verify only that.*

---

## ① Brute Force

Treat every string as a node; apply every legal `"XL"→"LX"` and `"RX"→"XR"` swap to get its neighbors; BFS from `start` looking for `end`.

```python
from collections import deque

def can_transform_brute(start, end):
    seen = {start}
    q = deque([start])
    while q:
        s = q.popleft()
        if s == end:
            return True
        for k in range(len(s) - 1):
            if s[k:k+2] == "XL":                      # slide an L left
                nxt = s[:k] + "LX" + s[k+2:]
                if nxt not in seen:
                    seen.add(nxt); q.append(nxt)
            if s[k:k+2] == "RX":                      # slide an R right
                nxt = s[:k] + "XR" + s[k+2:]
                if nxt not in seen:
                    seen.add(nxt); q.append(nxt)
    return False
```

**Why it's the natural first attempt:** it's a literal translation of the rules. Every arrow the problem gives you becomes an edge, and "can I reach `end`?" becomes plain graph reachability.

**Why it's not enough:** the number of reachable strings is exponential in the count of `X`s — each `L`/`R` can sit in many positions among the `X`s. For a length-`10^4` input this explores an astronomically large set before it can answer. It's not a little slow; it never finishes. You're building the entire universe of intermediate strings just to answer yes or no.

**Complexity:** Time `O(2^n)`-ish (exponential in the number of gaps), Space the same for the `seen` set.

---

## ② Optimised Solution

Don't simulate the motion — **check the invariants.** Walk both strings with two pointers, skipping `X`s. The non-`X` letters must appear in the same order, and each one must only have moved in its legal direction.

```python
def can_transform(start, end):
    if len(start) != len(end):
        return False
    n = len(start)
    i = j = 0
    while i < n or j < n:
        while i < n and start[i] == "X":     # next real letter in start
            i += 1
        while j < n and end[j] == "X":       # next real letter in end
            j += 1

        if i == n and j == n:                # both consumed everything → match
            return True
        if i == n or j == n:                 # one ran out of letters first → order differs
            return False
        if start[i] != end[j]:               # letters don't line up → order differs
            return False

        if start[i] == "L" and i < j:        # an L must end at same spot or LEFT: i >= j
            return False
        if start[i] == "R" and i > j:        # an R must end at same spot or RIGHT: i <= j
            return False

        i += 1
        j += 1
    return True
```

**Walk the example** `start = "RXXLRXRXL"`, `end = "XRLXXRRLX"`:

First, strip the `X`s in your head. `start` → `R L R R L`. `end` → `R L R R L`. Same sequence — good, we have a chance. Now line them up pairwise with their real indices:

| Pair | letter | `start` index `i` | `end` index `j` | rule | check |
|---|---|---|---|---|---|
| 1 | `R` | 0 | 1 | R needs `i ≤ j` | `0 ≤ 1` ✓ |
| 2 | `L` | 3 | 2 | L needs `i ≥ j` | `3 ≥ 2` ✓ |
| 3 | `R` | 4 | 5 | R needs `i ≤ j` | `4 ≤ 5` ✓ |
| 4 | `R` | 6 | 6 | R needs `i ≤ j` | `6 ≤ 6` ✓ |
| 5 | `L` | 8 | 7 | L needs `i ≥ j` | `8 ≥ 7` ✓ |

Every letter matches and every one moved only in its legal direction → **`true`**. ✅

Now the counter-case — an `L` trying to cheat rightward: `start = "LX"`, `end = "XL"`. Strip `X`s: both are `L`, order matches. But the `L` sits at index `0` in `start` and index `1` in `end` — it would have to move **right**, and `L` can't do that. The check `start[i] == "L" and i < j` → `0 < 1` fires → **`false`**. Exactly right.

**Why it's correct:** the two moves can't change the relative order of the non-`X` letters (an `L` and `R` never swap with each other — only with `X`), so if the stripped sequences differ, `end` is simply unreachable, and the pointer walk catches that as a letter mismatch or a length mismatch. When the sequences *do* match, the only remaining freedom is position: an `L` reaches its target iff its start index is `≥` its end index (it only slides left), and an `R` iff its start index is `≤` its end index (it only slides right). Those two inequalities are both **necessary** (the moves can't violate them) and **sufficient** (given the room, the `X`s let you slide each letter to exactly where it needs to be). Checking all of them in one pass settles it.

**Complexity:** Time `O(n)` — each pointer crosses the string once. Space `O(1)`.

---

## ③ Space Optimization

**Already optimal.** We hold two integer indices and nothing else — no `seen` set, no copy of either string, no auxiliary structure that grows with the input. Everything is read in place from `start` and `end`.

```python
# Nothing to cut: two pointers i and j, both O(1). We never allocate anything
# proportional to n. The linear scan with constant extra memory is the floor.
```

**Complexity:** Time `O(n)`, Space `O(1)`.

> Say it out loud: *"Space is O(1) — I only carry two indices and never build an intermediate string. There's nothing to optimize away because there's nothing being stored."* Naming the absence of a trick is as strong as finding one.

---

## Java (for Java interviewers)

```java
public boolean canTransform(String start, String end) {
    if (start.length() != end.length()) return false;
    int n = start.length();
    int i = 0, j = 0;
    while (i < n || j < n) {
        while (i < n && start.charAt(i) == 'X') i++;   // next real letter in start
        while (j < n && end.charAt(j) == 'X') j++;      // next real letter in end

        if (i == n && j == n) return true;              // both consumed → match
        if (i == n || j == n) return false;             // one ran out first → order differs
        if (start.charAt(i) != end.charAt(j)) return false;

        char c = start.charAt(i);
        if (c == 'L' && i < j) return false;            // L must move LEFT: i >= j
        if (c == 'R' && i > j) return false;            // R must move RIGHT: i <= j

        i++;
        j++;
    }
    return true;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (BFS over reachable strings) | O(2^n) | O(2^n) |
| Optimised (two-pointer invariant check) | O(n) | O(1) |
| Space-optimised | O(n) | O(1) *(already optimal)* |

---

## Say it out loud (interview narration)

> *"The brute force is BFS over every string I can reach with the swaps, but that set is exponential, so it times out. The key observation is what the moves can't change: an L only ever slides left, an R only ever slides right, and they never swap past each other — only past X's. So two invariants must hold. One: delete the X's and the L/R sequences of start and end must be identical, since order is fixed. Two: line the letters up pairwise — each L's start index must be greater-or-equal to its end index because it can only go left, and each R's start index must be less-or-equal because it can only go right. I verify both with a single two-pointer pass, skipping X's. That's O(n) time and O(1) space."*

Before coding, ask the one clarifying question that shows you read the rules: *"An L can only move left and an R only right — and they can never cross each other, correct?"* That's the exact insight the whole solution hinges on, and surfacing it early is what Google's rubric rewards.

## Related / follow-ups
- **Backspace String Compare (LC 844)** — same DNA: strip/skip characters with two pointers and compare what's left, ideally in O(1) space.
- **Valid Palindrome II (LC 680)** — two-pointer scan with a directional rule about what may move.
- **Swapping to make strings equal / minimum swaps** — reasoning about what a restricted swap operation can and cannot achieve.
- **Rotate String (LC 796)** — another "which target strings are actually reachable under this operation?" question.
