# Student Attendance Record II

> **LeetCode:** 552. Student Attendance Record II · **Difficulty:** 🔴 Hard · **Pattern:** Dynamic Programming / state-machine DP over a fixed state set · **Google frequency:** ⭐ high

*The previous problem asked "can you make a DP transition fast enough?" This one asks the other half of the DP question Google cares about: **what is the state?** There's no array to index into here, no grid, no obvious `dp[i]`. You have to invent the state yourself — and the whole lesson is that the right state is tiny.*

---

## Problem

A student's attendance record is a string of length `n` over the alphabet `{'A', 'L', 'P'}` — Absent, Late, Present. A record is **rewardable** if:

1. it contains **at most one `'A'`** in the entire string, **and**
2. it never contains **three or more consecutive `'L'`s**.

Given `n`, return **how many rewardable records of length `n` exist**, modulo `10^9 + 7`.

**Example:** `n = 2` → `8` *(all 9 two-letter strings are legal except `"AA"`, which has two absences: `PP PL PA LP LL LA AP AL` — that's 8.)*

**Example:** `n = 1` → `3` *(`"A"`, `"L"`, `"P"` — all three are fine.)*

**Constraints that matter:** `1 ≤ n ≤ 10^5`. Two things fall out of that. First, the answer space is `3^n` strings — you cannot enumerate them, so the counting has to be structural. Second, `n = 10^5` means the algorithm has to be **linear** (or logarithmic) in `n` with a **constant** amount of work per step. And because the count explodes past 64-bit range almost immediately, the modulus isn't decoration — it has to be applied on every addition.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Generate every string of length `n` over `{A, L, P}` and test each one." That's honest, and it's the right thing to *say* — it defines the problem precisely. It's also `3^n`. At `n = 20` that's ~3.5 billion strings. Dead.
- **Where it hurts:** the brute force keeps the **entire string** around, but the validity test barely looks at it. To decide whether appending one more character is legal, you need exactly two facts: *have I already used my one `'A'`?* and *how many `'L'`s are sitting at the end right now?* Everything else about the prefix — its length, its layout, where the A was — is irrelevant to the future. We're carrying a 100,000-character string to answer a two-bit question.
- **The leap:** if two different prefixes agree on those two facts, then **every legal completion of one is a legal completion of the other**. So don't track prefixes — track *buckets* of prefixes. A-count is `0` or `1` (2 options). Trailing-L count is `0`, `1`, or `2` (3 options — a count of 3 is already illegal, so it never exists). That's **2 × 3 = 6 buckets**, total, forever, no matter how big `n` gets. Instead of `3^n` strings, carry **6 counters**, and each new character just moves counts from one bucket to another.
- **Pattern trigger:** **"count the strings/sequences that never violate a local rule" → state-machine DP.** The tell is that the constraints are *bounded and local*: "at most one A" is a small counter, "no three L's in a row" is a short suffix condition. Whenever the legality of the next character depends only on a **bounded summary** of what came before, that summary *is* your DP state — and the number of distinct summaries is your state count. Build the transition table once, then it's `O(n × states)`.

---

## ① Brute Force

Generate all `3^n` strings, keep the ones that pass both rules.

```python
from itertools import product

MOD = 10**9 + 7

def checkRecord_brute(n):
    total = 0
    for combo in product("APL", repeat=n):          # all 3^n records
        record = "".join(combo)
        if record.count("A") <= 1 and "LLL" not in record:
            total += 1
    return total % MOD
```

**Why it's the natural first attempt:** the problem literally says "count the strings that satisfy these rules," and this is that sentence typed out. It's also a genuinely useful tool — this is what you'd use to *verify* the fast solution on small `n` (and it's exactly how the recurrence below was checked: `n=1 → 3`, `n=2 → 8`, `n=3 → 19`).

**Why it's not enough:** `3^n`. `n = 10` is 59,049 — instant. `n = 20` is **3,486,784,401** — you're now generating three and a half billion strings, each of which you also scan. `n = 10^5` isn't slow, it's physically impossible; the number of records has more digits than there are atoms in the observable universe. This is the timeout moment, and it arrives before `n` reaches 25.

**Complexity:** Time `O(n · 3^n)`, Space `O(n)`.

---

## ② Optimised Solution

Stop tracking strings. Track the **state** a prefix leaves you in: `(a, l)` where `a` ∈ {0, 1} is how many `'A'`s you've used and `l` ∈ {0, 1, 2} is how many `'L'`s are currently trailing. Six states. `dp[i][a][l]` = the number of length-`i` prefixes that land in state `(a, l)`.

From any state, appending a character does this:

| Append | Effect | Allowed when |
|---|---|---|
| `'P'` | `(a, l) → (a, 0)` — breaks any L-streak | always |
| `'L'` | `(a, l) → (a, l+1)` — extends the streak | `l < 2` (a third L would make `LLL`) |
| `'A'` | `(a, l) → (1, 0)` — uses the absence, breaks the streak | `a == 0` (only one A allowed) |

