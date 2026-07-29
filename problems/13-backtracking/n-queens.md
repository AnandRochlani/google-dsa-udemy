# N-Queens

> **LeetCode:** 51. N-Queens · **Difficulty:** 🔴 Hard · **Pattern:** Subsets & Backtracking · **Google frequency:** medium

---

## Problem

Place `n` queens on an `n × n` chessboard so that **no two queens attack each other** — no two share a row, column, or diagonal. Return **all distinct board configurations**, each drawn as a list of strings using `'Q'` for a queen and `'.'` for empty.

**Example:** `n = 4` → 2 solutions:
```
[".Q..",      ["..Q.",
 "...Q",       "Q...",
 "Q...",       "...Q",
 "..Q."]       ".Q.."]
```

**Constraints that matter:** `1 ≤ n ≤ 9`. The number of solutions grows fast (e.g. `n=8` has 92) and the **output is exponential** — inherent to "return all configurations." The art is **aggressive pruning**: a naive "try all placements" explores `n^n` or worse; smart constraint tracking collapses the tree enormously.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Place queens somewhere on the board and check nothing attacks." But queens can't share a row, so **exactly one queen per row** — that's the key structural insight. Now the problem becomes: for row 0 pick a column, row 1 pick a column, ... row n-1 pick a column, such that no column or diagonal repeats. One decision per row → backtracking.

- **The decision tree mental model:** level `row` chooses which **column** the queen in that row occupies. Branching factor is `n` (columns), depth is `n` (rows). A **leaf at row == n** is a full valid placement. We prune any branch where the chosen column conflicts with a queen already placed.

- **The three conflict rules — and how to check them in O(1):** two queens at `(r1,c1)` and `(r2,c2)` attack iff same column (`c1==c2`), or same **↘ diagonal** (`r1-c1 == r2-c2`), or same **↙ anti-diagonal** (`r1+c1 == r2+c2`). So maintain three sets:
  - `cols` — occupied columns,
  - `diag1` — occupied `row - col` values (↘ diagonals),
  - `diag2` — occupied `row + col` values (↙ anti-diagonals).
  Placing a queen at `(row, col)` is legal iff `col`, `row-col`, `row+col` are all absent from their sets — an **O(1) check** instead of re-scanning the board.

- **Pruning is the whole game:** the moment a column is unsafe, we skip it — we never descend into a doomed subtree. Compared with placing then checking, the sets let us reject in constant time and prune before recursing.

- **The backtracking skeleton — same rhythm:** **CHOOSE** a safe column (add `col`, `row-col`, `row+col` to the three sets, record the queen), **RECURSE** to the next row, then **UN-CHOOSE** (remove all three, un-record) to try the next column.

- **Pattern trigger:** **"place N items under mutual constraints, find all valid layouts"** → backtracking with **constraint sets** for O(1) conflict checks and early pruning.

---

## ① Brute Force

The unpruned framing: place one queen per row by trying every column, and verify safety by **scanning all previously placed queens** each time (no sets, no diagonals precomputed).

```python
def solve_n_queens_brute(n):
    result = []
    queens = []                               # queens[row] = col

    def is_safe(row, col):
        for r in range(row):                  # re-scan every earlier queen
            c = queens[r]
            if c == col or abs(r - row) == abs(c - col):   # same col or diagonal
                return False
        return True

    def backtrack(row):
        if row == n:
            result.append(build_board(queens, n))
            return
        for col in range(n):
            if is_safe(row, col):             # O(row) check each time
                queens.append(col)            # CHOOSE
                backtrack(row + 1)            # RECURSE
                queens.pop()                  # UN-CHOOSE

    backtrack(0)
    return result

def build_board(queens, n):
    return ['.' * c + 'Q' + '.' * (n - c - 1) for c in queens]
```

**Why it's the natural first attempt:** "one queen per row, check it doesn't clash with earlier ones" is the direct model, and it's correct.

**Why we look further:** `is_safe` re-scans up to `row` queens on *every* placement attempt → an extra `O(n)` factor. We can make the safety check `O(1)` by remembering occupied columns and diagonals in sets, which also makes the choose/un-choose the single source of truth.

**Complexity:** Time `O(n! · n)` (the `!` from pruning down from `n^n`, `× n` for the scan), Space `O(n)` recursion + output.

---

## ② Optimised Solution

Three sets for O(1) conflict checks; add/remove them as the choose/un-choose.

