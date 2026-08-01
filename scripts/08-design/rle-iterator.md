# 🎬 Recording Script — RLE Iterator

**Pattern: Design (pointer over run-length encoding) · LeetCode 900 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** iterator design — but this time the data is *compressed*, and decompressing it is the trap.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an editor with a two-line constructor: `self.seq.extend([value] * count)`. A memory gauge fills, turns red, and a "Memory Limit Exceeded" banner slams in — before a single query ever runs.]**

> This problem kills your solution **in the constructor** — before you answer a single query.
>
> The input looks harmless: a compressed list like `[3, 8, 0, 9, 2, 5]`. Your first instinct is to decompress it and walk it. Clean, obvious, correct on the example. Then one hidden number in the constraints turns that instinct into a **billion-element array**, and you're dead before `next` is ever called.
>
> By the end of this video you'll handle a billion-copy run with **one subtraction** — and you'll own a reflex that transfers to a whole family of Google design questions. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below it, `encoding = [3, 8, 0, 9, 2, 5]` with brackets pairing it into (3,8) (0,9) (2,5), decoding to the stream `8 8 8 5 5`.]**

> One line: **the sequence is stored as run-length pairs — `count, value, count, value` — and you must build an iterator with one method, `next(n)`.**
>
> Our tiny example: `[3, 8, 0, 9, 2, 5]`. Three 8s, zero 9s, two 5s. So the decoded stream is just five elements: `8, 8, 8, 5, 5`.
>
> `next(n)` **exhausts** — consumes — the next `n` elements and returns the **last one consumed**. If fewer than `n` remain, it eats whatever's left and returns `-1`. Consumed means gone; the next call continues after them.

**[VISUAL: the constraint line appears and 10⁹ pulses: "count up to 10⁹, up to 1000 pairs".]**

> And here's the number that *is* the whole problem: a single count can be **ten to the ninth**. One pair can mean a billion copies of 8. Hold that — it decides everything.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — let them feel the waste)*

**[VISUAL: the encoding expands into a flat list `[8, 8, 8, 5, 5]` with a read arrow `pos`. Each `next(n)` slides the arrow.]**

> Let's do what your brain does first: decode it. `[3,8]` becomes `8, 8, 8`. Skip the zero 9s. `[2,5]` becomes `5, 5`. Now keep a position pointer, and `next(n)` just jumps it forward `n` steps.
>
> `next(2)` — arrow slides past two 8s, lands on the second one. Return **8**. `next(1)` — the third 8. Return **8**. `next(1)` — first 5. Return **5**. `next(2)` — only one 5 left, we needed two. Consume it, return **-1**. Perfect answers.

**[VISUAL: rewind. The pair `(3, 8)` morphs into `(1000000000, 8)`. The expansion animation starts spewing 8s; a counter races — 1M… 50M… 400M… — the memory gauge redlines and the screen stutters to a halt.]**

> Now swap one number. Make the first pair a **billion** 8s — the constraints allow it. Watch the constructor try to expand that... it's building a billion-element list. Gigabytes of memory, a giant up-front loop — it dies before any query runs.
>
> And here's the insult: every one of those billion elements is **identical**. We manufactured a billion copies of the number 8... to answer questions we could have answered from the pair itself.

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the pair `(1000000000, 8)` next to the mountain of expanded 8s. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The pair already tells us everything: the value, and how many. Expanding it adds *zero information* — it just costs a billion slots.
>
> **LEARNER:** Okay, but `next(n)` walks element by element, right? At some point don't you *have* to touch the elements one at a time?
>
> **TEACHER:** That's the exact assumption to attack. Pause the video: if I ask you for the next 7 elements of "a billion 8s"... do you need a loop to answer? Or is there a single arithmetic operation that does it? What would you keep track of?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:25`
*(elaboration + analogy — derive it)*

**[VISUAL: the flat list vanishes. The encoding reappears as a row of water tanks: tank 1 labeled "8" with level 3, tank 2 labeled "9" level 0, tank 3 labeled "5" level 2. A pointer `i` hovers over tank 1.]**

> **TEACHER:** No loop. `next(7)` on a billion 8s is just `1,000,000,000 − 7` — and the answer is 8. Consumption is **subtraction**.
>
> So don't walk the elements — **walk the runs**. Picture each pair as a water tank: the label is the value, the level is how many are left. Keep one pointer `i` parked at the current tank.
>
> `next(n)` becomes: does the current tank hold at least `n`? **Yes** — drain `n` units from it, done; the last element consumed came from this tank, so return its label. **No** — empty the tank completely, subtract what it held from `n`, step to the next tank, and ask again.

**[VISUAL: `next(2)` on tank "8": level drops 3 → 1 in one motion, "8" glows as the returned value. Then a `next` that empties tank 8, hops over the level-0 tank 9 without stopping, and lands in tank 5.]**