```python
MOD = 10**9 + 7

def checkRecord_table(n):
    # dp[i][a][l] = # of length-i prefixes with `a` absences and `l` trailing L's
    dp = [[[0] * 3 for _ in range(2)] for _ in range(n + 1)]
    dp[0][0][0] = 1                                      # the empty record
    for i in range(1, n + 1):
        for a in range(2):
            for l in range(3):
                cur = dp[i - 1][a][l]
                if cur == 0:
                    continue
                dp[i][a][0] = (dp[i][a][0] + cur) % MOD          # append 'P'
                if l < 2:
                    dp[i][a][l + 1] = (dp[i][a][l + 1] + cur) % MOD  # append 'L'
                if a == 0:
                    dp[i][1][0] = (dp[i][1][0] + cur) % MOD       # append 'A'
    return sum(dp[n][a][l] for a in range(2) for l in range(3)) % MOD
```

**Walk one example** — the six counters, day by day. Columns are `(a=0: l=0, l=1, l=2)` then `(a=1: l=0, l=1, l=2)`:

| Day | `a0l0` | `a0l1` | `a0l2` | `a1l0` | `a1l1` | `a1l2` | Total |
|---|---|---|---|---|---|---|---|
| 0 (empty) | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
| 1 | 1 | 1 | 0 | 1 | 0 | 0 | **3** |
| 2 | 2 | 1 | 1 | 3 | 1 | 0 | **8** |
| 3 | 4 | 2 | 1 | 8 | 3 | 1 | **19** |

Day 1 reads off directly: `"P"` sits in `a0l0`, `"L"` in `a0l1`, `"A"` in `a1l0` — three records, matching `n = 1 → 3`. ✅
Day 2 totals 8, which is `9 − 1`: every two-character string except `"AA"`. ✅
Day 3 totals 19, which is `27 − 8`: minus `"LLL"`, minus the seven strings with two or more A's. ✅

**Why it's correct:** two claims. **(1) The state is sufficient.** Whether a future character can be appended depends only on `a` (can I still spend an A?) and `l` (would another L make three?) — nothing else about the prefix constrains the future. So all prefixes sharing a state have identical sets of legal completions, and lumping them into one counter loses nothing. **(2) The transitions partition.** Every length-`i` record is exactly one length-`(i−1)` record plus exactly one final character, so each length-`i` record is counted exactly once — no double-counting, no gaps. Illegal moves are simply absent from the table (there's no `l = 3` slot and no `a = 2` slot), so nothing invalid is ever counted. The answer is the sum over all six terminal states, since **every** reachable state is a valid record.

**Why the modulus goes on every addition:** the true count grows roughly like `1.84^n`. At `n = 40` it already exceeds `2^31`; around `n = 90` it blows past `2^63`. If you only mod at the end, you've overflowed long before you get there. Modding after each `+` is safe because addition is compatible with mod — `(x + y) mod m = ((x mod m) + (y mod m)) mod m` — and we only ever add.

**Complexity:** Time `O(n)` — six states, three transitions, constant work per character. Space `O(n)` for the full `(n+1) × 2 × 3` table.

---

## ③ Space Optimization

Look at the recurrence: `dp[i]` reads only `dp[i - 1]`. The other `n − 1` rows are dead weight the moment they're written. So drop the table and keep **six rolling variables**.

Writing out the transitions in "who flows *into* me" form makes it a straight six-line update:

- `a0l0` ← every `a=0` state appends `'P'`
- `a0l1` ← old `a0l0` appends `'L'`
- `a0l2` ← old `a0l1` appends `'L'`
- `a1l0` ← every `a=0` state appends `'A'`, **plus** every `a=1` state appends `'P'`
- `a1l1` ← old `a1l0` appends `'L'`
- `a1l2` ← old `a1l1` appends `'L'`

```python
MOD = 10**9 + 7

def checkRecord(n):
    # six rolling counters: [absences used][trailing L's]
    a0l0, a0l1, a0l2 = 1, 0, 0      # start: the empty record — 0 absences, 0 trailing L's
    a1l0, a1l1, a1l2 = 0, 0, 0

    for _ in range(n):
        n0l0 = (a0l0 + a0l1 + a0l2) % MOD                          # 'P' from any a=0 state
        n0l1 = a0l0                                                # 'L' onto 0 trailing L's
        n0l2 = a0l1                                                # 'L' onto 1 trailing L
        n1l0 = (a0l0 + a0l1 + a0l2 + a1l0 + a1l1 + a1l2) % MOD     # 'A' from a=0, 'P' from a=1
        n1l1 = a1l0                                                # 'L' onto 0 trailing L's
        n1l2 = a1l1                                                # 'L' onto 1 trailing L

        a0l0, a0l1, a0l2 = n0l0, n0l1, n0l2
        a1l0, a1l1, a1l2 = n1l0, n1l1, n1l2

    return (a0l0 + a0l1 + a0l2 + a1l0 + a1l1 + a1l2) % MOD
```

