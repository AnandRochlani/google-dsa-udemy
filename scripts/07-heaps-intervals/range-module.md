# 🎬 Recording Script — Range Module
**Pattern: Sorted disjoint-interval structure (TreeMap / bisect) · LeetCode 715 · Hard · Target length ~14 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** My Calendar I (sorted intervals + binary search). If they've seen that, this is that idea with teeth.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a number line from 0 to 1,000,000,000. A single command types itself: `addRange(0, 1000000000)`. A memory meter starts climbing — 1 GB, 2 GB, 4 GB — then the screen flashes red: `MemoryError`.]**

> One line of code. `addRange(0, one billion)`. And your solution just tried to allocate eight gigabytes of RAM to store a single, simple fact: *"everything is covered."*
>
> That's the trap. This one's rated Hard and it earns it — not because the algorithm is exotic, but because the obvious data structure is off by a factor of a hundred thousand. Here's the promise. By the end of this video, `addRange(0, one billion)` will cost you **two integers**. Queries will be `O(log n)`. And the idea that gets you there is one sentence long. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: three method signatures stacked. Below them, a short number line from 8 to 22 with tick marks, currently all grey.]**

> Three operations on a number line.
> **`addRange(left, right)`** — paint everything from `left` up to `right` as covered.
> **`removeRange(left, right)`** — un-paint it.
> **`queryRange(left, right)`** — return true only if **every single number** in that span is covered. Not "some of it." All of it.
>
> And one detail that decides every comparison you'll write today: the ranges are **half-open**. `[10, 20)` means 10, 11, all the way to 19. **Not** 20. So `[10,20)` and `[20,30)` don't overlap — they touch. Hold that thought; it'll matter more than you expect.
>
> **[VISUAL: the tiny example appears as four lines:]**
>
> ```
> addRange(10, 20)
> removeRange(14, 16)
> queryRange(10, 14) → ?
> queryRange(13, 15) → ?
> ```
>
> Four calls. We'll answer those question marks by hand before we write a line of code.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — let them feel the waste)*

**[VISUAL: a row of ~15 checkboxes labelled 8 through 22, all unchecked. A "cells touched" counter, top-right, at 0.]**

> Let's do what your brain does first. Coverage is a property of each number — so keep a boolean per number. One array. Dead simple.
>
> `addRange(10, 20)`. Walk from 10 to 19, tick each box.
>
> **[VISUAL: boxes 10–19 tick green one at a time; counter climbs to 10.]**
>
> `removeRange(14, 16)`. Walk from 14 to 15, untick.
>
> **[VISUAL: boxes 14 and 15 flip back to grey; counter → 12.]**
>
> `queryRange(10, 14)` — scan 10, 11, 12, 13. All green. **True.**
> `queryRange(13, 15)` — scan 13, 14, 15. Box 14 is grey. **False.**
>
> **[VISUAL: those two answers lock in with a ✅ and a ❌.]**
>
> And honestly? This is *correct*. Every answer is right, and saying it out loud in the interview costs you nothing. Then you look at the constraints.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — pause #1)*

**[VISUAL: the constraint line blown up huge: `0 <= left < right <= 10^9` and `at most 10^4 calls`. Then the checkbox row zooms out and out and out until the boxes are a solid grey smear stretching off both edges of the screen.]**

