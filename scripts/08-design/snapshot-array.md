# 🎬 Recording Script — Snapshot Array

**Pattern: Design (per-index version history + binary search) · LeetCode 1146 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** binary search on a sorted list (Section 2) + one-value-per-key maps from Logger Rate Limiter — now the value is a whole *timeline*.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a memory-usage bar filling as an array of 50,000 cells gets photocopied over and over — copy #1, #2, #3… bar goes red, a "Memory Limit Exceeded" banner slams in.]**

> Google onsite. The interviewer says: *"Design an array that remembers its past. I can snapshot it, keep changing it, and later ask — what was slot 7 back at snapshot 3?"*
>
> Your brain goes straight to the obvious thing: every snapshot, copy the array. And that answer doesn't just get slow — with fifty thousand slots and fifty thousand snapshots, it's **two and a half billion** stored numbers. Memory dies before time does.
>
> The real solution copies **nothing**. Snap becomes a single `+= 1`. By the end of this video you'll see the storage flip that makes that possible — and it's the same trick real databases use to time-travel. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below it, a tiny 3-slot array [0, 0, 0] and the four operations listed as cards: SnapshotArray(length), set, snap, get.]**

> One line: **build an array where `snap()` freezes the current state and returns an id, and `get(index, snap_id)` reads a slot *as it was* at that snapshot.**
>
> Four operations. The constructor makes `length` slots, all zero. `set` writes to the live array. `snap` freezes a version and hands back its id — first snap is id 0, next is 1, and so on. `get` reads from the past.
>
> Here's our tiny example — three slots, and watch slot 0 closely:

**[VISUAL: the call sequence appears line by line:]**

```
SnapshotArray(3)      → array is [0, 0, 0]
set(0, 5)             → live array [5, 0, 0]
snap()        → 0     → snapshot 0 frozen
set(0, 6)             → live array [6, 0, 0]
get(0, 0)     → ?     → slot 0... at snapshot 0
```

> That last call is the whole game. The live value is 6 — but snapshot 0 was taken when it was 5. `get(0, 0)` must return **5**. The past has to stay frozen while the present keeps moving.
>
> Before you'd write a line of this in the room, one clarifying question is worth asking out loud: *"Does `snap()` return the id before or after incrementing — first snapshot is id 0, yes?"* Hold onto that instinct — we'll come back to why it matters.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:30`
*(worked example — let them feel the waste)*

**[VISUAL: the live array [5,0,0] on top. Each snap() stamps a full photocopy of it into a growing stack of versions below. A "cells stored" counter top-right.]**

> Let's do the literal thing first. "Take a snapshot" — fine, photocopy the array. Keep a list of versions. `get(index, snap_id)` is then just `versions[snap_id][index]`. Two lookups. Beautiful.
>
> Run our example. `set(0, 5)` — live array becomes `[5, 0, 0]`. `snap()` — photocopy all three cells, stash it as version 0, return 0.
>
> **[VISUAL: a copy of [5,0,0] drops into the stack; counter ticks +3.]**
>
> `set(0, 6)` — live array `[6, 0, 0]`. Another `snap()` — copy all three again.
>
> **[VISUAL: [6,0,0] drops in; counter +3. Then fast-forward: the array grows to 50,000 cells, snaps fire, copies pile up, the counter spins toward 2,500,000,000 in red.]**
>
> Now look at what we copied. Between those two snapshots, **one** cell changed. We stored three. At fifty thousand slots, one `set` between snaps means we re-store 49,999 values that are *identical to the previous copy*. Scale both length and snap count to their limit of fifty thousand and you're at two and a half billion stored integers. That's the killer: `snap()` is O(length) — every single time.

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on two stacked copies [5,0,0] and [6,0,0]; the two identical zero-columns gray out, only the 5→6 cell glows. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Look at the two copies side by side. Almost everything is duplicate. The only *actual information* in snapshot 1 is: "slot 0 became 6." Everything else is dead weight.
>
> **LEARNER:** Okay, so store diffs — only what changed since the last snap. But then reading gets ugly, right? To answer `get(2, 40)` I might have to walk back through forty diffs looking for the last time slot 2 changed.
>
> **TEACHER:** *That* is the exact tension — cheap writes versus cheap reads — and there's a way to get both. Pause the video. Hint: stop organizing storage by *snapshot*. What else could own the history?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:30`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the stack of array-copies rotates 90° and collapses into three horizontal timelines — one per index. Each timeline holds little (snap_id, value) tags.]**

