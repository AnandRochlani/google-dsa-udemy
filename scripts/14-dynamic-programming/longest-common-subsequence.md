# 🎬 Recording Script — Longest Common Subsequence
**Pattern: Dynamic Programming (2-D grid) · LeetCode 1143 · Medium · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the two-axis state from Partition Equal Subset Sum; "define the subproblem" from LIS.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides. **TEACHER** carries the thread; **LEARNER** is a sharp peer who speaks 3–5 times only.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: two words stacked: `abcde` and `ace`. Faint lines link the a's, c's, e's. The linked letters glow: "ace".]**

> Two strings. Find the longest sequence of characters that appears in **both**, left to right — you can skip letters but not reorder them. `abcde` and `ace` share `ace`, length 3.
>
> This is *the* string-DP problem. Master it and you've basically pre-solved Edit Distance, diff tools, DNA alignment, autocorrect — they're all this same grid. Today we build that grid from scratch, one cell at a time, and you'll never be scared of a 2-D DP table again. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: `text1 = "abcde"`, `text2 = "ace"` → 3. Below: `text1="abc"`, `text2="def"` → 0.]**

> One line: **the length of the longest common subsequence** — longest run of characters in the same order in both strings, gaps allowed.
>
> `"abcde"` and `"ace"` → **3** (`ace`). `"abc"` and `"def"` → **0**, nothing shared. Notice we want the *length*, not the string itself — that keeps the DP simple.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — the decision at the ends)*

**[VISUAL: two strings with a pointer on the last char of each. `abcde` (e) and `ace` (e).]**

> The decision trick: look at the **last character** of each string and ask what to do with it.
>
> **Case match** — the last characters are equal, like both `e`. Then that `e` can be the tail of our common subsequence. Grab it — that's `1 +` the LCS of everything before it in *both* strings.
>
> **Case mismatch** — last characters differ, say `e` vs `c`. Then at least one of them is *not* in the LCS. We don't know which, so try both: drop the last char of string 1, or drop the last char of string 2, and take the better.
>
> **[VISUAL: boxed — "match → 1 + LCS(i-1, j-1); mismatch → max( LCS(i-1, j), LCS(i, j-1) )".]**
>
> Base case: if either string is empty, LCS is 0.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: recursion tree over prefix-pairs (i, j). On mismatches it forks two ways; the same (i, j) pair lights up repeatedly across branches.]**

> **TEACHER:** As plain recursion, every mismatch forks into two calls, so the tree is exponential — roughly 2 to the (m+n). But the *state* is just a pair: how far into string 1, how far into string 2. There are only `m × n` such pairs, and the recursion keeps revisiting them.
>
> **LEARNER:** So the state is two indices, `(i, j)` — two axes again, like the knapsack. But here both axes are *string positions* instead of "items and sum"?
>
> **TEACHER:** Exactly the pattern-match I want you making. Two-axis state → a 2-D table. Last problem the axes were items and a running sum; here they're prefix lengths of the two strings.
>
> Predict: if the state is `(i, j)` over two strings, **what shape is the table, and how do you fill it?** Pause.
>
> *(3-second think timer)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration — derive the grid)*

**[VISUAL: a grid appears, rows = "abcde", cols = "ace", plus an empty-string row and column of zeros.]**

> **TEACHER:** It's a **grid**. `dp[i][j]` = the LCS length of the first `i` characters of string 1 and the first `j` characters of string 2. We pad with an empty-string row and column, all zeros — that's the "either string empty → 0" base case, baked in.
>
> Now fill cell by cell. For each cell, apply the same decision:
>
> **[VISUAL: fill the grid. On a matching char (a, c, e) the cell = its diagonal-up-left neighbor + 1, glowing. On a mismatch, cell = max(up, left).]**
>
> If the characters for this row and column **match**, take the **diagonal** neighbor (up-and-left) and add 1 — because those are the two prefixes with both matched characters removed. If they **mismatch**, take the **max of up and left** — the better of dropping one character from either string.
>
> Watch the matches trace a staircase: `a` lights a 1, `c` bumps to 2, `e` bumps to 3. The bottom-right cell is the answer.

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed — "Match → diagonal + 1. Mismatch → max(up, left)."]**

> The line, and it's shockingly compact: **match takes the diagonal plus one; mismatch takes the better of up or left.** Two rules, whole problem.
>
> That "diagonal on match, max of neighbors on mismatch" grid is a template. Edit Distance, next lesson, is *literally the same grid* with a third neighbor. Lock the shape in now.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: editor. Type chunk 1.]**

> Build the grid — one extra row and column of zeros for the empty-prefix base.

```python
def lcs_2d(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
```

> **[VISUAL: add chunk 2, highlight.]** Fill every interior cell with the two rules.

```python
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1       # match: diagonal + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])   # mismatch: up vs left
    return dp[m][n]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:15`
*(elaboration — why each line exists)*

**[VISUAL: the grid; spotlight the three neighbors of one cell — diagonal, up, left.]**