> **TEACHER:** Coordinates go up to **ten to the ninth** — a billion. But you only ever get **ten thousand calls**. Sit with that gap for a second.
>
> A billion booleans in Python is about eight gigabytes. Even a packed `bytearray` is a full gigabyte, allocated before you've done anything. And `addRange(0, 10^9)` is a **billion** individual writes — for *one* call. Ten thousand of those is ten to the thirteenth operations. That's hours.
>
> **LEARNER:** Okay, but what if I use a `set` instead? Then I only store the numbers that are actually covered — no wasted gigabyte for empty space.
>
> **TEACHER:** Smart, and it fixes the *empty* space. But run `addRange(0, 10^9)` on it. How many elements go into that set?
>
> **LEARNER:** …a billion. Same wall.
>
> **TEACHER:** Same wall, just further down the road. And that's the clue. Here's your think, and I want you to actually pause.
>
> **[VISUAL: freeze frame. Two numbers side by side, huge: `10^9 positions` vs `10^4 calls`. A 5-second "🤔 your turn" timer.]**
>
> **After ten thousand calls, how many separate "pieces" of covered number line can there possibly be?** Not how many *numbers* — how many *pieces*. Pause the video and put a number on it.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:40`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the number line again. `addRange(0, 1000000000)` runs — and instead of a billion boxes, ONE long green bar appears, labelled with just two numbers: `0` and `1000000000`.]**

> Ten thousand. At most. Every `addRange` can create at most one new piece. Every `removeRange` can split one piece into at most two. That's it.
>
> So `addRange(0, one billion)` isn't a billion facts. It's **one** fact, and it takes **two integers** to write down — the memory meter from the cold open just went from eight gigabytes to sixteen bytes.
>
> That's the whole leap. **Stop storing points. Store intervals.** The covered set is always a union of disjoint ranges, kept in a list sorted by start. Think of a highlighter on a very long page: you don't record which *letters* are highlighted, you record where each **stripe** begins and ends. Highlight half the book — still one stripe.
>
> **[VISUAL: two adjacent green bars, `[10,14)` and `[14,20)`, sitting shoulder to shoulder with a visible seam. Then they fuse into one bar `[10,20)` with a satisfying snap.]**
>
> And now the second idea — the one that separates a working solution from a clean one. We don't just keep the intervals **disjoint**. We keep them **non-touching**. If `[10,14)` and `[14,20)` ever end up side by side, we fuse them into `[10,20)` immediately.
>
> **LEARNER:** Why bother? They're already disjoint — nothing overlaps. Isn't the seam harmless?
>
> **TEACHER:** It's harmless for *storage*. It's poison for *queries*. If I allow that seam, `queryRange(10, 20)` has to walk a **chain** — check `[10,14)`, see it stops short, hop to the next, check it starts exactly at 14, continue… That's a loop, and loops mean bugs and worst-case `O(n)`. But if touching intervals are always fused, coverage of a span can **only** come from **one single interval** — because if it took two, there'd be a gap between them, and a gap means not covered. Find one interval, check one number. Done.
>
> **[VISUAL: side by side. Left: "touching allowed" → a chain of hops, marked `O(n)` in red. Right: "always fused" → one bar, one arrow, marked `O(log n)` in green.]**
>
> That's a design principle worth stealing for your whole career: **normalize on write, so reads are trivial.** Do the messy merging work when you're already modifying the structure. Never make the reader clean up after you.

---

## 6. THE KEY MOVE (signaling) — `5:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line, centre screen: "Keep disjoint, NON-TOUCHING intervals sorted by start → binary-search the affected slice → splice."]**

> Burn this in: **keep the covered set as disjoint, non-touching intervals sorted by start. Every operation is: binary-search the affected slice, then splice a tiny replacement in.**
> `addRange` — find every interval that touches or overlaps you, collapse them all into one, splice it in.
> `removeRange` — find every interval that *strictly* overlaps you, keep the surviving left fragment and right fragment, delete the middle.
> `queryRange` — find the one interval that could contain you, check if it reaches far enough.
>
> Three operations. One structure. One move.

---

## 7. CODE IT — LIVE & CHUNKED — `6:10`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> I'll keep two parallel sorted lists — all the starts, all the ends. Sounds odd for about ten seconds, then you'll see why: it lets me binary-search *starts* and *ends* independently, with plain `bisect`, no tricks.

```python
import bisect

class RangeModule:
    def __init__(self):
        self.starts = []      # sorted starts of disjoint [start, end) intervals
        self.ends = []        # ends[k] pairs with starts[k];  ends[k] < starts[k+1]
```

