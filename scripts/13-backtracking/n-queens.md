# 🎬 Recording Script — N-Queens
**Pattern: Backtracking · LeetCode 51 · Hard · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the full skeleton — choose→recurse→un-choose, `used`-style tracking, and *pruning* — from every video in this folder. This is the capstone.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beats with no dialogue are single TEACHER voice.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an 8×8 chessboard. Queens drop randomly; attack lines flare red across rows, columns, diagonals, colliding everywhere. Title: "Place N queens so none attack. How many ways?"]**

> **TEACHER:** The classic. Place n queens on an n-by-n board so that *no two attack each other* — no shared row, no shared column, no shared diagonal. Return every valid arrangement.
>
> This is the Hard one, and it *looks* terrifying — queens attack in every direction. But here's the secret: it's the exact same skeleton you've built up over six videos — choose, recurse, un-choose — plus the sharpest pruning we've done yet, checking three constraints in *constant time*. By the end, this "hard" problem will feel like an old friend wearing a crown. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: a 4×4 board. The two solutions drawn side by side: .Q.. / ...Q / Q... / ..Q.  and  ..Q. / Q... / ...Q / .Q..]**

> One line: **every way to place n non-attacking queens**, each board drawn with `Q` and `.`.
>
> Let's use n = 4 — small enough to hold in your head. It has exactly *two* solutions. There they are. Notice in each: every row has one queen, every column has one queen, and no two sit on a shared diagonal. Two valid boards. Hold that number.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — let them feel the waste)*

**[VISUAL: a 4×4 board; a queen tries every one of 16 squares for placement 1, then every remaining square for placement 2… a counter of "arrangements to check" spins toward the thousands.]**

> The brute-force instinct: try placing queens on *any* squares, then check nothing attacks. Sixteen squares for the first queen, fifteen for the next… that's a combinatorial explosion — thousands of arrangements for a tiny 4×4, and it detonates for larger n.
>
> **[VISUAL: highlight two queens landing in the same row — an obvious clash that we only catch AFTER placing.]**
>
> But look — a huge share of those are instantly, *obviously* illegal: two queens in the same row. We're generating those doomed layouts and only rejecting them afterward. There's massive structure we're ignoring.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on two queens sharing row 2, stamped illegal. Then a spotlight on the word "ROW". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste screams a structural fact we've been ignoring: **no two queens can share a row.** So in a valid board, each of the n rows holds *exactly one* queen. Placing two in a row is a whole category of arrangements we should never even generate.
>
> **LEARNER:** Okay — so is this basically permutations? One queen per row, and we're really just choosing a *column* for each row… that's picking an ordering of columns, isn't it?
>
> **TEACHER:** *Exactly* the right instinct — it's a pruned permutation of columns. That collapses the problem enormously. Pause and predict: **if I go row by row and only decide the column, columns are easy to keep distinct — but how do I check the two *diagonal* attacks fast, without re-scanning the whole board every time?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a decision tree. Level = row; each level branches over columns 0..n-1. Depth n. A leaf at row==n is a full board. Branches that conflict are pruned (grayed).]**

> **TEACHER:** Restructure with the row insight. Level `row` of our tree decides *which column* the queen in that row takes. Branching factor n — the columns. Depth n — the rows. A leaf at `row == n` means we placed a queen in every row: a complete board. That's our familiar tree.
>
> Now, the three ways two queens attack, and how to check each in *O(1)*. Two queens at `(r1,c1)` and `(r2,c2)` clash if:
> - **Same column:** `c1 == c2`.
> - **Same ↘ diagonal:** here's the gem — on a "down-right" diagonal, `row - col` is *constant*. So `r1 - c1 == r2 - c2`.
> - **Same ↙ anti-diagonal:** on a "down-left" diagonal, `row + col` is constant. So `r1 + c1 == r2 + c2`.
>
> **[VISUAL: overlay the board with row−col labels on one diagonal (all equal) and row+col on the other (all equal). Lightbulb.]**
>
> So we keep **three sets**: occupied columns, occupied `row − col` values, occupied `row + col` values. Placing a queen at `(row, col)` is legal if and only if `col`, `row−col`, and `row+col` are *all absent* from their sets. That's a constant-time safety check — no board re-scan.
>
> **[VISUAL: hand walks down: choose col for row 0 (add 3 keys to the sets), row 1, row 2… hits a conflict, backs up, removes the keys, tries the next column.]**
>
> And the rhythm is what it's always been. **CHOOSE**: pick a safe column — add `col`, `row−col`, `row+col` to the three sets, record the queen. **RECURSE**: next row. **UN-CHOOSE**: remove all three keys and un-record, so the next column starts clean. The pruning — skipping any column that hits a set — is the whole game: we never descend into a doomed board.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: one boxed line: "One queen per row → pick a column. Three sets: cols, row−col (↘), row+col (↙). Safe = all three free."]**

> The line to burn in: **one queen per row, pick its column; a placement is safe when its column, its `row−col` diagonal, and its `row+col` anti-diagonal are all free.** Three sets, three O(1) checks. That's the entire trick.

