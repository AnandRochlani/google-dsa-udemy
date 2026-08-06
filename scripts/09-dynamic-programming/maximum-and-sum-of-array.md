# 🎬 Recording Script — Maximum AND Sum of Array
**Pattern: bitmask assignment DP (half-slot split + popcount collapse) · LeetCode 2172 · Hard · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Section 9's row DP (Maximum Number of Points with Cost) taught you to speed up a *transition*. This one is harder in a different direction: the transition is trivial — **finding the state** is the whole problem.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a LeetCode constraints panel, zoomed. One line glows: `1 <= numSlots <= 9`. Below it: `n <= numSlots * 2`. A red annotation slams in: "n ≤ 18".]**

> Constraints are usually background noise. Not here. Look at this one: **at most 18 numbers.** Eighteen.
>
> That's not the problem being generous. That's the problem **telling you the answer** — and most candidates read straight past it, write a beautiful backtracking solution, and watch it churn through twelve *trillion* placements.
>
> **[VISUAL: a spinning recursion tree; a counter blurs past 10¹³. Then a red "Time Limit Exceeded".]**
>
> By the end of this video you'll read `n ≤ 18` the way a senior engineer does — as three words: **"bitmask over subsets."** And you'll see one collapse so clean that a two-dimensional DP table becomes one-dimensional for free. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, three numbered boxes labelled "slot 1", "slot 2", "slot 3", each with two empty seats drawn inside. Six number chips wait at the bottom: 1 2 3 4 5 6.]**

> The whole problem in one line: **drop every number into a numbered slot — at most two numbers per slot — and your score is the sum of `number AND slot-number`. Maximize it.**
>
> The AND is against the slot's **number**, not against whatever else is in it. Slot 3 is the literal integer 3.
>
> Here's the real LeetCode example: numbers one through six, three slots.
>
> **[VISUAL: chips animate in — 1 and 4 into slot 1; 2 and 6 into slot 2; 3 and 5 into slot 3. Each lands with its AND value floating up.]**
>
> `1 AND 1` is 1. `4 AND 1` is 0. `2 AND 2` is 2. `6 AND 2` is 2. `3 AND 3` is 3. `5 AND 3` is 1. Add them: **9**. That's the best possible.
>
> Hold that number — 9 — we'll earn it properly later.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: shrink to a tiny case — numbers `[1, 2, 3]`, two slots. A recursion tree grows: number 1 branches to slot 1 / slot 2, then number 2 branches, then number 3. A "leaves" counter ticks.]**

> Let's do what your brain does first. Take `nums[0]`. Try it in slot 1. Then take `nums[1]` — try *it* in slot 1, then slot 2. Recurse. Keep the best total.
>
> **[VISUAL: highlight two sibling branches side by side — "1→slot 1, then 2→slot 2" and "1→slot 2, then 2→slot 1". Both subtrees below them light up identically in orange.]**
>
> Now watch these two branches. On the left, number 1 went to slot 1 and number 2 went to slot 2. On the right, they swapped. **Different scores so far.**
>
> But look at what's *left* to do. Both branches: number 3 still homeless, slot 1 down one seat, slot 2 down one seat. The remaining problem is **byte-for-byte identical** — and we solve it twice from scratch.
>
> At three numbers that's a rounding error. Scale it up.
>
> **[VISUAL: a table fills in — n=12 → 7.5 million · n=14 → 681 million · n=16 → 81 billion · n=18 → 12,504,636,144,000.]**
>
> At the actual constraint ceiling — 18 numbers, 9 slots — that's **twelve and a half trillion** placements. That's not slow. That's geologic.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — **pause #1**)*

**[VISUAL: freeze on the two identical subtrees. A thought bubble over them: "the future doesn't care HOW we got here." A 5-second "🤔 your turn" timer.]**

