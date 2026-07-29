# Lesson 08: The Two-Pointer Idea — Pair with Target Sum
**Section 2: Two Pointers | Problem: Pair with Target Sum (sorted) · Easy | Duration: ~9 min**

> LeetCode analog: **167. Two Sum II — Input Array Is Sorted**

---

# PART 1: THE PATTERN (~3 min)

## HOOK (0:00)

> The problem looks trivial: *"Given a sorted array, find two numbers that add up to a target."*
>
> So you write the obvious thing — two nested loops — and it works on the example. Then the hidden test has 100,000 numbers, your solution runs 10 billion operations, and it times out. The interviewer says nothing.
>
> The fix is two little indices walking toward each other. Let me show you.

---

## STORY / ANALOGY (0:30)

> Picture a bookshelf of books, sorted by width, thinnest on the left, widest on the right.
>
> You want two books whose widths add up to exactly 30 cm. You put one finger on the **thinnest** book (left) and one on the **widest** (right).
>
> - Too wide? The widest book is the problem — slide the **right** finger inward to a thinner book.
> - Too thin? You need more width — slide the **left** finger inward to a wider book.
>
> Each move throws away a whole set of pairs you no longer need to check. You never go backward. That's two pointers.

**[SLIDE: Sorted shelf, two fingers (left/right arrows) squeezing inward]**

---

## THE PATTERN (1:30)

> **Two pointers** = two indices moving through the array so you avoid a second loop.
>
> When the array is **sorted**, the two ends tell you which way to move:
> - `left` starts at index 0 (smallest), `right` at the end (largest).
> - `sum = arr[left] + arr[right]`.
> - Too big → move `right` left (shrink the sum). Too small → move `left` right (grow the sum). Equal → found it.
>
> **The recognition signal:** *sorted array* + *find a pair (or triplet) by value*. The moment you see those two things together, your hand should reach for two pointers.

---

## QUICK CHECK (2:30)

> *"Find two numbers in an **unsorted** array that sum to a target."* — Does the two-pointer trick fire directly?
>
> *(pause)*
>
> Not directly — the left/right logic only works because sorted order tells you which way to move. If it's unsorted, you either **sort first** (O(n log n)) or use a **hash map** (O(n) — that's L04 and L100). Two pointers *needs the sort*. Hold that thought; it's exactly the tradeoff we'll compare.

---

# PART 2: THE SOLVE (~6 min)

## ① THE BRUTE FORCE (3:00)

> Check every pair. For each number, scan the rest of the array for its partner.

```python
def pair_sum_brute(arr, target):
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target:
                return [i, j]
    return [-1, -1]
```

> Walk it on `arr = [1, 3, 4, 6, 8, 11]`, target `10`:
> - `i=0 (1)`: check 3,4,6,8,11 → none make 10 with 1. (5 checks)
> - `i=1 (3)`: check 4,6,8,11 → none. (4 checks)
> - `i=2 (4)`: check 6 → 4+6=10. Found → `[2, 3]`.
>
> It works. But count the checks: for `n` elements it's `n + (n-1) + ... ≈ n²/2` comparisons.
>
> **Complexity: O(n²) time, O(1) space.** On the 4-element example it's instant. On the 100,000-element hidden test it's ~5 billion comparisons — **time limit exceeded.** The interviewer is waiting for you to notice *you're ignoring the sort*.

---

## ② THE OPTIMISED SOLUTION (5:00)

> The array is **sorted**. The brute force throws that gift away. Two pointers uses it.
>
> Put `left` at the start, `right` at the end. Look at their sum and decide which pointer to move.

```python
def pair_sum(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return [left, right]      # found the pair
        if s < target:
            left += 1                 # sum too small → need a bigger number
        else:
            right -= 1                # sum too big → need a smaller number
    return [-1, -1]                   # no pair
```