> **[VISUAL: highlight the comment `ends[k] < starts[k+1]` and put a badge on it: "THE INVARIANT".]** That comment is the invariant. Strictly less-than. Non-touching. Everything below exists to preserve it.
>
> **[VISUAL: add chunk 2.]** `addRange`. Step one: find the slice of intervals that touch or overlap me.

```python
    def addRange(self, left, right):
        i = bisect.bisect_left(self.ends, left)      # first interval with end  >= left
        j = bisect.bisect_right(self.starts, right)  # first interval with start >  right
```

> **[VISUAL: add chunk 3.]** Everything in `[i, j)` gets swallowed. So stretch my bounds to cover the whole group.

```python
        if i < j:
            left = min(left, self.starts[i])         # leftmost start in the group
            right = max(right, self.ends[j - 1])     # rightmost end in the group
```

> **[VISUAL: add chunk 4, highlight the two splice lines.]** And now the magic trick — one splice replaces the entire group with a single merged interval.

```python
        self.starts[i:j] = [left]
        self.ends[i:j] = [right]
```

> Note what happens when `i == j`: the slice is empty, so this is a plain **insert** at position `i`. Merge and insert are the same two lines — no special case.
>
> **[VISUAL: add chunk 5 — `queryRange`, on a clean panel.]** Now the query. Remember, only one interval can possibly cover me.

```python
    def queryRange(self, left, right):
        k = bisect.bisect_right(self.starts, left) - 1   # last interval starting at/before left
        return k >= 0 and self.ends[k] >= right          # does it reach far enough?
```

> Two lines. That's what the non-touching invariant bought us.
>
> **[VISUAL: add chunk 6 — `removeRange`, building line by line.]** And remove — the mirror image. Same two searches, then instead of one merged interval we splice in the **survivors**: a head fragment and a tail fragment, if they exist.

```python
    def removeRange(self, left, right):
        i = bisect.bisect_right(self.ends, left)     # first interval with end  >  left
        j = bisect.bisect_left(self.starts, right)   # first interval with start >= right

        new_s, new_e = [], []
        if i < j:
            if self.starts[i] < left:                       # left fragment survives
                new_s.append(self.starts[i]); new_e.append(left)
            if self.ends[j - 1] > right:                    # right fragment survives
                new_s.append(right); new_e.append(self.ends[j - 1])

        self.starts[i:j] = new_s
        self.ends[i:j] = new_e
```

> Same splice. Different payload. That's the whole class — about twenty lines.

---

## 8. EXPLAIN THE CODE (the WHY) — `9:00`
*(elaboration — why each line exists)*

**[VISUAL: `addRange` and `removeRange` side by side, with their four bisect calls circled and colour-matched.]**

> Now the part that actually gets you hired. Look at these four searches together.
>
> In **`addRange`** I used `bisect_left` on ends and `bisect_right` on starts.
> In **`removeRange`** I used `bisect_right` on ends and `bisect_left` on starts.
>
> They're swapped. That is not a typo, and it is not luck.
>
> **LEARNER:** That's exactly what I was going to flag. Why would adding and removing need *different* binary searches? Same intervals, same math.
>
> **TEACHER:** Because "touching" means opposite things to them.
>
> When I **add** `[14, 20)` and `[10, 14)` is already sitting there — they touch, and I *want* to absorb it, because fusing keeps my invariant. So the search must be **inclusive**: `bisect_left(ends, 14)` finds an interval whose end is `>= 14` — it catches the toucher.
>
> When I **remove** `[14, 20)` and `[10, 14)` is sitting there — they touch, but share **zero numbers**; `[10,14)` doesn't contain 14. So removing must **not** disturb it. The search must be **strict**: `bisect_right(ends, 14)` only finds ends `> 14` — it skips the toucher entirely.
>
> **[VISUAL: two panels. Top — "ADD: touching → absorb it" with two bars fusing. Bottom — "REMOVE: touching → leave it alone" with one bar untouched and the other erased.]**
>
> That's the half-open convention doing its job, and it's why I keep hammering on `[left, right)`. In a **closed** world — `[10, 14]` including 14 — every one of those comparisons flips and you'd hand-reason `+1` and `−1` on every boundary. Half-open makes touching mean exactly one thing: `a.end == b.start`. Length is just `right − left`. Splitting `[a, c)` at `b` gives `[a, b)` and `[b, c)` — the boundary written once, not twice.
>
> **[VISUAL: a boxed line — "Half-open [left, right): length = right − left. Touching = end == start. No ±1 anywhere."]**
>
> Adopt it everywhere, even when the problem hands you closed intervals — convert on the way in.
>
> One more line worth defending: in `queryRange`, `bisect_right(self.starts, left) - 1`. Why `bisect_right`? Because if an interval starts **exactly** at `left`, I want it — it's my best candidate. `bisect_right` lands just past it, so minus one hits it. `bisect_left` would land one short and check the wrong interval.