> **TEACHER:** So here's the exact waste, in one sentence: **the future doesn't care how we got here — only which seats are already gone.** Anytime that's true, you're not looking at a backtracking problem. You're looking at a DP wearing a backtracking costume. The only question left is: what's the state?
>
> **LEARNER:** Then the state's just "how full is each slot," right? Nine slots, each holding zero, one, or two. But that's not a bitmask — a bit is on or off, and I've got *three* levels per slot. Do I need a nine-dimensional array?
>
> **TEACHER:** That is precisely the wall, and it's where most people stall out. Pause the video right now. You need a state that's a clean set of on/off things, but a slot has three occupancy levels. **How do you turn a bin that holds two items into something a single bit can describe?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:25`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: slot boxes on screen. A vertical dashed line slices each one down the middle, splitting it into two labelled seats. Slot 1 becomes seats 0 and 1; slot 2 becomes seats 2 and 3; slot 3 becomes seats 4 and 5.]**

> **TEACHER:** Here's move one. **Stop thinking about slots. Think about seats.**
>
> A slot that holds two numbers is really two seats that hold one number each. So `numSlots` slots become `2 × numSlots` seats — and every seat is exactly one thing: **taken or free.** One bit. The awkward three-level counter just became a plain subset.
>
> Think of it like a cinema row. You don't track "row C is 60% full" — you track which *chairs* are occupied. Same information, infinitely easier to index.
>
> **[VISUAL: seat indices 0..5 appear under the seats, with the mapping `slot = b // 2 + 1` written large.]**
>
> And we lose nothing, because the seat remembers its slot: **seat `b` lives in slot `b // 2 + 1`.** Seats 0 and 1 → slot 1. Seats 2 and 3 → slot 2. Integer division does the whole job.
>
> **LEARNER:** Hang on — I just doubled the thing that's in the exponent. Nine slots became eighteen seats, so `2^18` instead of `2^9`. Isn't that a terrible trade?
>
> **TEACHER:** It *is* a real cost, and you should feel it — `2^9` would be five hundred states, `2^18` is two hundred sixty thousand. What you bought is a state you can actually index with one integer and update with two bit operations. And hold that objection, because in the space beat I'm going to hand you most of that cost back.
>
> So now: `dp[mask][i]` — best score after placing the first `i` numbers into the seats named by `mask`. Eighteen seats, `2^18` masks, times 18 values of `i`. Fine. But…
>
> **[VISUAL: the `[i]` in `dp[mask][i]` starts pulsing red.]**
>
> **TEACHER:** Look at `i` for a second. If I always place numbers in array order — number 0, then 1, then 2 — and each one takes exactly one seat… then how many seats are occupied when I've placed `i` numbers?
>
> **[VISUAL: a mask `101101` with its set bits counting up: 1, 2, 3, 4. Beside it: `i = 4`.]**
>
> **Exactly `i`.** Always. So `i` isn't information — `i` is just `popcount(mask)`. It's a *function* of the mask, not a second dimension.
>
> **[VISUAL: the `[i]` dimension shatters and falls away, leaving `dp[mask]`.]**
>
> Delete it. The table is one-dimensional. That right there is the most beautiful thing in this problem.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line, held on screen: "capacity-2 slot → 2 capacity-1 seats · dp[mask] · popcount(mask) = which number you're placing."]**

> Burn these two lines in.
>
> **One: a bin of capacity `c` becomes `c` bins of capacity one — that's how a counting state turns into a bitmask.**
>
> **Two: if items are consumed in a fixed order, `popcount(mask)` already tells you which item you're on — so you never need an "index" dimension.**
>
> That second one is the transferable weapon. Any time your DP state is "a subset of used positions" and you process items in order, **check whether the item index is redundant.** Half the time it is, and your table gets a whole dimension lighter.

---

## 7. CODE IT — LIVE & CHUNKED — `5:35`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it in four small pieces. First, the seats and the table.

```python
def maximumANDSum(nums, numSlots):
    n = len(nums)
    m = 2 * numSlots                       # every slot splits into 2 seats
    dp = [0] * (1 << m)                    # dp[mask] = best score so far
```

> **[VISUAL: add chunk 2, highlight it.]** Now sweep every mask. And this is the collapse in code — one line recovers the item index.

