# 🎬 Recording Script — Pair with Target Sum (Two Sum II, Sorted)
**Pattern: Two Pointers · LeetCode 167 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Role in course:** the FIRST two-pointer lesson — introduces the pattern from scratch. Everything after (3Sum, Container) builds on this.

> Format: **[VISUAL: …]** = on screen. **TEACHER:** / **LEARNER:** = the two voices (LEARNER is a smart peer, used sparingly). Read every spoken line aloud.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion)*

**[VISUAL: editor with a two-nested-loop solution. A red "Time Limit Exceeded" banner drops in.]**

> **TEACHER:** Here's a problem so simple it feels like a warm-up: *"Given a sorted list of numbers, find the two that add up to a target."*
>
> You write the obvious thing — two loops, try every pair. It passes the tiny example. You submit… Time Limit Exceeded.
>
> Simple problem. And it's about to teach you the single most reused trick in coding interviews — one that turns a two-loop solution into a one-pass solution. Once it clicks here, you'll spot it everywhere. Let's build it.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:30`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below: six sorted tiles `1  3  4  6  8  11`, and "target = 10".]**

> **TEACHER:** One line: find the two numbers that add up to the target, and return their positions. The list is **sorted** — hold onto that word, it's the whole game.
>
> Tiny example: these six numbers, target ten. Which two? Take a second… four and six. But *how* we find them is the point.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:05`
*(worked example — feel the waste)*

**[VISUAL: the six tiles; markers i and j; a "comparisons" counter.]**

> **TEACHER:** Let's do what the brain does first. Pin `i` on the first number, one. Now `j` checks everyone after it: 1+3, 1+4, 1+6, 1+8, 1+11 — nope. Five checks, nothing.
>
> **[VISUAL: counter climbs 5… then i moves and it keeps climbing.]**
>
> Move `i` to three. Check 3+4, 3+6, 3+8, 3+11. Then `i` to four: 4+6 — ten! Found it. But look — we did a dozen checks, and for a big list this is n-times-n. On 100,000 numbers, that's ten billion. That's your TLE.

---

## 4. THE PAIN POINT + PREDICT — `2:10`
*(generation effect — first pause; LEARNER voices the doubt)*

**[VISUAL: freeze; highlight `j` re-scanning; a 4-second "🤔" timer.]**

> **TEACHER:** So what are we wasting? For every `i`, `j` re-scans the whole rest of the list from scratch.
>
> **LEARNER:** But that's the job, right? To find the pair you kind of have to look at the pairs.
>
> **TEACHER:** That's the instinct to break. We're ignoring a gift the problem handed us. Pause and stare at those six numbers: **they're sorted. How could "sorted" tell us which way to look — instead of checking everything?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `2:55`
*(elaboration + analogy — derive it)*

**[VISUAL: two hands appear — one on the far-left `1`, one on the far-right `11`.]**

> **TEACHER:** Here's the move. Put one finger on the smallest number, one on the largest. Add them.
>
> One plus eleven is twelve. Too big. Now think: to get a *smaller* sum, which finger do I move? The big one — slide the right finger left, to eight.
>
> **[VISUAL: right hand moves 11 → 8. Sum shows 9.]**
>
> One plus eight is nine. Too small now. So move the *left* finger up, to three. Three plus eight, eleven — too big, right finger down to six. Three plus six, nine — too small, left finger up to four. Four plus six… ten. Done.
>
> **[VISUAL: comparisons counter shows just 5 — beside the old "10 billion".]**
>
> Five steps. And here's why it's not luck: the list is sorted, so "too big" *always* means shrink from the right, "too small" *always* means grow from the left. Each move throws away numbers we've proven can't work.

---

## 6. THE KEY MOVE (signaling) — `4:05`
*(one crisp line)*

**[VISUAL: boxed line: "Sum too big → move right in. Too small → move left in."]**

> **TEACHER:** The whole pattern in one line: **too big, move the right pointer in; too small, move the left in; equal, you're done.** That's two pointers. Say it with me once — it's the sentence you'll reuse for the next dozen problems.

---

## 7. CODE IT — LIVE & CHUNKED — `4:40`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor; type chunk 1.]**

> **TEACHER:** Two pointers — one at each end.

```python
def pair_sum(arr, target):
    left, right = 0, len(arr) - 1
