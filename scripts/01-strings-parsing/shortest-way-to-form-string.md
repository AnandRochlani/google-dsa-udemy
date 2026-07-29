# 🎬 Recording Script — Shortest Way to Form String
**Pattern: Greedy / Two Pointers · LeetCode 1055 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: two strings on a black screen — `source = "abc"` glowing green, `target = "abcbc"` glowing amber. A cursor blinks under `target`.]**

> Interviewer slides you two strings. *"Build the second one by gluing together subsequences of the first. How few pieces can you use?"*
>
> Your gut says: *"This smells like some heavy DP table."* You reach for a 2-D grid… and you freeze.
>
> Here's the good news. This one bends to a single greedy idea you can code in eight lines — no DP, no grid. But there's a catch buried in it: a moment where being greedy *feels* dangerous, like you'll regret it later. By the end of this video you'll know exactly why greedy is bulletproof here. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:30`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it: `source = "abc"`, `target = "abcbc"`. A reminder box: "subsequence = delete some letters, keep the order."]**

> The whole problem in one line: **glue together subsequences of `source` to spell `target`, using as few subsequences as possible — or return `-1` if it can't be done.**
>
> A subsequence just means: take `source`, delete some letters, keep the rest in order. So from `"abc"` you can make `"abc"`, `"ab"`, `"ac"`, `"bc"`, `"a"`… any in-order slice.
>
> Keep your eye on this tiny example. The answer here is **two**. Don't chase it yet — just hold that: two.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:05`
*(worked example — feel the mechanism)*

**[VISUAL: `target = "a b c b c"` across the top, a pointer `j` under the first `a`. Below, `source = "a b c"` ready to sweep. A "pieces used" counter at 0.]**

> Let's do what your brain does first. Point at the start of `target`. Now sweep `source` left to right, and every time a `source` letter matches the letter `j` is on, grab it — slide `j` forward.
>
> **[VISUAL: sweep 1. `a` matches `a` → j moves to `b`. `b` matches `b` → j to `c`. `c` matches `c` → j to the *second* `b`. End of source.]**
>
> One full pass of `source` used up `"abc"` — that's piece number one. Counter ticks to **1**. But `target` isn't done — `j` is sitting on the second `b`.
>
> **[VISUAL: sweep 2. Reset source to the left. `a` ≠ `b`, skip. `b` matches `b` → j to last `c`. `c` matches `c` → j falls off the end. Done.]**
>
> Second pass grabs `"bc"`. Counter ticks to **2**. `j` walked off the end — `target` is covered. Two pieces. That matches the answer we promised.

---

## 4. THE PAIN POINT + PREDICT — `2:15`
*(curiosity gap + generation effect — first pause)*

**[VISUAL: freeze on sweep 1, the moment `j` reaches the second `b`. A thought bubble: "should I have stopped grabbing sooner?" A 4-second 🤔 timer.]**

> **LEARNER:** Wait — in that first pass you *greedily* grabbed `a`, `b`, `c`, as much as you could. But what if grabbing all three was a mistake? What if stopping early would've lined up the next pass better and saved a piece?
>
> **TEACHER:** That is *exactly* the right fear, and it's the heart of this problem. So pause the video. Predict: can taking the **longest possible bite** each pass ever cost you extra pieces later? Yes or no — and why?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `2:55`
*(elaboration + analogy — derive it)*

**[VISUAL: two horizontal bars. Bar A "greedy": long chunk consumed. Bar B "stopped early": shorter chunk. Arrows show where the *next* pass can start on each.]**

> **TEACHER:** Here's why greedy is safe. Think of each pass as eating along `target` from wherever you left off. If greedy pass eats up to position 3, and some "cautious" pass stops at position 2 — where does the *next* pass start? Greedy starts further ahead. It is *never behind*.
>
> **[VISUAL: Bar A's next arrow lands right of Bar B's. Caption: "greedy is always ≥ ahead."]**
>
> Eating more now can't strand you later, because the next subsequence starts fresh from the *whole* `source` anyway. The passes don't compete for letters — each one gets a full clean copy of `source`. So more progress this pass is pure upside.
>
> **LEARNER:** Okay — but what if `target` has a letter that just isn't in `source` at all?
>
> **TEACHER:** Then you're stuck forever — no pass ever moves past it. That's your `-1`. And you catch it up front: compare the letter sets. If `target` has anything `source` doesn't, bail immediately. One line, before you loop.
>
> **[VISUAL: `source="abc"`, `target="acdbc"` → the `d` flashes red, "not in source → -1".]**

---

## 6. THE KEY MOVE (signaling) — `4:05`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line — "Sweep source, take the longest bite of target each pass. Count the passes."]**

> Burn this in: **each pass, eat as much of `target` as one sweep of `source` can. Count the passes. That count is your answer.**
>
> Greedy works because subsequences don't share — every pass restarts from a full `source`, so getting further now never hurts you. That one sentence is the whole solution.

---

## 7. CODE IT — LIVE & CHUNKED — `4:40`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. Chunk one — the feasibility guard. If `target` has a letter `source` lacks, it's impossible.

```python
def shortestWay(source, target):
    if set(target) - set(source):
        return -1
```

> **[VISUAL: add chunk 2, highlight it.]** Two counters: `count` for pieces, `j` for how far into `target` we've gotten.

```python
    count = 0
    j = 0
    n = len(target)
```

> **[VISUAL: add chunk 3.]** The outer loop is "keep taking passes until `target` is covered." The inner loop is one sweep of `source`.

```python
    while j < n:
        prev = j                     # where this pass started
        for ch in source:
            if j < n and ch == target[j]:
                j += 1               # greedily consume this target char
        count += 1                   # one full sweep = one subsequence
```

