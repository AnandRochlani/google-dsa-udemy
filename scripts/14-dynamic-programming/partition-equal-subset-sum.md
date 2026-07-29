# 🎬 Recording Script — Partition Equal Subset Sum
**Pattern: Dynamic Programming (0/1 Knapsack) · LeetCode 416 · Medium · Target length ~14 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the "take-it-or-leave-it" decision from House Robber; the 1-D table from Coin Change.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides. **TEACHER** carries the thread; **LEARNER** is a sharp peer who speaks 3–5 times only.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: numbers `[1, 5, 11, 5]` sliding onto a balance scale. It tips, then settles level: {1,5,5} on one side, {11} on the other.]**

> Can you split these numbers into **two piles with equal sum**? `[1, 5, 11, 5]` — yes: `1+5+5 = 11` on one side, `11` on the other. Balanced.
>
> This looks like a puzzle about *splitting into two*. But the real unlock is realizing it's secretly a completely different, famous problem in disguise — the **knapsack**. Once you see the reframe, a scary "partition" question becomes a clean checkbox DP. And it hides one of the most notorious one-line bugs in all of DP — a loop that has to run *backwards*. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: `[1, 5, 11, 5]` → true. Below: `[1, 2, 3, 5]` → false, with "sum = 11, odd" flagged.]**

> One line: **can the array be split into two subsets with equal sum?** True or false.
>
> Example: `[1, 5, 11, 5]` → **true**. And a quick false: `[1, 2, 3, 5]` sums to 11 — an *odd* number. You can't split an odd total into two equal halves, so it's instantly false. That parity check is our free first move.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — the reframe, then the decision)*

**[VISUAL: total = 22 splits into two 11s. The "two piles" framing fades; one question remains: "Can any subset sum to 11?"]**

> Here's the reframe that changes everything. Two equal piles means each pile is exactly `total / 2`. Our total is 22, so each side must be 11. But if I can find *one* subset that sums to 11, the leftovers *automatically* sum to 11 too. So forget "two piles." The real question is:
>
> **[VISUAL: boxed — "Is there a subset summing to target = total / 2?"]**
>
> **Can some subset hit `target = total/2`?** And that's just House Robber's decision wearing a new hat: for each number, **include it in my subset, or don't.**
>
> If I include `nums[i]`, my remaining target drops by `nums[i]`. If I skip it, the target's unchanged. Success is hitting target exactly zero:
>
> **[VISUAL: boxed — `canMake(i, t) = canMake(i+1, t) OR canMake(i+1, t - nums[i])`.]**

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: recursion tree branching include/exclude. Two different paths — {1,5} and {5,1} — arrive at the SAME node (same remaining target, same position), highlighted identically.]**

> **TEACHER:** Run it as recursion and the tree branches two ways per number — 2ⁿ leaves. But look closely: the state is really a *pair* — which item index I'm at, and how much target is left. Picking `{1, 5}` versus `{5, 1}` lands me at the **same** state: same position, same remaining target. Recomputed.
>
> **LEARNER:** So the state is two-dimensional now — `(index, remaining target)` — not just a single number like House Robber?
>
> **TEACHER:** Exactly the leap. The "decision" is still binary — take or skip — but the *state* grew a second axis. That's what makes this a knapsack. And it's *good* news: there are only `n × (target+1)` distinct states, so memoizing turns exponential into polynomial.
>
> Predict: the state is `(i, t)`. **What does the table look like, and what's the cleanest shape for it?** Pause.
>
> *(3-second think timer)*

---

## 5. BUILD THE INTUITION (the aha) — `3:45`
*(elaboration — derive the 1-D boolean table)*

**[VISUAL: a 2-D grid dp[item][sum], then it visibly flattens into a single boolean row dp[sum].]**

> **TEACHER:** The full table is `dp[i][t]` = "can items up to `i` make sum `t`?" — a grid of true/false. But the interview-favorite collapses it to a **single boolean array** `dp[t]` = "is sum `t` achievable with the numbers I've processed so far?"
>
> Seed: `dp[0] = True` — sum zero is always achievable, by picking nothing. Everything else starts False.
>
> Now feed in numbers one at a time. Each new number `x` unlocks new reachable sums: if `t - x` was already reachable, then `t` becomes reachable by adding `x`.
>
> **[VISUAL: processing [1,5,11,5], the set of reachable sums grows: {0} → {0,1} → {0,1,5,6} → {0,1,5,6,11,...} — 11 lights up green.]**
>
> Start `{0}`. Add 1 → `{0,1}`. Add 5 → `{0,1,5,6}`. Add 11 → now 11 and beyond appear. The moment `dp[11]` turns True, we're done — **true**.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed — "dp[t] = dp[t] OR dp[t - x], for each number x. Answer = dp[target]."]**

> The line: **each number either extends the set of reachable sums or it doesn't** — `dp[t] = dp[t] or dp[t - x]`.
>
> This is the **0/1 knapsack** skeleton — "0/1" because each item is used **at most once**. Keep that phrase; it's about to matter enormously for one loop direction.

---

## 7. CODE IT — LIVE & CHUNKED — `5:35`
*(cognitive load — build in pieces)*

**[VISUAL: editor. Type chunk 1.]**

> First the free parity check and the target.

```python
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
```

> **[VISUAL: add chunk 2, highlight.]** Set up the boolean array — sum 0 always reachable.

```python
    dp = [False] * (target + 1)
    dp[0] = True
```

> **[VISUAL: add chunk 3, highlight the reversed range hard.]** Now the crux. For each number, update the reachable sums — iterating **high to low**.