> The *why*:
>
> The `+1` on the padded row/column indexing — `text1[i-1]` — because `dp[i]` means "first `i` characters," so the character at that row is at index `i-1`. Off-by-one lives here; get it right once and copy it forever.
>
> `dp[i-1][j-1] + 1` on a match — the diagonal is "both prefixes minus their matched last char." Add one for the match. It *must* be the diagonal, not up or left, because a match consumes a character from **both** strings.
>
> `max(dp[i-1][j], dp[i][j-1])` on a mismatch — up means "drop string1's last char," left means "drop string2's last char." Best of the two.
>
> **LEARNER:** On a mismatch, why not also consider the **diagonal** — dropping *both* last characters at once?
>
> **TEACHER:** Great objection, and the answer is subtle: the diagonal is already *covered*. Dropping both is never better than dropping just one, because `dp[i-1][j-1] ≤ dp[i-1][j]` and `≤ dp[i][j-1]` — the diagonal cell is a smaller prefix of both those neighbors, so its value can't exceed them. Considering it would be redundant, never wrong but never helpful. Up and left already dominate it.

---

## 9. DRY-RUN THE CODE — `7:30`
*(worked example — prove it, close the loop)*

**[VISUAL: the full grid filled, matches on the diagonal highlighted.]**

> Fill the grid for `"abcde"` (rows) and `"ace"` (columns):

| | "" | a | c | e |
|---|---|---|---|---|
| "" | 0 | 0 | 0 | 0 |
| a | 0 | **1** | 1 | 1 |
| b | 0 | 1 | 1 | 1 |
| c | 0 | 1 | **2** | 2 |
| d | 0 | 1 | 2 | 2 |
| e | 0 | 1 | 2 | **3** |

> The three matches — `a`, `c`, `e` — each grab a diagonal + 1, stepping 1 → 2 → 3 down the highlighted diagonal. Mismatches just carry the max forward. Bottom-right `dp[5][3] = 3`. **3**, exactly `ace`.

---

## 10. COMPLEXITY, OUT LOUD — `8:15`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(2^(m+n)). Grid: O(m·n) time, O(m·n) space.]**

> To the interviewer: *"Brute recursion is exponential from forking on every mismatch. The grid has m-times-n cells, each O(1) work — O(m·n) time and O(m·n) space."*
>
> For two 1000-char strings that's a million cells — instant. The exponential version wouldn't finish before the heat death of the interview.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:45`
*(depth + honesty — the strong beat)*

**[VISUAL: the full grid with only two rows spotlighted — the current row and the one above; older rows crumble.]**

> The space beat, and it's a clean win. Look at what any cell reads: the diagonal, the cell above, the cell to the left — all in the **current row or the one directly above**. It never reaches two rows up. So we don't need the whole grid — just **two rows**.

```python
def lcs(text1, text2):
    if len(text2) > len(text1):            # make text2 the shorter → smaller rows
        text1, text2 = text2, text1
    m, n = len(text1), len(text2)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                curr[j] = prev[j - 1] + 1              # diagonal
            else:
                curr[j] = max(prev[j], curr[j - 1])    # up vs left
        prev = curr
    return prev[n]
```

> `prev[j-1]` is the diagonal, `prev[j]` is up, `curr[j-1]` is the freshly-written left. That's O(m·n) time but only **O(min(m, n))** space — and swapping to keep the shorter string as the row width is the reason for that `min`.
>
> Say it: *"Each cell only touches the row above and the left neighbor, so I keep two rows — O(min(m,n)) space instead of the full grid."* You *can* squeeze to one row plus a diagonal scalar, but two rows is the version to write under pressure — obviously correct, same asymptotics.

---

## 12. YOUR TURN (active recall) — `9:55`
*(retrieval practice)*

**[VISUAL: "Your turn → Longest Common Substring". Note: "contiguous!"]**

> Before the next video: **Longest Common Substring** — the sneaky sibling. Now the shared run must be **contiguous**. Here's the one change to figure out: on a **mismatch**, instead of `max(up, left)`, you reset the cell to **0** — a broken run starts over — and you track the global maximum across the whole grid, not just the bottom-right. Small tweak, different problem. Try it.

---

## 13. LOCK IT IN — `10:30`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Two strings → two axes → a 2-D grid** `dp[i][j]` over prefix lengths.
> 2. **Match = diagonal + 1; mismatch = max(up, left).** The whole recurrence in one breath.
> 3. **Cells reach only up/left/diagonal → keep two rows,** O(min(m,n)) space.
>
> Memory peg — *"longest thing common to two strings, order preserved"* → **grid: diagonal on a match, best neighbor on a miss.**

---

## 14. CLIFFHANGER — `11:00`
*(open loop to next lesson)*

**[VISUAL: blurred title — "Edit Distance". `horse → ros` with insert/delete/replace tags.]**

> This grid just quietly solved a huge family of problems. Next, we add **one more neighbor** and flip max to min — and suddenly the same table answers *"how many edits to turn one word into another?"* That's Edit Distance, the Hard problem that's really this Medium in a trench coat. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// O(min(m,n)) space — two rolling rows
public int longestCommonSubsequence(String text1, String text2) {
    int m = text1.length(), n = text2.length();
    int[] prev = new int[n + 1];
    for (int i = 1; i <= m; i++) {
        int[] curr = new int[n + 1];
        for (int j = 1; j <= n; j++) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                curr[j] = prev[j - 1] + 1;
            } else {
                curr[j] = Math.max(prev[j], curr[j - 1]);
            }
        }
        prev = curr;
    }
    return prev[n];
}
```
