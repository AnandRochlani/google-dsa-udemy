# 🎬 Recording Script — Stock Price Fluctuation

**Pattern: Design / stale-entry handling (timestamp map + ordered multiset) · LeetCode 2034 · Medium · Target length ~11–12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Logger Rate Limiter — a map keyed by identity holding one truth per key. Today, one map isn't enough.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a live stock ticker chart climbing. A tick prints at $10 and a "SESSION HIGH: $10" badge lights up. Then a red "CORRECTION" banner slides in: "t=1 was actually $3". The chart redraws — but the badge still stubbornly says $10.]**

> A price feed at a trading firm. A tick comes in: ten dollars. Your dashboard proudly shows "session high: 10." Then the exchange sends a **correction** — that tick was a glitch, the real price at that moment was *three*.
>
> Every clean solution you know — a running max variable, a max-heap — keeps showing **10**. A maximum that never actually happened. Google asks this one because the fix isn't a bigger data structure — it's knowing what to do with entries that become *lies*. There are exactly two ways to handle a stale entry, and by the end you'll know both by name. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top: "Build a StockPrice class: update / current / maximum / minimum — where update can CORRECT the past." Below, the tiny call sequence appears line by line.]**

```
update(1, 10)
update(2, 5)
current()  -> 5
maximum()  -> 10
update(1, 3)    ← correction!
maximum()  -> ?
update(4, 2)
minimum()  -> 2
```

> One line: **records `(timestamp, price)` stream in — possibly out of order, and a repeated timestamp means the old record was wrong. Answer `current`, `maximum`, and `minimum` at any moment.**
>
> Here's our tiny example — eight calls, and we'll live inside it for the whole video. Notice `maximum()` returns 10 while `current()` is 5 — the max lives in the *past*, at timestamp 1. Then `update(1, 3)` lands: timestamp 1 was never really 10.
>
> So — that second `maximum()`. What should it say? Hold that question. It's the entire problem.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: a dict `rec = {timestamp: price}` builds up. Each `maximum()` call fires a scan arrow that sweeps across ALL values; a "values scanned" counter ticks.]**

> First instinct — and it's a good one: a dictionary, `rec`, timestamp to price. An update just writes the key. A *repeated* timestamp **overwrites** the key — corrections handled for free, because a dict has one truth per key. Keep a `latest` timestamp variable, and `current` is one lookup.
>
> `maximum` and `minimum`? Just scan every value.
>
> `update(1,10)`, `update(2,5)` — rec is `{1:10, 2:5}`. `maximum()` — scan both, answer 10. `update(1,3)` — overwrite, rec is `{1:3, 2:5}`. `maximum()` — scan again, answer **5**. Correct! The correction just… worked.
>
> **[VISUAL: the counter keeps climbing; the dict stretches to "100,000 entries…" and the scan arrow crawls.]**
>
> But now scale it. Up to a hundred thousand calls, so up to a hundred thousand live records — and *every* `maximum()` re-scans all of them. That's ten to the tenth operations in the worst case. Time Limit Exceeded, and almost all of it re-checking prices that didn't change since the last scan.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the long scan arrow. A "max_so_far = 10" sticky note appears as the tempting patch. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste is obvious — re-scanning unchanged values. So here's the patch everyone reaches for.
>
> **LEARNER:** Right — just keep a running `max_so_far`. Update it on every `update`. That's O(1), problem solved… isn't it?
>
> **TEACHER:** Watch it die. `max_so_far` is 10. Now `update(1, 3)` arrives and *retracts* the 10 — the very value your variable is holding. What's the new max? The runner-up… which your single variable never kept. Same failure for a plain max-heap: the 10 is still sitting on top, now a lie.
>
> Pause the video. Between two updates, how much does the *set of live prices* actually change? Count the changes — and ask what structure could apply exactly those changes and still hand you max and min.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:30`
*(elaboration + analogy — derive it)*

**[VISUAL: split screen. Left: `rec` the dict. Right: a sorted shelf of price cards `prices = [5, 10]`. The correction pulls the "10" card OFF the shelf and slots a "3" card in — two moves, everything else untouched.]**

> **TEACHER:** Here's what the dry-run showed us: one update changes the live prices by exactly **one removal plus one insertion**. Correction at timestamp 1? The stale 10 leaves, the new 3 enters. Every other price is untouched.
>
> So keep the prices on a **sorted shelf** — an *ordered multiset*. Insert a card in log time, remove a card in log time, and max and min are just the two **ends** of the shelf. No scanning, ever.
>
> And the removal is the beautiful part: which card is stale? The dict already knows! `rec[timestamp]` *is* the old price being retracted. The map is the truth; the shelf is the truth *kept sorted*.
>
> **[VISUAL: analogy card — a librarian's shelf, books ordered by height. Swapping one book = pull one, slot one. Tallest and shortest always at the ends.]**
>
> **LEARNER:** Wait — a *multiset*? Why not a plain sorted set?
>
> **TEACHER:** Because two different timestamps can hold the **same price**. If timestamps 3 and 7 are both at $5 and timestamp 3 gets corrected, only *one* copy of 5 must leave the shelf — timestamp 7's five is still real. A set would nuke both. The multiset counts copies, and that's exactly the semantics corrections need.

---

## 6. THE KEY MOVE (signaling) — `4:50`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Map = the truth. Multiset = the truth, sorted. On correction: remove the OLD truth, insert the new."]**

> The key move: **keep the truth in a map, mirror it in an ordered multiset, and on every correction remove the old truth before inserting the new one.** The map tells the multiset exactly which entry went stale — eager deletion, the moment the lie is exposed.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Chunk 1 typed live.]**

> Three fields. The truth map, the sorted shelf, and the newest timestamp.

```python
from sortedcontainers import SortedList