```python
    for x in nums:
        for t in range(target, x - 1, -1):     # HIGH → LOW — this direction is the whole trick
            if dp[t - x]:
                dp[t] = True
        if dp[target]:
            return True
    return dp[target]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — the reverse-loop crux)*

**[VISUAL: the inner loop. Two filmstrips side by side: LOW→HIGH reuses x twice (wrong); HIGH→LOW uses x once (right).]**

> Everything here rides on one line, so let's earn it.
>
> **LEARNER:** That `range(target, x - 1, -1)` — why backwards? I'd have written it low-to-high without thinking. What breaks?
>
> **TEACHER:** This is *the* bug, so lean in. We're doing 0/1 knapsack — each number used **at most once**. Say `x = 5`. If I loop **low to high**, I first set `dp[5] = True` using this 5. Then later in the *same* pass I reach `t = 10`, check `dp[10 - 5] = dp[5]` — which I just set — and mark `dp[10]` True. But that used the 5 **twice**. That's the *unbounded* knapsack, the wrong problem.
>
> Going **high to low** fixes it: when I compute `dp[t]`, the entry `dp[t - x]` still holds its value from *before this number* — the previous item's state — so each number contributes at most once per pass.
>
> `if dp[target]: return True` — a nice early exit; the instant target's reachable, stop.
>
> Say the crux out loud in the room: *"0/1 knapsack, so I iterate the sum high to low — that guarantees each number is used at most once."* Interviewers listen for exactly that sentence.

---

## 9. DRY-RUN THE CODE — `8:15`
*(worked example — prove it, close the loop)*

**[VISUAL: the boolean array, columns 0..11, flipping to True as each number is processed.]**

> Trace `[1, 5, 11, 5]`, target 11. I'll show which sums are True after each number:

| after processing | reachable sums (True) |
|---|---|
| {} (seed) | 0 |
| 1 | 0, 1 |
| 5 | 0, 1, 5, 6 |
| 11 | 0, 1, 5, 6, 11 → **hit!** |

> `dp[11]` flips True when we process the 11 (from `dp[0]`). Early-exit returns **true**. (Even the second 5 wasn't needed here.) Done.

---

## 10. COMPLEXITY, OUT LOUD — `9:00`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(2ⁿ). DP: O(n × target) time, O(target) space.]**

> To the interviewer: *"Brute force is 2ⁿ subsets. The knapsack DP is O(n × target) time — n numbers times target-plus-one sums — and O(target) space for the boolean row."*
>
> And add the honest caveat: *"target is total/2, so this is **pseudo-polynomial** — polynomial in the numeric value of the sum, not the input length."* Saying that unprompted signals real understanding.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:40`
*(depth + honesty — the strong beat)*

**[VISUAL: the 2-D grid dp[i][t] fading, leaving one row dp[t]; a note: "each row only needs the row above."]**

> This *is* the space-optimization beat, and it's the crown jewel of this problem. The natural table is 2-D — `dp[i][t]` — costing O(n × target) memory. But each row depends only on the row directly above it. So we collapsed it to **one** boolean row, O(target) space — that's the code we already wrote.
>
> The subtlety — and it's the reason this beat is famous — is that collapsing 2-D to 1-D is exactly *why* the loop must run backwards. In the 2-D version, `dp[i][t]` reads `dp[i-1][t-x]` — the previous row. When you flatten to one row, "the previous row's value at `t-x`" only survives if you haven't overwritten it yet — which means you must reach `t` before `t-x`, i.e. iterate **high to low**.
>
> Say it: *"Collapsing the 2-D knapsack to a 1-D array forces the reverse iteration, because that's what preserves the previous-row value I depend on."* That single sentence ties the space trick and the loop direction into one idea.

---

## 12. YOUR TURN (active recall) — `10:45`
*(retrieval practice)*

**[VISUAL: "Your turn → Target Sum (LC 494)". Numbers with + / − signs.]**

> Before the next video: **Target Sum.** You assign a `+` or `−` to each number to hit a target `S`. Here's the reduction to chew on: if `P` is the sum of the plus-numbers, then `P − (total − P) = S`, so `P = (S + total) / 2`. Suddenly it's *this* problem — count subsets summing to `P`. Same knapsack, but *counting* instead of true/false. Try it before peeking.

---

## 13. LOCK IT IN — `11:20`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Reframe "two equal piles" as "one subset hits total/2."** Odd total → instant false.
> 2. **0/1 knapsack = take-or-skip with a running sum axis.** `dp[t] = dp[t] or dp[t−x]`.
> 3. **Flattening 2-D → 1-D forces the high-to-low loop.** Reverse iteration = each item used once.
>
> Memory peg — *"can I hit an exact sum, each item at most once"* → **0/1 knapsack, boolean row, loop the sum backwards.**

---

## 14. CLIFFHANGER — `11:55`
*(open loop to next lesson)*

**[VISUAL: blurred title — "Longest Common Subsequence". Two strings with matching letters linked.]**

> Our state just grew from one dimension to two — items and sum. Next problem keeps a 2-D state but makes *both* axes strings, and the table becomes a genuine **grid** you fill cell by cell. It's the gateway to every string-DP question Google loves: Longest Common Subsequence. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public boolean canPartition(int[] nums) {
    int total = 0;
    for (int x : nums) total += x;
    if (total % 2 != 0) return false;
    int target = total / 2;
    boolean[] dp = new boolean[target + 1];
    dp[0] = true;
    for (int x : nums) {
        for (int t = target; t >= x; t--) {     // high -> low: 0/1 knapsack
            if (dp[t - x]) dp[t] = true;
        }
        if (dp[target]) return true;
    }
    return dp[target];
}
```
