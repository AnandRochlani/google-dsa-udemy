# 🎬 Recording Script — Word Search
**Pattern: Backtracking · LeetCode 79 · Medium · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the choose→recurse→un-choose skeleton; the *in-place mark/restore* idea echoes the swap-back from **Permutations**.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beats with no dialogue are single TEACHER voice.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a 3×4 letter grid. A snaking arrow tries to spell "ABCCED", weaving between cells. Title: "Is this word hiding in the grid?"]**

> **TEACHER:** A grid of letters, and a word. Can you spell the word by walking cell to cell — up, down, left, right — never stepping on the same cell twice?
>
> This is backtracking's *grid* form, and it's a favorite at Google because one detail trips almost everyone: the "no cell twice" rule. Get the un-choose wrong and you'll either corrupt the board forever or block cells you shouldn't. By the end you'll handle it with a one-character trick and zero extra memory. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: board `[[A,B,C,E],[S,F,C,S],[A,D,E,E]]`. Word "ABCCED" traced: A(0,0)→B(0,1)→C(0,2)→C(1,2)→E(2,2)→D(2,1). Below: "ABCB → false".]**

> One line: **can the word be spelled along adjacent cells, no cell reused?**
>
> Our board, and the word "ABCCED". There's the path — A to B to C, down to the second C, down to E, left to D. True. But "ABCB"? False — the second B would have to reuse the cell we already stood on. That reuse ban is the crux.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — build the shape)*

**[VISUAL: from cell A(0,0), four arrows fan out to neighbors. Only the one matching the next letter 'B' survives; the rest die.]**

> Here's the natural idea. Find where the first letter lives, then walk to a neighbor holding the second letter, then its neighbor for the third, and so on.
>
> **[VISUAL: hand steps A→B→C→C→E→D, matching each letter; at each cell four directions are tried, mismatches pruned instantly.]**
>
> From any cell you can go four directions. If a direction's letter doesn't match what you need next, that branch is dead — prune it. If a direction dead-ends deeper in, back up and try another. Walk, dead-end, back up, try another — that's backtracking on a grid.
>
> And since the word could start anywhere, we try *every* cell as a launch point.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: a path curls back toward a cell it already used; a red loop forms — the word "AAAA" spelled by bouncing on one cell. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the trap. Nothing yet stops the path from stepping *back* onto a cell it already used. Imagine the word "ABAB" — the walker could bounce B, A, B, A between two cells forever, or reuse one cell to fake a match. The "no cell twice" rule isn't decoration; without it the whole thing is wrong.
>
> **LEARNER:** So just keep a `visited` set of coordinates, add a cell when I step on, check it before moving. Done, right?
>
> **TEACHER:** That works and it's correct — but it costs a whole extra set, with hashing on every step. Pause and predict: **the board is already sitting right there in memory. Could I mark a cell as "currently standing on it" using the board *itself*, and un-mark it on the way back — no separate set at all?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a decision tree rooted at a start cell; each node branches into ≤4 neighbor cells. Dead branches: out of bounds, letter mismatch, already-on-path. Success leaf: k == len(word).]**

> **TEACHER:** Draw the tree. The root tries each start cell. From a matching cell, you branch into up to four neighbors, each an attempt at the next letter. A **success leaf** is reaching the end of the word — every letter matched. **Dead branches**: off the board, wrong letter, or a cell already on your current trail.
>
> Now the trick for that last one. When you step onto a cell, **overwrite it in place** with a sentinel — say `'#'`. While you're standing there, that cell reads as `'#'`, which never matches any real letter, so the search *can't* step back onto it. Then, on the way back out, you **restore** the original letter.
>
> **[VISUAL: hand steps onto A(0,0) → cell becomes '#'; recurse into neighbors; on return, '#' flips back to 'A'. Trail of '#' marks the live path; they vanish as the hand retreats.]**
>
> That mark-then-restore *is* the un-choose — same spirit as the swap-back in permutations, where the array was its own scratchpad. The board is our path. **CHOOSE**: step on, mark `'#'`. **RECURSE**: into the four neighbors. **UN-CHOOSE**: restore the letter, freeing the cell for other paths.
>
> Why restore, not just leave it marked? Because "visited" must be scoped to *this trail only*. A different starting attempt, or a sibling branch, needs a clean board. If you never restored, you'd permanently blacklist cells and miss real answers.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: one boxed line: "Mark the cell '#' on the way IN, restore it on the way OUT." Below: "the board IS the visited-set."]**

> The line: **mark the cell on the way in, restore it on the way out.** The board itself is your visited-set — zero extra memory — and the restore is the backtracking un-choose. Miss the restore and you corrupt the board.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Build it. The DFS takes a cell `(r,c)` and `k`, the index of the letter we need next.

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def dfs(r, c, k):
        if k == len(word):
            return True                   # matched every letter
```

> **[VISUAL: add chunk 2, highlight the guard — this is the prune.]** Bail on anything that can't work: off the board, or wrong letter.

```python
        if (r < 0 or r >= rows or c < 0 or c >= cols
                or board[r][c] != word[k]):   # out of bounds or mismatch → prune
            return False
```

> **[VISUAL: add chunk 3, highlight mark → recurse → restore.]** The heart: mark in place, explore four directions, restore.

```python
        temp = board[r][c]
        board[r][c] = '#'                 # CHOOSE: mark visited in place
        found = (dfs(r+1, c, k+1) or dfs(r-1, c, k+1)
                 or dfs(r, c+1, k+1) or dfs(r, c-1, k+1))
        board[r][c] = temp                # UN-CHOOSE: restore the letter
        return found
