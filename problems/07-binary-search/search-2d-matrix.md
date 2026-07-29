# Search a 2D Matrix (Flatten the Index)

> **LeetCode:** 74. Search a 2D Matrix · **Difficulty:** 🟡 Medium · **Pattern:** Modified Binary Search · **Google frequency:** medium

---

## Problem

Given an `m × n` matrix where **each row is sorted left-to-right** and **the first integer of each row is greater than the last integer of the previous row**, determine whether `target` is present. Must run in **O(log(m·n))**.

**Example:**
```
matrix = [[ 1,  3,  5,  7],
          [10, 11, 16, 20],
          [23, 30, 34, 60]]
target = 3  → True
target = 13 → False
```

**Constraints that matter:** `m·n` up to ~10⁴, and the problem **demands O(log(m·n))**. The two ordering guarantees together mean that if you read the matrix **row by row**, the values are **one single sorted list** — that's the whole insight.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "It's a grid — scan every cell, or scan the right row then that row." Cell-by-cell is O(m·n); even "find the row (O(m)) then binary search it (O(log n))" is O(m + log n).
- **Where it hurts:** Scanning ignores that the whole grid is globally ordered. And the two-step "find the row linearly" version still pays O(m) to locate the row — wasteful when the rows are themselves ordered relative to each other.
- **The leap:** Read the guarantees literally. Row `r` ends below where row `r+1` begins, and each row is internally sorted. So concatenating the rows gives a **single strictly increasing array** of length `m·n`. You don't need to physically flatten it — you can *pretend* it's a 1-D array of indices `0 … m·n − 1` and convert any flat index `i` back to a cell with `row = i // n`, `col = i % n`. Now it's literally LC 704 binary search on a virtual array.
- **Pattern trigger:** **"sorted grid / globally-ordered 2-D structure + O(log) required"** → **treat it as a flat sorted array via index arithmetic.** The transferable move: the *logical* shape (one sorted list) matters more than the *physical* shape (a grid).

---

## ① Brute Force

Scan every cell.

```python
def searchMatrix_brute(matrix, target):
    for row in matrix:
        for x in row:
            if x == target:
                return True
    return False
```

**Why it's the natural first attempt:** it's a grid, so "look at each cell" is the reflex.

**Why it's not enough:** O(m·n), and it throws away *both* sorted guarantees. It also violates the required O(log(m·n)).

**Complexity:** Time `O(m·n)`, Space `O(1)`.

---

## ② Optimised Solution

Binary search over the **virtual flattened index** `[0, m·n − 1]`, mapping each mid back to `(row, col)`. Same inclusive `[left, right]` template as LC 704.

```python
def searchMatrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1          # virtual flat indices
    while left <= right:
        mid = left + (right - left) // 2
        val = matrix[mid // n][mid % n] # decode flat index → (row, col)
        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1
    return False
```

**The index decode is the only new idea:** flat index `i` in a row-major `m × n` grid sits at `row = i // n`, `col = i % n`. (Divide by the number of **columns** `n`, not rows — a classic slip.) Everything else is the untouched canonical template.

**Walk the example** (target `3`, `m=3`, `n=4`, so flat range `[0, 11]`):

| left | right | mid | mid//4, mid%4 | val | action |
|---|---|---|---|---|---|
| 0 | 11 | 5 | (1, 1) | 11 | 11 > 3 → right = 4 |
| 0 | 4 | 2 | (0, 2) | 5 | 5 > 3 → right = 1 |
| 0 | 1 | 0 | (0, 0) | 1 | 1 < 3 → left = 1 |
| 1 | 1 | 1 | (0, 1) | 3 | 3 == 3 → **return True** ✅ |

**Why it's correct (loop invariant):** the virtual array `A[i] = matrix[i // n][i % n]` is strictly increasing (given the two ordering guarantees), and *"if target exists, its flat index is in `[left, right]`."* Every step discards a half that provably can't contain it — identical reasoning to LC 704, just with an index translation layered on top.

**Complexity:** Time `O(log(m·n))`, Space `O(1)`.

---

## ③ Space Optimization

Already **O(1)** — two integer indices plus the constant-time decode. We never build the flattened array; the mapping `mid // n, mid % n` gives us the value on demand, so no extra O(m·n) memory.

> Actually flattening the matrix into a real list would cost O(m·n) time *and* space just to set up — defeating the point. Computing the cell on the fly is the whole elegance.

---

## Java (for Java interviewers)

```java
public boolean searchMatrix(int[][] matrix, int target) {
    int m = matrix.length, n = matrix[0].length;
    int left = 0, right = m * n - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        int val = matrix[mid / n][mid % n];   // decode flat index
        if (val == target) return true;
        else if (val < target) left = mid + 1;
        else right = mid - 1;
    }
    return false;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (scan cells) | O(m·n) | O(1) |
| Row-search + row binary search | O(m + log n) | O(1) |
| Optimised (flatten-index binary search) | O(log(m·n)) | O(1) |

---

## Say it out loud (interview narration)

> *"The two guarantees — each row sorted, and every row starts above the previous row's end — mean the whole matrix is really one sorted list read row by row. So I binary-search over a virtual flat index from 0 to m·n−1, and convert each mid back to a cell with row = mid // n, col = mid % n. That's exactly the standard binary search template with one index-decode line, O(log(m·n)) time, O(1) space — no need to actually flatten anything."*

## Related / follow-ups
- **Search a 2D Matrix II** (LC 240 — rows and columns sorted but *not* globally ordered; use staircase search from a corner, O(m+n))
- **Binary Search** (LC 704 — the 1-D template this reduces to)
- **Kth Smallest Element in a Sorted Matrix** (LC 378 — binary search on the value range)