> **TEACHER:** Flip the table. Instead of *"for each snapshot, the whole array,"* store *"for each index, the history of its changes."* Every index gets its own little diary: a list of `(snap_id, value)` records, and we append one **only when `set` actually touches that index**.
>
> Think of your bank statement. The bank doesn't photocopy every account in the vault at midnight. It records **transactions** — and your balance on March 3rd is just the last transaction at or before March 3rd.
>
> **[VISUAL: bank-statement analogy card: a ledger of dated entries, a finger scanning up from March 3rd to the latest entry at-or-before it.]**
>
> Now watch what each operation costs. `set(index, val)` — append one tag to one diary. `snap()` — nothing changed, nothing to copy: just return the current counter and tick it up. **Snap is O(1). The counter *is* the snapshot.**
>
> And `get(index, snap_id)`? Read that index's diary and find the **latest entry whose snap_id is ≤ the one you asked for**. If slot 0's diary says `(0, 5)` then `(1, 6)`, the value at snapshot 0 is 5 — the last entry at or before 0.
>
> **LEARNER:** Wait — the diary could be long. Isn't that the same walk-back problem I was worried about?
>
> **TEACHER:** Here's the gift: we only ever append at the *current* snap_id, and the counter never goes backwards. So every diary is **already sorted by snap_id** — no sorting step, it's sorted by construction. And "latest entry ≤ target in a sorted list" — you've done that move before. That's a **binary search**. Log time, not a walk.
>
> One more piece of polish: seed every diary with `(0, 0)` at construction. Every slot starts at zero, so that record is *true* — and it means every diary always has at least one entry at or before any legal snap_id. No empty-history edge case, ever.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Store deltas per index, not copies per snapshot. snap = counter++. get = binary search for latest snap_id ≤ query."]**

> Burn this in: **don't store the array per snapshot — store, per index, its sorted `(snap_id, value)` history. Snap just bumps a counter; get binary-searches for the newest record at or before the queried id.**
>
> That's a reusable pattern, not a one-off: any time an interviewer says *"value of X as of time T"* — versioned reads — your reflex is per-key sorted history plus binary search. Same skeleton as a time-based key-value store, same idea databases call MVCC.

---

## 7. CODE IT — LIVE & CHUNKED — `5:35`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Build it in pieces. Constructor first: one counter, one seeded diary per index.

```python
import bisect

class SnapshotArray:
    def __init__(self, length: int):
        self.snap_id = 0
        # one history per index; seed (0, 0) so every index
        # has a defined value at snapshot 0 — no edge cases.
        self.history = [[(0, 0)] for _ in range(length)]
```

> **[VISUAL: add chunk 2, highlight the if/else.]** Now `set`. One subtlety: if we've *already* written this index at the current snap_id, overwrite that record instead of appending a second one.

```python
    def set(self, index: int, val: int) -> None:
        records = self.history[index]
        if records[-1][0] == self.snap_id:
            # already wrote at this snap_id → overwrite, don't duplicate
            records[-1] = (self.snap_id, val)
        else:
            records.append((self.snap_id, val))
```

> **[VISUAL: add chunk 3 — two lines, spotlight how small it is.]** And here's the payoff line of the whole design — `snap`, in its entirety.

```python
    def snap(self) -> int:
        self.snap_id += 1            # no copying — just bump the counter
        return self.snap_id - 1      # return the id we just froze
```

> No loop. No copy. The fifty-thousand-cell photocopier from the cold open is now a plus-equals-one.
>
> **[VISUAL: add chunk 4, highlight the bisect line.]** Last piece — `get`. Binary-search the diary for the latest record at or before `snap_id`.

```python
    def get(self, index: int, snap_id: int) -> int:
        records = self.history[index]
        # last record with its snap_id <= the queried snap_id:
        # bisect_right lands just past it; step back one.
        i = bisect.bisect_right(records, (snap_id, float('inf'))) - 1
        return records[i][1]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:10`
*(elaboration — why each line exists)*

