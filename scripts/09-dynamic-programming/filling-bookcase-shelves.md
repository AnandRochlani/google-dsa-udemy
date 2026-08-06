# 🎬 Recording Script — Filling Bookcase Shelves
**Pattern: DP / linear DP over prefixes (partition DP) · LeetCode 1105 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Text Justification (LC 68) — we lean on it hard as the *contrast* case. Also assumes they've seen the row-DP lesson (LC 1937).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a bookcase graphic. Books slide on left-to-right, cramming each shelf completely full. A total height counter ticks up: `8`. Then a red stamp: "Wrong Answer — Expected 6". The counter mocks you.]**

> Here's a problem where your instinct is going to betray you in the first ten seconds.
>
> You've got a stack of books and a bookcase. Put them on shelves, in order, don't exceed the shelf width. Minimise the total height. Obvious, right? **Cram each shelf as full as it fits.** One loop. Thirty seconds. Ship it.
>
> That answer is **wrong**. And it's not wrong on some evil hidden test — it's wrong on the *example in the problem statement*. Greedy says eight. The answer is six.
>
> **[VISUAL: freeze on "8 vs 6".]**
>
> By the end of this video you'll know exactly why greedy dies here, when it *does* work — because two lessons ago it worked perfectly — and the one-line DP that fixes it. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below: three book tiles drawn to scale — a wide short one `w3 h1`, then two skinny tall ones `w1 h5`, `w1 h5`. A shelf ruler marked `shelfWidth = 4`.]**

> The whole problem in one line: **place the books onto shelves in the given order; each shelf's height is its tallest book; minimise the sum of the shelf heights.**
>
> Two rules do all the work. One — **you cannot reorder the books.** They go on in the order you're given. Two — a shelf costs the height of its **tallest** book. Adding a short book next to a tall one is free. Adding a *tall* book is not.
>
> Here's our tiny example. Three books. Shelf width four. Book one: three wide, one tall — a wide paperback lying flat. Books two and three: one wide, five tall — two skinny hardbacks.
>
> Hold onto these three. Everything today runs on them.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the trap)*

