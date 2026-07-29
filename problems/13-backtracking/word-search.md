# Word Search

> **LeetCode:** 79. Word Search · **Difficulty:** 🟡 Medium · **Pattern:** Subsets & Backtracking · **Google frequency:** ⭐ high

---

## Problem

Given an `m × n` grid of characters `board` and a string `word`, return `true` if `word` can be **constructed from letters of sequentially adjacent cells**, where "adjacent" means horizontally or vertically neighboring. **The same cell may not be used more than once** within a single word.

**Example:** `board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]`, `word = "ABCCED"` → `true` *(path A(0,0)→B(0,1)→C(0,2)→C(1,2)→E(2,2)→D(2,1)).* `word = "ABCB"` → `false` *(the second B would reuse cell (0,1)).*

**Constraints that matter:** `1 ≤ m, n ≤ 6`, `1 ≤ word.length ≤ 15`. Small grid, but every cell is a potential start, and from each we branch up to 4 directions per letter → the search is exponential in `word.length` (`O(m·n·4^L)`). This is the **grid** flavor of backtracking: the "path" is a trail through the board, and the un-choose is *un-marking the visited cell.*

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Find where the first letter appears, then walk to a neighbor matching the second letter, and so on." From any cell you can go up/down/left/right. When one direction dead-ends, back up and try another — that "walk, dead-end, back up, try another" is backtracking on a grid.

- **The decision tree mental model:** the root tries each cell as the starting square. From a cell matching `word[k]`, you branch into up to 4 neighbors, each an attempt at `word[k+1]`. A **success leaf** is reaching `k == len(word)` (matched every letter). **Dead branches**: the cell is out of bounds, its letter ≠ `word[k]`, or it's already on the current path.

- **The visited constraint — the crux:** "same cell can't be reused" means each cell in the current trail is off-limits to the rest of that trail. We mark a cell as visited when we step onto it and **un-mark it when we back out** — that un-mark *is* the un-choose. Miss it and you'd either forbid reusing a cell in a *different* path (wrong) or corrupt the board permanently.

- **The in-place visited trick:** instead of a separate `visited` set, temporarily overwrite `board[r][c]` with a sentinel like `'#'` while we're standing on it, then restore the original letter on the way back. Zero extra grid-sized memory. (A `visited` boolean grid is the equally-valid explicit alternative.)

- **Pruning:** the `word[k]` letter check *is* the prune — if the current cell doesn't match the needed letter, cut the branch instantly. Reaching the word's end short-circuits everything with `True`.

- **The backtracking skeleton — same rhythm:** **CHOOSE** to step onto a cell (mark visited), **RECURSE** into its 4 neighbors for the next letter, then **UN-CHOOSE** (restore the cell) so other paths can use it.

- **Pattern trigger:** **"find a path/word in a grid by moving to neighbors, no cell reused"** → DFS backtracking with mark/restore of visited cells.

---

## ① Brute Force

Even the "brute force" here *is* backtracking — there's no filter-everything alternative. The naive framing is: **without a visited guard**, or exploring every cell/direction blindly. Below is a version that uses a *separate* `visited` set (correct, just heavier) and no early letter check beyond the base — the honest baseline before we tighten it.

```python
def exist_brute(board, word):
    rows, cols = len(board), len(board[0])
    visited = set()

    def dfs(r, c, k):
        if k == len(word):
            return True
        if (r < 0 or r >= rows or c < 0 or c >= cols
                or (r, c) in visited or board[r][c] != word[k]):
            return False
        visited.add((r, c))                   # CHOOSE (mark visited)
        found = (dfs(r+1, c, k+1) or dfs(r-1, c, k+1)
                 or dfs(r, c+1, k+1) or dfs(r, c-1, k+1))
        visited.remove((r, c))                # UN-CHOOSE (unmark)
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
```

**Why it's the natural first attempt:** it directly encodes "try each start, walk to matching neighbors, don't reuse cells."

**Why we look further:** it's correct, but the `visited` **set** costs `O(L)` hashing and extra memory. Since the board is fungible, we can mark visited *in place* by mutating the cell — same logic, `O(1)` extra memory, faster.

**Complexity:** Time `O(m · n · 4^L)`, Space `O(L)` for the visited set + recursion.

---

## ② Optimised Solution

