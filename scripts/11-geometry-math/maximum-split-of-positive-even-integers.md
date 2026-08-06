# 🎬 Recording Script — Maximum Split of Positive Even Integers
**Pattern: Greedy math construction · LeetCode 2178 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none required — but call back to the greedy exchange argument from the interval-packing lessons.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: the number `10,000,000,000` fills the screen. Beneath it, a wall of even numbers 2, 4, 6, 8, … scrolling forever. A recursion tree starts drawing itself, branches doubling, then freezes with a red "still running…" spinner.]**

> Here's a problem that looks like it needs a search, and doesn't. Split a number into as many **distinct positive even** numbers as you can. Ten to the tenth is the limit.

> Your brain says subset-sum. Take it, skip it, branch, recurse. And that recursion tree? It never finishes. Not slow — *never*.

> **[VISUAL: the tree collapses. Four lines of code fade in where it was.]**

> The real solution is four lines and runs in microseconds. But there's one line in it that looks illegal the first time you see it — you add a leftover number onto the end of your list, and somehow everything stays valid. By the end of this video you'll be able to *prove* why that's safe. That proof is the whole lesson. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below it, a big number `12` with three coins labeled 2, 4, 6 dropping into it.]**

> The whole problem in one line: **given `finalSum`, break it into the longest possible list of distinct positive even numbers that add up to exactly it.**

> Three words do all the work. **Distinct** — no repeats. **Positive even** — 2, 4, 6, and up; never zero, never odd. And **maximum** — you're maximising *how many* numbers, not how big they are.

> Tiny example. `finalSum = 12`. Answer: **2, 4, 6**. Three numbers, all even, all different, they sum to twelve.

> **[VISUAL: a second attempt appears — 2, 4, 6, 8 — with a red X and "= 20, too big".]**

> Could you get four? The four *cheapest* distinct evens are 2, 4, 6, 8 — that's already 20. Blows past 12. So three is the ceiling here.

> Hold that number 12. And hold a second one: **28**. We'll come back to 28, because that's where it gets interesting.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: a take/skip binary tree for finalSum = 12, drawn by hand. Root "remaining 12, next 2". Two children: "take 2 → rem 10" and "skip 2 → rem 12". Branches keep splitting.]**

> Let's do what your brain does first. Distinct numbers from a pool, hitting a target — that's subset-sum. So: line up 2, 4, 6, 8, and for each one, branch. Take it, or skip it.

> Take 2, remaining 10. From there, take 4, remaining 6. Take 6, remaining 0 — hit! Three numbers. Record it.

> **[VISUAL: that path highlights green. Then the camera pulls back and dozens of other branches light up grey, most ending in red dead-ends.]**

> But we can't stop there — we don't know it's the *longest* until we've explored the rest. Skip 2, take 4, take 8 — that's 12 too, but only two numbers. Worse. Keep going. Every branch, twice as many below it.

> **[VISUAL: a counter "nodes explored" spinning up; the tree depth labeled "finalSum / 2".]**

> Two branches per even number, and there are `finalSum / 2` evens to consider. That's **2 to the power of finalSum over 2**.

> **[VISUAL: "finalSum = 60 → already crawling" then "finalSum = 10¹⁰ → 🪦".]**

> At sixty, it's already crawling. At ten billion, you're not getting an answer in this lifetime. This isn't a "optimise the constant" situation. It's the wrong shape entirely.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: the frozen tree. A spotlight on one node showing "take 2? or skip 2?" with a big question mark. A 5-second "🤔 your turn" timer.]**

> **TEACHER:** Name the waste. Look at any single node in that tree. We're *searching* — branching on take-or-skip — as if the choice were hard. But is it?

> **LEARNER:** Wait. I'm trying to maximise the *count* of numbers, not their size. So a big number and a small number both count as one item — but the big one eats way more of my budget.

> **TEACHER:** That's the crack in it. If every part is worth exactly one point, and each part costs you budget… Pause the video right now. Two questions. One — which even number should you always take first? Two — before you search at all, is there an input where you can answer in *zero* steps?

> *(pause — 5 seconds)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: split screen. Left: "7" with a red gate slamming shut. Right: a shopping cart labeled "budget: 28" next to a shelf of price tags 2, 4, 6, 8, 10…]**

