# 🎬 Recording Script — Minimum Cost to Set Cooking Time

**Pattern: Simulation / exhaustive enumeration over a tiny domain · LeetCode 2162 · Medium · Target length ~11–12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the whole Design section so far — Snapshot Array, Detect Squares, Stock Price Fluctuation — where the win came from *inventing a structure*. Today there is no structure to invent, and that's the lesson.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a microwave keypad, digits 0–9. A finger rests on `1`. Display reads `10:00`. Then the display flickers and shows `09:60` — same duration, different keys. A "which one is cheaper?" caption pulses between them.]**

> Ten minutes on a microwave. You type one-zero-zero-zero. Done, right?
>
> Except the machine will also accept **zero-nine-six-zero** — nine minutes and *sixty* seconds. Same six hundred seconds. Different keys. Different cost.
>
> This is a problem where people lose twenty minutes hunting for a formula that doesn't exist — and where the *correct* answer is the thing you've been trained to feel guilty about: **brute force.** But brute force done with discipline, over a domain so small it's almost funny.
>
> By the end of this video you'll know exactly how many ways there are to type any target time. The number will surprise you. It's **two.** Let's earn that.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below it, the keypad with the finger on `1`, and two cost cards: "move to a different digit = moveCost", "push the digit under your finger = pushCost".]**

> One line: **your finger starts on some digit, moving it to a different digit costs `moveCost`, pushing costs `pushCost` — type at most four digits so the display reads a time equal to `targetSeconds`, as cheaply as possible.**
>
> The display is `MMSS`. First two digits are minutes, last two are seconds. Type fewer than four digits and the machine **prepends zeros for you** — punch `9 5 4` and it shows `09:54`, nine minutes fifty-four. You don't pay for the zeros it adds. You only pay for keys you actually press.
>
> Here's our whole example:

```
startAt = 1        (finger already on the 1 key)
moveCost = 2       (each time the finger travels)
pushCost = 1       (each key press)
targetSeconds = 600
```

**[VISUAL: the two candidate displays side by side — `10:00` typed as `1 0 0 0`, and `09:60` typed as `9 6 0`.]**

> Six hundred seconds. Ten minutes. Two ways to say it. Which one costs less — and how would you *know* you found them all? That's the whole problem.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — let them feel where it breaks)*

**[VISUAL: a big `targetSeconds ÷ 60` division appearing, feeding `mm` and `ss` boxes, which feed a 4-cell display.]**

> Do what your brain does first. Minutes is `600 // 60` — that's 10. Seconds is `600 % 60` — that's 0. Display `1000`. Type it.
>
> Cost it by hand, finger starting on `1`:

**[VISUAL: the finger animates over the keypad; a running total ticks up beside each key.]**

> Digit `1` — finger's already there. No move. Push: **+1**, total 1.
> Digit `0` — different key. Move: **+2**. Push: **+1**. Total 4.
> Digit `0` — same key, no move. Push: **+1**. Total 5.
> Digit `0` — same again. Push: **+1**. Total **6**.
>
> Six. And that happens to be the right answer here. Which is exactly why this instinct is dangerous — it *passes the sample*.
>
> **[VISUAL: target flips to `6000`. The division runs: mm = 100. The two-digit minutes box overflows in red — "100 doesn't fit".]**
>
> Now feed it `targetSeconds = 6000`. `6000 // 60` is **100** minutes. The display has *two* digits for minutes. There is no `100`. Your formula just produced a time the microwave cannot show — and the answer isn't "impossible," because six thousand seconds is perfectly typeable. You just can't get there by dividing.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — pause #1)*

**[VISUAL: three red "trap" cards stack up: 1) "seconds stop at 59?" 2) "leading zeros — typed or free?" 3) "the finger remembers where it is". A 5-second "🤔 your turn" timer.]**