**[VISUAL: greedy packing animated. Book 1 (w3) lands on shelf 1. Book 2 (w1) slides in beside it — `3+1 = 4`, exactly full, shelf glows. Shelf height label jumps from 1 to **5**. Book 3 can't fit → drops to shelf 2, height **5**.]**

> Let's do what your brain does first. Greedy. Fill every shelf to the brim.
>
> Shelf one: book one, three wide. Room for one more unit — and book two is exactly one wide. **Perfect fit.** Shelf one is completely full. Nice.
>
> But watch the height label. It was **one**. Book two is five tall. So shelf one now costs **five**.
>
> **[VISUAL: shelf 1 height label animates 1 → 5, flashing red.]**
>
> Book three won't fit — shelf's full. New shelf. It's five tall, all by itself. Shelf two costs **five**.
>
> Total: five plus five. **Ten.**
>
> **[VISUAL: total = 10, with a big empty gap of wasted air on shelf 2.]**
>
> And look at all that empty space on shelf two. We packed shelf one perfectly and *still* wasted the whole bookcase. Something's off.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(pause #1 — generation effect)*

**[VISUAL: the greedy result (10) on the left, frozen. On the right, an empty bookcase outline with the same three books waiting. A 5-second "🤔 your turn" timer.]**

> **TEACHER:** So here's the question. Can you beat ten — with these exact three books, in this exact order, shelf width four?
>
> **LEARNER:** But shelf one was *completely full*. There's no wasted width anywhere. How can there be a better arrangement?
>
> **TEACHER:** That's exactly the right objection, and it's the trap. You're optimising **width**. The problem is charging you for **height**. Those aren't the same thing.
>
> Pause the video. Three books, shelf width four. Find an arrangement that beats ten. I'll wait.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration — derive it from the dry-run)*

**[VISUAL: the better arrangement builds. Shelf 1: book 1 alone, a big empty gap beside it, height label **1**. Shelf 2: books 2 and 3 side by side, width 2, height label **5**. Total = **6**.]**

> Here it is. Leave book one **alone** on shelf one — deliberately waste a unit of width. Shelf one costs **one**.
>
> Now the two tall books land on shelf two, side by side. They're both five tall, so they *share* that height. Shelf two costs **five**.
>
> One plus five. **Six.** We beat greedy by four, and we did it by leaving space empty on purpose.
>
> **[VISUAL: side-by-side. Left "greedy, packed tight: 10". Right "leave a gap: 6". The two tall books on the right glow — "these two overlap in height, so they're nearly free together".]**
>
> Here's the mechanism, and I want you to feel it, not memorise it. A shelf's cost is a **max**. One tall book poisons the entire shelf. Once you've paid five for that shelf, every short book you add next to it is **free** — but every *other* tall book you didn't put there is going to cost you five all over again.
>
> So the winning move is: **get the tall books to share a shelf.** Sometimes that means shoving a short book out of the way — or letting it sit alone.
>
> **[VISUAL: split-screen callback. Left: the Text Justification lesson thumbnail, greedy line-packing, a green tick. Right: this bookcase, greedy, a red cross.]**
>
> **LEARNER:** Hang on — two lessons ago, in Text Justification, greedy line-packing was the *correct* answer. Same shape of problem. Why does it break now?
>
> **TEACHER:** Beautiful question, and this is the transferable lesson of the whole video. In Text Justification, a line costs you **nothing**. Any packing that fits is legal — the spaces just spread out. So packing tight is never worse.
>
> Here, every shelf sends you a bill: **the max height on it**. And a max doesn't get cheaper when you add more stuff. That's what changed. **The chunk has a cost, and the cost isn't smooth.** The instant a per-chunk cost is a max — or a product, or anything with a cliff in it — greedy is a guess, not an algorithm.

---

## 6. THE KEY MOVE (signaling) — `4:40`
*(one crisp, repeatable line)*

**[VISUAL: a single boxed line: "dp[i] = min height for the first i books. Ask only: which books share the LAST shelf?"]**

> So we do DP. And here's the whole thing in one sentence:
>
> **`dp[i]` is the minimum height for the first `i` books — and the only question I ever ask is: which books share the *last* shelf?**
>
> That's it. That's the algorithm. And notice *why* it's legal: the books go on **in order**. So a half-finished bookcase is described by exactly one number — how many books I've placed. No sets, no permutations. One index.
>
> **[VISUAL: the phrase "in the given order" highlighted in the problem statement, with an arrow to "→ state = one index".]**
>
> If you were allowed to reorder the books, this would be bin packing and it'd be NP-hard. That one phrase in the spec — *in the given order* — is the entire reason a clean DP exists. Say that out loud in your interview.

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. The table, and the one base case that matters.

```python
def minHeightShelves(books, shelfWidth):
    n = len(books)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0                     # zero books → zero height
```

> **[VISUAL: add chunk 2, highlight the loop header.]** Now fill left to right. For each `i`, I'm going to look at every possible **last shelf**.

```python
    for i in range(1, n + 1):
        width, height = 0, 0
        j = i
```

> **[VISUAL: add chunk 3. Animate `j` sliding backwards from `i` while a shelf outline grows leftward.]** Here's the heart. Walk `j` **backwards** from `i`, pulling one more book onto the last shelf each step.

```python
        while j >= 1:
            width += books[j - 1][0]
            if width > shelfWidth:
                break
            height = max(height, books[j - 1][1])
```

> **[VISUAL: add chunk 4, highlight the min line.]** And this is the whole recurrence. The last shelf holds books `j` through `i`. Everything before it is already solved — that's `dp[j-1]`.

```python
            dp[i] = min(dp[i], dp[j - 1] + height)
            j -= 1

    return dp[n]
```

> Eleven lines. That's the entire solution.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:50`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk the *why*.
>
> **`dp[0] = 0`.** Zero books, zero height. Everything else starts at infinity so the `min` has something to beat.
>
> **Why `j` goes backwards.** This is the piece people get wrong. The last shelf holds books `j..i`, and I need its **width sum** and its **max height**. If I looped `j` forwards, every candidate shelf would be a fresh range and I'd have to recompute that max from scratch — an extra loop inside the loop. Going backwards, each step just adds *one* book to the left end, so `width += ...` and `height = max(...)` update in constant time. Same answer, one loop cheaper.
>
> **LEARNER:** That `break` — isn't it dangerous? You're bailing out of the loop. Could a shelf that's too wide right now become legal if you kept going?
>
> **TEACHER:** Nope, and this is the nicest little proof in the problem. Reaching back further only ever **adds** books, and every width is at least one. So once the shelf overflows, it can only get wider. It's monotone. `break` isn't a shortcut — it's the correct stopping condition. And it's also why this thing runs fast in practice: the inner loop only spins as many times as books fit on one shelf.
>
> **And the recurrence itself** — `dp[j-1] + height`. Read it in English: *"the best possible bookcase for everything before book `j`, plus the cost of one more shelf holding books `j` through `i`."* Those two pieces don't interfere. The books below don't change the shelf above, and the shelf above doesn't change the books below. That independence is optimal substructure, and it's the thing greedy was assuming without checking.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close the loop)*

