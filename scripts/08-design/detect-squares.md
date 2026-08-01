# 🎬 Recording Script — Detect Squares

**Pattern: Design (hash-map counting + diagonal corners) · LeetCode 2013 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** hash-map counting (Logger Rate Limiter keyed a map by message; here the key is a coordinate pair and the value is a *count*).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a 2-D grid raining down points, one by one. A query point flashes at (11,10) with "how many squares?" Then a triple-nested loop appears in an editor and a red "Time Limit Exceeded" banner slams over it.]**

> Points keep streaming onto a grid. At any moment, someone hands you one more point and asks: *"how many squares can you complete with it?"*
>
> The honest first answer — try every three stored points and check — is a triple loop. Cubic per query, and you get up to five thousand queries. Dead on arrival.
>
> Here's what's wild: the fix isn't a clever data structure. It's a piece of eighth-grade geometry — one fact about squares that turns three nested loops into **one**. And you don't *search* for the other corners at all. You **compute** them. Let's find that fact.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below, a small coordinate grid; the call sequence appears one line at a time.]**

> One line: **build a class with two methods — `add(point)` stores a 2-D point, `count(point)` returns how many axis-aligned, positive-area squares use the query point as one corner and three previously added points as the other three.**
>
> Axis-aligned means the sides run parallel to the axes — no tilted squares. Positive area means side length can't be zero. And one detail that matters: **duplicates count.** Add `[1,1]` three times, and there are genuinely three copies sitting there.
>
> Here's our whole example — three adds, two queries:

```
add([3, 10])
add([11, 2])
add([3, 2])
count([11, 10])  → ?
count([14, 8])   → ?
```

**[VISUAL: the three points drop onto the grid; (11,10) pulses with a "?".]**

> Three stored points, and a query at `(11, 10)`. Eyeball it — do you see a square hiding in there? Hold your answer; we're about to check by hand.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: the grid with the 3 stored points. A "triples tested" counter, top-right. Arrows lasso every combination of three points.]**

> First instinct, straight from the problem statement: store every point in a list. On `count`, try **every triple** of stored points, and check whether those three plus the query form an axis-aligned square.
>
> With three stored points there's exactly one triple: `(3,10)`, `(11,2)`, `(3,2)`, plus the query `(11,10)`. Check it: two distinct x's — 3 and 11. Two distinct y's — 2 and 10. Gaps: `11−3 = 8` and `10−2 = 8`. Equal, non-zero, all four grid corners present. **That's a square.** An 8-by-8. Answer: 1.
>
> **[VISUAL: the square (3,2)-(3,10)-(11,10)-(11,2) draws itself in green; "triples tested: 1".]**
>
> Cute — with three points. Now imagine a few thousand adds before this query.
>
> **[VISUAL: the grid floods with points; the counter morphs into "k³ ≈ billions" with a red glow.]**
>
> A thousand stored points means a *billion* triples — for **one** query. And you get up to five thousand calls. Feel the waste: almost every triple you test shares *no geometry whatsoever* with the query point. You're checking three strangers and hoping they happen to box in your corner.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The query point (11,10) glows gold; the words "one corner — FREE" stamp next to it. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's what the brute force ignores. A square has four corners — and the query already **hands you one for free**. You're brute-forcing all four when one is nailed down before you start.
>
> **LEARNER:** Okay, but fixing one corner doesn't feel like enough. A corner touches two sides — there are still tons of possible squares hanging off that one point, in every direction and every size.
>
> **TEACHER:** Exactly right — one corner still leaves too many squares to enumerate. So here's your pause-and-think: **how many corners do you need to pin down before the entire square is forced — no choices left?** And which stored point would you pick as that second corner? Pause the video.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the query (11,10) and the point (3,2) light up. A dashed diagonal connects them — and the other two corners (3,10) and (11,2) snap into place automatically, like magnets.]**

