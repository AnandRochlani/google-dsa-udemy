# 🎬 Recording Script — Sort Integers by The Power Value

**Pattern: Memoization on a recursive sequence (top-down DP) + custom sort · LeetCode 1387 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** "Maximum Number of Points with Cost" taught DP as *speed*. This one teaches DP as *memory* — the other half of the same coin.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an interview screen. Ten lines of Python appear, clean. Green checkmark: "Accepted · 112 ms". The candidate smiles. Then the interviewer's voice-over caption slides in: "Nice. Now make it fast." The smile drops. Cut to a single red line under the code: `memo = [0] * (hi + 1)` with a blinking cursor.]**

> Here's a problem you will solve in about thirty seconds. Seriously — the statement literally hands you the algorithm. You'll write ten lines, hit submit, and get Accepted.
>
> And that is exactly the trap.
>
> Because the interviewer isn't asking *can you transcribe a spec*. They're asking: **do you see the work you just wasted?** And there's a second trap sitting underneath — a one-line "optimization" that looks obviously right, compiles fine, and crashes on a number you'd never think to test.
>
> By the end of this video you'll own both: the cache that kills the waste, and the exact reason that cache **cannot** be an array. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one boxed sentence up top. Below it, the rule as two arrows: `even → x/2` in blue, `odd → 3x+1` in orange.]**

> One line: **every integer has a "power value" — the number of steps it takes to reach 1 — and we sort a range by that, then return the k-th one.**
>
> The step rule is two cases. Even? Halve it. Odd? Triple it and add one. Repeat until you hit 1. Count the steps. That count is the power value.
>
> **[VISUAL: `12 → 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1` animating left to right, a step counter ticking 1…2…3…up to 9. The `3 → 10` hop is drawn as a jump UP and flashes orange.]**
>
> Let's do 12 by hand. 12 is even — halve it, 6. Even again — 3. Now 3 is **odd**, so three times three plus one — that's **10**. Watch that: the number went *up*. That's not a bug, that's the rule, and hold onto it because it's going to bite us in about four minutes.
>
> Ten is even — 5. Odd — 16. Then 8, 4, 2, 1. Count the arrows: **nine steps. Power of 12 is 9.**
>
> **[VISUAL: the ask — `lo = 12, hi = 15, k = 2` → `?` with a question mark.]**
>
> So: given `lo`, `hi`, and `k`, take every integer from `lo` to `hi`, sort them by power ascending, break ties by the value itself ascending, and hand back the k-th one. **One-indexed** — k equals 2 means the second one, not the third.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:35`
*(worked example — let them feel the waste)*

**[VISUAL: four chains stacked vertically for 12, 13, 14, 15, drawing one at a time, left to right. A "steps walked" counter in the corner climbs.]**

> Let's do what your brain does first: walk all four chains from scratch.
>
> Twelve — we just did it. Nine steps. Counter says 9. Thirteen: odd, so 40, then 20, 10, 5, 16, 8, 4, 2, 1 — nine steps, counter's at 18.
>
> Fourteen: 14, 7, 22, 11, 34, 17, 52, 26, 13, 40, and then the rest — **seventeen** steps. Counter's at 35. Fifteen: 15, 46, 23, 70, 35, 106, 53, 160, 80, 40, and down — also **seventeen**. Counter: **52 steps walked.**
>
> **[VISUAL: chains 12 and 13 slide together and align. Their shared tail `10 → 5 → 16 → 8 → 4 → 2 → 1` lights up bright red in BOTH rows simultaneously.]**
>
> Now look at what we actually did. Twelve's chain ends: ten, five, sixteen, eight, four, two, one. Thirteen's chain ends: ten, five, sixteen, eight, four, two, one.
>
> **Identical.** We walked that exact tail twice. And it's worse — fourteen's chain runs straight into **thirteen** after eight steps, so we re-walked all nine of thirteen's steps too. Fifteen crashes into **forty**, which thirteen already visited.
>
> Fifty-two steps walked. Only **twenty-nine distinct numbers** ever visited. We're doing nearly double the work on four numbers. Scale it to the full range — one to a thousand — and it's **fifty-nine thousand steps** for **two thousand two hundred** distinct values. Twenty-seven times the necessary work.

---

## 4. THE PAIN POINT + PREDICT — `3:00`
*(close loop #1 + generation effect — pause #1)*

**[VISUAL: freeze on the two overlapping chains. The value `10` pulses in both, with a label: "we computed power(10) twice." A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Name the waste precisely, because vague is useless in an interview. It's this: **`power(10)` is 6. It is always 6. It does not care which chain walked into it.** Twelve arrived at ten, we computed six. Thirteen arrived at ten, we computed six *again*, from scratch.
>
> **LEARNER:** So the answer for a number doesn't depend on how you got there. That's… that's the definition of a subproblem, isn't it?
>
> **TEACHER:** That's exactly it, and you just said the magic words. Pause the video right here. If `power(x)` depends only on `x` — and chains keep landing on each other — **what's the one line of code that kills all of that repeated work?** And more interesting: *where do you store it?* Think about it before I show you.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:45`
*(elaboration + analogy — derive it)*