```python
    for mask in range(1 << m):
        i = bin(mask).count("1")           # Python 3.10+: mask.bit_count()
        if i >= n:
            continue                       # every number seated — nothing left to place
```

> **[VISUAL: add chunk 3.]** For the current mask, try seating `nums[i]` in every seat that's still free, and push the result forward.

```python
        for b in range(m):
            if mask >> b & 1:
                continue                   # seat b is taken
            nxt = mask | (1 << b)
            gain = nums[i] & (b // 2 + 1)  # seat b belongs to slot b // 2 + 1
            if dp[mask] + gain > dp[nxt]:
                dp[nxt] = dp[mask] + gain
```

> **[VISUAL: add chunk 4, highlight `max(dp)` in yellow.]** And the answer. Look closely at this line — it is *not* what you'd guess.

```python
    return max(dp)
```

> Eleven lines. That's the whole Hard.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:10`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not what.
>
> `i = bin(mask).count("1")` — this is the popcount collapse doing its job. It's not a helper, it's the second dimension of the DP, recomputed for free. In Java it's `Integer.bitCount`, which is a single CPU instruction.
>
> `if i >= n: continue` — once all `n` numbers are seated, this mask has nothing to extend. Skipping is what stops us from placing number 19 that doesn't exist.
>
> `b // 2 + 1` — the seat-to-slot map. Seats 0,1 → slot 1; seats 2,3 → slot 2. Get this off by one and everything still *runs*, which is the cruelest kind of bug. Test it on paper.
>
> `for mask in range(1 << m)` in plain numeric order — is that safe? Yes, and here's the proof in one line: `nxt = mask | (1 << b)` sets a bit that wasn't set, so `nxt > mask`, **always**. Every state we write to is strictly ahead of us. By the time the loop arrives at `nxt`, every path into it has already been counted.
>
> **LEARNER:** Okay, `max(dp)` is bugging me. Isn't the answer just the full mask — every seat filled?
>
> **TEACHER:** Only when `n` is exactly `2 × numSlots`. But the constraint says `n ≤ numSlots * 2` — three numbers with two slots is legal. Then the full mask has popcount 4, and we `continue`d out of every state that would have written to it. It sits at **zero** forever. Your answer is on the popcount-`n` layer, wherever that is.
>
> **LEARNER:** But then `max(dp)` also sees half-finished states. Can't a partial score beat a complete one?
>
> **TEACHER:** Sharp — and no, and the reason matters. Every gain is a bitwise AND of non-negative numbers, so **every gain is ≥ 0**. A partial placement can always be extended — `n ≤ 2·numSlots` guarantees there's a free seat for everyone left — and extending never *lowers* the score. So no partial state can exceed the best complete one. `max(dp)` is safe precisely because the score is monotone. If any AND could be negative, this line would be a bug.

---

## 9. DRY-RUN THE CODE — `8:35`
*(worked example — prove it, close the loop)*

**[VISUAL: tiny case — `nums = [1, 2, 3]`, `numSlots = 2`. Four seats drawn: b0,b1 in slot 1; b2,b3 in slot 2. A gains cheat-sheet appears beside them.]**

> Small enough to do fully by hand. Three numbers, two slots, so four seats. Masks written `b3 b2 b1 b0`.
>
> The gains, precomputed on screen: `1&1 = 1`, `1&2 = 0` · `2&1 = 0`, `2&2 = 2` · `3&1 = 1`, `3&2 = 2`.
>
> **[VISUAL: the layer table fills in row by row, one popcount layer at a time.]**

| Layer | Placing | Masks → `dp` |
|---|---|---|
| 0 | `nums[0] = 1` | `0000` → **0** |
| 1 | `nums[1] = 2` | `0001` → 1, `0010` → 1 *(1 went to slot 1)* · `0100` → 0, `1000` → 0 *(1 went to slot 2; `1&2 = 0`)* |
| 2 | `nums[2] = 3` | `0011` → 1 *(1 and 2 both in slot 1)* · `0101`,`0110`,`1001`,`1010` → **3** *(1→slot 1, 2→slot 2)* · `1100` → 2 |
| 3 | — done | `0111` → 4, `1011` → 4 · `1101` → **5**, `1110` → **5** |
| 4 | — | `1111` → **0**, never written |