---

## 7. CODE IT — LIVE & CHUNKED — `5:45`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Build it. Setup — where solutions go, the queen columns, and the three constraint sets.

```python
def solve_n_queens(n):
    result = []
    queens = []                           # queens[row] = col
    cols = set()                          # occupied columns
    diag1 = set()                         # occupied (row - col)  ↘
    diag2 = set()                         # occupied (row + col)  ↙
```

> **[VISUAL: add chunk 2, highlight the leaf building a board.]** The walker is indexed by `row`. When it fills all n rows, render the board.

```python
    def backtrack(row):
        if row == n:                      # a queen in every row → solution
            result.append(['.' * c + 'Q' + '.' * (n - c - 1) for c in queens])
            return
```

> **[VISUAL: add chunk 3, highlight the prune — the `continue`.]** Try each column; skip any that's attacked. This is the prune.

```python
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue                  # PRUNE: attacked — skip this column
```

> **[VISUAL: add chunk 4, highlight the symmetric choose / un-choose.]** Choose — add to all three sets. Recurse. Un-choose — remove all three.

```python
            # CHOOSE
            queens.append(col)
            cols.add(col); diag1.add(row - col); diag2.add(row + col)
            # RECURSE
            backtrack(row + 1)
            # UN-CHOOSE
            queens.pop()
            cols.discard(col); diag1.discard(row - col); diag2.discard(row + col)

    backtrack(0)
    return result
```

> Look at the choose and un-choose — three adds going in, three removes coming out, perfectly mirrored. That symmetry is your correctness guarantee.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:45`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight each line, especially the diagonal formulas.]**

> The *why*.
>
> Recursing by `row` bakes in "one queen per row" — a whole class of illegal boards can't even be expressed. That's the permutation insight made structural.
>
> `(row - col) in diag1` and `(row + col) in diag2` — these two formulas are the heart. Every square on a ↘ diagonal shares the same `row − col`; every square on a ↙ anti-diagonal shares the same `row + col`. So membership in a set *is* the diagonal-attack test — no scanning, O(1).
>
> **LEARNER:** Wait — why *three* separate sets? Couldn't one set of occupied `(row, col)` squares do the job?
>
> **TEACHER:** A set of squares would tell you if a *square* is taken — but a queen attacks along entire lines, not single squares. You'd still have to scan the whole diagonal to check for a clash. The genius of `row−col` and `row+col` is that it collapses each *entire diagonal* to a *single number*. Checking one number against a set is O(1); scanning a diagonal is O(n). Three sets, three numbers, three constant-time checks — that's the upgrade from the brute-force re-scan.
>
> And the un-choose removes all three keys. Forget even one — say you pop the column but leave `row−col` in `diag1` — and a phantom queen haunts that diagonal, silently blocking legal placements in sibling branches. All three, every time.

---

## 9. DRY-RUN THE CODE — `9:00`
*(worked example — prove it, close the loop)*

**[VISUAL: 4×4 board; hand places queens row by row, sets updating; conflicts flash and prune; a solution locks in.]**

> Trace n = 4. Columns 0 to 3.

```
row 0: place (0,0)  cols={0} diag1={0} diag2={0}
  row 1: col 0 → in cols, skip. col 1 → row−col = 0 in diag1, skip.
         col 2 → free → place (1,2)
    row 2: col 1 → row+col = 3 in diag2 (from (1,2)), skip.
           col 3 → free → place (2,3)
      row 3: every column attacked → dead end, back up ✂
    … col-0 start yields nothing → backtrack, remove keys
row 0: place (0,1) → … → columns [1,3,0,2] → SOLUTION ✅  (.Q.. / ...Q / Q... / ..Q.)
row 0: place (0,2) → … → columns [2,0,3,1] → SOLUTION ✅  (..Q. / Q... / ...Q / .Q..)
row 0: place (0,3) → mirror of col-0 start → nothing
```

> Every `continue` is a branch we never entered. Starting from column 0 dead-ends and we cleanly unwind — removing every key — before column 1 succeeds. Two solutions, exactly the two we promised. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `10:15`
*(transfer to interview)*

**[VISUAL: "Brute (rescan): O(n!·n)." "Constraint sets: O(n!)." "Output: all boards, each O(n²)."]**

> Out loud: *"Row 0 has n column choices, row 1 has at most n−1 that survive the prune, row 2 fewer still — so the search is bounded around n-factorial, pruned way below the naive n-to-the-n. The brute force pays an extra factor of n to re-scan for safety; my three sets make each check O(1), so I shave that factor off. Building each solution board is O(n²), but there are few leaves. The output — all valid boards — is inherent."*
>
> The story arc interviewers love: *n-to-the-n → n-factorial via the one-queen-per-row insight → same n-factorial but a factor of n cheaper per node via constraint sets.* Tell it as a story.

---

## 11. CAN WE USE LESS MEMORY? (space) — `11:15`
*(depth + honesty — output vs auxiliary + the bitmask trick)*

**[VISUAL: box "OUTPUT: all boards, each O(n²) — inherent." box "AUXILIARY: O(n) — three sets + queens + stack." Then three bitmasks shifting.]**

> Output versus auxiliary. Output stores every solution board — inherent. Auxiliary: three sets plus the `queens` list, each `O(n)` (at most n queens on the board), plus `O(n)` recursion depth → `O(n)`. Already lean.
>
> Now the slick variant — the **bitmask** trick. Replace the three sets with three *integers*, where bit `i` means "column or diagonal `i` occupied." Conflict checks and updates become bit operations.

```python
def total_n_queens(n):                    # counts solutions; same idea builds boards
    count = 0
    def backtrack(row, cols, diag1, diag2):
        nonlocal count
        if row == n:
            count += 1
            return
        available = (~(cols | diag1 | diag2)) & ((1 << n) - 1)   # free columns as set bits
        while available:
            bit = available & (-available)  # lowest free column
            available ^= bit                # mark it tried
            backtrack(row + 1, cols | bit,
                      (diag1 | bit) << 1,    # diagonals SHIFT as we descend a row
                      (diag2 | bit) >> 1)
    backtrack(0, 0, 0, 0)
    return count
