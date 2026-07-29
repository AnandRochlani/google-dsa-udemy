# 🎬 Recording Script — Time-Based Key-Value Store
**Pattern: Hash Map + Binary Search · LeetCode 981 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** binary search on a sorted array — finding the rightmost element `≤` a target.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A class `TimeMap` with `set` and `get`. Inside `get`, a `for` loop scanning a list. A LeetCode "Time Limit Exceeded — 41/54" banner slides in red.]**

> Google gives you this one a lot: *"Build a key-value store, but with a time machine. Ask what a key's value was at any past moment."*
>
> You write the obvious version — keep every write in a list, loop through to find the right one. Passes the examples. You hit submit… Time Limit Exceeded.
>
> The idea wasn't wrong. It just does way more work than it needs to — and the fix is hiding in one sentence of the problem most people skim right past. By the end of this video, you'll spot that sentence and turn a slow scan into a binary search. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, two method signatures: `set(key, value, timestamp)` and `get(key, timestamp)`.]**

> The whole thing in one line: **store values stamped with a time, and get the value from at-or-before any moment you ask about.**
>
> Two methods. `set` files a value under a key with a timestamp. `get` asks: "for this key, what was the value at the largest timestamp that's *at or before* the time I'm giving you?" If nothing was set that early, you return an empty string.
>
> Keep your eye on one key — `"foo"` — we'll build up its timeline and query it by hand.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: key `"foo"` mapped to a growing list of stamped tiles. `set("foo","bar",1)` drops a tile `(1,"bar")`; `set("foo","bar2",4)` drops `(4,"bar2")`. A "steps" counter, top-right.]**

> Let's do what your brain does first. Map each key to a list of its writes.
>
> `set("foo","bar",1)` — list is now `[(1,"bar")]`. `set("foo","bar2",4)` — `[(1,"bar"),(4,"bar2")]`.
>
> Now `get("foo", 3)`. The obvious move: walk the list. Is timestamp 1 at-or-before 3? Yes — remember `"bar"`. Is timestamp 4 at-or-before 3? No — stop. Answer: `"bar"`.
>
> **[VISUAL: an arrow crawls tile by tile across the list, steps counter ticking 1, 2, 3…]**
>
> Fine for two tiles. But now imagine `"foo"` was set a hundred thousand times, and you query it a hundred thousand times. Every query walks the *entire* history from the start.
>
> **[VISUAL: the list stretches off-screen; the steps counter morphs into "≈ 10,000,000,000".]**
>
> Ten billion steps. There's your Time Limit Exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight the arrow re-walking the same sorted list from the left, over and over. A 4-second "🤔 your turn" timer appears.]**

> **TEACHER:** So where's the waste? Every `get` re-scans the whole list from the beginning — even though the list never changes shape between reads. We're doing linear work on something we read again and again.
>
> **LEARNER:** But it's just a list of writes in the order they came in. What is there to exploit? Don't we kind of *have* to look through them?
>
> **TEACHER:** That's the instinct to break — and the answer is sitting in the problem statement. Pause the video and reread the constraints. **What do you notice about the order the timestamps arrive in for a single key?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the constraint line highlighted: "timestamps for each key are strictly increasing." The `"foo"` tiles glow to show they're already in time order: `1 → 4`.]**

> **TEACHER:** Here's the sentence: **for each key, the timestamps arrive strictly increasing.** We `set` them in time order — so the list for `"foo"` is *already sorted by timestamp*. We didn't sort it. It just is.
>
> **LEARNER:** Okay… but so what? It being sorted doesn't change what I'm looking for.
>
> **TEACHER:** It changes *how fast* you can find it. Think of a dictionary — words in order. You don't read every page to find "otter." You flip to the middle, decide left or right, and halve the search each time. That's **binary search**. And a sorted list of timestamps is exactly a dictionary of times.
>
> So the question "what's the largest timestamp at-or-before 3?" becomes: binary-search the sorted timestamps for the **rightmost one that's `≤` 3.**
>
> **[VISUAL: the `[1, 4]` timeline with a query marker at 3. A pointer jumps to the middle, compares, converges on index 0 → `"bar"`. Steps counter shows "log₂ n".]**
>
> On a hundred-thousand-long history, that's about **seventeen steps** instead of a hundred thousand. Same answer. A rounding error of the work.