> Read the winner backwards. `1101` is seat `b0` — slot 1 — plus seats `b2` and `b3` — both slot 2. It got its 5 from mask `0101`, which held 3, plus number `3` into seat `b3` for a gain of `3 AND 2 = 2`.
>
> **[VISUAL: the physical picture — chip 1 sits in slot 1; chips 2 and 3 both sit in slot 2. Values float up: 1 + 2 + 2 = 5.]**
>
> Number 1 alone in slot 1, numbers 2 and 3 together in slot 2. `1 + 2 + 2 = 5`.
>
> And there's the full mask `1111`, sitting at **zero** — never touched, because we only ever had three numbers. `dp[full]` would have returned zero. `max(dp)` returns five. That's the loop I opened at the `return` line, closed.
>
> **[VISUAL: cut back to the six-number example; the code output prints `9`, matching the promise from beat 2.]**
>
> Run the same code on our opening example — six numbers, three slots — and it prints **9**. Exactly what we held onto at the start.

---

## 10. COMPLEXITY, OUT LOUD — `10:00`
*(transfer to interview)*

**[VISUAL: two big numbers side by side. Left, red: "12,504,636,144,000". Right, green: "4,718,592". Below: "2,650,000× fewer".]**

> Say it the way you'd say it in the room: *"There are `2^(2·numSlots)` masks, and each one tries up to `2·numSlots` free seats — so `O(2^(2·numSlots) · 2·numSlots)`. At the ceiling that's two-to-the-eighteen times eighteen: **four point seven million operations.** Space is `2^18` integers, about a megabyte."*
>
> Twelve and a half **trillion** versus four point seven **million** — a factor of two and a half million, all from noticing that the future only depends on which seats are gone. And don't just say "exponential." Say the number. `4.7 million` tells the interviewer you know it *fits*; "exponential" tells them you're guessing.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:35`
*(depth + honesty — **pause #2**)*

**[VISUAL: the `dp` array as a long bar of 262,144 cells. A "roll it?" thought bubble, then a red ✗.]**

> **TEACHER:** Honest answer first: in this bitmask form, **there's no rolling trick.** In a row DP you keep one row because row `r` only reads row `r-1`. Here `dp[mask]` reads the layer below it — but we iterate masks in *numeric* order, and that layer is scattered all over the array, not a window you can slide.
>
> There's a partial win: the transition only ever goes from layer `i` to layer `i+1`, so you *could* keep two layers. The biggest layer is `C(18,9) = 48,620`, so two layers is about 97 thousand cells versus 262 thousand — roughly two-and-a-half times less. The price is a mask-to-rank mapping that's more code than it's worth. Mention it, don't build it.
>
> But there's a **real** win hiding in something we did on purpose. Pause and look at the trace table again.
>
> **[VISUAL: highlight the four masks `0101`, `0110`, `1001`, `1010` — all showing dp = 3. A 5-second "🤔 your turn" timer.]**
>
> **TEACHER:** Four different masks. All storing the same value, 3. **Why?** What did the half-slot trick cost us?
>
> *(pause)*
>
> **[VISUAL: seats b0 and b1 swap places in an animation; the picture is unchanged.]**
>
> **TEACHER:** Because the two seats inside a slot are **interchangeable**. "Number 1 in seat 0" and "number 1 in seat 1" are the same physical situation. The bitmask is spending `2^18` states to describe only `3^9` genuinely different ones.
>
> So drop the bitmask and store the occupancy directly, base 3: digit `s` is how many numbers are in slot `s+1` — zero, one, or two.
>
> **[VISUAL: `3^9 = 19,683` next to `2^18 = 262,144`. A "13.3×" badge.]**
>
> Nineteen thousand states instead of two hundred sixty thousand. Thirteen times less memory, and about twenty times faster in practice.
>
> **In the interview: lead with the bitmask** — it's the expected answer and it's easier to get right under pressure. Then add one sentence: *"the two half-slots in a slot are symmetric, so a base-3 occupancy state would cut this to `3^numSlots`."* That sentence costs you eight seconds and reads as senior.

---

## 12. YOUR TURN (active recall) — `11:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Minimum XOR Sum of Two Arrays (LC 1879)". A blank editor.]**