**[VISUAL: the recurrence appears one piece at a time: `power(1) = 0` then `power(x) = 1 + power(next(x))`. Then a dict panel opens on the right, empty except `{1: 0}`.]**

> **TEACHER:** Write the rule as a recurrence and it's already a DP. `power(1)` is **zero** — you're already at 1, zero steps needed. And for anything else: `power(x)` equals **one step, plus the power of wherever that step lands you.** That's it. That's the whole recursion.
>
> A recurrence, plus subproblems that keep showing up — that's a dynamic program. And when the subproblems are scattered like this instead of laid out in a neat grid, the natural shape is **top-down**: recurse, and cache what you compute.
>
> Here's the analogy I want stuck in your head. Think of a **river delta**. Every number is a stream starting somewhere different — but they all merge on the way to the sea. Once you've mapped the main channel from ten down to one, every stream that joins at ten gets the rest of the trip **for free**. You don't re-survey the river.
>
> **[VISUAL: re-run the four chains, but now with the dict panel filling live. Chain 12 fills 9 entries. Chain 13 walks 13 → 40 → 20, then SLAMS into `10` — a big "CACHE HIT: 6" badge — and stops dead. It never touches 5, 16, 8, 4, 2, 1.]**
>
> Watch thirteen with the cache on. Thirteen, forty, twenty… and then **ten**. Ten's already in the cache — it's 6. So thirteen is three steps plus six equals **nine**. Done. It never walked the tail. Fourteen? Eight steps and it hits thirteen. Fifteen? Nine steps and it hits forty. Every collision is free work we didn't do.
>
> **LEARNER:** Hang on. If everything eventually funnels into the same tail, doesn't the cache basically pay for itself on the *second* number?
>
> **TEACHER:** It does. That's why this problem is such a clean teaching case — there's no threshold where memoization "starts being worth it." It's winning by number two.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "power(x) = 1 + power(next(x)) · cache EVERY value the chain touches — not just the ones in [lo, hi]."]**

> The key move, one sentence: **when a value is defined recursively in terms of exactly one other value, memoize the function — and cache every value the recursion *touches*, not just the ones you were asked about.**
>
> That second half is doing a lot of work. Say it again: the states are **not** `lo` to `hi`. The states are *everything the chains can reach*. Those are different sets, and confusing them is how this problem gets people.

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. The base-case line types in first, alone.]**

> Three chunks. Chunk one — the cache, pre-seeded with the base case.

```python
def getKth(lo, hi, k):
    memo = {1: 0}                       # base case: power(1) = 0
```

> A **dict**, not a list. Circle that in your notes; I'll tell you why in ninety seconds.
>
> **[VISUAL: the power function types in, four lines, each highlighted as it lands.]** Chunk two — the recurrence, verbatim from what we derived.