> **TEACHER:** The answer is **two** — as long as they're the *right* two. Fix the query `(qx, qy)` as one corner, and pick a stored point `(px, py)` as the **diagonally opposite** corner.
>
> Here's the eighth-grade geometry: for an axis-aligned square, *the two diagonal corners completely determine the other two.* If `(qx,qy)` and `(px,py)` sit across the diagonal, the remaining corners **must** be `(qx, py)` and `(px, qy)` — just swap one coordinate each. No freedom. No search.
>
> **[VISUAL: picture-frame analogy — grip two opposite corners of a photo frame; the frame snaps rigid. Caption: "two diagonal corners = the whole frame".]**
>
> Think of holding a picture frame by two opposite corners. Grip those two and the whole frame is locked — the other corners can't be anywhere else. So instead of *searching* for the other two points, I **compute** their coordinates and ask my hash map: *"how many copies of you exist?"*
>
> When is a stored point a legal diagonal partner? The diagonal of a square spans equally in both directions: `abs(px − qx) == abs(py − qy)`. And positive area means that span isn't zero: `px != qx`. Every stored point either passes that test or it doesn't — **one loop, no triples.**
>
> **LEARNER:** And that's why duplicates were called out in the problem, right? If `(3,10)` was added twice, both copies close a separate square?
>
> **TEACHER:** Exactly — which is why we don't store points in a list, we store them in a **counter**: key `(x, y)`, value = how many copies. Then "does this corner exist?" upgrades to "how many of this corner exist?" — and we *multiply* the three counts. Every combination of copies is a distinct square, and one multiplication counts them all.

---

## 6. THE KEY MOVE (signaling) — `4:50`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Fix the query. Loop candidate DIAGONALS. The other two corners are computed, not searched — multiply their counts."]**

> Burn this in: **loop over each stored point as the diagonal corner — the other two corners are forced, so look them up and multiply the counts.**
>
> That's the transferable design move, way beyond this problem: *when a shape is fully determined by two of its points, iterate the second point and multiply hash-map lookups for the rest.*

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. One field — a Counter keyed by coordinate.

```python
from collections import Counter

class DetectSquares:
    def __init__(self):
        self.cnt = Counter()                   # (x, y) -> how many copies added
```

> **[VISUAL: add chunk 2, highlight it.]** `add` is one line. Duplicates just increment.

```python
    def add(self, point):
        self.cnt[tuple(point)] += 1            # O(1); duplicates increment
```

> **[VISUAL: add chunk 3 — the loop header and the diagonal test, highlighted.]** Now `count`. Unpack the query, then loop every distinct stored point as a **candidate diagonal** — keeping only real diagonals: equal span both ways, and non-zero.

```python
    def count(self, point):
        qx, qy = point
        total = 0
        # each stored point is a candidate DIAGONAL corner (px, py)
        for (px, py), c in self.cnt.items():
            if abs(px - qx) == abs(py - qy) and px != qx:
```

> **[VISUAL: add chunk 4 — the multiply line lands with the two computed corners flashing on the grid.]** And the payoff line. The other two corners are `(qx, py)` and `(px, qy)` — swap one coordinate each. Multiply the three multiplicities.

```python
                # diagonal fixed -> other corners forced: (qx, py) and (px, qy)
                total += c * self.cnt[(qx, py)] * self.cnt[(px, qy)]
        return total
```

> That's the whole class. One counter, one loop, one multiplication. And notice the quiet Python favor: `Counter` returns **0** for a missing key instead of crashing — so if a forced corner was never added, the product is zero and the candidate silently contributes nothing. No `if`-checks needed.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full class; spotlight each line as it's named.]**

