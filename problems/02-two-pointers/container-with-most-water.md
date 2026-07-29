# Container With Most Water

> **LeetCode:** 11. Container With Most Water · **Difficulty:** 🟡 Medium · **Pattern:** Two Pointers · **Google frequency:** ⭐ high

---

## Problem

You're given `height`, an array where `height[i]` is the height of a vertical wall at position `i`. Pick two walls that, with the x-axis, form a container. The water it holds is `width × min(height of the two walls)`. Return the **maximum** water any pair can hold.

**Example:** `height = [1, 8, 6, 2, 5, 4, 8, 3, 7]` → `49` *(walls at index 1 (height 8) and index 8 (height 7): width 7 × min(8,7)=7 → 49).*

**Constraints that matter:** `n` can be up to ~10⁵. Checking every pair is O(n²) ≈ 10¹⁰ → too slow. We need O(n). Key insight to keep in mind: water is capped by the **shorter** of the two walls — a tall wall is wasted next to a short one.

---

## 🧠 Intuition — how you'd actually arrive at this


- **First instinct:** "Try every pair of walls, compute the area, keep the biggest." Two nested loops. That's the brute force, O(n²).
- **Where it hurts:** you evaluate every one of the ~n²/2 pairs even though most are obviously bad. There's structure you're ignoring: area = `width × min(left, right)`, and the two ingredients pull against each other — moving the walls apart raises width but often lowers the height cap.
- **The leap:** start as **wide as possible** — one pointer at each end. That maximizes width immediately, so any *other* pair is narrower. Now, which pointer do you move? The area is limited by the **shorter** wall. Moving the *taller* wall inward can only make things worse or equal: width drops and the cap is still the short wall. Moving the *shorter* wall gives up width but is the *only* move that could raise the height cap — your one shot at a bigger area. So: **always move the shorter wall inward.** Every step you either find a bigger area or safely discard a wall that can't help.
- **Pattern trigger:** **maximize/minimize over pairs where the value depends on a min/max of the two ends** → **Two Pointers from both ends, advance the limiting side.** The signal is "the bottleneck is one of the two endpoints — move that one."

---

## ① Brute Force

Every pair of walls, compute area, track the max.

```python
def max_area_brute(height):
    n = len(height)
    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            area = (j - i) * min(height[i], height[j])
            best = max(best, area)
    return best
```

**Why it's the natural first attempt:** "the best pair" reads as "check all pairs and keep the best."

**Why it's not enough:** O(n²) pairs. At n=10⁵ that's ~5 billion evaluations → Time Limit Exceeded. It also re-derives from scratch which wall is the bottleneck every single time.

**Complexity:** Time `O(n²)`, Space `O(1)`.

---

## ② Optimised Solution

Two pointers at the ends. Compute area, then move the **shorter** wall inward.

```python
def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        area = (right - left) * min(height[left], height[right])
        best = max(best, area)
        if height[left] < height[right]:
            left += 1          # short wall on the left — its only chance is to move
        else:
            right -= 1         # short (or equal) wall on the right — move it
    return best
```

**Walk the example** `[1, 8, 6, 2, 5, 4, 8, 3, 7]`:

| left (h) | right (h) | width | area = w × min | best | move |
|---|---|---|---|---|---|
| 0 (1) | 8 (7) | 8 | 8×1 = 8 | 8 | left shorter → left++ |
| 1 (8) | 8 (7) | 7 | 7×7 = **49** | 49 | right shorter → right-- |
| 1 (8) | 7 (3) | 6 | 6×3 = 18 | 49 | right shorter → right-- |
| 1 (8) | 6 (8) | 5 | 5×8 = 40 | 49 | equal → right-- |
| 1 (8) | 5 (4) | 4 | 4×4 = 16 | 49 | right-- |
| 1 (8) | 4 (5) | 3 | 3×5 = 15 | 49 | right-- |
| 1 (8) | 3 (2) | 2 | 2×2 = 4 | 49 | right-- |
| 1 (8) | 2 (6) | 1 | 1×6 = 6 | 49 | right-- → pointers meet |

Answer: **49**. ✅

**Why it's correct:** the invariant is "we never skip a pair that could beat our current best." When we move the shorter wall, every pair we *discard* (the short wall with any wall still inside) had that same short wall as its cap **and** a smaller width — so its area is strictly less than the area we just recorded. Nothing better is lost. The pointers converge, so it's a single pass.

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## ③ Space Optimization

Already O(1) space — only two indices and a running max, nothing scales with the input. There's no auxiliary structure to cut; the win over brute force was purely in **time** (O(n²) → O(n)), achieved by the "move the shorter wall" rule that lets one pass replace all-pairs.

> Say it out loud: *"Space was never the issue here — it's O(1) both ways. The whole gain is collapsing O(n²) pairs into one O(n) sweep by only ever moving the limiting wall."*

---

## Java (for Java interviewers)

```java
public int maxArea(int[] height) {
    int left = 0, right = height.length - 1, best = 0;
    while (left < right) {
        int area = (right - left) * Math.min(height[left], height[right]);
        best = Math.max(best, area);
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }
    return best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (all pairs) | O(n²) | O(1) |
| Optimised (two pointers) | O(n) | O(1) |
| Space-optimised | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"Brute force checks all pairs — O(n²), too slow at 10⁵. The area is width times the shorter wall, so I start as wide as possible with a pointer at each end. The short wall is the bottleneck, so moving the taller one can never help — I always move the shorter wall inward, because that's the only move that might raise the cap. Every step either improves the answer or safely drops a wall that can't beat it. One pass, O(n) time, O(1) space."*

## Related / follow-ups
- **Trapping Rain Water** (two pointers, but sum water over *every* bar)
- **Pair with Target Sum / Two Sum II** (converging pointers on sorted input)
- **Largest Rectangle in Histogram** (max area, but via a monotonic stack)