> **TEACHER:** Name the pain honestly. There's nothing *algorithmically* hard here — the hard part is that the problem is a pile of representational traps. Seconds might not stop at 59. Leading zeros might not be typed. And the finger has memory, so repeating a digit is free while alternating is expensive.
>
> **LEARNER:** Then can't I just be exhaustive? Loop `mm` from 0 to 99, `ss` from 0 to 99, keep the pairs where `mm*60 + ss` equals the target, cost each one. Ten thousand checks — that's nothing.
>
> **TEACHER:** You're right, and that instinct is genuinely good — it's the version that's hardest to get wrong, and I'd rather you write that than a wrong formula. But before we do: pause the video and answer one question. **For a fixed target, how many of those ten thousand pairs can actually survive?** Not "how many do we check" — how many can *possibly* hit the target. Guess a number.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:25`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a horizontal number line of `ss` values with a green window marked 0–99. As `mm` steps 8 → 9 → 10 → 11, a marker jumps in strides of 60. Only two strides land inside the green window.]**

> **TEACHER:** Let's derive it. Fix the minutes at `mm`. Then the seconds field isn't a choice — it's forced: `ss = targetSeconds − 60*mm`. One `mm`, one `ss`. Done.
>
> Now bump `mm` up by one. `ss` drops by exactly **60**. Bump again, drop 60 again. So as `mm` walks, `ss` marches in strides of sixty.
>
> And the legal window for `ss` is `0` to `99` — that window is **one hundred wide**. Your stride is sixty. Two consecutive strides span 120, which is *wider than the window*. So **at most two** values of `mm` can ever land `ss` inside it. Not ten thousand. Two.
>
> **[VISUAL: analogy card — a car odometer where the tenths wheel only shows 0–99 but ticks in jumps of 60. Caption: "stride 60 into a window of 100 → at most two landings."]**
>
> For target 600: `mm = 10` gives `ss = 0`. `mm = 9` gives `ss = 60`. `mm = 11` gives `ss = −60` — negative, dead. `mm = 8` gives `ss = 120` — over 99, dead. **Two survivors, and they're always the two neighbours:** `(t//60, t%60)` and `(t//60 − 1, t%60 + 60)`.
>
> **LEARNER:** Hold on — `ss = 60`? Sixty seconds isn't a time. That's one minute. Surely the machine rejects `09:60`.
>
> **TEACHER:** That's the misconception this problem is built to punish, so let's kill it. The display holds **two digits** for seconds — anything from `00` to `99`. It does not enforce clock semantics. `09:60` means nine minutes plus sixty seconds, which is six hundred seconds, which is exactly what you asked for. It's legal.
>
> And it's not a curiosity — remember `targetSeconds = 6000`? `mm = 100` is dead, so the *only* surviving candidate is `mm = 99`, `ss = 60`. Display `99:60`. If you believe seconds stop at 59, every target from 6000 to 6039 fails outright, and you'll silently overpay on a pile of others.

---

## 6. THE KEY MOVE (signaling) — `4:55`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Only TWO encodings can exist: (t//60, t%60) and (t//60 − 1, t%60 + 60). Validate both. Simulate the typing cost of both. Take the min."]**

> Burn this in: **there are only two candidate encodings — so stop deriving and just try both.**
>
> No greedy rule. No formula for "which is cheaper." You *simulate* the finger for each candidate, honestly, key by key, and return the smaller number.
>
> And the transferable lesson is bigger than microwaves: **when the constraints cap the search space at a handful, the entire difficulty moves into the costing function.** Spend your effort on edge cases, not on shaving an asymptotic that's already constant. That's a senior instinct, and interviewers notice it.

---

## 7. CODE IT — LIVE & CHUNKED — `5:25`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Build the costing function first — it's the whole problem. Step one: is this candidate even real?

```python
def minCostSetTime(startAt, moveCost, pushCost, targetSeconds):
    def cost(mm, ss):
        # a candidate is only real if both fields fit on the 2-digit display
        if not (0 <= mm <= 99 and 0 <= ss <= 99):
            return float('inf')
```

> Infinity, not an exception. An illegal candidate should just *lose* the `min` — no branching at the call site.
>
> **[VISUAL: add chunk 2, highlight the `str(...)` expression.]** Step two: turn the candidate into the digits a human actually presses.

```python
        total, cur = 0, startAt
        # mm*100 + ss is the 4-digit display; str() strips leading zeros,
        # which is exactly what an optimal typist does
        for d in map(int, str(mm * 100 + ss)):
```

> `mm * 100 + ss` packs the display into one integer — `(10, 0)` becomes `1000`, `(9, 60)` becomes `960`. And `str()` of `960` is three characters, not four. The leading zero **strips itself for free**, which is precisely the behaviour we want.
>
> **[VISUAL: add chunk 3 — the two-line body, with the keypad animating beside it.]** Step three: the simulation. This is the spec, verbatim.

```python
            if d != cur:            # move the finger only when the digit changes
                total += moveCost
                cur = d
            total += pushCost       # push every digit we actually type
        return total
```

> **[VISUAL: add chunk 4 — two lines, spotlight.]** And the driver — name the two candidates, take the cheaper.

```python
    mm, ss = divmod(targetSeconds, 60)
    return min(cost(mm, ss), cost(mm - 1, ss + 60))
```

> That's the entire solution. Two calls. No loop over ten thousand anything.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each region as it's named.]**