---

## 6. THE KEY MOVE (signaling) — `4:20`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Sorted timestamps ⇒ binary search the history."]**

> Burn this one line in: **sorted timestamps means binary search the history.**
>
> And be precise about *which* binary search: you want the **rightmost timestamp `≤` the query.** The clean way to get it — find the first timestamp *strictly greater* than the query (that's an "upper bound"), then **step back one.** The slot just before it is your answer.

---

## 7. CODE IT — LIVE & CHUNKED — `5:00`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. Two parallel lists per key — one for timestamps, one for values — so we can binary-search the raw timestamps directly.

```python
import bisect

class TimeMap:
    def __init__(self):
        self.times = {}      # key -> sorted list of timestamps
        self.vals = {}       # key -> parallel list of values
```

> **[VISUAL: add chunk 2, highlight it.]** `set` is just an append. Because timestamps arrive increasing, appending *keeps the list sorted* — no work.

```python
    def set(self, key, value, timestamp):
        if key not in self.times:
            self.times[key] = []
            self.vals[key] = []
        self.times[key].append(timestamp)
        self.vals[key].append(value)
```

> **[VISUAL: add chunk 3.]** Now `get` — the binary search. `bisect_right` gives the first index whose timestamp is strictly greater than the query.

```python
    def get(self, key, timestamp):
        if key not in self.times:
            return ""
        i = bisect.bisect_right(self.times[key], timestamp)
```

> **[VISUAL: add chunk 4, highlight the step-back.]** Step back one to land on the largest timestamp `≤` the query. If `i` is 0, everything was set *after* the query — return empty.

```python
        if i == 0:
            return ""
        return self.vals[key][i - 1]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: the full class; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> Two dictionaries, `times` and `vals`, kept in lockstep — index `i` in one lines up with index `i` in the other. That lets `bisect` chew on a plain array of integers instead of tuples.
>
> `set` just appends. This is the whole payoff of the "strictly increasing" gift: a new timestamp is always the biggest so far, so tacking it on the end *keeps the list sorted*. That's why `set` is O(1) — no shifting, no re-sorting.
>
> `bisect_right(times, timestamp)` — this returns how many timestamps are `≤` the query, which is the same as the first index strictly *greater* than it.
>
> **LEARNER:** Wait — why `bisect_right` and then `i - 1`? Why not `bisect_left`?
>
> **TEACHER:** Sharp question. We want the *rightmost* timestamp that's `≤` the query — including an exact match. `bisect_right` puts the cursor just past any exact hits, so `i - 1` lands *on* the match if there is one, or on the closest earlier write if there isn't. `bisect_left` would step back too far on an exact match. `right` then minus one is the clean idiom for "largest `≤` target."
>
> And `if i == 0: return ""` — that's the guard for "the query time is before this key ever existed." Index 0 means nothing sits at or before it. Empty string, as the spec asks.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close the loop)*

**[VISUAL: `times["foo"] = [1, 4]`, `vals["foo"] = ["bar", "bar2"]`, and a trace table filling row by row.]**

> Let's run the actual code on our timeline — `times = [1, 4]`, `vals = ["bar","bar2"]` — the exact sequence from the problem.

| call | `bisect_right([1,4], t)` | `i - 1` | result |
|---|---|---|---|
| `set("foo","bar",1)` | — | — | `times=[1]` |
| `get("foo",1)` | 1 | `vals[0]` | **"bar"** |
| `set("foo","bar2",4)` | — | — | `times=[1,4]` |
| `get("foo",3)` | 1 | `vals[0]` | **"bar"** |
| `get("foo",4)` | 2 | `vals[1]` | **"bar2"** |

> Walk the tricky one — `get("foo",3)`. No write at 3. `bisect_right([1,4], 3)` returns 1, because one timestamp (the `1`) is `≤` 3. Step back: `vals[0]` = `"bar"`. Exactly right — at time 3, the last thing set was `"bar"` at time 1.
>
> And `get("foo",4)` hits `4` exactly — `bisect_right` returns 2, step back to `vals[1]` = `"bar2"`. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:00`
*(transfer to interview)*

**[VISUAL: two rows — Brute force get: O(n). Ours get: O(log n). set: O(1). Space: O(total writes).]**

> **TEACHER:** Say it the way you'd say it to the interviewer: *"set is O(1) — it's just an append, and it stays sorted because timestamps arrive increasing. get is O(log n), because it's a binary search over that key's sorted history. Brute force was O(n) per get, which times out on a hot key."*
>
> That contrast — O(n) scan versus O(log n) search — is the sentence that earns the checkmark.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:35`
*(depth + honesty)*

**[VISUAL: the full history for a key, with a red "can we drop old writes?" crossed out.]**

> Quick and honest. Space is **O(total writes)** — every value ever set, for every key. Can we shrink it?
>
> No — and knowing *why* is the skill. A `get` can ask about *any* past timestamp, so any old write might still be the answer to a future query. There's nothing safe to throw away.
>
> Say it out loud in the room: *"Space is O(total writes) and that's inherent — a get can target any historical moment, so I have to keep the full history. Nothing compresses without losing answers."* Naming that an optimization *isn't possible*, and why, is just as strong as finding a trick.

---

## 12. YOUR TURN (active recall) — `10:05`
*(retrieval practice)*

**[VISUAL: "Your turn → Snapshot Array (LC 1146)". A blank editor.]**

> Before the next video, try **Snapshot Array**. Same soul — you store values at versions and later ask "what was index `i` at snapshot `k`?" — and you'll reach for the exact same move: keep a sorted list of `(version, value)` per index and **binary search** it.
>
> Don't peek at the solution. Wrestle with it for ten minutes. That struggle is what moves this from "I saw it" to "I own it."

---

## 13. LOCK IT IN — `10:35`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Map each key to a sorted list of its writes** — hash map on the outside, sorted history inside.
> 2. **"Rightmost `≤` target" is `bisect_right` minus one.** Memorize that idiom.
> 3. **The constraint is the unlock** — "timestamps strictly increasing" is what makes the list pre-sorted and set O(1).
>
> And here's the one that matters most for the interview: the very first thing to *ask* is **"are the timestamps for a key increasing?"** That clarifying question is exactly what a Google interviewer wants to hear — it's how you *earn* the sorted-array assumption instead of guessing it. (That's your **GCA — Gather requirements, Clarify, Assumptions** — before you write a line.)
>
> The memory peg: **sorted timestamps ⇒ binary search the history.**

---

## 14. CLIFFHANGER — `11:05`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Median of Two Sorted Arrays".]**

> Binary search just turned a linear scan into log-n on a single sorted list. But what if you're handed *two* sorted lists and asked for their combined median — in log time — without ever merging them? That's binary search at its sneakiest, and it's the next one. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

Manual binary search — the version most interviewers want to watch you write.

```java
class TimeMap {
    private final Map<String, List<Integer>> times = new HashMap<>();
    private final Map<String, List<String>> vals = new HashMap<>();

    public TimeMap() { }

    public void set(String key, String value, int timestamp) {
        times.computeIfAbsent(key, k -> new ArrayList<>()).add(timestamp);
        vals.computeIfAbsent(key, k -> new ArrayList<>()).add(value);
    }

    public String get(String key, int timestamp) {
        List<Integer> ts = times.get(key);
        if (ts == null) return "";
        int lo = 0, hi = ts.size() - 1, ans = -1;
        while (lo <= hi) {                         // rightmost ts <= timestamp
            int mid = (lo + hi) >>> 1;
            if (ts.get(mid) <= timestamp) {
                ans = mid;                          // candidate; try further right
                lo = mid + 1;
            } else {
                hi = mid - 1;                       // too big; go left
            }
        }
        return ans == -1 ? "" : vals.get(key).get(ans);
    }
}
```

*(One-liner alternative: a `TreeMap<Integer,String>` per key and `floorKey(timestamp)` — mention it, then show the manual search above, since implementing the search is the point.)*