> Before the next video, do **Minimum XOR Sum of Two Arrays**, LeetCode 1879. Pair every element of `nums1` with a distinct element of `nums2` to *minimize* the XOR sum.
>
> It's the same weapon with the training wheels on: capacity is one, so you skip the half-slot split and go straight to `dp[mask]` with `popcount(mask)` as your index. One trap to enjoy — you're minimizing now, so initialise to infinity, not zero. If it clicks, follow it with **Beautiful Arrangement**, LC 526: same collapse, but you're *counting* arrangements instead of maximizing.
>
> Wrestle for ten minutes before you peek. The struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `12:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **`n ≤ 18` is a pattern announcement**, not a courtesy. Subsets. Bitmask. Every time.
> 2. **A capacity-2 slot is two capacity-1 seats** — that's how you turn a counting state into a bit-set.
> 3. **`popcount(mask)` already knows which item you're on** — so the "index" dimension deletes itself.
>
> And the memory peg — one line that recalls the whole pattern:
>
> **[VISUAL: big box → "split the seats, count the bits, lose a dimension."]**
>
> *Split the seats, count the bits, lose a dimension.* When you next see "assign these `n` things to those positions" with `n` under twenty, that's the sentence your hand should reach for.
>
> *(GCA reminder — for the interview itself: read the constraint out loud, state the backtracking baseline with its real number, then narrate **why** the state is a subset before you write any code. Google's General Cognitive Ability signal isn't the eleven lines. It's you saying "the future only depends on which seats are gone, so this is a DP" — out loud, before you type.)*

---

## 14. CLIFFHANGER — `12:40`
*(open loop to next lesson)*

**[VISUAL: the DP table fades out. A dark grid appears with a small robot icon on it — and most of the grid is covered in fog. Blurred title: "Robot Room Cleaner". Section 10 badge.]**

> That's the Dynamic Programming section closed. And notice what made every one of those problems possible: **you could see the whole input.** The grid, the array, the slots — all right there, all countable.
>
> Next section, we take that away. You're a robot in a room. You cannot see the room. You don't know how big it is, you don't know where the walls are, and there's no array to loop over — just three commands: `move`, `turnLeft`, `clean`. Your job is to clean **every** reachable cell and never get stuck.
>
> No state to enumerate. No table to fill. Just you, a hidden world, and the question that breaks most candidates: *how do you back out of a dead end when you can't remember where you came from?*
>
> That's **Robot Room Cleaner** — the start of Backtracking & Interactive. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int maximumANDSum(int[] nums, int numSlots) {
    int n = nums.length;
    int m = 2 * numSlots;                       // every slot splits into 2 capacity-1 seats
    int[] dp = new int[1 << m];                 // dp[mask] = best score for first bitCount(mask) numbers

    int best = 0;
    for (int mask = 0; mask < (1 << m); mask++) {
        int i = Integer.bitCount(mask);         // the popcount collapse — free on modern CPUs
        best = Math.max(best, dp[mask]);        // running max: n may be < m, so the full mask can be unreachable
        if (i >= n) continue;                   // all numbers seated

        for (int b = 0; b < m; b++) {
            if ((mask & (1 << b)) != 0) continue;       // seat taken
            int next = mask | (1 << b);                 // strictly greater than mask — order is safe
            int gain = nums[i] & (b / 2 + 1);           // seat b lives in slot b/2 + 1
            dp[next] = Math.max(dp[next], dp[mask] + gain);
        }
    }
    return best;
}
```

*(Verified: `[1,2,3,4,5,6], 3` → `9`; `[1,3,10,4,7,1], 9` → `24`; worst case `n = 18, numSlots = 9` runs in ~23 ms.)*
