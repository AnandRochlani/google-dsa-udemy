# 🎬 Recording Script — Search a 2D Matrix (Flatten the Index)
**Pattern: Modified Binary Search · LeetCode 74 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the canonical `[lo, hi]` value-search template (LC 704). We reuse it verbatim — plus one index trick.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a 3×4 grid of sorted numbers. A red tag: "O(log(m·n)) required." A finger hovers, unsure whether to scan rows or columns.]**

> An Google favorite: here's a grid, find a number, in O(log of m times n). Your brain freezes — binary search is a *line* thing, and this is a *grid*. Two dimensions. Do I search rows? Columns? Both?
>
> People burn the whole interview building a clumsy row-then-column search. But this grid is hiding something: read it the right way and it's not a grid at all — it's **one straight sorted list** in disguise. By the end you'll run the plain LC 704 template on it, untouched, with a single line of index arithmetic. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: the matrix, rows and the "first-of-next-row > last-of-this-row" links highlighted with arrows.]**

```
[ 1,  3,  5,  7]
[10, 11, 16, 20]
[23, 30, 34, 60]
```

> One line: **each row is sorted left-to-right, and every row starts higher than the previous row ended — is `target` in the grid?** We'll hunt for `3`.
>
> Read those two rules together and watch: `7` then `10`, `20` then `23`. It never dips. Follow the rows end to end and the numbers just keep climbing: `1,3,5,7,10,11,16,20,23,30,34,60`. Hold that — the grid is *already* one sorted line.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: a marker snakes cell by cell through all 12 cells; "looks" counter ticks up to 2.]**

> Brute force: scan every cell. `1`? no. `3`? yes — found at row 0, col 1. Cheap here, twelve cells.
>
> But that's O(m·n) — every cell in the worst case. And it ignores *both* sorted guarantees. Even the "smarter" version — scan down to find the right row, then binary-search that row — still pays O(m) just to pick the row.
>
> **[VISUAL: grid grows to 100×100; the snake crawls across thousands of cells.]**
>
> Ten thousand cells, up to ten thousand looks. The O(log) demand says: stop treating the shape as a grid.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: the 12 values lifted out of the grid and laid in a single row `1 3 5 7 10 11 16 20 23 30 34 60`, indices `0..11` under them. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the whole grid poured into a line — one sorted array, indices 0 to 11. On *this*, you already know the O(log n) answer: binary search. Pause and predict: **I don't want to actually build this line — it wastes memory. If binary search hands me flat index 5, how do I figure out which row and column that is in the original 3×4 grid, without the line existing?**
>
> **LEARNER:** Hmm. Four columns per row… so index 5 is past one full row of 4, into the second row. Row 1, and then position 1 within it? So row `5 // 4`, column `5 % 4`?
>
> **TEACHER:** That's it — you just derived the entire trick. Divide and mod by the column count. Let's make it precise.

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: flat index 5 → arrow → `row = 5 // 4 = 1`, `col = 5 % 4 = 1` → the cell holding `11` lights up in the grid. lo/mid/hi markers ride the virtual line above the grid.]**

> Analogy: a bookshelf. Books numbered 0, 1, 2… left to right, top shelf then next shelf down. Book number 5, with 4 books per shelf? Shelf `5 // 4 = 1`, position `5 % 4 = 1`. You never re-shelve anything — you *compute* where book 5 sits.
>
> Same move here. Pretend there's a flat array of indices `0 … m·n − 1`. Binary-search *that*, exactly like LC 704 — `lo`, `mid`, `hi`, discard a half each step. The only new line: when you need the value at flat index `i`, decode it — **`row = i // n`, `col = i % n`**, where `n` is the number of **columns**. Read `matrix[row][col]`. No line ever gets built.
>
> **[VISUAL: mid at flat index 5 → value 11 > target 3 → the right half of the virtual line (indices 6–11) greys out; hi drops to 4.]**
>
> `mid` = flat 5 = value `11`. Target `3`. `11 > 3`, so the whole right half is gone — six cells deleted in one peek. That's binary search on a grid.

---

## 6. THE KEY MOVE (signaling) — `4:15`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Globally sorted grid = one flat sorted array. Binary-search indices 0…m·n−1; decode mid with row = mid // n, col = mid % n."]**

> The one line: **a globally-sorted grid is a flat sorted array — search the virtual index and decode each mid with `// n` and `% n`.** The *logical* shape (one sorted list) beats the *physical* shape (a grid). That reframing is the reusable skill.

---

## 7. CODE IT — LIVE & CHUNKED — `4:50`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Grab the dimensions, and set the bounds over the *virtual flat indices*.

```python
def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])   # rows, cols
    lo, hi = 0, m * n - 1                 # inclusive flat-index window
```

> **[VISUAL: add chunk 2, highlight the decode line.]** The identical LC 704 loop — with one decode line.

```python
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        val = matrix[mid // n][mid % n]   # decode flat index → (row, col)
```

> **[VISUAL: add chunk 3 — the untouched three-way branch.]** Same three-way discard as the canonical template.