**[VISUAL: four books now — `[3,1] [1,5] [1,5] [3,1]`, shelfWidth 4. A dp array of 5 cells fills left to right; the candidate last shelf highlights as a sliding bracket.]**

> Let's run the real code. I've added a fourth book — another wide short one — so we get a proper table. Widths and heights: three-by-one, one-by-five, one-by-five, three-by-one. Shelf width four.
>
> **[VISUAL: the dp array with `dp[0]=0, dp[1]=1, dp[2]=5` filled, and `dp[3]` blinking empty. A 5-second "🤔 your turn" timer.]**
>
> Actually — **pause here.** I'll give you the first three cells: zero, one, five. Row three is the interesting one. Book three is a skinny five-tall hardback. Work out `dp[3]` yourself: what are the candidate last shelves, and which one wins?
>
> *(pause)*

| `i` | candidate last shelves (`books j..i` → width, height, `dp[j-1] + h`) | `dp[i]` |
|---|---|---|
| 1 | `1..1` → w3, h1, `0+1 = 1` | **1** |
| 2 | `2..2` → w1, h5, `1+5 = 6` · `1..2` → w4, h5, `0+5 = 5` | **5** |
| 3 | `3..3` → w1, h5, `5+5 = 10` · `2..3` → w2, h5, **`1+5 = 6`** · `1..3` → w5 ✗ break | **6** |
| 4 | `4..4` → w3, h1, **`6+1 = 7`** · `3..4` → w4, h5, `5+5 = 10` · `2..4` → w5 ✗ break | **7** |

> `dp = [0, 1, 5, 6, 7]`. Answer: **seven**.
>
> Greedy on this same input gives **ten**. And look at row three — that's the moment. The DP considered putting book three alone on its own shelf (cost ten) and putting books two and three **together** (cost six). It picked six. It found the "let the two tall books share" move all by itself, just by trying every last shelf.
>
> **[VISUAL: backtrack arrows light up: dp[4] ← dp[3] ← dp[1] ← dp[0]. Shelves render: [book1] / [book2, book3] / [book4]. Heights 1 + 5 + 1 = 7.]**
>
> Trace it back: shelf one is book one alone, shelf two is the two tall books together, shelf three is book four. One plus five plus one. Seven. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: one row — Time: O(n²) worst case, really O(n·k). Space: O(n). Note: "n ≤ 1000".]**

> Say it the way you'd say it in the room: *"Outer loop over `n` prefixes, inner loop walks back over the last shelf — worst case that's `O(n²)`, though really it's `n` times however many books fit one shelf. Space is `O(n)` for the table."*
>
> And then add the sentence that shows you read the constraints: *"`n` is capped at a thousand, so a million operations is nothing. The constraint is telling me not to be clever — it's telling me to be **correct**."*
>
> That's a genuinely useful habit. When a Medium gives you a suspiciously small `n`, the interviewer is usually hiding a *correctness* trap, not a speed trap. Here the trap was greedy.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty — naming the absence)*

**[VISUAL: the dp array. An arrow from `dp[i]` reaches back one cell — then stretches, and stretches, and snaps all the way to `dp[i-1000]`. A crossed-out "two rolling variables?"]**