---

## 9. DRY-RUN THE CODE — `10:45`
*(worked example — prove it, close the loop — pause #2)*

**[VISUAL: the four original calls back on screen, with the two question marks still blank. An empty trace table below.]**

> Back to our tiny example — and before I run it, **pause and predict**.
>
> **[VISUAL: the structure shown as `starts = [10], ends = [20]`. The call `removeRange(14, 16)` highlighted. A 5-second "🤔 your turn" timer.]**
>
> We're about to remove `[14, 16)` from `[10, 20)`. **What should `starts` and `ends` look like afterwards — and how many intervals will there be?** Say it out loud. Pause.
>
> *(pause)* — here's the real trace.

| Call | Intervals before | `i`, `j` | What the code does | Intervals after |
|---|---|---|---|---|
| `addRange(10,20)` | `[]` | `i=0, j=0` | `i == j` → nothing to merge, pure insert | `[(10,20)]` |
| `removeRange(14,16)` | `[(10,20)]` | `i=0, j=1` | `starts[0]=10 < 14` → keep `(10,14)`; `ends[0]=20 > 16` → keep `(16,20)` | `[(10,14),(16,20)]` |
| `queryRange(10,14)` | `[(10,14),(16,20)]` | `k=0` | `ends[0] = 14 >= 14` ✓ | **true** |
| `queryRange(13,15)` | `[(10,14),(16,20)]` | `k=0` | `ends[0] = 14 >= 15`? **no** | **false** |
| `queryRange(16,17)` | `[(10,14),(16,20)]` | `k=1` | `ends[1] = 20 >= 17` ✓ | **true** |

> True, false, true — exactly the answers we worked out by hand at minute two. Loop closed.
>
> **[VISUAL: new table slides in — the merge stress test. Bars on a timeline fusing as each row lands.]** Now the case that proves the merging really works. Watch the last row especially.

| Call | Before | `i`, `j` | Merged bounds | After |
|---|---|---|---|---|
| `addRange(10,14)` | `[]` | `0, 0` | — | `[(10,14)]` |
| `addRange(16,20)` | `[(10,14)]` | `1, 1` | — | `[(10,14),(16,20)]` |
| `addRange(12,17)` | `[(10,14),(16,20)]` | `0, 2` | `min(12,10)=10`, `max(17,20)=20` | `[(10,20)]` |
| `addRange(25,30)` | `[(10,20)]` | `1, 1` | — | `[(10,20),(25,30)]` |
| `addRange(20,25)` | `[(10,20),(25,30)]` | `0, 2` | `min(20,10)=10`, `max(25,30)=30` | `[(10,30)]` |

> That final row is my favourite thing in this problem. `[20, 25)` shares **not a single number** with either neighbour — it only *touches* them, on both sides. And it correctly fuses three intervals into one clean `[10, 30)`. Two bisect calls with the right strictness, and the whole structure heals itself.

---

## 10. COMPLEXITY, OUT LOUD — `12:15`
*(transfer to interview)*

**[VISUAL: the comparison table — brute force row in red, ours in green.]**

> Say it the way you'd say it in the room. *"Brute force is O of the coordinate range — a billion — in both time and space. Mine is O(log n) for a query and O(log n) plus an O(n) list splice for add and remove, where n is the number of stored intervals, capped at ten thousand by the call count."*
>
> Then the honest footnote, because interviewers love this bit: **that `O(n)` splice is real, and here's why it doesn't bite.** A merge that swallows `m` intervals **destroys** `m` and creates one — long merges make the structure *smaller*. Each interval is born once and merged away once, so total merge work across the run amortizes to `O(total calls)`. And if they push: *"in Java I'd use a `TreeMap` with `floorKey` and `subMap().clear()` — genuinely `O(log n)` amortized, no array shift."* Know that before they ask.

---

## 11. CAN WE USE LESS MEMORY? (space) — `12:55`
*(depth + honesty)*

**[VISUAL: two bars. Left: "O(10^9)" — enormous, red, running off-screen. Right: "O(n) ≤ 10^4" — a tiny green sliver.]**

> This beat is usually "can we shave the space?" Here the answer is different, and better. **The space optimization *is* the solution.** We didn't compress a big structure — we changed *what we store*, from points to boundaries, and the coordinate range fell out of the complexity **entirely**. Ten to the ninth appears nowhere in our cost.
>
> Can we go below `O(n)`? **No, and I can prove it in one sentence.** Two separated covered intervals are distinguishable — some future `queryRange` returns a different answer depending on whether I remembered both. Every stored interval is load-bearing. `O(n)` is the floor.
>
> Say it in the room: *"My space is O(n) in the number of intervals, not O of the coordinate range — that decoupling is the actual solution, and O(n) is provably the floor because every interval is independently observable by a future query."*

---

## 12. YOUR TURN (active recall) — `13:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Count Integers in Intervals (LC 2276)". A blank editor.]**

> Before the next video, go do **Count Integers in Intervals**, LeetCode 2276. It's `addRange` with one extra requirement: also report **how many integers are covered in total**, at any moment.
>
> The structure is the one you just built. The twist is maintaining a running sum through the merges — when you swallow a group, you have to subtract what you destroyed before you add what you created. Don't peek. Ten minutes wrestling with that sum beats an hour watching me do it.

---

## 13. LOCK IT IN — `14:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets appear one at a time, then one big boxed line.]**

> Three things to keep:
> 1. **When the coordinate range dwarfs the operation count, index the operations, not the values.** A billion positions, ten thousand calls → store at most ten thousand intervals.
> 2. **Normalize on write so reads are trivial.** Keeping intervals non-touching is what makes `queryRange` a single binary search instead of a chain walk.
> 3. **Half-open `[left, right)` is the off-by-one killer.** Length is `right − left`, touching is `end == start`, and `bisect_left` versus `bisect_right` is exactly the switch between "absorb the toucher" and "leave it alone."
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "Don't paint the line. Store the stripes."]**
>
> When you see "huge range, few operations, mark and query spans," your hand should already be reaching for a sorted list of disjoint intervals — `TreeMap` in Java, `bisect` in Python.
>
> *(GCA reminder — for the interview itself: open by asking "half-open?", state the boolean-array baseline and kill it with the actual numbers — eight gigabytes, ten to the thirteenth operations — then derive the interval structure from the ten-thousand-call bound. Google's General Cognitive Ability signal isn't the splice; it's you noticing the 10^9-versus-10^4 mismatch and letting it dictate the design.)*

---

## 14. CLIFFHANGER — `14:40`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Amount of New Area Painted Each Day." A timeline where a new bar drops on top of existing ones, and only the *previously uncovered* slivers light up gold, with a counter reading "new area: 3".]**

> We answered "is it covered?" But here's the question that breaks everything we just built: **"how much of this range was *newly* covered — the part that wasn't already painted?"**
>
> Our `addRange` merges and moves on; it never counts what it actually changed. And the naive fix — diff the total before and after — starts looking suspiciously like `O(n)` per call all over again. There's a way to get the answer *while* you merge, almost for free. That's the next problem, and it's a real Google favourite. See you there.