> Notice the zero tank — zero 9s. It holds less than any request, so we drain nothing, hop past it, and keep going. And if we run out of tanks with `n` still unpaid — the sequence didn't have `n` elements — return `-1`.
>
> A billion-unit tank and a three-unit tank cost the exact same move: one subtraction. That's the whole aha.
>
> **LEARNER:** Wait — you're draining the tanks *in place*. Doesn't that destroy the encoding? Feels like we should keep a separate "how much have I consumed" counter instead.
>
> **TEACHER:** You could — track an offset into the current run and never touch the array; same idea, same complexity, just non-destructive. But here the iterator *owns* its state, and the encoding **is** the state. `enc[i]` stops meaning "original count" and starts meaning "**remaining** count" — one array does double duty, and everything left of `i` is guaranteed fully drained. That reframe — *the input is my bookkeeping* — is what makes the code four lines.

---

## 6. THE KEY MOVE (signaling) — `4:55`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Never decode. Walk the runs: enough in this run → subtract & return its value; else drain it and step the pointer by 2."]**

> The key move: **never materialize the decoded sequence — keep a pointer on the current run, and consume with arithmetic.** Enough left in this run? Subtract `n`, return its value. Not enough? Drain it, carry the remainder, pointer jumps two slots to the next pair.
>
> Bigger pattern, burn it in: **when the input is compressed and a count can hit ten-to-the-ninth, that count is a number to do math on — never a length to loop over.**

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type the constructor.]**

> The constructor is two lines — because we refuse to do the work the brute force died doing. Store the encoding as-is, and park the pointer at index 0.

```python
class RLEIterator:
    def __init__(self, encoding):
        self.enc = encoding    # enc[i] = remaining count, enc[i+1] = value
        self.i = 0             # index of the current run's *count*
```

> **[VISUAL: add the `next` skeleton — the while line and the happy path, highlighted.]** Now `next`. We loop over runs — not elements — and the happy path comes first: this run alone covers the request.

```python
    def next(self, n: int) -> int:
        while self.i < len(self.enc):
            if self.enc[self.i] >= n:          # this run covers the request
                self.enc[self.i] -= n          # consume by arithmetic
                return self.enc[self.i + 1]    # its value = last exhausted
```

> If the current run has at least `n` left, subtract — one operation, even for a billion — and the last element consumed is inside this run, so its value is the answer.
>
> **[VISUAL: add the drain-and-advance chunk, then the final return.]** Otherwise: drain this run into `n`, zero it out, and hop the pointer forward by two — count slots live at even indices. Fall off the end, and there weren't `n` elements left.

```python
            n -= self.enc[self.i]              # take everything it had
            self.enc[self.i] = 0               # mark it empty
            self.i += 2                        # next run's count
        return -1                              # ran out of elements
```

> That's the entire class. A constructor that stores, and a `next` that subtracts.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:50`
*(elaboration — why each line exists)*