> **[VISUAL: add chunk 4, highlight the `prev` check.]** One safety line: if a whole pass matched *nothing*, we're stuck — but the set check already guarantees that won't happen, so it's a belt-and-suspenders guard. Then return the count.

```python
        if j == prev:
            return -1
    return count
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:10`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `set(target) - set(source)` — set subtraction. It's every letter in `target` that `source` is missing. Non-empty means impossible. This is the whole `-1` case in one line.
>
> `if j < n and ch == target[j]` — the `j < n` guard matters. Once `j` hits the end mid-sweep, we must stop advancing or we'd index off `target`. That guard is easy to forget and it's the classic bug here.
>
> **LEARNER:** Why increment `count` *after* the whole inner sweep, and not each time we match a character?
>
> **TEACHER:** Because a subsequence is *one entire pass* of `source`, however many letters it happened to grab. Match five letters or match one — it's still a single piece. So the count ticks once per sweep, not per letter. That distinction is the whole problem: we're counting *passes*, not characters.
>
> `if j == prev: return -1` — if a full pass moved `j` nowhere, no pass ever will; we'd loop forever. The set check makes this unreachable, but it's a cheap insurance line.

---

## 9. DRY-RUN THE CODE — `7:15`
*(worked example — prove it, close the loop)*

**[VISUAL: `source="xyz"`, `target="xzyxz"`. A trace table filling row by row; `j` pointer riding along `target`.]**

> New example so it's not memorized — `source = "xyz"`, `target = "xzyxz"`. Let's run the actual code.

| Pass | sweep of `source` matches | `j`: start → end | `count` |
|---|---|---|---|
| 1 | `x`→x, `y`≠z, `z`→z | 0 → 2 (past `x z`) | 1 |
| 2 | `x`≠y, `y`→y, `z`≠x | 2 → 3 (past `y`) | 2 |
| 3 | `x`→x, `y`≠z, `z`→z | 3 → 5 (past `x z`) | 3 |

> `j` reached 5 — the end. Three passes: `"xz"` + `"y"` + `"xz"`. Answer **3**. Loop closed — the greedy sweep did exactly what we traced by hand.

---

## 10. COMPLEXITY, OUT LOUD — `8:15`
*(transfer to interview)*

**[VISUAL: two rows — "Passes × sweep = O(|source| · |target|) time", "O(1) space". Below, a faded second option: "next-index table → O((|source|+|target|)·26)".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Worst case I take about `|target|` passes, and each pass sweeps all of `source`, so it's `O(|source| · |target|)` time. Space is `O(1)` — just two indices and a counter."*
>
> Then the upgrade line that shows depth: *"If `source` were huge, or reused against many targets, I'd precompute a next-index table — for each spot and each letter, the next place that letter appears. Matching becomes one lookup instead of a scan: `O((|source| + |target|) · 26)` time for `O(|source| · 26)` space."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:00`
*(depth + honesty)*

**[VISUAL: the two-pointer code with a green "O(1)" badge; beside it the table version with an "O(|source|·26)" badge and a two-way arrow labeled "time ⇄ space".]**

> Quick but important — and here honesty scores.
>
> The two-pointer version I just wrote is *already* `O(1)` space. Nothing grows with the input — two indices, one counter, a couple of 26-letter sets. There's no memory to trim.
>
> The next-index table is the *opposite* trade: it spends `O(|source|·26)` memory to buy speed. So this isn't "optimal vs not" — it's a genuine **fork**. Say that out loud: *"At n up to a thousand I'd ship the O(1) sweep for clarity; the table is my move only if source is large or reused."* Naming the trade-off beats blindly reaching for the fancy one.

---

## 12. YOUR TURN (active recall) — `9:40`
*(retrieval practice)*

**[VISUAL: "Your turn → Is Subsequence (LC 392)" and its follow-up. A blank editor.]**

> Before the next video, do **Is Subsequence** — LeetCode 392. It's the single atom this whole problem is built from: does one string appear as a subsequence of another? One pass, two pointers.
>
> Then read its follow-up: *what if you had billions of queries against the same string?* That's where the next-index table earns its keep — the exact table I mentioned. Wrestle with it for ten minutes before you peek. That struggle is what makes it stick.

---

## 13. LOCK IT IN — `10:10`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Check the letter sets first.** A letter in `target` that's missing from `source` → instant `-1`.
> 2. **One sweep of `source` = one subsequence.** Count passes, not characters.
> 3. **Greedy is safe** because passes don't share letters — eating more now never strands a later pass.
>
> And the memory peg:
>
> **[VISUAL: big box → "Longest bite every pass. Count the bites."]**
>
> When you see *"build one string out of repeated passes of another,"* your hand should already be reaching for a greedy two-pointer — not a DP grid.
>
> *(GCA reminder — for the interview itself: Google scores how you *think out loud*. Ask the clarifying question first — "can I reuse source freely? are these lowercase letters?" — then state the greedy plan and *say why greedy is safe* before you code. Narrating naive → greedy → the safety argument is the General Cognitive Ability signal, more than the code itself.)*

---

## 14. CLIFFHANGER — `10:45`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Shortest Common Supersequence" — two strings feeding into a woven, interleaved result, with a DP grid ghosting behind it.]**

> Here's the twist that breaks everything we just did. What if you *can't* take whole clean passes — what if you're allowed to **interleave** two strings, weaving them character by character into the shortest string that contains both? Suddenly greedy falls apart, and the DP grid we dodged today comes roaring back. That's **Shortest Common Supersequence** — next video. See you there.
