# 🎬 Recording Script — Amount of New Area Painted Each Day
**Pattern: Interval union / Union-Find "jump pointer" · LeetCode 2158 · Hard · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Union-Find with path compression (from the graphs section) and half-open intervals (My Calendar I) — we're about to bend the first one into a shape you've never seen.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a paint roller drags across a number line, cells filling in. Then the same stretch gets rolled again… and again… a "cells touched" counter spins to 2,500,000,000. A red "Time Limit Exceeded" banner slams in.]**

> Fifty thousand days. Each day, someone paints a stretch of an infinitely long fence, and you report how much *fresh* fence they covered — not the parts already painted.
>
> You write the obvious thing: a set of painted cells, walk each day's stretch, count the new ones. Correct. Passes the examples. Then day after day repaints the same huge span, your loop re-walks two and a half *billion* cells that are already wet… and the judge kills you.
>
> Here's the promise: by the end of this video, standing on a painted cell won't mean *walking* through the painted run — it'll mean **teleporting past it in one hop**. And the tool that does it is Union-Find, wearing a disguise you need to recognize for Google. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below, a number line 0–9 and three labeled brushes:]**

```
paint = [[1,4], [4,7], [5,8]]   →   answer: [3, 3, 1]
```

> The whole problem in one line: **for each day's segment, return how much of it lands on never-before-painted ground.**
>
> One catch that decides every boundary in this problem: the segments are **half-open**. `[1, 4)` paints cells 1, 2, 3 — *not* 4. If My Calendar I taught you anything, it's that this is the first clarifying question out of your mouth.
>
> So our tiny example: day zero paints cells 1, 2, 3 — all fresh, that's 3. Day one paints 4, 5, 6 — fresh again, 3. Day two paints 5, 6, 7 — but 5 and 6 are already wet. Only 7 is new. That's 1. Answer: `[3, 3, 1]`. Keep this exact example on screen — we'll earn it three different ways.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: the number line; a `painted` set below it; a "cells visited" counter top-right at 0.]**

> Let's do what your brain does first: keep a set of painted cells. Each day, step through the segment cell by cell, and count the ones not in the set.
>
> Day zero, `[1, 4)`. Visit 1 — new, paint it. Visit 2 — new. Visit 3 — new. Three visits, three fresh cells. Fine.
>
> **[VISUAL: cells 1–3 fill in; counter reads 3.]**
>
> Day one, `[4, 7)`. Visit 4, 5, 6 — all new. Counter's at 6. Still fine.
>
> Day two, `[5, 8)`. Visit 5 — *already painted, no credit.* Visit 6 — *already painted, no credit.* Visit 7 — new. Three visits for **one** unit of real work.
>
> **[VISUAL: cells 5 and 6 flash gray "wasted"; counter ticks anyway.]**
>
> Two wasted steps on a toy example. Now scale it: fifty thousand days that *all* paint `[0, 50000)`. Day zero does real work. Days one through 49,999 each re-walk fifty thousand wet cells and paint **nothing**. That's the two-and-a-half-billion from the cold open. O(n · range) — and it's not the counting that's slow. It's the **re-walking of runs we've already filled.**

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. A long solid painted run on the line; a cursor stepping through it cell… by cell… by cell. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Look at what the brute force does when it lands on a painted run. It *knows* cell 5 is painted. And then it checks 6 anyway. And 7. It steps through territory it has already conquered, one cell at a time, learning nothing.
>
> **LEARNER:** But what else can it do? It doesn't know where the run *ends* — it has to look at each cell to find the next free one, right?
>
> **TEACHER:** Does it, though? Here's your think: the first time we painted cell 5, we were *standing right there*. What one piece of information could we have **left behind at cell 5** so that anyone landing on it later doesn't have to walk at all? Pause the video. What would you write on the cell?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:25`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: cell 5 gets a signpost planted on it: "→ 6". Then 6 gets "→ 7". A stick figure lands on 5 and ricochets along the arrows straight to 7 in one animated hop.]**

> **TEACHER:** Leave a **signpost**. The moment I paint cell 5, I plant a pointer on it: *"5 is taken — next candidate is 6."* When I paint 6: *"next candidate is 7."* Now watch what happens on day two. I land on 5, read the signpost — go to 6. Read 6's signpost — go to 7. The painted run isn't a hallway I walk through anymore; it's a chain of arrows that *flings* me to the first free cell.
>
> It's like the "next available" sign at a parking garage. You don't crawl past every occupied spot — the sign at the entrance already points you at the first open one.
>
> **[VISUAL: the chain 5→6→7 collapses into a single fat arrow labeled "one hop". ]**
>
> And one more trick makes it airtight: after I chase the chain once, I go back and repoint *every* signpost on the path straight at the destination. Next visitor doesn't hop three times — they hop **once**. Sound familiar?
>
> **LEARNER:** That's path compression. But hang on — Union-Find is about *groups*. `parent[x]` is supposed to point toward a group's leader, and `find` tells you which component you're in. There are no groups here. How is this Union-Find?
>
> **TEACHER:** That's the misconception to kill today, and killing it is the whole lesson. `parent[x]` was never sacred — it's just a pointer you chase with compression. Here we redefine it: **`parent[x]` means "the next free cell at or after x."** A cell with no entry is free — it's its own answer. A painted cell points forward. "Union" is just painting: set `parent[x] = x + 1`, welding x onto the run ahead of it. Same `find`, same compression, same near-constant amortized cost — the *meaning* changed, not the machinery. That's the disguise Google loves: Union-Find as a **find-the-next-free-slot** engine.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "parent[x] = next free cell ≥ x · paint it → point it forward → teleport."]**

> Burn this in: **`parent[x]` is the next free cell at or after `x`. To paint a segment: jump to the first free cell, paint it, point it at `x + 1`, and teleport onward — painted runs collapse into single hops.**
>
> And the guarantee that makes it fast: each cell gets its signpost planted **at most once, ever**. Once painted, always painted. So total work across all fifty thousand days is bounded by the number of cells ever painted — not the sum of the segment lengths.

---

## 7. CODE IT — LIVE & CHUNKED — `5:40`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. A dict, not an array — cells with no entry are free, and untouched coordinates cost us nothing.

```python
def amountPainted(paint):
    parent = {}     # parent[x] = next free coordinate at or after x