> Now the whys — every condition earns its place.
>
> `abs(px - qx) == abs(py - qy)` — the diagonal of a square spans equally in x and y. Unequal spans would make a rectangle, not a square. This test is what makes the candidate a *legal* diagonal.
>
> **LEARNER:** Wait — you check `px != qx` for positive area, but never `py != qy`. Isn't that only half the check?
>
> **TEACHER:** Sharp catch — and it's already covered. We only reach `px != qx` **after** the spans passed as equal. If the horizontal span isn't zero, the vertical span — being equal to it — can't be zero either. One check does both jobs. Write the second check if it helps you sleep; it'll just never fire.
>
> `c * self.cnt[(qx, py)] * self.cnt[(px, qy)]` — the multiplication is the duplicates story. `c` copies of the diagonal, times copies of each forced corner: every combination is its own square, exactly as the problem demands.
>
> **LEARNER:** One thing bugs me. The other two corners of a real square are *also* stored points — so when the loop reaches *them* as candidates, don't we count the same square again?
>
> **TEACHER:** That's the classic worry, and here's why the answer is no. Look at where those other corners sit relative to the query: `(qx, py)` shares the query's **x**, and `(px, qy)` shares its **y**. Share a coordinate, and one of the two spans is zero — so `abs(px−qx) == abs(py−qy)` fails, or `px != qx` fails. Adjacent corners *can't* pass the diagonal test. Each square has exactly **one** diagonal partner for the query, so each square is counted exactly once. The filter that finds squares is the same filter that prevents double counting.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: the grid with the 3 points and query (11,10); the trace table fills row by row, and the green square redraws on the winning row.]**

> Run the real code on our example. Counter: `{(3,10): 1, (11,2): 1, (3,2): 1}`. Query `(qx, qy) = (11, 10)`.

| Candidate `(px,py)` | `abs(px−11) == abs(py−10)`? | `px ≠ 11`? | Forced corners `(qx,py)`, `(px,qy)` | Adds |
|---|---|---|---|---|
| `(3,10)` | 8 vs 0 → no | — | — | 0 |
| `(11,2)` | 0 vs 8 → no | no | — | 0 |
| `(3,2)` | 8 vs 8 → **yes** | yes | `(11,2)`, `(3,10)` | `1 · 1 · 1 = 1` |

> Total: **1** — the same 8-by-8 square we found by hand, `(11,10)–(3,10)–(3,2)–(11,2)`. And see rows one and two: those are the square's *adjacent* corners failing the diagonal test, live — that's the no-double-counting guarantee playing out in the table.
>
> **[VISUAL: second mini-table for count([14,8]) — three rows, all "no".]**
>
> Second query, `(14, 8)`: spans are 11-vs-2, 3-vs-6, 11-vs-6 — nothing matches. Total **0**. Both answers, proven.

---

## 10. COMPLEXITY, OUT LOUD — `9:10`
*(transfer to interview)*

**[VISUAL: two rows — Brute: add O(1), count O(k³). Ours: add O(1), count O(d). Caption: "d = distinct stored points".]**

> Say it the way you'd say it in the room: *"`add` is one hash-map increment — O(1). `count` loops the distinct stored points once, doing O(1) lookups per candidate — O(d), where d is the number of distinct points. Versus the brute force's O(k³) per query, that's the difference between billions of checks and a few thousand."*
>
> And here's your **GCA moment** — remember, Google explicitly scores General Cognitive Ability, and *narrating your route from naive to optimal is half that rubric*. So before writing a line, ask the clarifying question: **"do duplicate points count as separate corners?"** That single question changes the code from `total += 1` to `total += c · a · b` — and asking it out loud, then naming the diagonal insight before coding it, is exactly the signal they're grading.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:50`
*(depth + honesty)*

**[VISUAL: the counter map; a "shrink it?" thought bubble gets a red ✗. Then points regroup into columns, and a count() sweep scans only one column.]**

> Space is `O(d)` — one entry per distinct point — and that's the floor. **Say why:** any future `count` might need any past point as a corner, so there's nothing you're allowed to forget. Naming the floor beats silently accepting it.
>
> There *is* a **time** refinement worth offering: bucket points **by column** — a dict `x → Counter of y's at that x`. Then `count` walks only the y-values in the query's own column as the "same-x corner," and checks the diagonal `side` to the left and right. Worst case is still `O(d)`, but when points cluster across many columns, each query touches far fewer candidates. That's the exact nudge an interviewer gives when they ask *"can you do better in practice?"* — and knowing it's a constant-factor win, not a big-O win, is the honest, senior answer.

