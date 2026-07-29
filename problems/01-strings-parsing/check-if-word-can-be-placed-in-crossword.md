# Check if Word Can Be Placed In Crossword

> **LeetCode:** 2018. Check if Word Can Be Placed In Crossword · **Difficulty:** 🟡 Medium · **Pattern:** Grid / Simulation · **Google frequency:** ⭐ high

---

## Problem

You're given an `m × n` `board` and a `word`. Each board cell is one of three things: a space `' '` (empty), a hash `'#'` (blocked), or a **lowercase letter** (already filled in). A **slot** is a *maximal* run of non-`'#'` cells in a single row or a single column — a horizontal or vertical strip bounded on both ends by a `'#'` or by the border of the board.

You can place `word` into a slot if **two** conditions hold:

1. The slot's length is **exactly** the length of `word` — not longer, not shorter.
2. Reading the slot cell by cell, every cell is either empty (`' '`) or already holds the matching letter of `word`.

The word may be placed **forward or backward**, **horizontally or vertically**. Return `true` if `word` can go anywhere on the board, else `false`.

**Example:** `board = [["#"," ","#"],[" "," ","#"],["#"," ","#"]]`, `word = "cat"` → `true`

```
# . #          the middle COLUMN is an empty
. . #          vertical slot of length 3:
# . #          . / . / .  → "cat" drops right in
```

