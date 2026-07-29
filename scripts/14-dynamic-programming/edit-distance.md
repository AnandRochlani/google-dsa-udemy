# 🎬 Recording Script — Edit Distance
**Pattern: Dynamic Programming (2-D grid) · LeetCode 72 · Hard · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the match/mismatch **grid** from Longest Common Subsequence — this is that grid with one more neighbor.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides. **TEACHER** carries the thread; **LEARNER** is a sharp peer who speaks 3–5 times only.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: `horse` morphing to `ros` in steps: horse → rorse → rose → ros, each step tagged replace / delete / delete.]**

> How many single-character edits — insert, delete, or replace — to turn `horse` into `ros`? The answer's 3. This is the math behind spellcheck, autocorrect, DNA alignment, and `git diff`.
>
> It's tagged **Hard**. But here's the secret: you already learned it last lesson. Edit Distance is the Longest Common Subsequence grid with *one extra neighbor* and `min` instead of `max`. If you followed LCS, this Hard problem is going to feel almost unfair. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: `word1 = "horse"`, `word2 = "ros"` → 3. Three operations listed: insert, delete, replace, each cost 1.]**

> One line: **the minimum number of edits to convert `word1` into `word2`,** where each insert, delete, or replace of a single character costs 1. This is the classic **Levenshtein distance**.
>
> `"horse"` → `"ros"` is **3**: replace `h`→`r`, delete one `r`, delete `e`. Hold that number.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — the decision at the ends)*

**[VISUAL: pointers on the last char of each word. `horse` (e) vs `ros` (s).]**

> Same move as LCS — look at the **last characters** of the two prefixes and decide.
>
> **If they match** — the tails already agree. Free. Just recurse on both shorter prefixes, no cost.
>
> **If they mismatch** — you must spend one edit, and there are exactly **three** ways to fix that last spot:
> - **Replace** `word1`'s last char with `word2`'s → `1 +` the cost for both prefixes minus one (the *diagonal*).
> - **Delete** `word1`'s last char → `1 +` the cost for `word1` shorter, `word2` same (the *up* neighbor).
> - **Insert** `word2`'s last char into `word1` → `1 +` `word1` same, `word2` shorter (the *left* neighbor).
>
> Take the cheapest of the three.
>
> **[VISUAL: boxed — "match → dp[i-1][j-1]; mismatch → 1 + min( replace diag, delete up, insert left )".]**

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: recursion tree forking THREE ways on each mismatch; same (i, j) prefix pairs light up repeatedly.]**

> **TEACHER:** As recursion, each mismatch forks **three** ways now — replace, delete, insert — down to depth m+n. That's O(3^(m+n)), even bushier than LCS. But again the state is just the pair `(i, j)` — prefix lengths — and the same pairs recur endlessly.
>
> **LEARNER:** So it's the LCS grid again — same `(i, j)` state, same 2-D table — just three neighbors feeding each cell instead of two, and a min instead of a max?
>
> **TEACHER:** That is *precisely* it, and if you saw that unprompted you've basically solved a Hard problem by pattern-matching. Same grid, one more incoming arrow, minimize instead of maximize.
>
> Predict the part that's genuinely *different* from LCS: **what are the base cases here?** In LCS the empty-string row was all zeros. Is it zeros here? Pause and think.
>
> *(4-second think timer)*

---

## 5. BUILD THE INTUITION (the aha) — `3:45`
*(elaboration — derive the grid, especially the base row)*

**[VISUAL: grid, rows = "horse", cols = "ros". The empty row fills 0,1,2,3; the empty column fills 0,1,2,3,4,5 — NOT zeros.]**