> Second question first, because it's free money. **If `finalSum` is odd, the answer is an empty list.** Even plus even is even, always. You can never build an odd total out of even parts. One modulo check, done — no search.

> **[VISUAL: "7 → [] " with a green check.]**

> Now the real one. Think of it as **shopping with a fixed budget**, where you're trying to walk out with the most *items* — not the most value. Every item counts as one. So what do you do? You buy the **cheapest thing on the shelf**, every single time.

> The cheapest distinct positive even is 2. Then 4. Then 6. There's no decision to make — the greedy choice is forced.

> **[VISUAL: budget counter at 28. Coins fly into a cart one at a time: 2 (budget 26), 4 (22), 6 (16), 8 (8). Then the next price tag "10" glows red against a budget of 8.]**

> Let's spend 28. Grab 2 — 26 left. Grab 4 — 22 left. Grab 6 — 16 left. Grab 8 — 8 left. Next up is 10… and I've only got 8. Can't afford it.

> **[VISUAL: freeze. The leftover 8 sits alone on the counter, blinking.]**

> And here's the awkward moment. I've got **8 left over**. I can't buy another item with it — but I can't leave it behind either, because my numbers have to sum to *exactly* 28.

> **LEARNER:** So just… stick it onto the last one? Make the 8 into a 16? That feels like cheating. Doesn't that risk colliding with a number I already took?

> **TEACHER:** Best question in the problem — and the answer is no, it can never collide. Here's why, and I want you to be able to say this out loud in an interview.

> **[VISUAL: three proof cards flip up one at a time.]**

> **Card one: the leftover is even.** The total started even, everything I subtracted was even, so what's left is even. Even plus even is even — the last element stays legal.

> **Card two: it only grows the maximum.** The last number I took was already the biggest in my list. Adding to it pushes it *further* above everything else. You can't create a duplicate by making your largest number larger.

> **Card three: the count doesn't change.** I edited an existing item; I didn't add one or drop one. So the length I earned in the loop is the length I return.

> **[VISUAL: cart updates → [2, 4, 6, 16], with "sum = 28 ✓ · distinct ✓ · all even ✓ · 4 parts ✓".]**

> 2, 4, 6, 16. Four parts. Legal on every rule.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: one boxed line: "odd → [] · take 2, 4, 6, … while you can afford it · dump the leftover on the last one."]**

> Burn this in: **odd sum means empty list. Otherwise buy the cheapest even you haven't used, over and over, then pour whatever's left into the last number.**

> That sentence *is* the algorithm. Everything from here is typing.

---

## 7. CODE IT — LIVE & CHUNKED — `5:25`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Chunk one — the parity gate. This is the whole "impossible" case, in two lines.

```python
def maximumEvenSplit(finalSum):
    if finalSum % 2:
        return []                     # sum of evens is even → odd target is impossible
```

> **[VISUAL: add chunk 2, highlight it.]** Chunk two — the shopping loop. `i` is the price tag; `finalSum` doubles as the shrinking budget.

```python
    res = []
    i = 2
    while i <= finalSum:              # can the remaining budget still afford `i`?
        res.append(i)                 # buy the cheapest unused even
        finalSum -= i                 # spend it
        i += 2                        # next cheapest
```