```

> The beautiful part: the diagonal masks *shift* by one each row — going down a row moves every diagonal threat one column over — so the geometry falls out of a bit-shift. And because the masks are passed *by value*, **there's no explicit un-choose** — each call gets its own copy, the parent's untouched. The undo is automatic.
>
> Say it: *"I can pack the column and two diagonal sets into three bitmasks; the diagonals shift left and right by one as I move to the next row, and passing them by value makes the backtrack undo automatic."* Auxiliary space stays `O(n)` — the stack — but the constants collapse. This is how you push N-Queens to large n.

---

## 12. YOUR TURN (active recall) — `12:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Sudoku Solver (LC 37)". A 9×9 grid, some cells filled.]**

> Try **Sudoku Solver** — fill a 9×9 grid so every row, column, and 3×3 box has 1–9. It's N-Queens' sibling: instead of column-and-two-diagonals, you track *row, column, and box* constraint sets, and backtrack cell by cell. Same choose-recurse-un-choose, three constraint sets, aggressive pruning. If N-Queens clicked, this is your victory lap.

---

## 13. LOCK IT IN — `13:10`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **One queen per row** turns it into a pruned permutation of columns.
> 2. **`row−col` and `row+col` collapse each diagonal to one number** — O(1) safety via three sets.
> 3. **Un-choose removes *all three* keys** — miss one and a phantom queen corrupts sibling branches.
>
> The peg: **a diagonal is a single number.** The moment you see "no two on a diagonal," reach for `row−col` and `row+col`.

---

## 14. CLIFFHANGER — `13:45`
*(open loop — close the whole unit)*

**[VISUAL: all seven problem thumbnails — Subsets, Permutations, Combination Sum, Letter Combinations, Generate Parentheses, Word Search, N-Queens — snap together around one glowing core: "CHOOSE → RECURSE → UN-CHOOSE".]**

> Step back and look at what you built. Seven problems — subsets, permutations, combination sum, phone letters, parentheses, a word in a grid, and queens on a board — and *every single one* was the same three-beat skeleton: choose, recurse, un-choose, a depth-first walk of a decision tree, with pruning to cut the branches that can't win.
>
> That's the whole point of this unit: backtracking isn't seven tricks, it's *one* trick wearing seven costumes. Next unit, we leave exhaustive search behind — because for some of these, we don't need *every* answer, just the *best* one, and re-walking the whole tree is too slow. That's where **dynamic programming** picks up. The decision tree stays; we learn to stop re-computing it. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public List<List<String>> solveNQueens(int n) {
    List<List<String>> result = new ArrayList<>();
    int[] queens = new int[n];                        // queens[row] = col
    Set<Integer> cols = new HashSet<>(), d1 = new HashSet<>(), d2 = new HashSet<>();
    backtrack(0, n, queens, cols, d1, d2, result);
    return result;
}

private void backtrack(int row, int n, int[] queens,
                       Set<Integer> cols, Set<Integer> d1, Set<Integer> d2,
                       List<List<String>> result) {
    if (row == n) {
        List<String> board = new ArrayList<>();
        for (int r = 0; r < n; r++) {
            char[] line = new char[n];
            Arrays.fill(line, '.');
            line[queens[r]] = 'Q';
            board.add(new String(line));
        }
        result.add(board);
        return;
    }
    for (int col = 0; col < n; col++) {
        if (cols.contains(col) || d1.contains(row - col) || d2.contains(row + col)) continue; // PRUNE
        queens[row] = col;                            // CHOOSE
        cols.add(col); d1.add(row - col); d2.add(row + col);
        backtrack(row + 1, n, queens, cols, d1, d2, result);   // RECURSE
        cols.remove(col); d1.remove(row - col); d2.remove(row + col); // UN-CHOOSE
    }
}
```