> **TEACHER:** Here's where Edit Distance diverges from LCS, and it's the whole "aha." The base row and column are **not** zeros.
>
> Think about what they mean. `dp[i][0]` = cost to turn the first `i` characters of `word1` into the *empty* string. That's `i` **deletes**. And `dp[0][j]` = cost to build `word2`'s first `j` characters from nothing — `j` **inserts**. So the first row and column count up: `0, 1, 2, 3, …`.
>
> **[VISUAL: the grid fills. Matches copy the diagonal; mismatches take 1 + min of the three neighbors, each highlighted as it's read.]**
>
> Then the interior fills by the recurrence. Match → copy the diagonal, free. Mismatch → 1 plus the cheapest of diagonal (replace), up (delete), left (insert). Fill row by row, and the bottom-right cell is your minimum edit count.
>
> That's the answer to the predict: the base cases *carry real cost* here, because editing to or from empty isn't free — it's one op per leftover character.

---

## 6. THE KEY MOVE (signaling) — `5:15`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed — "Match → diagonal (free). Mismatch → 1 + min(diagonal=replace, up=delete, left=insert)."]**

> The line: **match copies the diagonal for free; mismatch pays one, plus the cheapest of the three neighbors — diagonal is replace, up is delete, left is insert.**
>
> Memorize *which neighbor is which operation* — that mapping is the entire problem, and it's what people blank on at the whiteboard.

---

## 7. CODE IT — LIVE & CHUNKED — `6:00`
*(cognitive load — build in pieces)*

**[VISUAL: editor. Type chunk 1.]**

> Grid, plus the meaningful base row and column.

```python
def edit_2d(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i          # i deletes to reach ""
    for j in range(n + 1):
        dp[0][j] = j          # j inserts to build word2
```

> **[VISUAL: add chunk 2, highlight.]** Fill the interior with match-or-three-way-min.

```python
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]           # match: free diagonal
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1],  # replace
                                   dp[i - 1][j],      # delete
                                   dp[i][j - 1])      # insert
    return dp[m][n]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:15`
*(elaboration — why each line exists)*

**[VISUAL: the grid; spotlight the three neighbors and label them replace / delete / insert.]**

> The *why*:
>
> `dp[i][0] = i` and `dp[0][j] = j` — the base costs we derived. Skip these and every interior cell inherits garbage. In LCS these were zeros; here they *count*. That's the one line most people get wrong porting LCS to Edit Distance.
>
> Match → `dp[i-1][j-1]` with **no** `+1` — agreeing tails cost nothing, just shrink both prefixes.
>
> Mismatch → `1 + min(...)` — one edit, cheapest repair. Diagonal is replace (both prefixes shrink, one swap), up is delete (word1 shrinks), left is insert (word2's char added, word1 unchanged).
>
> **LEARNER:** Wait — "insert into word1" but the code reads `dp[i][j-1]`, which shrinks `word2`'s index, not word1's. Why does inserting map to the *left* neighbor?
>
> **TEACHER:** This is the confusing one, so slow down. Inserting `word2`'s last character onto the end of `word1` makes that character *match* `word2`'s last — so both of those matched characters are now handled, and what remains to solve is `word1`'s full prefix (`i`) against `word2` *minus* its last char (`j-1`). That remaining subproblem is `dp[i][j-1]` — the left neighbor. The insert is "accounted for" by the `+1`; the left cell is the leftover work. Trace it once by hand and it clicks permanently.

---

## 9. DRY-RUN THE CODE — `8:45`
*(worked example — prove it, close the loop)*

**[VISUAL: the full grid filled, path from bottom-right traced back.]**

> Fill for `"horse"` (rows) and `"ros"` (columns):

| | "" | r | o | s |
|---|---|---|---|---|
| "" | 0 | 1 | 2 | 3 |
| h | 1 | 1 | 2 | 3 |
| o | 2 | 2 | 1 | 2 |
| r | 3 | 2 | 2 | 2 |
| s | 4 | 3 | 3 | 2 |
| e | 5 | 4 | 4 | **3** |

> The first row and column are the pure insert/delete ladders. `o` matches `o` → the diagonal `1` copies through. Bottom-right `dp[5][3] = 3`. **3 edits**, exactly the replace-delete-delete we opened with. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:40`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(3^(m+n)). Grid: O(m·n) time, O(m·n) space.]**

> To the interviewer: *"Brute recursion is O(3 to the m+n) — three-way branch on each mismatch. The grid has m-times-n cells, O(1) each — so O(m·n) time, O(m·n) space."*
>
> For two 500-char words that's 250,000 cells. Trivial. This is why *every* string-distance system is built on this table.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:15`
*(depth + honesty — the strong beat)*

**[VISUAL: full grid → two spotlighted rows (current + previous); older rows crumble.]**

> The space beat — same lever as LCS, and worth doing carefully because Hard problems reward the follow-through. Every cell reads the diagonal, up, and left — all in the current row or the one directly above. So keep **two rows**:

```python
def edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    prev = list(range(n + 1))            # dp[0][j] = j  (base row)
    for i in range(1, m + 1):
        curr = [i] + [0] * n             # curr[0] = dp[i][0] = i
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]                # diagonal, free
            else:
                curr[j] = 1 + min(prev[j - 1],       # replace (diagonal)
                                  prev[j],           # delete (up)
                                  curr[j - 1])       # insert (left)
        prev = curr
    return prev[n]
```

> The two tricky initializations: `prev` starts as the base *row* `0,1,2,…`, and each new `curr` starts with `curr[0] = i` — the base *column* value for this row. Miss either and the edges break.
>
> That's O(m·n) time, **O(n)** space — O(min(m,n)) if you swap so `word2` is the shorter one sizing the rows. Say it: *"Each cell only needs the previous row and the left cell, so two rows — O(min(m,n)) space."* You can push to one row plus a diagonal scalar, but two rows is the safe interview default.

---

## 12. YOUR TURN (active recall) — `11:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Delete Operation for Two Strings (LC 583)". Only deletes allowed.]**

> Before the next video: **Delete Operation for Two Strings.** Now the *only* allowed op is delete, from either word, and you want the fewest deletes to make them equal. Here's the elegant connection to chew on: the characters you *keep* form the LCS, so the answer is `m + n − 2 × LCS`. You can solve it as a fresh grid, or reuse last lesson's LCS. Try both and see they agree.

---

## 13. LOCK IT IN — `12:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **It's the LCS grid + one neighbor, min instead of max.** Diagonal/up/left = replace/delete/insert.
> 2. **The base row and column carry real cost** — `i` deletes, `j` inserts — not zeros. That's the LCS trap.
> 3. **Two rolling rows → O(min(m,n)) space,** with careful edge initialization.
>
> Memory peg — *"minimum edits between two strings"* → **Levenshtein grid: free on a match, else one plus the cheapest of replace, delete, insert.**

---

## 14. CLIFFHANGER — `12:40`
*(open loop to next lesson)*

**[VISUAL: blurred title — "Unique Paths". A robot at the corner of a grid.]**

> We've been filling grids where each cell reads three neighbors. Next, a grid so clean the recurrence is just **up plus left** — a robot counting paths across a board — and the space collapse becomes a single, almost magical line: `dp[j] += dp[j-1]`. A gentle grid to cement the pattern before we go harder. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
// O(min(m,n)) space — two rolling rows
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[] prev = new int[n + 1];
    for (int j = 0; j <= n; j++) prev[j] = j;      // base row
    for (int i = 1; i <= m; i++) {
        int[] curr = new int[n + 1];
        curr[0] = i;                                // base column
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                curr[j] = prev[j - 1];
            } else {
                curr[j] = 1 + Math.min(prev[j - 1], Math.min(prev[j], curr[j - 1]));
            }
        }
        prev = curr;
    }
    return prev[n];
}
```