**[VISUAL: the full class; spotlight each region as it's named.]**

> Now the *why* behind each choice.
>
> The `(0, 0)` seed — it makes `get` unconditional. Every diary has an entry with snap_id 0, and every legal query id is ≥ 0, so the binary search can never land at nothing. Delete the seed and you'd need a "no record found → return 0" branch on every read.
>
> The overwrite in `set` — if you call `set(0, 5)` then `set(0, 9)` before snapping, only the 9 exists as far as any snapshot can tell. Keeping both would waste memory *and* it's the final value that gets frozen. Overwriting keeps at most one record per index per snapshot. It also protects the sort: append-only-at-a-new-id plus overwrite-at-the-same-id means snap_ids in each diary are strictly increasing.
>
> `snap` returning `self.snap_id - 1` — that's the clarifying question from minute one, resolved in code. Bump first, return the *old* value: first call returns 0, exactly as the spec demands. Get this backwards and every single `get` is off by one.
>
> **LEARNER:** The `bisect_right` line bugs me. Why search for `(snap_id, float('inf'))` — where does infinity come from?
>
> **TEACHER:** Because the records are tuples, and tuples compare element by element. I want the insertion point *after* any record whose id equals `snap_id`. Searching for `(snap_id, inf)` says: "pretend I'm looking for a record at this exact snap_id with an impossibly large value" — so it sorts after `(snap_id, anything_real)` but before `(snap_id + 1, anything)`. `bisect_right` then lands one past the record I want, and minus one steps back onto it. Search for plain `(snap_id,)` tricks or use `bisect_left` carelessly and you can land *on* the matching record instead of after it — and return the value from one snapshot too early.
>
> **LEARNER:** One more thing feels off. `snap()` does *nothing* — it doesn't visit the indexes at all. So if I `set(2, 7)`, then snap five times, and ask `get(2, 4)`… no record in slot 2's diary says snap 4. How is that not a bug?
>
> **TEACHER:** That's the misconception to kill, and killing it is the moment this design clicks. **No record at snap 4 means the value didn't change — and unchanged is information.** Slot 2's diary says `(0, 7)` — after the overwrite of its seed — and the binary search for "latest id ≤ 4" finds exactly that record. Silence in the diary isn't missing data; it's the diary saying *"still 7."* That's precisely why we get to store deltas instead of copies.

---

## 9. DRY-RUN THE CODE — `8:40`
*(worked example — prove it, close the loop)*

**[VISUAL: trace table filling row by row; slot 0's diary shown evolving alongside.]**

> Run the exact code on our example and watch slot 0's diary.

| Call | `snap_id` | what the code does | `history[0]` after |
|---|---|---|---|
| `SnapshotArray(3)` | 0 | seed all three diaries | `[(0,0)]` |
| `set(0, 5)` | 0 | last id 0 == 0 → overwrite seed | `[(0,5)]` |
| `snap()` → **0** | 0→1 | bump counter, return old id | `[(0,5)]` |
| `set(0, 6)` | 1 | last id 0 ≠ 1 → append | `[(0,5), (1,6)]` |
| `get(0, 0)` | 1 | bisect for latest id ≤ 0 | reads `(0,5)` → **5** ✅ |

> The money call: `get(0, 0)`. `bisect_right([(0,5), (1,6)], (0, inf))` — `(0, inf)` sorts after `(0,5)` and before `(1,6)`, so it returns 1. Minus one is index 0: record `(0, 5)`. Answer **5** — the past stayed frozen even though the live value is 6. Loop from the top of the video: closed.
>
> Two bonus reads to prove the edges. `get(1, 0)` — slot 1 was never touched, its diary is just the seed `[(0,0)]`, search returns that: **0**, correct. And after one more `snap()` — which returns **1** — `get(0, 1)` searches for latest id ≤ 1, lands on `(1, 6)`: **6**. Past and present, both right.

---

## 10. COMPLEXITY, OUT LOUD — `9:40`
*(transfer to interview)*

**[VISUAL: comparison table — Brute: snap O(length), space O(length × snaps). Ours: set O(1), snap O(1), get O(log k), space O(length + writes).]**

> Say it the way you'd say it in the room: *"`set` is amortized O(1) — an append or an in-place overwrite. `snap` is O(1) — it's just a counter bump. `get` is O(log k), where k is the number of writes to that particular index, because I binary-search that one index's sorted history. Space is O(length plus total writes) — one seed per slot, one record per real set — instead of O(length times snaps) for full copies."*
>
> From two and a half billion cells down to one record per actual change. That's the flip.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:10`
*(depth + honesty)*

**[VISUAL: each stored record lights up with the query that can still read it — nothing is unreachable. A "shrink further?" bubble gets a measured ✗.]**

> Can we shrink it further? **Essentially no — and saying *why* scores points.** Every record we keep is a value some snapshot can still legally ask for; delete any of them and some `get` returns the wrong answer. The same-snapshot overwrite already collapses redundant writes. Nothing we store scales with length × snaps.
>
> Two honest micro-tweaks, not asymptotic wins: you could drop the per-index seeds and special-case "search found nothing → return 0" — saves `length` records, costs a branch on every read, basically a wash. And you could keep two parallel lists per index — `snap_ids[]` and `values[]` — so bisect runs on raw ints with no `(snap_id, inf)` tuple trick. Same big-O, slightly less overhead.
>
> Out loud: *"Space is O(total writes), not O(length × snaps), because I store per-index deltas instead of copies — and I can't do meaningfully better, since every record is still reachable by some snapshot."*

---

## 12. YOUR TURN (active recall) — `10:45`
*(retrieval practice)*

**[VISUAL: "Your turn → Time Based Key-Value Store (LC 981)". A blank editor.]**

> Before the next video, go build **Time Based Key-Value Store** — LeetCode 981. It's this problem wearing a different shirt: `set(key, value, timestamp)` and `get(key, timestamp)` returns the value at the largest timestamp at or below the query. Per-key sorted history, binary search for the floor — the exact skeleton you just learned, keyed by strings instead of indexes.
>
> Ten minutes, no peeking. If you can rebuild the bisect-for-the-floor move from memory, this pattern is yours.

---

## 13. LOCK IT IN — `11:15`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Copying the array per snap is O(length × snaps)** — almost all of it duplicate data. The information in a snapshot is only what changed.
> 2. **Flip the storage: per-index sorted `(snap_id, value)` history.** Snap becomes a counter bump; the seed `(0, 0)` kills the edge cases.
> 3. **Read = floor search: latest record with snap_id ≤ query** — `bisect_right(...) - 1` in Python, `floorEntry` in Java. And no record means *unchanged*, not missing.
>
> The memory peg:
>
> **[VISUAL: big box → "Don't photocopy the array — give every index a diary, and binary-search the diary."]**
>
> When you hear *"value of X as of time T,"* your hand should already be reaching for per-key history plus binary search.
>
> *(GCA reminder — for the interview itself: Google scores General Cognitive Ability, and half that rubric is your narration, not your final code. State the copy-everything brute force, point at the duplicate data out loud, ask the clarifying question — "snap returns the id before incrementing, so the first is 0?" — and *then* flip the storage. The examiner is grading the path, so make the path audible.)*

---

## 14. CLIFFHANGER — `12:00`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Detect Squares" — a scatter of points on a grid, three dots pulsing, a fourth corner drawn as a "?".]**

> Today our structure answered questions about *time* — what was this slot, back then. Next, the structure has to answer questions about *space*. You're fed a stream of points on a plane, and each query asks: with this point as one corner, **how many axis-aligned squares** can you complete from the points you've stored — duplicates counted?
>
> Same design-a-class setup, but now the whole game is choosing what to count as points arrive so the square query doesn't melt. What would *you* key the map on? That's Detect Squares. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class SnapshotArray {
    // one TreeMap per index: snap_id -> value, sorted by snap_id.
    // floorEntry(snapId) = latest write at or before snapId.
    private final TreeMap<Integer, Integer>[] history;
    private int snapId = 0;

    @SuppressWarnings("unchecked")
    public SnapshotArray(int length) {
        history = new TreeMap[length];
        for (int i = 0; i < length; i++) {
            history[i] = new TreeMap<>();
            history[i].put(0, 0);          // seed value 0 at snapshot 0
        }
    }

    public void set(int index, int val) {
        history[index].put(snapId, val);   // put() overwrites on an equal key —
                                           // the same-snapshot collapse for free
    }

    public int snap() {
        return snapId++;                   // return current id, then increment
    }

    public int get(int index, int snapId) {
        // greatest key <= snapId; never null thanks to the seed.
        return history[index].floorEntry(snapId).getValue();
    }
}
```

*(TreeMap does both subtleties natively: `put` overwrites same-snapshot writes, and `floorEntry` is the direct analog of `bisect_right - 1`. Operations are O(log k) per call on that index's map.)*
