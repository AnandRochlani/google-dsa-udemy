# 🎬 Recording Script — Logger Rate Limiter

**Pattern: Design (hash map of last-seen timestamps) · LeetCode 359 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** hash-map O(1) lookup — now the value is a timestamp.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a live server log flooding the screen — the SAME error line repeating hundreds of times per second. Then a filter kicks in and it calms to one line every 10 seconds.]**

> Every real system hits this. Something breaks, and the same log line floods your console a thousand times a second, burying everything useful. So you build a **rate limiter**: print a given message at most once every 10 seconds.
>
> Google asks it because it's deceptively small — the code is four lines — but there's a **boundary condition** that trips up most people, and a systems follow-up that separates the juniors from the seniors. By the end you'll nail both. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below, a call list of (timestamp, message) → true/false.]**

> One line: **`shouldPrintMessage(timestamp, message)` returns true if this message may print now** — and a message may print at most **once every 10 seconds**.
>
> Calls arrive in non-decreasing time order. Watch this sequence — `foo` at time 1 prints, `foo` at time 3 is blocked, and `foo` at time 11...

**[VISUAL: the calls appear; (11, "foo") has a "?" — will it print?]**

> Time 11 is the interesting one. Foo last printed at time 1. Does 11 clear the 10-second window? Hold that — it's the exact boundary the problem is testing.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: a growing list of every (message, timestamp) ever printed. On each call, a scan sweeps the whole list looking for this message's latest time.]**

> First instinct: keep a log of everything we've printed — every (message, timestamp) pair. On each call, scan that log to find the last time *this* message printed, and compare.
>
> `(1, foo)` — nothing logged, print, record it. `(3, foo)` — scan the log, find foo at 1, is `3 − 1 ≥ 10`? No, block. `(8, bar)`... and the log keeps growing.