```python
    def power(x):
        if x in memo:                   # already solved — read it off the shelf
            return memo[x]
        nxt = x // 2 if x % 2 == 0 else 3 * x + 1
        memo[x] = 1 + power(nxt)        # one step + the rest
        return memo[x]
```

> Line one is the whole optimization: *have I seen this? then stop.* Line two is the step rule — even, halve; odd, triple-plus-one. Line three is the recurrence, and notice it **writes to the cache on the way back up**, so every value on the chain gets recorded, not just the one we asked for.
>
> **[VISUAL: the final line lands. The sort key tuple `(power(x), x)` gets a bracket underneath: "primary · tiebreak".]** Chunk three — sort and index.

```python
    return sorted(range(lo, hi + 1), key=lambda x: (power(x), x))[k - 1]
```

> The key is a **tuple**: power first, then the value itself. Python compares tuples left to right, so it sorts by power, and any tie falls through to value ascending — which is precisely the spec, for free. Then `k - 1`, because `k` is one-indexed and Python isn't.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — the misconception, confronted)*

**[VISUAL: split screen. Left: `memo = {1: 0}` in green. Right: `memo = [0] * (hi + 1)` in red with a "looks smarter?" thought bubble. A 5-second "🤔 pause and predict" timer over the red side.]**

> Now the line I told you to circle. Why a dict? A dict has hashing overhead. An array is faster. And we only care about `lo` to `hi`, so an array of size `hi + 1` should be strictly better, right?
>
> **LEARNER:** That's genuinely what I'd have written. `hi` is at most a thousand — allocate a thousand-and-one slots, index directly, done. What breaks?
>
> **TEACHER:** Good — say the wrong answer out loud, that's how it stops being yours. **Second pause here, and this one's the money question:** look back at the chain for 15 on screen and tell me what value that array is about to be indexed with. Predict before I show you.
>
> *(pause)*
>
> Here's what breaks.
>
> **[VISUAL: the chain for 15 replays: `15 → 46 → 23 → 70 → 35 → 106 → 53 → 160 → 80 → 40 → …`. When it hits 160, a red line labeled "hi = 15" is drawn far below it. The 160 sits way above the line, flashing.]**
>
> Remember the odd rule — `3x + 1` — the one I told you to hold onto? It makes numbers go **up**. Our range was 12 to 15. Fifteen's chain climbs to **160**. That's more than ten times `hi`.
>
> And that's the gentle case. In the real constraint range — `lo` and `hi` up to a thousand — the number **703** climbs all the way to **two hundred and fifty thousand, five hundred and four** before it comes back down.
>
> **[VISUAL: `memo[250504]` typed against a 1001-slot array → red `IndexError: list assignment index out of range`. Beneath: "Java: ArrayIndexOutOfBoundsException".]**
>
> So `memo = [0] * (hi + 1)` doesn't merely waste space. It **crashes**. In Java it compiles clean and throws at runtime on an input you'd never hand-pick.
>
> Here's the sentence that fixes it permanently: **the cache is keyed by reachable values, not by input values.** Those are two different sets. Dict, HashMap, or an array sized to a bound you can actually *defend* out loud. There's no third option, and if you catch this unprompted in an interview, the interviewer notices.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close the loop)*

**[VISUAL: trace table filling row by row; the dict panel grows alongside; cache hits flash gold.]**

> Run it on `lo = 12, hi = 15, k = 2` — the same four numbers, now with the cache watching.

| x | walks until… | cache hit | power | new entries |
|---|---|---|---|---|
| 12 | 12→6→3→10→5→16→8→4→2 | `1` = 0 | **9** | 9 |
| 13 | 13→40→20 | **`10` = 6** | 3 + 6 = **9** | 3 |
| 14 | 14→7→22→11→34→17→52→26 | **`13` = 9** | 8 + 9 = **17** | 8 |
| 15 | 15→46→23→70→35→106→53→160→80 | **`40` = 8** | 9 + 8 = **17** | 9 |