> Now why every line earns its place.
>
> The guard `0 <= mm <= 99 and 0 <= ss <= 99` is doing **three** different jobs. It kills `mm = 100` when the target is 6000 or more. It kills `ss = 119` when the second candidate overshoots — `t % 60` of 59 plus 60 is 119, off the display. And it kills `mm = −1` when the target is under sixty seconds and the "borrow a minute" candidate goes negative. Three edge cases, one line.
>
> `cur = startAt` — the finger's memory. Forget to update `cur` inside the `if` and every digit after the first looks like a move; you'll pay `moveCost` for `1 0 0 0` three times instead of once. That's the number-one silent wrong answer on this problem.
>
> And notice the order inside the loop: **move first, then push.** You can't push a key your finger isn't on.
>
> **LEARNER:** The `str()` trick bothers me. You're *assuming* stripping leading zeros is always optimal. Couldn't a leading zero ever be a bargain — like if my finger already sits on `0`, pressing it costs no move, and maybe that sets up a cheaper path?
>
> **TEACHER:** Best question in the lesson, and it deserves a real proof, not a shrug. Compare the two typings of the same display. The stripped version starts at `startAt` and travels straight to the first significant digit. The padded version travels `startAt → 0`, then `0 → first significant digit`. Two things follow. One: the padded version's move count is **never lower** — it still has to arrive at that same first digit, it just may take an extra hop to get there. Two: it pays at least one extra `pushCost` for the zero, and `pushCost` is at least 1 by the constraints. So padded costs strictly more, always. Zero setup value — moving to `0` doesn't make the next hop cheaper, because every hop costs the same flat `moveCost` regardless of distance.
>
> **LEARNER:** So `min(cost(a), cost(b))` with `inf` for invalid — what if *both* are invalid?
>
> **TEACHER:** Can't happen, and it's worth being able to say why. Take `mm = t // 60` and `ss = t % 60`. `ss` is in 0–59 by construction, always legal. And `mm` only breaks the display when `t ≥ 6000` — but the constraints cap `targetSeconds` at 6039, and for that entire 6000–6039 band the *other* candidate, `mm = 99` with `ss` between 60 and 99, is legal. At least one always survives. You never return infinity.

---

## 9. DRY-RUN THE CODE — `8:25`
*(worked example — prove it, close the loop)*

**[VISUAL: `divmod(600, 60) = (10, 0)` on screen, branching into two candidate cards. A 4-second "🤔 predict" timer before the table fills.]**