class StockPrice:
    def __init__(self):
        self.rec = {}                 # timestamp -> latest (corrected) price
        self.prices = SortedList()    # multiset of all LIVE prices
        self.latest = 0               # newest timestamp seen
```

> **[VISUAL: add chunk 2, highlight the `if` line.]** Now `update` — and the first two lines are the entire lesson. Seen this timestamp before? Then the shelf is holding a stale price. Evict it *before* anything else.

```python
    def update(self, timestamp: int, price: int) -> None:
        if timestamp in self.rec:
            self.prices.remove(self.rec[timestamp])   # retract the stale price
        self.rec[timestamp] = price
        self.prices.add(price)
        self.latest = max(self.latest, timestamp)
```

> **[VISUAL: add chunk 3 — the three getters land together.]** And the queries barely exist — that's the sign the design is right. The work all happened in `update`.

```python
    def current(self) -> int:
        return self.rec[self.latest]

    def maximum(self) -> int:
        return self.prices[-1]        # largest live price

    def minimum(self) -> int:
        return self.prices[0]         # smallest live price
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: full class on screen; spotlight each line as it's named.]**

> The why, line by line.
>
> `self.prices.remove(self.rec[timestamp])` — remove by *value*, and the value comes from the map. Delete this line and every correction leaves a ghost price on the shelf; `maximum()` reports highs that never happened — our cold-open bug, in one missing line. And `remove` on a multiset takes out exactly **one copy**, so a duplicate price at another timestamp survives, just like it should.
>
> `self.latest = max(self.latest, timestamp)` — records can arrive **out of order**. A correction to old timestamp 1 must *not* make `current()` look at timestamp 1. Taking the max means only genuinely-newer timestamps move the needle.
>
> **LEARNER:** One thing bugs me — `update` might be called with a timestamp we've never seen, so there's nothing to remove. Doesn't the remove crash?
>
> **TEACHER:** That's what the `if timestamp in self.rec` guard is for — brand-new timestamp, skip the eviction, just insert. The two cases share every other line: write the map, add to the shelf, bump `latest`. One guard, no duplicated logic.
>
> And `SortedList`? Think of it as Python's balanced-BST multiset — `add` and `remove` in log n, and reading either end is instant. In Java the same role is played by a `TreeMap` of price to count — that version's in the appendix.

---

## 9. DRY-RUN THE CODE — `8:10`
*(worked example — prove it, close the loop)*

**[VISUAL: trace table filling row by row; `prices` drawn as the sorted shelf, cards entering and leaving on the correction row, which pulses red.]**

| Call | `rec` after | `prices` after | `latest` | returns |
|---|---|---|---|---|
| update(1,10) | {1:10} | [10] | 1 | — |
| update(2,5) | {1:10, 2:5} | [5, 10] | 2 | — |
| current() | — | — | 2 | rec[2] = **5** ✅ |
| maximum() | — | — | — | prices[-1] = **10** ✅ |
| update(1,3) | {1:3, 2:5} | remove 10, add 3 → [3, 5] | 2 (1 < 2) | — |
| maximum() | — | — | — | prices[-1] = **5** ✅ |
| update(4,2) | {1:3, 2:5, 4:2} | [2, 3, 5] | 4 | — |
| minimum() | — | — | — | prices[0] = **2** ✅ |

> There's the answer to our beat-two question: after the correction, `maximum()` says **5**. Watch that fifth row — `rec[1]` told us the stale value was 10, we pulled exactly that card, slotted the 3, and the phantom high died on the spot. And `latest` stayed at 2, because 1 is old news — so `current()` keeps pointing at the right record. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:10`
*(transfer to interview)*