Mark visited **in place** with a sentinel, restore on the way out.

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def dfs(r, c, k):
        if k == len(word):
            return True                       # matched every letter
        if (r < 0 or r >= rows or c < 0 or c >= cols
                or board[r][c] != word[k]):    # out of bounds or letter mismatch → prune
            return False

        temp = board[r][c]
        board[r][c] = '#'                     # CHOOSE: mark visited in place
        found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1)
                 or dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
        board[r][c] = temp                    # UN-CHOOSE: restore the letter

        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
```

**Walk part of the search** for `word = "ABCCED"` starting at `(0,0)`:

```
dfs(0,0,'A') match -> mark '#'
  dfs(0,1,'B') match -> mark '#'
    dfs(0,2,'C') match -> mark '#'
      dfs(1,2,'C') match -> mark '#'
        dfs(2,2,'E') match -> mark '#'
          dfs(2,1,'D') match -> mark '#'
            k==6 == len(word) -> return True  ✅ (unwinds, restoring each cell)
```

The `'#'` marks stop the search from stepping back onto the trail (e.g. from the second C back to the first). Each `return` restores the cell, so a *different* starting attempt sees a clean board.

**Why it's correct:** the in-place `'#'` guarantees no cell is reused *within the current path* (a `'#'` never equals `word[k]`, so it fails the match check). Restoring on unwind means the visited-state is scoped exactly to the live trail — sibling searches are unaffected. Trying every start cell means no valid placement is missed. The letter check prunes mismatches immediately.

**Complexity:** Time `O(m · n · 4^L)` — `m·n` starts, branching ~4 (really 3 after the first, since you don't revisit where you came from) to depth `L`. Space `O(L)` recursion depth, `O(1)` extra beyond the board.

---

## ③ Space Optimization

This *is* the space-optimized version. The teaching point is **auxiliary space**:

- **A `visited` boolean grid** costs `O(m · n)` extra memory.
- **A `visited` set of coordinates** costs `O(L)` (only cells on the current path).
- **The in-place `'#'` sentinel** costs `O(1)` extra — we reuse the board itself, restoring on backtrack.

So the in-place trick drops auxiliary space to just the **recursion stack, `O(L)`** (bounded by the word length, since the path can't be longer than the word). There's no separate output to store — the answer is a single boolean. Say it: *"I mark visited by overwriting the cell in place and restore it when I back out, so my only extra memory is the O(L) call stack — no visited grid, no set."*

Caveat worth voicing: mutating the input isn't always allowed (concurrent readers, immutability contracts). If the interviewer forbids it, fall back to the `O(L)` visited set.

---

## Java (for Java interviewers)

```java
public boolean exist(char[][] board, String word) {
    int rows = board.length, cols = board[0].length;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            if (dfs(board, word, r, c, 0)) return true;
    return false;
}

private boolean dfs(char[][] board, String word, int r, int c, int k) {
    if (k == word.length()) return true;
    if (r < 0 || r >= board.length || c < 0 || c >= board[0].length
            || board[r][c] != word.charAt(k)) return false;

    char temp = board[r][c];
    board[r][c] = '#';                                // CHOOSE: mark visited
    boolean found = dfs(board, word, r + 1, c, k + 1)
                 || dfs(board, word, r - 1, c, k + 1)
                 || dfs(board, word, r, c + 1, k + 1)
                 || dfs(board, word, r, c - 1, k + 1);
    board[r][c] = temp;                               // UN-CHOOSE: restore
    return found;
}
```

---

## Complexity Summary

| Approach | Time | Space (aux) |
|---|---|---|
| DFS + visited set | O(m · n · 4^L) | O(L) set + O(L) stack |
| DFS + in-place mark | O(m · n · 4^L) | O(L) stack only |

*(L = word length.)*

---

## Say it out loud (interview narration)

> *"I try every cell as a starting point, then DFS to neighbors that match the next letter. The catch is a cell can't be reused in one path, so when I step onto a cell I mark it — I overwrite it with '#' in place — recurse into the four neighbors, then restore the original letter when I back out. That mark-then-restore is the backtracking un-choose, and it scopes 'visited' exactly to the current trail. The letter mismatch is my prune, and reaching the end of the word short-circuits to true. Time is O(m·n·4^L); auxiliary space is just the O(L) recursion stack because I reuse the board instead of a visited set. If mutating the input is off-limits, I'd swap in an O(L) visited set."*

## Related / follow-ups
- **Word Search II** (LC 212 — many words at once; build a Trie so shared prefixes prune together)
- **Number of Islands** (LC 200 — grid DFS, but flood-fill without needing to un-mark)
- **Robot / path-in-grid problems** (same 4-direction DFS skeleton)
- **Sudoku Solver** (LC 37 — grid backtracking with constraint checks)