```python
def solve_n_queens(n):
    result = []
    queens = []                               # queens[row] = col
    cols = set()                              # occupied columns
    diag1 = set()                             # occupied (row - col)  ↘
    diag2 = set()                             # occupied (row + col)  ↙

    def backtrack(row):
        if row == n:                          # placed a queen in every row → solution
            result.append(['.' * c + 'Q' + '.' * (n - c - 1) for c in queens])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue                      # PRUNE: attacked — skip this column
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

**Walk part of the decision tree** for `n = 4`:

```
row 0: try col 0 -> place (0,0)  cols={0} d1={0} d2={0}
  row 1: col 0 in cols? yes skip; col 1: (1-1)=0 in d1? yes skip;
         col 2 -> place (1,2)  ok
    row 2: cols={0,2}; col 0,2 taken; col 1: (2+1)=3 not seen, (2-1)=1 not seen -> place (2,1)? 
           check anti-diag (2+1=3): (0,0)->0,(1,2)->3  CONFLICT with (1,2) -> skip
           col 3: (2-3)=-1,(2+3)=5 free -> place (2,3)
      row 3: only col left is 1 -> (3-1)=2 free? (3+1)=4 free? but col 1 vs (2,3).. 
             (3,1): col1 free, d1=2 free, d2=4 free -> place -> row==4? no, need row3 done
             ... this branch dead-ends, backtrack
  ... eventually col 0 start yields no solution; backtrack
row 0: try col 1 -> place (0,1) ... leads to  [1,3,0,2]  ✅ (".Q..","...Q","Q...","..Q.")
row 0: try col 2 -> leads to  [2,0,3,1]  ✅
```

Each `continue` is a pruned branch we never enter; each successful placement adds to all three sets and is undone symmetrically on backtrack.

**Why it's correct:** every solution has one queen per row (enforced by recursing row-by-row). The three sets encode *exactly* the column/diagonal attack relations, so a placement passes iff it's safe against all prior queens. We try every column in every row, so no valid layout is skipped; the sets are restored on unwind, keeping state correct for sibling branches.

**Complexity:** Time `O(n!)` — first row `n` choices, next `≤ n-1` safe, etc., pruned well below `n^n`; the `build board` at each leaf is `O(n²)` but leaves are few. Space `O(n)` auxiliary (three sets + queens + recursion), plus output.

---

## ③ Space Optimization

The output holds every solution board (each `O(n²)`) — inherent.

**Output vs auxiliary space:** beyond the output, we use three sets and the `queens` list, each `O(n)` (at most `n` queens on the board at once), plus `O(n)` recursion depth → **auxiliary space `O(n)`**. Already lean.

**The bitmask trick** replaces the three sets with three integers, using bit `i` to mean "column/diagonal `i` occupied." Conflict check and update become bit operations — `O(1)` with tiny constant and `O(1)` extra space for the masks (still `O(n)` stack):

```python
def total_n_queens(n):                        # counts solutions; same idea builds boards
    count = 0
    def backtrack(row, cols, diag1, diag2):
        nonlocal count
        if row == n:
            count += 1
            return
        available = (~(cols | diag1 | diag2)) & ((1 << n) - 1)   # free columns as set bits
        while available:
            bit = available & (-available)    # lowest free column
            available ^= bit                  # mark it tried
            backtrack(row + 1, cols | bit,
                      (diag1 | bit) << 1,      # diagonals shift as we go down a row
                      (diag2 | bit) >> 1)
    backtrack(0, 0, 0, 0)
    return count
```

The masks are passed by value, so there's *no explicit un-choose* — each recursive call gets its own copy and the parent's masks are untouched. That's a slick variant to mention: *"I can pack the column and two diagonal sets into three bitmasks; the diagonals shift left/right by one as I move to the next row, and passing them by value means the backtrack undo is automatic."* Auxiliary space stays `O(n)` (the stack), but constants drop sharply — this is the standard way to push N-Queens to large `n`.

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space (aux) |
|---|---|---|
| Brute force (rescan safety) | O(n! · n) | O(n) |
| Constraint sets | O(n!) | O(n) |
| Bitmask | O(n!) (smaller constant) | O(n) stack |

---

## Say it out loud (interview narration)

> *"Since no two queens share a row, I place exactly one per row and only decide its column — that turns it into a clean row-by-row backtrack. For O(1) safety checks I keep three sets: occupied columns, occupied `row−col` diagonals, and occupied `row+col` anti-diagonals. At each row I try every column, skip any that hits a set — that's the prune — otherwise I add the three keys, recurse to the next row, then remove them to try the next column. When I've filled all n rows I record the board. Time is roughly O(n!) after pruning; auxiliary space is O(n). To go faster I'd pack those three sets into bitmasks, shifting the diagonal masks by one each row, so the undo is automatic since they're passed by value."*

## Related / follow-ups
- **N-Queens II** (LC 52 — just *count* solutions; drop the board building, ideal for the bitmask form)
- **Sudoku Solver** (LC 37 — grid backtracking with row/col/box constraint sets)
- **Combination Sum / Subsets** (same choose→recurse→un-choose skeleton, simpler constraints)
- **Permutations** (LC 46 — N-Queens columns are essentially a pruned permutation)