> Can we squeeze the space down? Last lesson we rolled a whole 2-D table into one row. So — can we roll this `O(n)` array into a couple of variables?
>
> **No. And knowing why is the actual skill here.**
>
> Think about what `dp[i]` reads. It reads `dp[j-1]` for every `j` where the shelf still fits. How far back is that? **It depends on the data.** If every book is one unit wide and the shelf is a thousand wide, one shelf holds a thousand books — so `dp[i]` reaches all the way back to `dp[i - 1000]`. If every book is exactly shelf-width, it only ever reads `dp[i-1]`.
>
> **[VISUAL: two mini-diagrams — "skinny books → reach 1000" vs "fat books → reach 1".]**
>
> The lookback window is **unbounded and data-dependent.** You can't size a rolling buffer for that without... an `O(n)` buffer. So `O(n)` is the floor.
>
> Compare it to House Robber or Fibonacci, where two variables do the job. The difference is one word: whether the lookback is bounded by a **constant**. Here it isn't. Say that in the interview instead of inventing a fake optimisation — *"I'd keep the full array; the DP window is unbounded so there's no rolling trick"* is a strong-hire answer.

---

## 12. YOUR TURN (active recall) — `10:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Partition Array for Maximum Sum (LC 1043)". A blank editor.]**

> Before the next video, do **Partition Array for Maximum Sum**, LeetCode 1043. It's the near-twin of this one, and I mean *near*.
>
> Same `dp[i]` over prefixes. Same backwards inner loop tracking a running max. The only two differences: the chunk limit is "at most `k` elements" instead of a width budget, and you're **maximising** instead of minimising.
>
> If you understood today, you can write it in five minutes. If you can't — that's useful information, come back and re-watch beat six. Don't peek at the solution. The struggle is the part that sticks.

---

## 13. LOCK IT IN — `11:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Greedy is a claim, not a default.** Before you pack tight, ask: *does this chunk's cost punish me for packing tight?* If the cost is a `max`, it does.
> 2. **"In the given order" is the DP permission slip.** Fixed order means your state is one index — `dp[i]` over prefixes.
> 3. **The only question is the last chunk.** Walk `j` backwards, accumulate the chunk's cost, `break` when it's illegal.
>
> And the memory peg — **one tall book poisons a shelf.** Picture it. That single image tells you why greedy fails, why you'd leave a gap on purpose, and why you have to try every last shelf instead of guessing one.

---

## 14. CLIFFHANGER — `11:35`
*(open loop to next lesson)*

**[VISUAL: a blurred title card — "Burst Balloons (LC 312)". Behind it, a row of balloons; a cut line tries to slide in from the left and bounces off.]**

> One last thought before you go. Today's whole DP worked because a partial answer was a **prefix** — books one through `i`, a clean left-to-right story. Every partition DP you'll meet has that shape.
>
> So here's the itch. What happens when the chunks **don't** line up as prefixes? When the thing you remove from the middle changes what its two neighbours are worth — so there's no "first `i` items" to build on at all?
>
> Your `dp[i]` array is useless there. You need a second dimension, and you have to stop asking *"what's the last chunk?"* and start asking a much stranger question: *"what's the **last** thing standing?"*
>
> That's interval DP. That's Burst Balloons. And it's the hardest, prettiest idea in this whole section. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int minHeightShelves(int[][] books, int shelfWidth) {
    int n = books.length;
    int[] dp = new int[n + 1];
    dp[0] = 0;                                   // zero books → zero height

    for (int i = 1; i <= n; i++) {
        dp[i] = Integer.MAX_VALUE;
        int width = 0, height = 0;
        // walk j backwards: books j..i share the LAST shelf
        for (int j = i; j >= 1; j--) {
            width += books[j - 1][0];
            if (width > shelfWidth) break;       // monotone — can only get wider
            height = Math.max(height, books[j - 1][1]);
            dp[i] = Math.min(dp[i], dp[j - 1] + height);
        }
    }
    return dp[n];
}
```

*(`n ≤ 1000` and heights `≤ 1000`, so the total maxes out near 10⁶ — plain `int` is safe. And `dp[i]` can never be left at `MAX_VALUE`, because the spec guarantees every single book fits on a shelf by itself.)*