```

> **[VISUAL: add chunk 2, highlight it.]** Now `find` — chase the signposts to the first free cell, then compress the path behind us.

```python
    def find(x):
        root = x
        while root in parent:
            root = parent[root]      # follow the "skip me" pointers
        while x in parent:           # path compression:
            parent[x], x = root, parent[x]   # repoint every hop at root
        return root
```

> First loop: walk the chain until we hit a cell with no entry — that cell is free, that's our answer. Second loop: walk the *same* chain again and point every cell on it directly at the destination. Two passes, and the chain is flattened forever.
>
> **[VISUAL: add chunk 3.]** Now the paint loop — one day at a time.

```python
    worklog = []
    for start, end in paint:
        count = 0
        x = find(start)              # first free cell at or after start
```

> **[VISUAL: add chunk 4, highlight the three-line body.]** While we're still inside today's segment: paint, plant the signpost, teleport.

```python
        while x < end:
            count += 1               # brand-new cell — take the credit
            parent[x] = x + 1        # union: x is taken, next candidate is x+1
            x = find(x + 1)          # teleport to the next free cell
        worklog.append(count)
    return worklog
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:20`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `x = find(start)` — not `x = start`. Day two starts at 5, but 5 is painted; `find` delivers us straight to 7. The very first step of the day already skips the wet paint.
>
> `while x < end` — strict less-than, because `end` is excluded. The segment `[5, 8)` owns 5, 6, 7 — the moment `find` lands on 8, we're out. The half-open rule from the problem statement lives in this one comparison.
>
> `parent[x] = x + 1` — the signpost. Note what we do *not* say: we don't point at the end of the run, we just say "next candidate is one to the right." If `x + 1` is painted too, chasing pointers — plus compression — sorts that out lazily.
>
> **LEARNER:** That's the line I'd flub — `x = find(x + 1)`. We *just* painted `x`, so `x + 1`… why the `find`? Why not just `x = x + 1` and let the `while` check it?
>
> **TEACHER:** Because `x + 1` might have been painted **days ago**. Picture painting `[3, 6)` when cell 4 is already wet from last week: I paint 3, step to 4 — and if I just walk in, I'm the brute force again, shuffling cell by cell through old paint. `find(x + 1)` asks, "and where's the next *free* cell from here?" — maybe it's 4, maybe it's 40. Drop that `find` and you don't get a wrong answer — you'd need an `if` to skip credit — you get the *slow* answer back. The teleport **is** the algorithm.
>
> And the invariant that makes the whole thing correct: `find(x)` always returns the smallest unpainted coordinate at or after `x`. Painting preserves it — we mark a cell taken and aim its pointer at the next candidate. Compression preserves it — shortcuts change the path, never the destination. So the loop paints *exactly* the free cells in `[start, end)`, and every unit of area is credited exactly once, on the day it first turns wet.

---

## 9. DRY-RUN THE CODE — `8:50`
*(worked example — prove it, close the loop)*

**[VISUAL: the number line with signposts appearing; a trace table filling row by row.]**

> Let's run the real code on `[[1,4], [4,7], [5,8]]` and close the loop from minute one.

| Day | Segment | `find` hops | Painted | `parent` after | worklog |
|---|---|---|---|---|---|
| 0 | `[1,4)` | find(1)=1 ✓, find(2)=2 ✓, find(3)=3 ✓, find(4)=4 — `4 < 4`? no | 1, 2, 3 | 1→2, 2→3, 3→4 | **3** |
| 1 | `[4,7)` | find(4)=4 ✓, find(5)=5 ✓, find(6)=6 ✓, find(7)=7 — stop | 4, 5, 6 | + 4→5, 5→6, 6→7 | **3** |
| 2 | `[5,8)` | find(5) **chains 5→6→7** = 7 ✓, find(8)=8 — stop | 7 only | + 7→8, and 5,6 compressed →7 | **1** |

> Day two is the money row. The brute force would visit 5, then 6, then 7 — three steps. Our code calls `find(5)`, rides the signposts 5 → 6 → 7 in one collapsed hop, paints 7, and it's done. And path compression quietly repointed 5 and 6 straight at 7 on the way through — the next visitor hops once.
>
> Worklog: `[3, 3, 1]`. Exactly what we promised at second forty. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:50`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n · range) ≈ 2.5·10⁹. Ours: O((painted + n) · α) ≈ near-linear. A note: "each cell painted at most once, ever".]**

