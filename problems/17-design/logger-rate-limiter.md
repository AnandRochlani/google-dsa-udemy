# Logger Rate Limiter

> **LeetCode:** 359. Logger Rate Limiter · **Difficulty:** 🟡 Medium *(tagged Easy on LeetCode)* · **Pattern:** Design (hash map of last-seen timestamps) · **Google frequency:** medium

---

## Problem

Design a logger that **rate-limits repeated messages**. Implement:

- `shouldPrintMessage(timestamp, message)` — return `True` if the message **should be printed** at this timestamp, else `False`. A message may be printed **at most once every 10 seconds**: it prints only if it hasn't been printed in the previous 10 seconds.

Calls arrive in **non-decreasing timestamp order**.

**Example** (each call is `timestamp, message`):
```
shouldPrintMessage(1,  "foo")  -> true    // first time → print; remember foo@1
shouldPrintMessage(2,  "bar")  -> true    // first time → print; remember bar@2
shouldPrintMessage(3,  "foo")  -> false   // foo last printed at 1; 3 < 1+10 → block
shouldPrintMessage(8,  "bar")  -> false   // bar last printed at 2; 8 < 2+10 → block
shouldPrintMessage(10, "foo")  -> false   // foo@1; 10 < 1+10 → still blocked
shouldPrintMessage(11, "foo")  -> true    // 11 >= 1+10 → print; update foo@11
```

**Constraints that matter:** up to `10⁴` calls; the check must be effectively **O(1) per call**. The message is a string, so we need string-keyed lookups — a hash map is the natural fit. The subtlety is the boundary: allowed exactly when `timestamp >= last_printed + 10` (i.e. `10 < 1+10` blocks, `11 >= 1+10` prints).

---

## 🧠 Intuition — how you'd actually arrive at this

> A rate limiter's whole job is "have I seen this recently?" — that's a lookup keyed by identity, which is a hash map.

- **First instinct:** keep a log of every `(message, timestamp)` printed, and on each call scan it for the last time this message printed. That works but is O(n) per call.
- **Where it hurts:** we only ever need the **most recent** print time for a given message — the older ones are irrelevant. Keeping the full history and re-scanning is wasted work.
- **The leap:** store just **one number per message**: `message → the next timestamp at which it's allowed to print` (or equivalently, the last time it printed). On a call, one hash lookup tells us instantly whether we're past the cooldown. Print iff `timestamp >= allowed_time`, and if we print, set `allowed_time = timestamp + 10`.
- **Pattern trigger:** *"limit repeats within a time window, keyed by identity"* → **hash map of last-seen (or next-allowed) timestamps**, O(1) per query. Storing "next allowed" instead of "last seen" makes the check a single comparison with no arithmetic at read time.

---

## ① Brute Force

Keep a list of every printed `(message, timestamp)` and scan it for the message's latest print time.

```python
class LoggerBrute:
    def __init__(self):
        self.printed = []   # list of (message, timestamp) actually printed

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        last = None
        for msg, ts in self.printed:      # O(n) scan every call
            if msg == message:
                last = ts                 # keep the latest (list grows in order)
        if last is None or timestamp - last >= 10:
            self.printed.append((message, timestamp))
            return True
        return False
```

**Why it's the natural first attempt:** it literally records what was printed and checks history — a direct reading of the spec.

**Why it's not enough:** each call scans the entire printed history → **O(n)** per call and **O(n)** memory that never stops growing. We only need the *latest* time per message, so almost all of that work and storage is redundant.

**Complexity:** Time O(n) per call, Space O(n) (unbounded).

---

## ② Optimised Solution

One hash map, `message → next timestamp it's allowed to print`.

```python
class Logger:
    def __init__(self):
        self.allowed = {}    # message -> earliest timestamp it may print again

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if message not in self.allowed or timestamp >= self.allowed[message]:
            self.allowed[message] = timestamp + 10
            return True
        return False
```

**Walk the example:**

| Call | `allowed[msg]` before | check | result | `allowed[msg]` after |
|---|---|---|---|---|
| `(1,"foo")` | — (absent) | print | ✅ true | foo → 11 |
| `(2,"bar")` | — (absent) | print | ✅ true | bar → 12 |
| `(3,"foo")` | 11 | `3 >= 11`? no | ❌ false | foo → 11 |
| `(8,"bar")` | 12 | `8 >= 12`? no | ❌ false | bar → 12 |
| `(10,"foo")` | 11 | `10 >= 11`? no | ❌ false | foo → 11 |
| `(11,"foo")` | 11 | `11 >= 11`? yes | ✅ true | foo → 21 |

The boundary is exact: at `timestamp = 10` we compare against `allowed = 11` and block; at `11` we hit `11 >= 11` and print, then push the window to `21`.

**Why it's correct:** we print exactly when the current timestamp has reached the stored next-allowed time (or the message is brand new), and every print advances that time by 10. So between any two prints of the same message at least 10 seconds elapse — precisely the rate limit. Other messages have independent entries and don't interfere.

**Complexity (per operation):** Time **O(1)** — one hash lookup and maybe one insert. Space **O(m)** where m is the number of *distinct* messages seen.

---

## ③ Space Optimization

The hash map holds one entry per distinct message and never releases them, so space is **O(distinct messages)** — already far better than the brute force's O(all calls). For the given limits that's fine.

If distinct messages were unbounded over a long-running service, you'd want to *evict* stale entries so memory doesn't grow forever. Because timestamps are non-decreasing, a message whose `allowed` time is already in the past can be safely re-created on demand, so you can prune it. A clean way:

```python
from collections import deque

class LoggerBounded:
    def __init__(self):
        self.allowed = {}       # message -> next-allowed timestamp
        self.q = deque()        # (allowed_time, message) in increasing time

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        # evict entries whose window has fully passed
        while self.q and self.q[0][0] <= timestamp:
            _, old = self.q.popleft()
            if self.allowed.get(old, -1) <= timestamp:
                self.allowed.pop(old, None)
        if message not in self.allowed or timestamp >= self.allowed[message]:
            self.allowed[message] = timestamp + 10
            self.q.append((timestamp + 10, message))
            return True
        return False
```

This caps live memory at roughly the messages seen within the last 10 seconds. Amortized still O(1) — each message is enqueued and dequeued once.

> Honest note: for LeetCode's constraints the plain one-map version is optimal and simplest; the queue-based pruning is the answer to the *systems* follow-up ("what if it runs for a year?"), which Google interviewers like to probe.

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | shouldPrintMessage | Space |
|---|---|---|
| Brute force (scan history) | O(n) | O(n) (all calls) |
| Hash map of next-allowed times | O(1) | O(distinct messages) |
| + queue pruning (long-running) | amortized O(1) | O(messages in last 10s) |

---

## Say it out loud (interview narration)

> *"A rate limiter is a 'have I seen this recently' question keyed by the message string, so a hash map is the obvious fit. I store, per message, the next timestamp it's allowed to print. On each call one lookup: if the message is new or the current timestamp has reached its next-allowed time, I print and set the next-allowed to timestamp plus ten; otherwise I block. That's O(1) per call and O(distinct-messages) space. Watch the boundary — at timestamp 10 against a window ending at 11 we block, at 11 we print. If this were a long-running service I'd add a queue to evict entries whose windows have expired so memory stays bounded."*

## Related / follow-ups
- **Design Hit Counter** (362) — count hits in the last 5 minutes; queue or bucket of timestamps.
- **Logger Rate Limiter** with a configurable window / per-user limits — the systems-design extension.
- **LRU Cache** (146) — another "recency via a map" design.
- **Design HashMap** (706) — the primitive underneath.