> **[VISUAL: add chunk 3, spotlight it hard — it's the money line.]** Chunk three. One line. The one we just proved.

```python
    res[-1] += finalSum               # dump the leftover onto the largest part
    return res
```

> That's the entire solution. Four working lines and a guard.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:20`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Walk the *why*, line by line.

> `if finalSum % 2` — not an optimisation, a **correctness gate**. Without it the loop runs, and then `res[-1] += finalSum` quietly makes your last element odd. You'd return a wrong answer with total confidence. That's the worst kind of bug.

> `while i <= finalSum` — read this as *"can I still afford the next item?"* Note `finalSum` is being mutated as the remaining budget. If that bothers you, name it `remaining` — it reads better and costs nothing.

> **LEARNER:** Why `i <= finalSum` and not `i < finalSum`? If they're equal, I spend my whole budget and land on exactly zero — is that fine?

> **TEACHER:** It's not just fine, it's the *best* case. Equal means the remaining budget is exactly the next even number: take it, remainder hits zero, and the absorb line adds nothing. That's `finalSum = 12` — take 2, take 4, then `i` is 6 and the budget is 6, so we take it and land clean on `[2, 4, 6]`. Switch to strict less-than and you'd stop one item early, then absorb a 6 into the 4 and return `[2, 10]`. Two parts instead of three. That single character is the difference between accepted and wrong-answer.

> `res[-1] += finalSum` — after the loop, `finalSum` holds the leftover. It's even, and it's going onto the element that's already the maximum, so distinctness is safe. Also: after the loop `finalSum` is *always* the true remainder, including zero — so this line needs no `if`. Zero is a no-op.

> One safety note: `res[-1]` would crash on an empty list, which only happens when `finalSum` is zero. The constraints say at least 1, so we're fine — but say that out loud in the interview instead of hoping nobody asks.

---

## 9. DRY-RUN THE CODE — `7:35`
*(worked example — prove it, close the loop)*

**[VISUAL: trace table filling row by row, with the cart animation mirroring it.]**

> Run the real code on 28.

| Step | `i` | `i <= remaining`? | `res` after | remaining |
|---|---|---|---|---|
| start | 2 | — | `[]` | 28 |
| take 2 | 2 | 2 ≤ 28 ✓ | `[2]` | 26 |
| take 4 | 4 | 4 ≤ 26 ✓ | `[2,4]` | 22 |
| take 6 | 6 | 6 ≤ 22 ✓ | `[2,4,6]` | 16 |
| take 8 | 8 | 8 ≤ 16 ✓ | `[2,4,6,8]` | 8 |
| stop | 10 | 10 ≤ 8 ✗ | `[2,4,6,8]` | **8 left** |
| absorb | — | — | `[2,4,6,`**`16`**`]` | 0 |

> Four parts. `[2, 4, 6, 16]`. Sums to 28. Loop closed — that's the promise from the cold open.

> **[VISUAL: two quick cards. Card A: "12 → [2,4,6], leftover 0, absorb is a no-op." Card B: "7 → odd → [] before the loop even starts."]**

> And our other two: 12 gives `[2, 4, 6]` with a zero leftover, so the absorb line does nothing. 7 is odd, so we return empty before the loop runs at all.

> **[VISUAL: freeze on `[2, 4, 6, 16]`. A "🤔 pause and predict" timer, 5 seconds, over the question "prove nobody can get 5 parts."]**

> Now the question an interviewer *will* ask, and I want you to answer it before I do. We got four parts out of 28. **Prove nobody can get five.** Pause the video. Hint: if a valid answer had five distinct even numbers, what's the *smallest* those five could possibly sum to?

> *(pause — 5 seconds)*

> **[VISUAL: five coins 2, 4, 6, 8, 10 land in a row; the total "30" stamps down next to "budget 28" with a red X. Then a bar chart: "2 + 4 + … + 2k = k(k+1)" with a horizontal red line at finalSum.]**

> There it is. Five distinct evens can't sum to less than 2 + 4 + 6 + 8 + 10 — that's **30**, and our budget is 28. Five is arithmetically impossible, no search needed.

> Generalise it: if any valid answer uses `k` numbers, the `k` cheapest distinct evens are 2, 4, up to 2k, and those sum to **k times k-plus-one**. So `k(k+1)` must be at most `finalSum` — a hard ceiling from arithmetic alone.

> And our loop? It stops exactly when it can't afford one more, which means it's sitting right at that ceiling. Greedy doesn't just find *a* good answer — it provably hits the bound.

---

## 10. COMPLEXITY, OUT LOUD — `8:45`
*(transfer to interview)*

**[VISUAL: two rows — Brute: O(2^(n/2)). Ours: O(√finalSum). Below: "10¹⁰ → 99,999 numbers".]**

> Complexity, and this one's satisfying. From `k(k+1) <= finalSum`, the answer holds about **√finalSum** numbers. So the loop runs √finalSum times. Time and space, both **O(√finalSum)**.

> Put a number on it — always put a number on it. At the limit, ten to the tenth, that's **99,999 numbers**. A hundred-thousand-element list, built in a hundred thousand operations. Microseconds.

> Say it the interview way: *"Brute force is exponential — take-or-skip over every even number. The greedy is O(√finalSum), because the answer can hold at most k numbers where k(k+1) ≤ finalSum. At the 10^10 limit that's about 10⁵ elements, so it's effectively instant."*

> Oh — and if you're writing Java: **`long`, everywhere.** Ten billion overflows a 32-bit `int` around 2.1 billion. `List<Long>`, `long i`. An `int` in that loop is a silent wrong-answer on exactly the tests you can't see.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:20`
*(depth + honesty)*

**[VISUAL: the output list glowing, labeled "this IS the answer". Beside it a tiny box: "aux: i, remaining → O(1)".]**

> Can we beat O(√finalSum) space? **No — and being able to explain why is worth more than any trick here.**

> That √finalSum is the size of **the output itself**. The problem asks you to *return the list*. You can't return a hundred thousand numbers using less than a hundred thousand numbers of space. The output dominates, so this is optimal — full stop.

> Everything *else* is O(1): one counter `i`, one shrinking remainder. Nothing else grows with the input.

> **[VISUAL: a "what if?" card — "count only? → k = (isqrt(4·finalSum + 1) − 1) // 2 → O(1)".]**

> Here's the proof that the √ is output-bound and not algorithm-bound. If the problem asked only *"how many parts?"* — not the list — you could answer in **O(1) time and O(1) space** with a square root: the largest `k` with `k(k+1) ≤ finalSum`. Same answer, no list, no loop.

> Say it out loud: *"Space is O(√finalSum), but that's the list I'm required to return, not overhead — auxiliary memory is O(1). If you only wanted the count, I'd give it to you in O(1) with a closed form."* That sentence is a strong-hire sentence. Naming why it can't shrink beats pretending there's a trick.

---

## 12. YOUR TURN (active recall) — `9:55`
*(retrieval practice)*

**[VISUAL: "Your turn → LC 1414. Minimum Number of Fibonacci Numbers Whose Sum Is K". A blank editor.]**

> Before the next video, go do **LeetCode 1414 — Minimum Number of Fibonacci Numbers Whose Sum Is K.**

> I picked it deliberately, because it's this problem in a **mirror**. Same move — greedy over a fixed family of numbers. But there you're *minimising* the count, so you grab the **largest** Fibonacci that fits, not the smallest. Cheapest-first versus biggest-first, driven purely by which direction the objective points.

> Get that contrast in your hands and you'll never again guess which end of the greedy to start from. Don't peek. Ten minutes of wrestling beats an hour of watching.

---

## 13. LOCK IT IN — `10:25`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three to keep:
> 1. **Check parity first.** A sum of evens is even — odd target, return empty, zero work. Free correctness, and it's the clarifying question you ask before you code.
> 2. **Maximise the count → take the cheapest legal piece, every time.** 2, then 4, then 6. There's no decision to search.
> 3. **Absorb the leftover into the largest element** — it stays even, it stays the maximum, so distinctness survives and the count doesn't change. And prove maximality with `k(k+1) ≤ finalSum`.

> The memory peg — the one line that recalls the whole pattern:

> **[VISUAL: big box → "cheapest first, then pour the rest on the biggest."]**

> **Cheapest first, then pour the rest on the biggest.** When a problem asks for the *most pieces* under a fixed budget, that's your reflex.

> *(GCA reminder — for the interview itself: lead with "if finalSum is odd there's no split at all, right?", then narrate "I want the most parts so I take the smallest evens first," then volunteer the two proofs — why absorbing is safe, and why k(k+1) bounds the answer — before you're asked. Google's General Cognitive Ability signal isn't the four lines of code. It's you proving the greedy is correct without being prompted.)*

---

## 14. CLIFFHANGER — `11:00`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in. Under it, the same shelf of numbers — but now every price tag flickers and *changes* as items are removed.]**

> Greedy worked here because the cheapest choice was *always* right — the shelf never changed, so grabbing 2 first could never hurt you later.

> But what happens when taking one item **changes the price of the next**? When the cheap move now makes every future move expensive? Greedy walks straight off a cliff, and you need something that can look ahead and un-commit.

> That's where this whole approach breaks — and where the next tool picks up. See you there.