**[VISUAL: the log grows unbounded; each call's scan arrow gets longer and longer.]**

> Two problems, both getting worse over time. Every call **scans the entire history** — O(n). And the history **never stops growing** — O(n) memory forever.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the scan hunting through old foo entries. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste: we store *every* print and re-scan for the latest. But think about what we actually *use*.
>
> **LEARNER:** For each message, we only ever care about the **most recent** print time, right? The older ones are dead weight.
>
> **TEACHER:** Exactly right — that's the whole optimization. Pause and predict: **if I only need one number per message, what structure maps a message-string to that single number, and answers "what's foo's last time?" in one step?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it)*

**[VISUAL: the giant log collapses into a tiny map — {"foo": 11, "bar": 12} — "next time each message is allowed to print".]**

> **TEACHER:** A rate limiter's real question is *"have I seen this recently?"* — a lookup keyed by the message's identity. That's a **hash map**. And we only need one value per message.
>
> The elegant choice: store, per message, **the next timestamp it's allowed to print** — that is, last-printed plus 10. Then each call is a single comparison: if the current timestamp has reached that allowed time (or the message is brand new), print, and push the allowed time to `timestamp + 10`. Otherwise block.
>
> **[VISUAL: a bouncer analogy — each message is a club-goer with a "come back after" time stamped on their hand. The bouncer just reads the stamp.]**
>
> Think of a bouncer with a stamp. When a message prints, stamp its hand: "come back at time 11." Anyone showing up before their stamp time gets turned away — no ledger, no scanning, just read the stamp.

---

## 6. THE KEY MOVE (signaling) — `4:20`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "map[message] = next allowed time. Print iff timestamp ≥ that; then set it to timestamp + 10."]**

> The key move: **store one number per message — its next-allowed timestamp — and print exactly when the clock reaches it.** Storing "next allowed" instead of "last seen" makes the check a single comparison with zero arithmetic at read time.

---

## 7. CODE IT — LIVE & CHUNKED — `4:55`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Init.]**

> One map.

```python
class Logger:
    def __init__(self):
        self.allowed = {}    # message -> earliest timestamp it may print again
```

> **[VISUAL: add the method, highlight the condition.]** And the whole logic — one condition.

```python
    def shouldPrintMessage(self, timestamp, message):
        if message not in self.allowed or timestamp >= self.allowed[message]:
            self.allowed[message] = timestamp + 10
            return True
        return False
```

> That's the entire solution. Four lines. The intelligence is all in that `or` and that `>=`.

---

## 8. EXPLAIN THE CODE (the WHY) — `5:40`
*(elaboration — why each line exists)*

**[VISUAL: the condition spotlighted, the two halves of the `or` colored differently.]**

> Why it's right.
>
> `message not in self.allowed` — brand-new message, always print. `timestamp >= self.allowed[message]` — we've reached or passed its next-allowed time. Either one prints, and on printing we set the next window to `timestamp + 10`.
>
> **LEARNER:** Why `>=` and not `>`? Feels like it could go either way, and that's exactly the kind of thing I'd get wrong under pressure.
>
> **TEACHER:** This is *the* boundary, so let's pin it. The rule is "at most once every 10 seconds" — meaning if foo printed at time 1, it may print again at time **11**, because 11 minus 1 is a full 10. We stored `allowed = 1 + 10 = 11`. At timestamp 11 we check `11 >= 11` — true, print. At timestamp 10 we check `10 >= 11` — false, block, because only 9 seconds passed. Use `>` and you'd wrongly block time 11 and stretch the gap to 11 seconds. The `>=` is what makes exactly-10 legal.

---

## 9. DRY-RUN THE CODE — `6:40`
*(worked example — prove it, close the boundary loop)*

**[VISUAL: trace table; the `allowed[msg]` before/after each call.]**

| Call | allowed before | check | result | allowed after |
|---|---|---|---|---|
| (1, foo) | absent | new | ✅ true | foo → 11 |
| (2, bar) | absent | new | ✅ true | bar → 12 |
| (3, foo) | 11 | 3 ≥ 11? no | ❌ false | foo → 11 |
| (8, bar) | 12 | 8 ≥ 12? no | ❌ false | bar → 12 |
| (10, foo) | 11 | 10 ≥ 11? no | ❌ false | foo → 11 |
| (11, foo) | 11 | 11 ≥ 11? **yes** | ✅ true | foo → 21 |

> There's our cliffhanger answer: `(11, foo)` **prints**. At time 10 we compared against 11 and blocked; at time 11, `11 >= 11` fires, we print and push the window to 21. The boundary is exact. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:30`
*(transfer to interview)*

**[VISUAL: two rows — Brute: O(n) time, O(n) space. Map: O(1) time, O(distinct messages) space.]**

> Out loud: *"One hash lookup and maybe one insert per call — O(1) time. Space is O(distinct messages), not O(all calls), because we keep one entry per unique message instead of the whole history."*
>
> Versus the brute force: *"The scan-the-log version was O(n) per call and O(n) memory that grows forever; collapsing to one timestamp per message fixes both."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:10`
*(depth + honesty — the systems follow-up)*

**[VISUAL: the map holding stale messages that will never repeat. Then a queue evicting expired entries.]**

> The plain map holds one entry per distinct message *forever* — fine for LeetCode's limits. But Google loves the systems follow-up: *"What if this runs for a year and sees millions of unique messages?"* Now that map leaks memory.
>
> The fix: because timestamps only increase, a message whose window has fully passed can be safely **forgotten** — if it ever recurs, it's treated as new, which is correct anyway. Add a queue of `(expiry_time, message)` and evict from the front as time advances.

```python
from collections import deque

class LoggerBounded:
    def __init__(self):
        self.allowed = {}       # message -> next-allowed timestamp
        self.q = deque()        # (allowed_time, message), increasing

    def shouldPrintMessage(self, timestamp, message):
        while self.q and self.q[0][0] <= timestamp:      # evict expired
            _, old = self.q.popleft()
            if self.allowed.get(old, -1) <= timestamp:
                self.allowed.pop(old, None)
        if message not in self.allowed or timestamp >= self.allowed[message]:
            self.allowed[message] = timestamp + 10
            self.q.append((timestamp + 10, message))
            return True
        return False
```

> This caps live memory at roughly the messages seen in the last 10 seconds. Still amortized O(1) — each message is enqueued and dequeued once.
>
> Say it out loud: *"For the given limits the one-map version is optimal and simplest. If it were a long-running service I'd add a queue to evict expired entries so memory stays bounded."* That sentence — knowing when the simple answer is enough *and* what the production version needs — is exactly what Google is probing.

---

## 12. YOUR TURN (active recall) — `9:20`
*(retrieval practice)*

**[VISUAL: "Your turn → Design Hit Counter (LC 362)".]**

> Before the next video, try **Design Hit Counter** — count how many hits happened in the last 5 minutes. Same time-window instinct, but now you're *counting* within the window rather than blocking repeats — a queue or a bucket of timestamps. It's the natural next step from this one.
>
> Ten minutes, no peeking.

---

## 13. LOCK IT IN — `9:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **"Seen recently?" keyed by identity → hash map** — one number per key, not a history.
> 2. **Store "next allowed time"** so the check is a single `>=` comparison.
> 3. **Watch the boundary** — exactly-10 is allowed, so `>=`, not `>`. Long-running? Add a queue to evict.
>
> The memory peg — *"stamp each message with 'come back after,' and just read the stamp."*

---

## 14. CLIFFHANGER — `10:20`
*(open loop to next lesson)*

**[VISUAL: a blurred pile of scrambled words — Group Anagrams.]**

> We've keyed maps by a value, and by a message string. Next, the key becomes something you have to *invent*: given a pile of words, group the ones that are rearrangements of each other. There's no ready-made key — you design a canonical form that all anagrams share. Same map reflex, a cleverer key. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class Logger {
    private final Map<String, Integer> allowed = new HashMap<>();  // msg -> next allowed ts

    public boolean shouldPrintMessage(int timestamp, String message) {
        Integer next = allowed.get(message);
        if (next == null || timestamp >= next) {
            allowed.put(message, timestamp + 10);
            return true;
        }
        return false;
    }
}
```