**[VISUAL: full code; spotlight each line as it's named. The invariant floats above: "everything before i is fully drained; enc[i] = what remains here".]**

> The why, line by line — held together by one invariant: **everything before `i` is fully drained, and `enc[i]` is exactly what remains of the current run.**
>
> `enc[i] >= n` — the request ends *inside* this run, so this run's value is the last thing consumed. Subtracting `n` keeps the invariant honest for next time.
>
> `n -= enc[i]` then `i += 2` — we pay `n` down with whatever this run has, then move on still owing the difference. The `while` keeps collecting until some run absorbs the final unit.
>
> **LEARNER:** Why `>=` and not `>`? If the run has *exactly* `n` left, they look interchangeable.
>
> **TEACHER:** They're not, and exact-fit is the boundary to nail. With `>=`: count goes to zero, we return this run's value — correct, the n-th element really was in here — and the zeroed run just gets skipped by a future call. With `>` only, an exact fit would fall into the drain branch, `n` becomes zero, and we'd go hunting in the *next* run for an element we already finished consuming. Off-by-one, wrong value. `>=` says: landing on the last drop of this tank still counts as this tank.
>
> And notice what we *didn't* write: no special case for zero-count runs like our `0, 9`. Since `n` is at least 1, a zero run always fails `enc[i] >= n` and gets drained for free — subtracting zero — and skipped. The general rule already covers it.

---

## 9. DRY-RUN THE CODE — `8:05`
*(worked example — prove it, close the loop)*

**[VISUAL: trace table filling row by row; above it, the live `enc` array with `i` as a marker, counts mutating in place.]**

> Full run on `[3, 8, 0, 9, 2, 5]` — decoded stream `8, 8, 8, 5, 5`. Watch the array itself do the bookkeeping.

| Call | start `i`, `enc` | what happens | returns | end `i`, `enc` |
|---|---|---|---|---|
| `next(2)` | `i=0`, `[3,8,0,9,2,5]` | `3 ≥ 2` → `enc[0] -= 2` | **8** | `i=0`, `[1,8,0,9,2,5]` |
| `next(1)` | `i=0`, `[1,8,0,9,2,5]` | `1 ≥ 1` → `enc[0] -= 1` | **8** | `i=0`, `[0,8,0,9,2,5]` |
| `next(1)` | `i=0`, `[0,8,0,9,2,5]` | `0 < 1` drain, `i→2`; `0 < 1` drain, `i→4`; `2 ≥ 1` → `enc[4] -= 1` | **5** | `i=4`, `[0,8,0,9,1,5]` |
| `next(2)` | `i=4`, `[0,8,0,9,1,5]` | `1 < 2` → `n=1`, drain, `i→6`; `6 ≥ len` | **-1** | `i=6`, `[0,8,0,9,0,5]` |

> Third call is the workhorse: it hops the dead 8-run *and* the zero-9s run in two quick drains, then takes one 5. Fourth call still owes one element when it falls off the end — `-1`, exactly the spec. And swap that leading 3 for a billion? Row one changes to `enc[0] = 999,999,998` — same single subtraction. Loop from the cold open: closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:00`
*(transfer to interview)*

**[VISUAL: two rows — Brute: O(decoded length) ≈ 10⁹, dead in the constructor. Ours: amortized O(1) per run; the pointer `i` shown only ever moving right.]**

> Say it the way you'd say it in the room: *"Each `next` call does constant work per run it touches, and the pointer only ever moves forward — it crosses each of the at-most-1000 pairs once over the object's entire lifetime. So the total work across all calls is O(number of pairs): amortized O(1) per run, no matter how huge the counts are."*
>
> Versus the brute force: *"decoding is O(total decoded length) — up to ten-to-the-ninth per run — in time and memory. Walking the runs replaces all of that with one subtraction per run."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:40`
*(depth + honesty — naming the absence is a skill)*

**[VISUAL: the state, itemized: the encoding array + a single integer `i`. A "shrink it?" thought bubble gets a red ✗ with the caption "nothing here scales with the counts".]**

> Space: the stored encoding — O(length of `encoding`) — plus one integer. Auxiliary space beyond the input: **O(1)**. Can we do better? No — and *say why*: nothing in our state scales with the dangerous number. A billion-copy run occupies the same one slot as a one-copy run. The win isn't a clever structure we added; it's the billion-element array we **refused to allocate**.
>
> One polish point if the interviewer frowns at mutating their input: track the current run's consumed amount in a separate variable instead of decrementing `enc[i]` in place. Same asymptotics, non-destructive — offering that unprompted reads as senior.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Design Compressed String Iterator (LC 604)". A blank editor.]**

> Before the next video, try **Design Compressed String Iterator** — a run-length *string* like `"L1e2t1C1o1d1e1"`, and you build `next()` and `hasNext()` without ever decompressing. It's this exact pattern with a parsing twist: same pointer, same remaining-count, one character at a time.
>
> Ten minutes, no peeking. The struggle is the point.

---

## 13. LOCK IT IN — `10:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three takeaways:
> 1. **Compressed input + astronomical counts = a trap.** The naive move — decode it — dies on one 10⁹ run.
> 2. **Walk the runs, not the elements:** pointer at the current pair; enough here → subtract and return the value; not enough → drain, carry the remainder, step by 2.
> 3. **The pointer only moves forward** → amortized O(1) per run, and O(1) auxiliary space — nothing you store scales with the counts.
>
> The memory peg: **"a count is a number to do math on, never a length to loop over."**
>
> *(GCA reminder — for the interview itself: Google scores General Cognitive Ability, and narrating your approach is half the rubric. Open your mouth before your editor: ask "how large can a count be?", then say out loud "10⁹ means decoding is a trap — I'll operate on the compressed form directly." Spotting the trap and naming it is worth more than typing the four lines.)*

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: blurred next title: "Snapshot Array" — an array with a camera-shutter icon, ghost copies of old versions stacking up behind it.]**

> Today's iterator only moves **forward** — consume and never look back, so one pointer was enough. Next problem flips the arrow of time: an array where you call `snap()` to freeze a moment, keep writing, and can later ask *"what was index 3 back in snapshot 5?"* Copy the whole array on every snap and you're right back in today's blow-up. There's a way to remember every version while barely storing anything — that's **Snapshot Array**. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class RLEIterator {
    private final long[] enc;   // long: counts reach 10^9; no overflow worries
    private int i = 0;          // index of the current run's remaining count

    public RLEIterator(int[] encoding) {
        enc = new long[encoding.length];
        for (int k = 0; k < encoding.length; k++) enc[k] = encoding[k];
    }

    public int next(int n) {
        while (i < enc.length) {
            if (enc[i] >= n) {            // this run covers the whole request
                enc[i] -= n;             // consume by arithmetic, no loop
                return (int) enc[i + 1]; // its value is the last exhausted
            }
            n -= enc[i];                 // drain this run
            enc[i] = 0;
            i += 2;                      // step to the next pair
        }
        return -1;                       // not enough elements left
    }
}
```

*(Note the `long` copy of the encoding: values fit in `int`, but keeping counts as `long` removes any overflow doubt when runs hold ~10⁹.)*