**[VISUAL: table — Brute: max/min O(n). Ours: update O(log n), current/max/min O(1). n = distinct timestamps.]**

> Say it the way you'd say it in the room: *"Update is O(log n) — one multiset removal, one insertion. Current, maximum, and minimum are O(1) — a map lookup or reading an end of the sorted structure. Space is O(n) over distinct timestamps: one map entry and one multiset entry each. The brute force paid O(n) per max query; we moved the work into update, where the change is tiny."*
>
> Paying a little on every write to make every read instant — that trade is half of system design, and saying it in those words is worth real points.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:45`
*(depth + honesty — and the rival approach)*

**[VISUAL: "can we forget old timestamps?" → a correction arrow reaches BACK to the current max and deletes it; the runner-up steps up. Then a side-by-side: "eager multiset: n entries" vs "lazy heaps: one entry per update".]**

> Can we shrink O(n)? **No — and here's the proof.** A future correction can dethrone the current maximum, making the runner-up the answer. Then the runner-up can fall too. *Any* timestamp's price might someday be the max — so all of them must stay queryable. O(n) isn't our choice; it's the problem's floor.
>
> But there IS a rival worth naming: **lazy deletion**. Two heaps of `(price, timestamp)` pairs; `update` just pushes — never deletes. At query time, while the heap's top disagrees with `rec` — a stale entry from before a correction — pop it and keep going. Same amortized log-time bounds, no third-party library… but the heaps hold one entry per *update call* instead of per timestamp, and every query starts by asking the top, "are you a lie?"
>
> *"Eager deletion in an ordered multiset, or lazy deletion with heaps"* — offer both, pick the multiset for cleanliness. Knowing the trade-off by name is the senior signal.

---

## 12. YOUR TURN (active recall) — `10:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Max Stack (LC 716)". A blank editor.]**

> Before the next video, try **Max Stack** — a stack that also pops its maximum, from the middle if it has to. It's the purest lazy-deletion problem there is: two structures pointing at shared entries, and removed elements linger as ghosts until a query sweeps them out. Everything from today's beat eleven, promoted to the main event.
>
> Ten minutes, no peeking. The struggle is the point.

---

## 13. LOCK IT IN — `11:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three takeaways:
> 1. **Corrections kill running variables and plain heaps** — nobody kept the runner-up.
> 2. **Map = truth, ordered multiset = truth sorted** — the map names the stale value so the multiset can evict it in log time.
> 3. **Stale entries, two idioms:** evict **eagerly** in a multiset, or push always and purge **lazily** at the heap top. Same bounds; the multiset holds less.
>
> The memory peg:
>
> **[VISUAL: big box → "When the past can change, every cached answer needs an eviction plan."]**
>
> When a design problem lets updates rewrite history, your first question should be: *which of my stored entries just became a lie — and when do I throw it out?*
>
> *(GCA reminder — for the interview itself: narrating the route is half of Google's rubric. Start with the dict-and-scan brute force, kill `max_so_far` out loud with the correction case, then reach for the multiset — and open with the clarifying questions: "can the same timestamp be corrected more than once?", "can records arrive out of order?" Both yes, and both shaped the design. Asking them is the General Cognitive Ability signal.)*

---

## 14. CLIFFHANGER — `11:35`
*(open loop to next lesson)*

**[VISUAL: a microwave keypad blurred in, digits glowing: "Minimum Cost to Set Cooking Time". A finger hovers over the pads.]**

> Today the cleverness lived in the data structure. Next time there's **no data structure at all** — just a microwave. You want it to run for a given number of seconds, every keypress costs something, and "90 seconds" can be typed as 1-3-0 *or* 9-0. The trap is inverted: people hunt for a clever formula, when the winning move is to **enumerate every sensible way to punch it in** and keep the cheapest — brute force, done with discipline, *is* the optimal solution. Knowing when clever is the wrong tool… that's the next lesson. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class StockPrice {
    private final Map<Integer, Integer> rec = new HashMap<>();        // timestamp -> latest price
    private final TreeMap<Integer, Integer> prices = new TreeMap<>(); // price -> count (multiset)
    private int latest = 0;

    public void update(int timestamp, int price) {
        Integer stale = rec.put(timestamp, price);      // returns old price if correction
        if (stale != null) {                            // retract exactly one copy
            int c = prices.get(stale);
            if (c == 1) prices.remove(stale);
            else prices.put(stale, c - 1);
        }
        prices.merge(price, 1, Integer::sum);           // insert the new truth
        latest = Math.max(latest, timestamp);
    }

    public int current() { return rec.get(latest); }
    public int maximum() { return prices.lastKey(); }
    public int minimum() { return prices.firstKey(); }
}
```