> Same array `[1, 3, 4, 6, 8, 11]`, target `10`:
> - `left=0(1), right=5(11)` → 12 > 10 → move right. `right=4`.
> - `left=0(1), right=4(8)` → 9 < 10 → move left. `left=1`.
> - `left=1(3), right=4(8)` → 11 > 10 → move right. `right=3`.
> - `left=1(3), right=3(6)` → 9 < 10 → move left. `left=2`.
> - `left=2(4), right=3(6)` → 10 == 10 → return `[2, 3]`. ✅
>
> Six comparisons instead of dozens — and it *scales*. Each step moves one pointer inward, so the two pointers together travel the array **once**.
>
> **Why it's correct:** when the sum is too big, the largest element (`arr[right]`) can't be in *any* valid pair with something ≥ `arr[left]`, so we safely discard it by moving `right` in. Symmetric argument for `left`. We never skip a real answer.
>
> **Complexity: O(n) time, O(1) space.** From quadratic to linear by *using the sort we were handed*.

**[SLIDE: The 5 steps animated — pointers squeezing, sum updating each move]**

---

## ③ SPACE OPTIMIZATION (7:00)

> Here's where you separate yourself. Contrast two ways to solve this:
>
> - **Hash-map approach** (great for *unsorted* input): one pass, store each value you've seen, look up the complement. **O(n) time — but O(n) space** for the map.
> - **Two-pointer approach** (this one, for *sorted* input): **O(n) time and O(1) space** — just two integer indices, nothing that grows with the input.
>
> So when the array is already sorted, two pointers is *strictly better on space* than the hash map. Say this out loud in the interview:
>
> > *"Since the array is sorted, I'll use two pointers instead of a hash map — same O(n) time, but O(1) space instead of O(n)."*
>
> That one sentence shows you didn't just solve it — you *chose* the solution that costs the least memory. That's the strong-hire signal.

---

## COMPLEXITY OUT LOUD (7:45)

> *"Brute force was O(n²) time, O(1) space. Using the sorted order, two pointers gets it to **O(n) time, O(1) space** — each pointer walks the array at most once, and I only store two indices. If the array weren't sorted, I'd sort first for O(n log n), or use a hash map for O(n) time at the cost of O(n) space."*

---

## ACTIVE RECALL (8:00)

> **Your turn before the next lesson.** Same idea, tiny twist:
>
> **Valid Palindrome** — given a string, ignore non-alphanumerics and case, return whether it reads the same forward and backward. (LeetCode 125.)
>
> Hint: where do the two pointers start, and which direction do they move? What's the *recognition signal* that told you it's two pointers? Try it, then watch L09.

---

## 3-POINT SUMMARY (8:30)

> 1. **Signal:** sorted array + find a pair by value → two pointers.
> 2. **Move rule:** sum too big → move `right` in; too small → move `left` in; equal → done. One pass, O(n).
> 3. **Space win:** two pointers is O(1) space — beats the hash map's O(n) *when the array is sorted*. Say that out loud.

---

## CLIFFHANGER (9:00)

> We moved two pointers *toward* each other from the ends. But what if they should start *together* and move *apart* — or one races ahead of the other? Next up: **Valid Palindrome**, where the same two-pointer squeeze checks a string from both ends at once. Then we'll level up to 3Sum, where two pointers rescues an O(n³) monster.

---

## APPENDIX — Java version (for Java interviewers)

Same three layers, Java syntax. Show the optimised two-pointer solve:

```java
// ② Optimised: O(n) time, O(1) space — needs a sorted array
public int[] pairSum(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int sum = arr[left] + arr[right];
        if (sum == target) {
            return new int[]{left, right};   // found the pair
        } else if (sum < target) {
            left++;                           // sum too small → bigger number
        } else {
            right--;                          // sum too big → smaller number
        }
    }
    return new int[]{-1, -1};                 // no pair
}
```

```java
// ① Brute force for contrast: O(n²) time, O(1) space
public int[] pairSumBrute(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        for (int j = i + 1; j < arr.length; j++) {
            if (arr[i] + arr[j] == target) return new int[]{i, j};
        }
    }
    return new int[]{-1, -1};
}
```

> Java note: `new int[]{left, right}` builds the result array inline. The logic — and the O(n) time / O(1) space — is identical to Python. The pattern is language-agnostic; only the syntax changes.