```

> **[VISUAL: add chunk 4.]** And launch from every cell.

```python
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
```

> The `or` chain short-circuits — the instant one direction returns True, we stop and bubble it up. But the `restore` line *always* runs on the way out, success or failure.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:15`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight each line.]**

> The *why*.
>
> `if k == len(word): return True` — the success base case fires *before* the bounds/letter check, because once we've matched the whole word, we're done, no matter where we are.
>
> The big guard combines *three* prunes into one: out of bounds, and letter mismatch. And notice — the `'#'` sentinel makes the "already visited" case fall out *for free*: a `'#'` cell can never equal `word[k]`, so it fails the mismatch check automatically. One line does the work of three.
>
> **LEARNER:** Why save `temp` and restore it — why not just set the cell back to `word[k]`? We know that's what it was.
>
> **TEACHER:** Sharp, and *usually* that'd work, since the cell matched `word[k]` to get here. But saving `temp` is bulletproof and self-documenting — it restores the exact original regardless of assumptions, and it reads as an obvious mark/restore pair. In an interview, the paired `temp = ...` and `board[r][c] = temp` instantly signals "I'm doing a clean backtrack." Clarity beats cleverness.
>
> And the double loop launching `dfs` from every cell — the word can start anywhere, so we can't miss a starting square.

---

## 9. DRY-RUN THE CODE — `8:30`
*(worked example — prove it, close the loop)*

**[VISUAL: board with '#' marks trailing the path as it descends; on the True return, marks restore behind the retreating hand.]**

> Run "ABCCED" starting at (0,0).

```
dfs(0,0,'A') match → mark '#'
  dfs(0,1,'B') match → mark '#'
    dfs(0,2,'C') match → mark '#'
      dfs(1,2,'C') match → mark '#'
        dfs(2,2,'E') match → mark '#'
          dfs(2,1,'D') match → mark '#'
            k==6 == len(word) → return True ✅
```

> As the True bubbles back up, every `'#'` flips back to its letter — the board ends *exactly* as it started. Crucially, when we were sitting on the second C at (1,2), the first C at (0,2) was `'#'` — so the search couldn't slither back onto it. The mark did its job. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:30`
*(transfer to interview)*

**[VISUAL: "Time: O(m·n·4^L)." "Auxiliary: O(L) stack, O(1) beyond the board."]**

> Out loud: *"There are m-times-n starting cells. From each, I branch up to 4 directions — really 3 after the first step, since I won't turn back — to a depth of L, the word length. So time is O(m·n·4-to-the-L)."*
>
> Unlike the enumeration problems, there's *no exponential output here* — the answer is a single boolean. The exponential is genuine search work, tamed by the letter-mismatch prune cutting most branches at step one.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:05`
*(depth + honesty — output vs auxiliary)*

**[VISUAL: three rows — "visited grid: O(m·n)", "visited set: O(L)", "in-place '#': O(1) beyond board". Winner highlighted.]**

> Here the space story *is* the whole optimization. Three ways to track visited:
> - A `visited` boolean grid — `O(m·n)` extra.
> - A `visited` set of the path's coordinates — `O(L)`.
> - The in-place `'#'` sentinel — `O(1)` extra; we reuse the board.
>
> So the in-place trick drops auxiliary space to just the **recursion stack, `O(L)`** — bounded by the word length, since the path can't exceed it. No output to store; the answer's a boolean.
>
> Say it: *"I mark visited by overwriting the cell in place and restore on the way out, so my only extra memory is the O(L) call stack — no visited grid, no set."*
>
> One honest caveat worth voicing: *"If mutating the input is off-limits — concurrent readers, an immutability contract — I'd fall back to the O(L) visited set."* Naming that constraint is a strong-hire move.

---

## 12. YOUR TURN (active recall) — `10:50`
*(retrieval practice)*

**[VISUAL: "Your turn → Number of Islands (LC 200)". A grid of 1s and 0s.]**

> Try **Number of Islands** — count connected blobs of land in a grid. Same four-direction grid DFS, but with a twist: once you flood-fill a piece of land, you *don't* un-mark it. Ask yourself *why* backtracking un-marks but flood-fill doesn't — that contrast will sharpen when the un-choose actually matters.

---

## 13. LOCK IT IN — `11:25`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three to keep:
> 1. **Grid backtracking = DFS with mark/restore of visited cells.**
> 2. **The `'#'` sentinel makes the board its own visited-set** — `O(1)` extra, `O(L)` stack.
> 3. **The letter check is the prune**; matching the whole word short-circuits to True.
>
> The peg: **the board is your scratchpad — mark on the way in, restore on the way out.** The restore is the un-choose made physical.

---

## 14. CLIFFHANGER — `11:55`
*(open loop to next lesson)*

**[VISUAL: a chessboard with queens; attack lines slicing across rows, columns, diagonals. Title: "N-Queens — Hard".]**

> Every problem so far had *one* simple constraint at a time. The finale — N-Queens — stacks *three at once*: no two queens share a row, a column, *or* a diagonal. The naive check re-scans the whole board every placement. The elegant version tracks three constraint sets for O(1) checks and prunes ferociously. It's the Hard one, it ties the whole pattern together, and it's where backtracking feels like magic. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