> Run the real code on our example — `startAt = 1`, `moveCost = 2`, `pushCost = 1`, `target = 600`.
>
> `divmod(600, 60)` gives `(10, 0)`. So candidate one is `(10, 0)` → display `1000`. Candidate two is `(9, 60)` → display `0960`, typed as `960`.
>
> **Second pause — predict before I trace it.** Candidate two types *three* keys instead of four. Fewer pushes. Does it win? Say your answer out loud.
>
> *(pause)*

**[VISUAL: the trace table fills row by row; the keypad animates the finger for each row.]**

| Candidate | Display | Typed digits | Simulation (finger starts at 1) | Cost |
|---|---|---|---|---|
| `(10, 0)` | `1000` | `1 0 0 0` | push 1 (+1) · move→0 (+2) push (+1) · push (+1) · push (+1) | **6** |
| `(9, 60)` | `0960` | `9 6 0` | move→9 (+2) push (+1) · move→6 (+2) push (+1) · move→0 (+2) push (+1) | 9 |

> `min(6, 9)` = **6**. ✅
>
> And look *why* the shorter one lost: three digits, but three different digits — three moves at 2 apiece. The four-digit version starts on the key the finger is already touching, and then repeats `0` three times for free. **Fewer keys is not cheaper. Fewer *changes* is cheaper.** That's the intuition the cold open was hiding.
>
> **[VISUAL: two quick edge-case cards flip in.]**
>
> Two more, fast. `targetSeconds = 6000`: candidate one is `(100, 0)` — guard rejects it, infinity. Candidate two is `(99, 60)` → display `9960` → move to 9 (+2) push (+1), push 9 again (+1), move to 6 (+2) push (+1), move to 0 (+2) push (+1) = **10**. The "impossible" case, answered by the encoding people forget exists.
>
> And `targetSeconds = 8`: candidate one is `(0, 8)` → `0*100 + 8` is `8` → the string is one character. Move to 8 (+2), push (+1) = **3**. Candidate two is `(−1, 68)` — negative minutes, rejected. One key press, correctly costed, because we never typed the zeros the machine adds for us.

---

## 10. COMPLEXITY, OUT LOUD — `9:30`
*(transfer to interview)*

**[VISUAL: two rows — Brute: scan all 100×100 displays, 10⁴ checks, O(1) space. Ours: 2 candidates × ≤4 digits, O(1) time, O(1) space.]**

> Say it the way you'd say it in the room: *"The full grid scan is ten thousand checks — constant, but blind, and nine thousand nine hundred ninety-eight of them are guaranteed misses. Naming the two candidates directly is **O(1) time** — two candidates, at most four digits each — and **O(1) space**. The display bounds the entire world."*
>
> Here's your **GCA moment.** Google scores General Cognitive Ability, and on a problem with no algorithm, the *only* thing left to score is how you explore the spec. So say the two clarifying questions out loud before you write a line: **"Seconds from 60 to 99 are legal on the display, correct?"** and **"Leading zeros are prepended by the machine, not typed — so I don't pay for them?"**
>
> Those aren't polite noise. They are literally the two hidden test cases. Asking them *is* the signal.

---

## 11. CAN WE USE LESS MEMORY? — `10:00`
*(depth + honesty)*

**[VISUAL: the state of the algorithm shown as three tiny boxes — `total`, `cur`, and a ≤4-char string. A "shrink further?" bubble gets a measured ✗.]**

> Can we use less memory? **No — and naming *why* is the strong move.**
>
> Look at the state: a running `total`, a finger position `cur`, and a digit string that is at most four characters. That's it. Nothing scales with the input, because the input *is* four integers. There's no array to shrink, no rolling window to apply, no second pass to fuse.

```python
# No space-optimised variant exists: state is (total, cur) plus a <=4-char
# digit string per candidate — already O(1) time and O(1) space.
```