```python
        if val == target:
            return True
        elif val < target:
            lo = mid + 1                  # drop left half + mid
        else:
            hi = mid - 1                  # drop right half + mid
    return False
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:15`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight `mid // n` and `mid % n`. A tiny 3×4 grid animates the decode for a couple of indices.]**

> Everything here is LC 704 except one line, so let's zoom on it. `mid // n` — integer-divide the flat index by the number of **columns** — gives the row. `mid % n` — the remainder — gives the column. Divide by `n`, the width, because each row *is* `n` wide; you're asking "how many full rows fit under me, and how far into the next one?"
>
> **LEARNER:** Why `n`, the columns? My gut wants to divide by `m`, the number of rows. How do I never mix that up?
>
> **TEACHER:** That's *the* classic slip, so here's the mnemonic: you divide by the length of the thing you're stepping *along*. You walk along rows, and a row is `n` cells wide, so you divide by `n`. Sanity-check it with a corner: the last valid flat index is `m·n − 1`. Decode it — row `(m·n−1) // n = m−1`, the last row; col `(m·n−1) % n = n−1`, the last column. Bottom-right corner, exactly right. If you'd used `m`, that check blows up. Always test the decode on a corner.
>
> **TEACHER:** Everything else — inclusive bounds, `lo <= hi`, `mid ± 1` — is the template you already own. We didn't reinvent binary search; we taught one integer to pretend it's two.

---

## 9. DRY-RUN THE CODE — `7:30`
*(worked example — prove it, close the loop)*

**[VISUAL: virtual line indices 0–11 above the grid; trace table; discarded half greys each row.]**

> Real code, `target = 3`, `m = 3`, `n = 4`, flat range `[0, 11]`.

| lo | hi | mid | mid//4, mid%4 | val | action |
|---|---|---|---|---|---|
| 0 | 11 | 5 | (1, 1) | 11 | 11 > 3 → hi = 4 |
| 0 | 4 | 2 | (0, 2) | 5 | 5 > 3 → hi = 1 |
| 0 | 1 | 0 | (0, 0) | 1 | 1 < 3 → lo = 1 |
| 1 | 1 | 1 | (0, 1) | 3 | 3 == 3 → **return True** ✅ |

> Four peeks over twelve cells, each decode landing on the right cell. Try `target = 13` at home — you'll watch `lo` cross `hi` and return `False`. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:30`
*(transfer to interview)*

**[VISUAL: rows — Scan cells: O(m·n). Row-find + row search: O(m + log n). Ours: O(log(m·n)), O(1) space.]**

> Say it: *"The two guarantees mean the whole grid is one sorted list read row by row. So I binary-search a virtual flat index 0 to m·n−1, decoding each mid with row = mid // n, col = mid % n. That's the standard template plus one line — O(log(m·n)) time, O(1) space, and I never actually flatten anything."* Naming that you *avoided* building the flat array is the strong-hire detail.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:05`
*(depth + honesty)*

**[VISUAL: a crossed-out `flat = [x for row in matrix for x in row]` (O(m·n) memory) beside the on-the-fly decode.]**

> Already O(1). And here's the honesty beat: you *could* physically flatten the matrix into a real list — but that's O(m·n) time *and* space just to set up, defeating the entire point. Computing `mid // n, mid % n` on demand gives the value for free. Say that out loud: "I decode instead of flatten, so it stays O(1)."

---

## 12. YOUR TURN (active recall) — `9:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Search a 2D Matrix II (LC 240)". A grid where rows AND columns are sorted, but NOT globally.]**

> Before next time, try **Search a 2D Matrix II**. Careful — it *looks* the same but the global-order guarantee is gone: rows and columns are each sorted, yet the flatten trick breaks. You'll need a different move — start from a corner and eliminate a row or column each step. Feel *why* today's trick fails there; that contrast is the lesson.

---

## 13. LOCK IT IN — `10:10`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **Two ordering guarantees → the grid is one flat sorted array.**
> 2. **Binary-search indices `0 … m·n − 1`; decode `row = mid // n`, `col = mid % n`.**
> 3. **Divide by columns `n`, not rows** — corner-test the decode to be sure.
>
> The peg — a **globally sorted grid is a line pretending to be a grid.** Flatten the *index*, not the data.

---

## 14. CLIFFHANGER — `10:45`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Koko Eating Bananas" — piles of bananas, a clock, and a mystery number `k` with a `?`.]**

> Every problem so far, we searched *inside* the data — an array, a grid, versions. Next, we do something that feels illegal: we binary-search over an **answer that isn't in any array at all** — a speed, a number we invent. No array to peek at. If your gut says "you can't binary-search something that isn't there" — good. Watch us do it anyway. That's next.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public boolean searchMatrix(int[][] matrix, int target) {
    int m = matrix.length, n = matrix[0].length;
    int lo = 0, hi = m * n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int val = matrix[mid / n][mid % n];    // decode flat index (divide by columns)
        if (val == target) return true;
        else if (val < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return false;
}
```