> Twelve pays full price — nine new entries. Thirteen walks **three** steps and hits ten. Fourteen walks eight and hits thirteen. Fifteen walks nine and hits forty. Twenty-nine cached values, versus fifty-two steps brute-forced.
>
> **[VISUAL: the four pairs sort into order — `(9,12) (9,13) (17,14) (17,15)` — then the value row `[12, 13, 14, 15]` with position 2 boxed.]**
>
> Now sort by the tuple. Twelve and thirteen both have power nine — **tie**, so the tiebreak fires and twelve goes first because twelve is smaller. Then fourteen and fifteen, both seventeen, same tiebreak. Final order: twelve, thirteen, fourteen, fifteen. `k = 2` means index one — **thirteen**. ✅
>
> And the tiny edge case people fumble: `lo = 1, hi = 1, k = 1`. The range is just `[1]`. `power(1)` is zero, straight from the base case — no chain at all. Index zero. Answer: **1**. ✅ If your `power` starts by taking a step instead of checking the base case, that one returns garbage.

---

## 10. COMPLEXITY, OUT LOUD — `9:05`
*(transfer to interview)*

**[VISUAL: table — Brute: 59,542 chain steps. Memoized: 2,228 distinct values. A 27× badge.]**

> Say it the way you'd say it in the room: *"Brute force is n times the average chain length — chains here run up to a hundred and seventy-eight steps. With memoization it's **D**, the number of distinct values the recursion ever touches, because each one is computed exactly once and read forever after. Plus O(n log n) for the sort. Space is O(D) — the cache."*
>
> Put numbers on it, because numbers land: across one to a thousand, brute force walks **59,542** steps. The memoized version touches **2,228** distinct values. Twenty-seven to one.
>
> **[VISUAL: a small aside card: "heapq.nsmallest(k, …) → O(n log k)".]** One more thing to have in your pocket. If the interviewer says *"do you really need to sort the whole range?"* — no. You need the k-th smallest, so a size-k heap gives you O(n log k) instead of O(n log n). With n at a thousand it doesn't matter; **knowing it exists** is what they're actually checking.
>
> And I'd write `power` iteratively — push the chain onto an explicit stack, then unwind it filling the cache backwards. Same complexity, but chain depth can never blow your call stack. Saying *why* you did that is free signal.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:50`
*(depth + honesty)*

**[VISUAL: the dict panel, with a "shrink me?" bubble → then a scale icon: "TIME ⟷ MEMORY", cache on one pan, 27× on the other.]**

> Now the beat that's backwards from every other lesson in this section. Usually I ask "can we use less memory?" Here the honest answer is: **the memory *is* the optimization.** We didn't accidentally allocate a cache — we spent memory, on purpose, to buy time. That's what top-down DP *is*.
>
> Can you drop back to O(1) auxiliary space? **Yes — and it's the brute force.** Delete the dict, recompute every chain, hold nothing but two variables. At `hi ≤ 1000` it still passes. At `hi` of a million it doesn't.
>
> Say the trade out loud instead of pretending one side wins: *"Space is O(D) for the cache, and that's deliberate — without it I'd repeat about twenty-seven times the chain work. If memory were the binding constraint I'd drop the cache and eat the recomputation, but here time is the scarce resource, so I pay in memory."* Naming a trade-off *as* a trade-off — rather than dressing your choice up as strictly optimal — is a seniority signal. Interviewers hear the difference immediately.

---

## 12. YOUR TURN (active recall) — `10:20`
*(retrieval practice)*

**[VISUAL: "Your turn → Integer Replacement (LC 397)". A blank editor. Below: `n even → n/2 · n odd → n+1 OR n−1`.]**

> Before the next video, go do **Integer Replacement**, LeetCode 397. Almost the same machinery: even, halve it; odd — but now you get to **choose**, plus one or minus one — and you want the *minimum* number of steps to reach 1.
>
> Same recurrence shape, same "memoize the function, not the range" instinct, same overshoot trap. The new muscle is a `min` over two branches instead of one forced path.
>
> Ten minutes, no peeking. Write it top-down with a dict — and before you size any cache, ask *what values can this thing actually reach?*

---

## 13. LOCK IT IN — `10:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line: "chains merge like rivers — survey the delta once."]**