> Out loud: *"Both time and space are constant — the two-digit display caps the world at two candidates of four digits each, so there's nothing to optimise."* Hunting for a space trick here would tell the interviewer you haven't noticed the domain is finite. **Recognising when there's no optimisation left is itself a skill.**

---

## 12. YOUR TURN (active recall) — `10:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Minimum Number of Pushes to Type Word II (LC 3016)". A blank editor.]**

> Before the next video, go do **Minimum Number of Pushes to Type Word Two** — LeetCode 3016. Same species: a keypad, a cost model, a tiny bounded domain, and the whole difficulty living inside "count the cost correctly," not "find the clever algorithm."
>
> And if you want the pure edge-case workout, do **String to Integer — atoi**, LeetCode 8. Zero algorithm, all spec discipline. Ten minutes each, no peeking. The struggle is the point.

---

## 13. LOCK IT IN — `11:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **A stride of 60 into a window of 100 lands at most twice** — so any target has **at most two** encodings: `(t//60, t%60)` and `(t//60 − 1, t%60 + 60)`. Validate both, cost both, take the min.
> 2. **The traps are representational, not algorithmic.** Seconds run 0–99, not 0–59. Leading zeros are free because the machine adds them — so cost the *stripped* string. And the finger has memory: update `cur` or you'll pay for moves that never happened.
> 3. **Fewer keys ≠ cheaper.** Fewer *changes* is cheaper. Repeated digits and a lucky `startAt` beat a shorter string every time.
>
> The memory peg:
>
> **[VISUAL: big box → "Two ways to say it. Try both. The finger remembers."]**
>
> When the constraints cap the world at a handful of candidates, stop searching for a formula — enumerate, and pour all your care into the costing function.

---

## 14. CLIFFHANGER — `11:35`
*(open loop to next lesson)*

**[VISUAL: the microwave keypad dissolves into a blurred grid of numbers, a glowing path snaking across the rows. Title tease: "Maximum Number of Points with Cost".]**

> That closes the Design section — and it closes it on a joke the interviewer is in on. Today "try every option" *was* the optimal solution, because the options numbered two.
>
> Next section, that trick dies. You get a grid of numbers, you pick exactly one cell per row, and every pick is penalised by how far it drifted from the pick in the row above. Same shape of question — *enumerate the options, take the best* — but now the options multiply row by row, and "try them all" is a hundred thousand to the power of a hundred thousand. Enumeration explodes.
>
> So what do you do when the candidate list is too big to try, but every candidate is built from a smaller one you've already solved? That's **dynamic programming**, and we open it with **Maximum Number of Points with Cost**. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class Solution {
    public int minCostSetTime(int startAt, int moveCost, int pushCost, int targetSeconds) {
        int mm = targetSeconds / 60, ss = targetSeconds % 60;
        return Math.min(cost(mm, ss, startAt, moveCost, pushCost),
                        cost(mm - 1, ss + 60, startAt, moveCost, pushCost));
    }

    private int cost(int mm, int ss, int startAt, int moveCost, int pushCost) {
        // candidate must fit the 2-digit minutes and 2-digit seconds display
        if (mm < 0 || mm > 99 || ss < 0 || ss > 99) return Integer.MAX_VALUE;
        String digits = String.valueOf(mm * 100 + ss);   // leading zeros drop off for free
        int total = 0, cur = startAt;
        for (char c : digits.toCharArray()) {
            int d = c - '0';
            if (d != cur) { total += moveCost; cur = d; } // travel only on digit change
            total += pushCost;                            // every typed digit is a push
        }
        return total;   // max real cost is 8 * 10^5 — no overflow risk
    }
}
```

*(`Integer.MAX_VALUE` plays the role of Python's `float('inf')` — an invalid candidate simply loses the `Math.min`. Safe here because we never add to a returned sentinel, only compare it.)*