```

> **[VISUAL: add chunk 2.]** Loop while they haven't met, and add them up.

```python
    while left < right:
        s = arr[left] + arr[right]
```

> **[VISUAL: add chunk 3.]** The three cases — the heart of it.

```python
        if s == target:
            return [left, right]
        if s < target:
            left += 1       # too small → grow the sum
        else:
            right -= 1      # too big → shrink the sum
    return [-1, -1]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:00`
*(elaboration — why each line)*

**[VISUAL: full function; spotlight each line named.]**

> **TEACHER:** `left` at 0, `right` at the last index — the two ends.
>
> **LEARNER:** Why `while left < right` and not `<=`?
>
> **TEACHER:** Good — if they're equal they're on the *same* number, and we'd be adding it to itself. We need two different numbers, so we stop when they meet.
>
> The `s < target` branch bumps `left` up to a bigger value; `else` pulls `right` down to a smaller one. That's the squeeze, and sorted order is what makes those directions correct. If we never find it, they cross and we return "not found."

---

## 9. DRY-RUN THE CODE — `6:55`
*(worked example — prove it)*

**[VISUAL: trace table filling row by row.]**

| left (val) | right (val) | sum | action |
|---|---|---|---|
| 0 (1) | 5 (11) | 12 | > 10 → right-- |
| 0 (1) | 4 (8) | 9 | < 10 → left++ |
| 1 (3) | 4 (8) | 11 | > 10 → right-- |
| 1 (3) | 3 (6) | 9 | < 10 → left++ |
| 2 (4) | 3 (6) | 10 | **== → return [2, 3]** ✅ |

> **TEACHER:** Five rows, and it lands on four and six. Exactly what we eyeballed — but now it scales to a million numbers.

---

## 10. COMPLEXITY, OUT LOUD — `7:35`
*(transfer to interview)*

**[VISUAL: Brute force O(n²) vs Ours O(n); space O(1).]**

> **TEACHER:** Interviewer voice: *"Brute force is O(n squared). With two pointers, each one only ever moves inward, so together they cross the array once — that's O(n) time, O(1) space."* Brute force, then the fix, then the cost. That's the rhythm they're grading.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:00`
*(depth + honesty; LEARNER misconception)*

**[VISUAL: a hash-map solution beside ours.]**

> **LEARNER:** Couldn't I just use a hash map — store what I've seen, look up the complement? Isn't that also O(n)?
>
> **TEACHER:** You could, and for an *unsorted* list that's the right call. But it costs O(n) *space* for the map. Here the list is sorted, so two pointers gets the same O(n) time at **O(1) space** — no map. When it's sorted, pointers win. Saying exactly that out loud is a strong-hire detail.

---

## 12. YOUR TURN (active recall) — `8:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Valid Palindrome (LC 125)".]**

> **TEACHER:** Before the next video: **Valid Palindrome.** Read a string forwards and backwards — same idea, two pointers, but starting *together at the ends* and squeezing in. Try it before you watch. The struggle is the learning.

---

## 13. LOCK IT IN — `8:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> **TEACHER:** Three to keep:
> 1. **"Sorted" is the trigger** — it tells the pointers which way to move.
> 2. **Too big → right in; too small → left in.**
> 3. **O(n) time, O(1) space** — beats the hash map when the list is sorted.
>
> The peg: when you see **sorted + find a pair**, your hands should already be reaching for both ends.

---

## 14. CLIFFHANGER — `9:05`
*(open loop)*

**[VISUAL: blurred next title: "3Sum".]**

> **TEACHER:** Two numbers was easy. But what if the interviewer says *three* numbers that add to zero — with duplicates you can't repeat? Your two loops become three, and it explodes. Next lesson, we take this exact squeeze and use it to tame 3Sum. See you there.

---

## Appendix — Java version

```java
public int[] pairSum(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left < right) {
        int s = arr[left] + arr[right];
        if (s == target) return new int[]{left, right};
        else if (s < target) left++;
        else right--;
    }
    return new int[]{-1, -1};
}
```