> Three takeaways:
> 1. **`power(x) = 1 + power(next(x))`, `power(1) = 0`** — a recurrence plus overlapping subproblems means top-down DP, every time.
> 2. **Cache reachable values, not input values.** `3x + 1` overshoots — 15 climbs to 160, 703 climbs to 250,504. Dict, not an array sized to `hi`. This is the bug most candidates ship.
> 3. **The tuple key `(power(x), x)` is the whole sort** — primary key, then tiebreak, and `k − 1` because `k` is one-indexed.
>
> The memory peg: **chains merge like rivers — survey the delta once.**
>
> *(GCA reminder — for the interview itself: this problem is over in thirty seconds, so the *code* isn't the signal. The signal is you saying "the brute force works, but chains 12 and 13 share a tail — I'm recomputing `power(10)` for every chain that passes through it," and then flagging the overshoot **before** you get bitten. And ask the one clarifying question that proves you read the spec: "ties break by value ascending, and k is one-indexed — right?" Both are stated, both are easy to invert, and asking costs five seconds.)*

---

## 14. CLIFFHANGER — `11:20`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Maximum AND Sum of Array". Numbers dropping into numbered slots, and above them a binary string `1011010…` ticking up. Caption fades in: "the cache key is the hard part."]**

> Today the cache key was easy: it was just `x`. One integer in, one answer out — you barely had to think about what a "state" was.
>
> Next lesson, that breaks. You'll be assigning numbers into slots, and the thing you need to remember isn't a number — it's **which slots you've already filled**. A whole *set*, as your dictionary key. That's bitmask DP, and it's where people who are comfortable with memoization suddenly freeze, because the recurrence is easy and the **state design** is brutal.
>
> That's Maximum AND Sum of Array. Bring the dict. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class Solution {
    // Chain values are NOT bounded by hi: 15 reaches 160, 703 reaches 250,504.
    // A fixed array sized to hi would go out of bounds — the cache must be a map.
    private final Map<Integer, Integer> memo = new HashMap<>();

    private int power(int x) {
        if (x == 1) return 0;                        // base case
        Integer cached = memo.get(x);
        if (cached != null) return cached;           // already solved
        int next = (x % 2 == 0) ? x / 2 : 3 * x + 1;
        int steps = 1 + power(next);                 // power(x) = 1 + power(next(x))
        memo.put(x, steps);
        return steps;
    }

    public int getKth(int lo, int hi, int k) {
        Integer[] nums = new Integer[hi - lo + 1];   // Integer[], so sort takes a comparator
        for (int i = 0; i < nums.length; i++) nums[i] = lo + i;

        Arrays.sort(nums, (a, b) -> {
            int pa = power(a), pb = power(b);
            return pa != pb ? Integer.compare(pa, pb)    // power ascending
                            : Integer.compare(a, b);     // tie → value ascending
        });

        return nums[k - 1];                              // k is 1-indexed
    }
}
```

*(Java's comparator calls `power` repeatedly during the sort — unlike Python's `key=`, which calls it once per element. That's fine precisely **because** it's memoized: every call after the first is a hash lookup. Point that out unprompted and you've shown you understand what the cache is actually buying you.)*

---

## Appendix — the iterative (no-recursion) `power`, for the "what if the range were huge?" follow-up

```python
def getKth(lo, hi, k):
    memo = {1: 0}

    def power(x):
        stack = []
        while x not in memo:             # climb until we land on something known
            stack.append(x)
            x = x // 2 if x % 2 == 0 else 3 * x + 1
        steps = memo[x]                  # the known anchor
        while stack:                     # unwind: each value is one step further out
            steps += 1
            memo[stack.pop()] = steps
        return steps

    return sorted(range(lo, hi + 1), key=lambda x: (power(x), x))[k - 1]
```

*(Chains top out at 178 steps for `hi ≤ 1000`, which fits under Python's default recursion limit of 1000 — but "fits" isn't "safe." This version has no stack risk at all, and it fills the cache in exactly the same order the recursion would.)*
