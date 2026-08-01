# Minimum Cost to Set Cooking Time

> **LeetCode:** 2162. Minimum Cost to Set Cooking Time · **Difficulty:** 🟡 Medium · **Pattern:** Simulation / exhaustive enumeration (tiny domain) · **Google frequency:** ⭐ high

---

## Problem

A microwave keypad has digits `0–9`. Your finger starts on digit `startAt`. Moving the finger to a **different** digit costs `moveCost`; **pushing** the digit under the finger costs `pushCost`. You push **at most four digits**; the microwave prepends zeros to normalize what you typed to four digits `MMSS` — the first two digits are **minutes**, the last two are **seconds**. So pushing `9 5 4` reads as `0954` → 9 minutes 54 seconds. Minutes and seconds must each be `0–99`, and at least one digit must be pushed. Find the **minimum total cost** to enter *some* valid `MMSS` whose duration `MM*60 + SS` equals `targetSeconds`.

**Example:** `startAt = 1, moveCost = 2, pushCost = 1, targetSeconds = 600` → `6`
*(Type `1 0 0 0` = 10:00. Finger is already on 1: push (1). Move to 0 (2), then push 0 three times (3). Total 6. The alternative encoding `0 9 6 0` = 9:60 costs 9.)*

**Constraints that matter:** `targetSeconds ≤ 6039` — that's the hard ceiling `99*60 + 99`, and it's tiny. There are at most 100×100 = 10,000 `(MM, SS)` displays *in total*, and for any fixed target only the pairs with `MM*60 + SS = targetSeconds` matter — since two minutes differ by 120 seconds and `SS` only spans 0–99, **at most two encodings can ever hit the target**: `(t//60, t%60)` and `(t//60 − 1, t%60 + 60)`. There is no algorithm to design here. The whole problem is *enumerate every valid candidate and cost each one honestly* — and the difficulty is the pile of edge cases (seconds 60–99 are legal! leading zeros are stripped! `MM = 100` is not a thing!), not the runtime.

---

## 🧠 Intuition — how you'd actually arrive at this

> When the domain is this small, don't be clever — be *complete*. Enumerate every candidate, cost them all, take the min.