Note the `n0l*` temporaries: all six new values must be computed from the **old** six before any of them is overwritten. Assign in place and `n0l1 = a0l0` would read a value that's already been clobbered — a classic, silent, wrong-answer bug.

**Complexity:** Time `O(n)`, Space `O(1)` — six integers, regardless of whether `n` is 5 or 100,000.

> Can we do better than `O(n)` time? Yes, and it's worth naming: the six-variable update is a **fixed linear map**, so it's a 6×6 matrix multiply. Raising that matrix to the `n`-th power by binary exponentiation gives `O(6³ log n)` — effectively `O(log n)`. Overkill for `n ≤ 10^5`, but mentioning it is the "I know where this generalizes" signal an interviewer is listening for. See the follow-ups.

---

## Java (for Java interviewers)

Use `long` for the accumulators. Each `n1l0` line sums six values that can each approach `10^9`, so an `int` would overflow *before* the mod is applied even though the modded result fits comfortably.

```java
class Solution {
    private static final int MOD = 1_000_000_007;

    public int checkRecord(int n) {
        // [absences used][trailing L's]
        long a0l0 = 1, a0l1 = 0, a0l2 = 0;   // no 'A' spent yet
        long a1l0 = 0, a1l1 = 0, a1l2 = 0;   // the one 'A' already spent

        for (int day = 0; day < n; day++) {
            long n0l0 = (a0l0 + a0l1 + a0l2) % MOD;                       // append 'P'
            long n0l1 = a0l0;                                             // append 'L'
            long n0l2 = a0l1;                                             // append 'L'
            long n1l0 = (a0l0 + a0l1 + a0l2 + a1l0 + a1l1 + a1l2) % MOD;  // 'A' from a=0, 'P' from a=1
            long n1l1 = a1l0;                                             // append 'L'
            long n1l2 = a1l1;                                             // append 'L'

            a0l0 = n0l0; a0l1 = n0l1; a0l2 = n0l2;
            a1l0 = n1l0; a1l1 = n1l1; a1l2 = n1l2;
        }
        return (int) ((a0l0 + a0l1 + a0l2 + a1l0 + a1l1 + a1l2) % MOD);
    }
}
```

*(Verified: `n=1 → 3`, `n=2 → 8`, `n=3 → 19`, `n=10101 → 183236316` — LeetCode's own third example.)*

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (enumerate all records) | O(n · 3ⁿ) | O(n) |
| Optimised (state-machine DP, full table) | O(n) | O(n) |
| Space-optimised (six rolling counters) | O(n) | **O(1)** |
| *Follow-up:* matrix exponentiation | O(log n) | O(1) |

*(The constant factor is the state count: 2 A-values × 3 trailing-L values = 6.)*

---

## Say it out loud (interview narration)

> *"The brute force is enumerate all `3^n` records and filter — correct, but `3^n` dies around n equals twenty, and n goes to a hundred thousand here. So the question becomes: what do I actually need to remember about a prefix in order to know which characters can follow it? Only two things — how many A's I've used, which is zero or one, and how many L's are currently trailing, which is zero, one, or two, because three is already illegal. That's six states, and it's six states no matter how long the string is. So `dp[i][a][l]` counts length-i prefixes in each state, and each character moves counts between states: P sends anything to trailing-L zero, L bumps the trailing count but only if it's below two, and A is only available from A-count zero and lands in state (1, 0). That's `O(n)` time with a constant factor of six. Then — since row `i` only reads row `i−1` — I drop the table entirely and keep six rolling variables, so space is `O(1)`. One implementation detail I'd call out: I compute all six new values into temporaries before assigning, or I'd be reading already-overwritten state. And I take the modulus on every addition, because the true count grows like 1.8 to the n and overflows 64 bits well before n hits a hundred. If you want it faster than linear, that six-variable update is a fixed 6×6 matrix, so matrix exponentiation gets it to `O(log n)`."*

The clarifying question that proves you read the spec: *"At most one `'A'` **in the whole string** — not one per window — and `'LLL'` means three **consecutive**, so `"LLPLL"` is fine, correct?"* Those two readings are the entire problem; confirming them before you code costs ten seconds and prevents a full rewrite.

## Related / follow-ups

- **Student Attendance Record I (LC 551)** — the easy version: given the actual string, is it rewardable? Do this first. It's the *validator*; today's problem is the *counter* built on the same two rules.
- **Matrix exponentiation** — the natural "push further" answer. Encode the six-state update as a 6×6 transition matrix `M`, then the answer is the state vector times `M^n`, computed with binary exponentiation in `O(6³ log n)`. Ask for it when the interviewer says "now n is 10^18."
- **Domino and Tromino Tiling (LC 790)** — another small-fixed-state-machine count where the states are partial-column configurations. Same skeleton, different alphabet.
- **Knight Dialer (LC 935)** — count length-`n` sequences on a 10-state machine; the transitions come from a keypad graph instead of a rule. Also the textbook place to show off the matrix-exponentiation upgrade.
- **Count Vowels Permutation (LC 1220)** — five states, transitions given as an explicit "which letter may follow which" table. If you can do that one cold, you own this pattern.