*(The three empty cells stacked in column 1 form a vertical slot of length 3. All three are blank, so `"cat"` fits — reading top-to-bottom or bottom-to-top, doesn't matter here.)*

A **false** example: same board, `word = "cats"` → `false`. There's no slot of length **4** anywhere. The vertical slot is length 3, every horizontal slot is length 1 or 2. Length mismatch kills it — even though `"cat"` would have fit, `"cats"` has nowhere legal to go.

**Constraints that matter:** `1 ≤ m·n ≤ 2·10^5`. That's your budget: you want a single sweep of the grid, `O(m·n)`. Cells are only `' '`, `'#'`, or lowercase letters, and `word` is lowercase — so an exact character match (`cell == word[i]`) is all you ever compare. The word can be reversed, so **every slot gets tested both ways**.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For every cell, try to lay the word down starting there — going right, going down — and check it fits." That's the by-hand instinct, and it's not wrong. The trap is the *bookkeeping*: to know you've found a real slot and not just a fitting sub-strip, you also have to check the cell **just before** the start and **just after** the end are blocked (or off-board). Forget one of those and you'll happily place `"cat"` into the first three cells of a length-4 slot — which the rules forbid.
- **Where it hurts:** that before/after boundary check is fiddly and easy to fumble under pressure, and you redo the scan up to four times per cell (two directions × two orientations). It works, but it's the version that passes the sample and then fails a hidden case because you botched an edge index.
- **The leap:** stop *placing* and start *collecting*. The `'#'` cells and the borders already carve the board into slots for you. So make one clean pass: walk each row splitting on `'#'`, walk each column splitting on `'#'`, and hand yourself a tidy list of maximal segments. Now the boundary problem **vanishes** — a segment is a slot *by construction*, its two ends are already `'#'`-or-border. All that's left is a length check plus a forward/backward character match.
- **Pattern trigger:** **"maximal runs separated by a delimiter"** → **split-on-delimiter scan**. The delimiter is `'#'`. The transferable move: when a grid problem talks about "runs bounded by walls," don't hunt from each cell — *sweep once and let the walls cut the runs for you.* You've turned a fragile placement problem into a boring segment-matching one.

---

## ① Brute Force

For every cell, in each of the two directions, try to lay the word down — forward and backward — and manually verify the run is a true slot by checking the cells just before the start and just after the end are blocked or off-board.

```python
def placeWordInCrossword_brute(board, word):
    m, n = len(board), len(board[0])
    L = len(word)

    def try_place(r, c, dr, dc, w):
        # the cell BEFORE the start must be '#' or off-board,
        # else this isn't the true start of a maximal slot
        pr, pc = r - dr, c - dc
        if 0 <= pr < m and 0 <= pc < n and board[pr][pc] != '#':
            return False
        # lay w down cell by cell
        for i in range(L):
            nr, nc = r + dr * i, c + dc * i
            if not (0 <= nr < m and 0 <= nc < n):
                return False                       # ran off the board → too short
            cell = board[nr][nc]
            if cell == '#' or (cell != ' ' and cell != w[i]):
                return False                       # blocked, or wrong letter
        # the cell AFTER the end must be '#' or off-board,
        # else the slot is longer than the word → illegal
        er, ec = r + dr * L, c + dc * L
        if 0 <= er < m and 0 <= ec < n and board[er][ec] != '#':
            return False
        return True

    for r in range(m):
        for c in range(n):
            for dr, dc in ((0, 1), (1, 0)):        # right, down
                if try_place(r, c, dr, dc, word) or \
                   try_place(r, c, dr, dc, word[::-1]):
                    return True
    return False
```

**Why it's the natural first attempt:** it mirrors solving a crossword by hand — pick a square, try writing the word rightward, then downward, and see if it clicks.

**Why it's not enough:** it *works*, but the before/after boundary checks are exactly where interview bugs live. Miss the "cell before must be blocked" test and you'll place a word starting mid-slot; miss the "cell after" test and you'll cram a 3-letter word into a 5-cell slot. And every cell pays for up to four full length-`L` scans. It's not catastrophically slow, but it's `O(m·n·L)` and it's **fragile** — the structure invites off-by-one errors.

**Complexity:** Time `O(m · n · L)`, Space `O(L)` (for the reversed word).

---

## ② Optimised Solution

Don't place — **collect**. Make one sweep over rows and one over columns, splitting each on `'#'` into maximal segments. Every segment is already a valid slot, so the only checks left are *length* and a *forward-or-backward* character match.

```python
def placeWordInCrossword(board, word):
    L = len(word)

    def can_place(seg):
        # seg is one maximal slot (a list of ' ' / letter cells)
        if len(seg) != L:
            return False                                   # length must match EXACTLY
        fwd = all(c == ' ' or c == word[i]         for i, c in enumerate(seg))
        bwd = all(c == ' ' or c == word[L - 1 - i] for i, c in enumerate(seg))
        return fwd or bwd                                  # forward OR reversed

    # rows first, then columns via zip(*board); a trailing '#'
    # sentinel flushes the final segment of each line
    lines = list(board) + [list(col) for col in zip(*board)]
    for line in lines:
        seg = []
        for cell in list(line) + ['#']:
            if cell == '#':
                if can_place(seg):
                    return True
                seg = []                                   # slot ended → reset
            else:
                seg.append(cell)
    return False
```

**Walk the example** `board = [["#"," ","#"],[" "," ","#"],["#"," ","#"]]`, `word = "cat"` (`L = 3`):

| Line scanned | Segments (split on `#`) | Length check | Verdict |
|---|---|---|---|
| Row 0: `# _ #` | `[' ']` | 1 ≠ 3 | skip |
| Row 1: `_ _ #` | `[' ', ' ']` | 2 ≠ 3 | skip |
| Row 2: `# _ #` | `[' ']` | 1 ≠ 3 | skip |
| Col 0: `# _ #` | `[' ']` | 1 ≠ 3 | skip |
| **Col 1: `_ _ _`** | `[' ', ' ', ' ']` | **3 = 3** ✓ | all blank → `fwd` true → **return `true`** |

We never even reach column 2. The middle column's length-3 all-blank slot matches, so `"cat"` fits. ✅ *(Swap the word for `"cats"` and no row or column ever produces a length-4 segment — every `can_place` fails the length gate, and we return `false`.)*

**Why it's correct:** splitting a line on `'#'` yields exactly the maximal non-`'#'` runs — i.e. the slots — with their boundaries handled *for free* by the split (each segment is flanked by a `'#'` or the line's edge). So the fragile before/after checks disappear. `len(seg) != L` enforces the exact-length rule; a slot longer than the word can never accept it, because a placed word must fill a slot end to end. The `fwd`/`bwd` pair tests both reading directions, and `c == ' ' or c == word[i]` allows a cell only if it's empty or already the right letter. If any slot passes, a valid placement exists; if none does, none exists.

**Complexity:** Time `O(m · n)` — each cell is visited once in the row sweep and once in the column sweep, and the total work inside `can_place` across all segments is bounded by the number of cells. Space `O(m · n)` here, because `zip(*board)` materializes the columns. We fix that next.

---

## ③ Space Optimization

The clean version above builds every column into a fresh list (`zip(*board)` → `O(m·n)` extra). We don't need that. Scan the columns **in place** with index loops, and only ever hold the *one* segment we're currently building. A segment can be at most `max(m, n)` long, so auxiliary space drops to `O(max(m, n))`.

```python
def placeWordInCrossword(board, word):
    m, n = len(board), len(board[0])
    L = len(word)

    def can_place(seg):
        if len(seg) != L:
            return False
        fwd = all(c == ' ' or c == word[i]         for i, c in enumerate(seg))
        bwd = all(c == ' ' or c == word[L - 1 - i] for i, c in enumerate(seg))
        return fwd or bwd

    # horizontal slots — one row at a time, one segment in hand
    for r in range(m):
        seg = []
        for c in range(n):
            ch = board[r][c]
            if ch == '#':
                if can_place(seg): return True
                seg = []
            else:
                seg.append(ch)
        if can_place(seg): return True          # flush the row's last slot

    # vertical slots — one column at a time, read cells in place
    for c in range(n):
        seg = []
        for r in range(m):
            ch = board[r][c]
            if ch == '#':
                if can_place(seg): return True
                seg = []
            else:
                seg.append(ch)
        if can_place(seg): return True          # flush the column's last slot

    return False
```

**Complexity:** Time `O(m · n)`, Space `O(max(m, n))` — we never materialize the whole set of columns, just the current segment.

> Say it out loud: *"The elegant `zip` version is O(m·n) space because it copies out the columns. I don't need the copy — I can walk the columns with index arithmetic and hold just the one segment I'm building, so auxiliary space is O(max(m, n)). Below that there's no trick, because I'm reading the given board, not building a new structure."* Knowing *why* the `zip` costs memory and cutting it deliberately is the strong-hire move.

---

## Java (for Java interviewers)

```java
public boolean placeWordInCrossword(char[][] board, String word) {
    int m = board.length, n = board[0].length;

    // horizontal slots
    for (int r = 0; r < m; r++) {
        StringBuilder seg = new StringBuilder();
        for (int c = 0; c < n; c++) {
            char ch = board[r][c];
            if (ch == '#') {
                if (canPlace(seg, word)) return true;
                seg.setLength(0);
            } else {
                seg.append(ch);
            }
        }
        if (canPlace(seg, word)) return true;      // flush row's last slot
    }

    // vertical slots — read the column in place
    for (int c = 0; c < n; c++) {
        StringBuilder seg = new StringBuilder();
        for (int r = 0; r < m; r++) {
            char ch = board[r][c];
            if (ch == '#') {
                if (canPlace(seg, word)) return true;
                seg.setLength(0);
            } else {
                seg.append(ch);
            }
        }
        if (canPlace(seg, word)) return true;      // flush column's last slot
    }

    return false;
}

private boolean canPlace(StringBuilder seg, String word) {
    int L = word.length();
    if (seg.length() != L) return false;           // exact length only
    boolean fwd = true, bwd = true;
    for (int i = 0; i < L; i++) {
        char cell = seg.charAt(i);
        if (cell != ' ' && cell != word.charAt(i))         fwd = false;
        if (cell != ' ' && cell != word.charAt(L - 1 - i)) bwd = false;
    }
    return fwd || bwd;                             // forward OR reversed
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (place at every cell, check boundaries) | O(m·n·L) | O(L) |
| Optimised (split on `#`, match segments) | O(m·n) | O(m·n) (materialized columns) |
| Space-optimised (scan columns in place) | O(m·n) | O(max(m, n)) |

*(m·n = board cells, L = length of `word`.)*

---

## Say it out loud (interview narration)

> *"The blocked cells and the borders already cut the board into slots for me, so I won't hunt for placements from each cell — that path forces fragile 'is the cell before and after me a wall?' checks. Instead I sweep once across the rows and once down the columns, splitting each line on `'#'` into maximal segments. Each segment is a slot by construction. Then for a segment I just check two things: is its length exactly the word length, and does every cell match the word either forward or backward, where a blank cell matches anything. First segment that passes, I return true. It's O(m·n) time — every cell seen twice — and I can keep space to O(max(m, n)) by scanning columns in place instead of copying them out."*

Before you code, ask the one clarifying question that shows you read the rules: *"The slot has to be **exactly** the word's length, right — I can't drop a 3-letter word into a 5-cell slot and leave two blanks?"* That exact-length rule is the detail people miss, and surfacing it early is precisely what Google's rubric rewards.

## Related / follow-ups
- **Word Search (LC 79) / Word Search II (LC 212)** — the *placement*-style grid search this problem lets you avoid; good contrast for when you genuinely must DFS from each cell.
- **Number of Islands (LC 200)** — another "runs bounded by walls" grid sweep, connectivity flavor.
- **Spiral Matrix / Set Matrix Zeroes** — same muscle: disciplined row-and-column traversal with careful indexing.
- **Valid Word Square (LC 422)** — row-vs-column symmetry checks on a grid, same read-both-ways instinct.