- **First instinct:** compute `minutes = targetSeconds // 60`, `seconds = targetSeconds % 60`, type those four digits, done. That's *one* encoding — and it's sometimes not even legal (`targetSeconds = 6000` gives `minutes = 100`, which doesn't fit in two digits), and often not the cheapest.
- **Where it hurts:** the traps are all representational, not algorithmic. **(1)** Seconds don't stop at 59 — the display `0960` is a perfectly valid way to say 600 seconds, because `9*60 + 60 = 600`. Miss that and you fail targets like 6000–6039 outright and overpay on many others. **(2)** Leading zeros aren't typed — `0008` is entered as one push of `8`, so the cost of a display depends on its *stripped* digit string. **(3)** The finger has state: consecutive equal digits cost no move, so `1000` can be dramatically cheaper than `0960` even though both mean 600.
- **The leap:** stop trying to *derive* the cheapest encoding and just **enumerate all of them**. `SS = targetSeconds − 60*MM` must land in `[0, 99]`, and consecutive `MM` values shift `SS` by 60 — so at most **two** `(MM, SS)` pairs are valid: `(t//60, t%60)` and `(t//60 − 1, t%60 + 60)`. Validate each (`0 ≤ MM ≤ 99`, `0 ≤ SS ≤ 99`), simulate typing its stripped digit string with a running finger position, and return the cheaper. Extra leading zeros are never worth pushing — every extra digit costs at least one `pushCost > 0` — so stripping is always optimal.
- **Pattern trigger:** **"tiny bounded domain + fiddly cost rules"** → **enumerate every candidate and simulate the cost of each**. The transferable lesson: when constraints cap the search space at a few thousand (here: two!), correctness of the *costing simulation* is the entire problem. Spend your effort on the edge cases, not on shaving asymptotics that are already O(1).

---

## ① Brute Force

Enumerate **all** 10,000 `(MM, SS)` displays, keep the ones whose duration equals the target, simulate typing each, take the min.

```python
def min_cost_brute(startAt, moveCost, pushCost, targetSeconds):
    best = float('inf')
    for mm in range(100):                    # every possible minutes display
        for ss in range(100):                # every possible seconds display (yes, 60-99 too)
            if mm * 60 + ss != targetSeconds:
                continue
            # str() of the 4-digit value strips leading zeros for free
            digits = str(mm * 100 + ss)
            total, cur = 0, startAt
            for d in map(int, digits):
                if d != cur:                 # finger has to travel
                    total += moveCost
                    cur = d
                total += pushCost            # every typed digit is pushed
            best = min(best, total)
    return best
```

**Why it's the natural first attempt:** it takes "find the cheapest valid way" completely literally — try every display the panel can show.

**Why it's not enough:** honestly? It *is* enough — 10,000 iterations is nothing, and this version is hard to get wrong, which has real interview value. But 9,998+ of those iterations are guaranteed misses: for a fixed target, `SS = targetSeconds − 60*MM` is forced by `MM`, and only two `MM` values can put `SS` inside `[0, 99]`. Scanning the full grid to find two candidates you could name directly is the wasted work.

**Complexity:** Time `O(M·S)` = 10,000 candidate checks (constant, but blind), Space `O(1)`.

---

## ② Optimised Solution

Name the **≤ 2 candidates** directly — `(t//60, t%60)` and `(t//60 − 1, t%60 + 60)` — validate each, and simulate typing its stripped digit string.

```python
def minCostSetTime(startAt, moveCost, pushCost, targetSeconds):
    def cost(mm, ss):
        # a candidate is only real if both fields fit on the 2-digit display
        if not (0 <= mm <= 99 and 0 <= ss <= 99):
            return float('inf')
        total, cur = 0, startAt
        # mm*100 + ss is the 4-digit display; str() strips leading zeros,
        # which is exactly what an optimal typist does
        for d in map(int, str(mm * 100 + ss)):
            if d != cur:            # move the finger only when the digit changes
                total += moveCost
                cur = d
            total += pushCost       # push every digit we actually type
        return total

    mm, ss = divmod(targetSeconds, 60)
    return min(cost(mm, ss), cost(mm - 1, ss + 60))
```

**Walk the example** `startAt = 1, moveCost = 2, pushCost = 1, targetSeconds = 600`:

`divmod(600, 60) = (10, 0)` → candidates `(10, 0)` and `(9, 60)`.

| Candidate | Display | Typed digits | Simulation (finger starts at 1) | Cost |
|---|---|---|---|---|
| `(10, 0)` | `1000` | `1 0 0 0` | push 1 (+1) · move→0 (+2) push (+1) · push (+1) · push (+1) | **6** |
| `(9, 60)` | `0960` | `9 6 0` | move→9 (+2) push (+1) · move→6 (+2) push (+1) · move→0 (+2) push (+1) | 9 |

`min(6, 9) = 6`. ✅ And note what the second row proves: `0960` is a *legal* encoding of 600 seconds — it just loses on cost here because `1000` reuses the starting finger position and repeats a digit.

**Why it's correct:** every valid display satisfies `MM*60 + SS = targetSeconds` with `SS ∈ [0, 99]`, and since consecutive `MM` values move `SS` by ±60, at most two `MM` can keep `SS` in range — exactly the two we test, so no encoding is ever missed. The validity check rejects `MM = 100` (target ≥ 6000) and `SS = 119`-style overflow (target % 60 ≥ 40 with the −1 candidate... any `ss + 60 > 99`), and `MM = −1` when `targetSeconds < 60`. Typing extra leading zeros only ever adds cost (each digit costs ≥ `pushCost` ≥ 1), so costing the stripped string is costing the optimal typing of that display. The simulation itself is the spec verbatim: pay `moveCost` exactly when the next digit differs from the finger's current digit, pay `pushCost` per digit.

**Complexity:** Time `O(1)` — 2 candidates × ≤ 4 digits. Space `O(1)`.

---

## ③ Space Optimization

**Already O(1) — and here's why.** The state is three scalars per candidate: the running `total`, the finger position `cur`, and the ≤ 4-digit string being walked. Nothing grows with the input — the input *is* four integers, and the search space was capped at two candidates by the two-digit display, not by anything we allocated. There's no array to shrink, no rolling trick to apply. Naming that in the interview ("both time and space are constant — the display bounds the world at two candidates of four digits") is the strong move; hunting for a space trick here would signal you don't see that the domain is finite.

```python
# No space-optimised variant exists: state is (total, cur) plus a ≤4-char
# digit string per candidate — already O(1) time and O(1) space.
```

**Complexity:** Time `O(1)`, Space `O(1)`.

---

## Java (for Java interviewers)

```java
class Solution {
    public int minCostSetTime(int startAt, int moveCost, int pushCost, int targetSeconds) {
        int mm = targetSeconds / 60, ss = targetSeconds % 60;
        return Math.min(cost(mm, ss, startAt, moveCost, pushCost),
                        cost(mm - 1, ss + 60, startAt, moveCost, pushCost));
    }

    private int cost(int mm, int ss, int startAt, int moveCost, int pushCost) {
        // candidate must fit the 2-digit minutes and 2-digit seconds display
        if (mm < 0 || mm > 99 || ss < 0 || ss > 99) return Integer.MAX_VALUE;
        String digits = String.valueOf(mm * 100 + ss);   // leading zeros drop off for free
        int total = 0, cur = startAt;
        for (char c : digits.toCharArray()) {
            int d = c - '0';
            if (d != cur) { total += moveCost; cur = d; } // travel only on digit change
            total += pushCost;                            // every typed digit is a push
        }
        return total;   // max real cost is 8 * 10^5 — no overflow risk
    }
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (scan all 100×100 displays) | O(M·S) = 10⁴ checks | O(1) |
| Optimised (name the ≤2 candidates) | O(1) | O(1) |
| Space-optimised | — (already O(1)) | O(1) |

---

## Say it out loud (interview narration)

> *"The display bounds everything: minutes and seconds are each two digits, so targetSeconds is at most 6039 and any valid encoding is a pair (MM, SS) with MM·60 + SS equal to the target and both fields in 0–99. Since bumping MM by one shifts SS by sixty, at most two pairs can be valid — t div 60 with t mod 60, and one minute less with sixty more seconds. So my plan is pure enumeration: validate each of those two candidates, simulate typing its digit string — leading zeros stripped, since typing them only adds pushes — tracking the finger so I pay moveCost only when the digit changes and pushCost per digit, and return the cheaper. Time and space are both O(1). The risk in this problem isn't complexity, it's edge cases, so let me confirm the spec: seconds from 60 to 99 are legal on the display, correct? And leading zeros are prepended by the machine, not typed?"*

Those two clarifying questions at the end aren't decoration — seconds-past-59 and stripped leading zeros are precisely the hidden test cases, and asking about them before coding is what Google's rubric scores as problem exploration.

## Related / follow-ups
- **Text Justification (68)** — the same species: zero algorithmic depth, all correctness-under-edge-rules.
- **String to Integer / atoi (8)** — careful spec simulation with representational traps.
- **Minimum Number of Pushes to Type Word (3014)** — keypad cost modeling, greedy over a tiny domain.
- **Design follow-up:** generalize to an N-digit panel or per-pair move costs — the enumeration frame survives, only the `cost` simulation changes.