> Say it the way you'd say it in the room: *"Brute force re-walks painted runs every day — O(n times range), up to two-and-a-half billion steps. With the jump pointers, each coordinate gets painted and pointed at most once across the entire run, and every lookup is inverse-Ackermann amortized thanks to path compression. So total time is O of painted-cells-plus-days, times alpha — effectively near-linear in the painted area."*
>
> That phrase — "each cell does work **once ever**, not once per day" — is the amortized argument in one breath. That's the sentence that flips this Hard.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:25`
*(depth + honesty)*

**[VISUAL: the dict beside a giant mostly-empty boolean array; the array grays out, the dict pulses green.]**

> Quick one, and honesty scores here.
>
> Space is **O(painted cells)** — the dict holds one entry per cell ever painted, nothing per day, nothing for untouched ground. That's already the floor: to avoid double-counting you *must* remember what's painted, and every stored cell maps to real area you returned. The dict beats a range-sized boolean array precisely when coordinates are huge and sparse.
>
> One alternative worth naming out loud: a sorted map of merged painted runs — TreeMap in Java — gives O(n log n) time and stores one entry per *run*, often fewer. Totally valid. But the jump-pointer dict is simpler to get right under pressure, so I'd lead with it and *mention* the interval map. Knowing two roads and choosing one, on purpose, is a senior signal.

---

## 12. YOUR TURN (active recall) — `11:00`
*(retrieval practice)*

**[VISUAL: "Your turn → Exam Room (LC 855) / next-free-seat problems". A blank editor.]**

> Before the next video, try this on **Exam Room**, or any "find the next available seat" flavor you can get your hands on: rebuild the `parent[x]` = next-free-slot trick from a blank editor, from memory. No peeking at this video.
>
> If you can re-derive *paint it, point it, teleport* cold, you own the pattern — and it'll surface anywhere slots get consumed left to right.

---

## 13. LOCK IT IN — `11:30`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **The waste is re-walking filled runs** — the brute force pays for wet paint every single day; O(n · range).
> 2. **Redefine `parent[x]` as "next free cell ≥ x"** — painting is `parent[x] = x + 1`; `find` plus compression turns solid runs into single hops.
> 3. **Each cell is painted and pointed at most once ever** — so total work is near-linear in the painted area, and space is O(painted cells), which is the floor.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "Don't walk wet paint — paint it, point it, teleport."]**
>
> When a problem says *fill intervals, skip what's filled, find the next free slot fast* — seats, servers, timestamps, fence cells — your hand should already be reaching for Union-Find with a forward pointer.
>
> *(GCA reminder — for the interview itself: open with the clarifying question — "these are half-open, so `[4,7]` paints 4, 5, 6 and not 7, right?" — then state the set-based brute force, name the re-walking of painted runs out loud, and only then unveil the jump pointer. Google scores General Cognitive Ability, and narrating that path from naive to optimal — plus asking the boundary question early — is half the rubric before you type a line.)*

---

## 14. CLIFFHANGER — `12:00`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "The Number of Weak Characters in the Game" — a scatter of (attack, defense) points; one point flashes "dominated".]**

> Today the intervals lived on a line, and one clever pointer let us skip everything already settled. Next problem: game characters with **two** stats — attack *and* defense — and a character is weak if someone beats it on *both*. Compare every pair and you're back in O(n²) jail. The escape is a sort so sneaky that after it, one single backward pass — tracking just one number — settles all fifty thousand characters. The whole trick hides in *how you break ties*. That's The Number of Weak Characters in the Game. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int[] amountPainted(int[][] paint) {
    // parent.get(x) = next free coordinate at or after x (absent = x itself is free)
    Map<Integer, Integer> parent = new HashMap<>();
    int[] worklog = new int[paint.length];

    for (int i = 0; i < paint.length; i++) {
        int start = paint[i][0], end = paint[i][1];
        int count = 0;
        int x = find(parent, start);          // first free cell >= start
        while (x < end) {                      // still inside today's segment?
            count++;                           // brand-new cell
            parent.put(x, x + 1);              // union: skip x forever
            x = find(parent, x + 1);           // teleport to next free cell
        }
        worklog[i] = count;
    }
    return worklog;
}

// find with iterative path compression
private int find(Map<Integer, Integer> parent, int x) {
    int root = x;
    while (parent.containsKey(root)) root = parent.get(root);
    while (parent.containsKey(x)) {
        int next = parent.get(x);
        parent.put(x, root);                   // compress: point straight at root
        x = next;
    }
    return root;
}
```