```python
from collections import Counter, defaultdict

class DetectSquaresByColumn:
    def __init__(self):
        self.cnt = Counter()                       # (x,y) -> multiplicity
        self.cols = defaultdict(Counter)           # x -> Counter of y's in that column

    def add(self, point):
        x, y = point
        self.cnt[(x, y)] += 1
        self.cols[x][y] += 1

    def count(self, point):
        qx, qy = point
        total = 0
        for py, c in self.cols[qx].items():        # same-column partners only
            side = abs(py - qy)
            if side == 0:                          # zero area — skip
                continue
            for px in (qx - side, qx + side):      # diagonal sits side away, left or right
                total += c * self.cnt[(px, qy)] * self.cnt[(px, py)]
        return total
```

---

## 12. YOUR TURN (active recall) — `10:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Minimum Area Rectangle (LC 939)". A blank editor.]**

> Before the next video, try **Minimum Area Rectangle** — given a point set, find the smallest axis-aligned rectangle. Same DNA: hash the points, iterate pairs as **diagonal** corners, and the other two corners are computed, not searched. If today's idea stuck, you'll feel your hand reaching for it inside a minute.
>
> Ten minutes, no peeking. The struggle is the point.

---

## 13. LOCK IT IN — `11:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three takeaways:
> 1. **Duplicates matter → store a Counter keyed by `(x, y)`,** not a list. Existence checks become multiplicity lookups.
> 2. **A square is pinned by its two diagonal corners** — loop candidates with `abs(dx) == abs(dy)` and `dx ≠ 0`, then the other corners are `(qx,py)` and `(px,qy)`, forced.
> 3. **Multiply the three counts** — every combination of copies is its own square; adjacent corners can't pass the diagonal test, so nothing double-counts.
>
> The memory peg:
>
> **[VISUAL: big box → "Grab the frame by its diagonal — the other corners have nowhere else to be."]**
>
> When a query point anchors a shape and duplicates count, your hand should already be reaching for a coordinate-keyed counter and a one-loop diagonal scan.

---

## 14. CLIFFHANGER — `11:30`
*(open loop to next lesson)*

**[VISUAL: a blurred stock chart with prices flickering — then one old price gets *corrected* and the max/min lines wobble. Title tease: "Stock Price Fluctuation".]**

> Today's structure only ever *accumulated* — every `add` was permanent, and one map handled everything. Next up, the stream fights back: stock prices arrive out of order, and an update can **rewrite the past** — a correction lands at an old timestamp, and suddenly your maximum might be a lie. One hash map can't save you when history itself changes; you'll need a second structure that can *un-know* things. That's **Stock Price Fluctuation**. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class DetectSquares {
    // encode (x, y) as one key x*1001 + y since 0 <= x, y <= 1000
    private final Map<Integer, Integer> cnt = new HashMap<>();

    public DetectSquares() {}

    public void add(int[] point) {
        int key = point[0] * 1001 + point[1];
        cnt.merge(key, 1, Integer::sum);           // duplicates increment
    }

    public int count(int[] point) {
        int qx = point[0], qy = point[1];
        int total = 0;
        // each stored point is a candidate diagonal corner
        for (Map.Entry<Integer, Integer> e : cnt.entrySet()) {
            int px = e.getKey() / 1001, py = e.getKey() % 1001;
            // valid diagonal: equal span both ways, non-zero (positive area)
            if (Math.abs(px - qx) == Math.abs(py - qy) && px != qx) {
                int c = e.getValue();
                int a = cnt.getOrDefault(qx * 1001 + py, 0);   // corner (qx, py)
                int b = cnt.getOrDefault(px * 1001 + qy, 0);   // corner (px, qy)
                total += c * a * b;
            }
        }
        return total;
    }
}
```
