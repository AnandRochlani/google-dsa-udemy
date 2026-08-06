# Race Car

> **LeetCode:** 818. Race Car · **Difficulty:** 🔴 Hard · **Pattern:** BFS over states → DP · **Google frequency:** ⭐ high

*This is the problem in the DP section that doesn't look like a DP. It looks like a search — and that's not a trap, it's the intended path. You get it right by solving it as a shortest-path BFS first, then noticing the state space has powers-of-two structure and collapsing it into a one-dimensional DP. Watching that collapse happen is the whole lesson.*

---

## Problem

Your car starts at **position 0** with **speed +1** on an infinite number line. You send it a string of instructions, each either `'A'` or `'R'`:

- `'A'` (accelerate): `position += speed`, then `speed *= 2`.
- `'R'` (reverse): `speed` becomes `-1` if it was positive, otherwise `+1`. **Position does not change.**

Given `target`, return the **length of the shortest instruction sequence** that gets the car to exactly `position == target`.

**Example:** `target = 6` → `5`, via `"AAARA"`.

| Instruction | position | speed |
|---|---|---|
| start | 0 | +1 |
| `A` | 1 | +2 |
| `A` | 3 | +4 |
| `A` | 7 | +8 |
| `R` | 7 | −1 |
| `A` | **6** | −2 |

*(Overshoot to 7 — the nearest `2^k − 1` past 6 — flip around, and one backward step lands on 6.)*

Sanity checks you should be able to reproduce by hand: `target = 3` → `2` (`"AA"`), `target = 4` → `5` (`"AARRA"`), `target = 5` → `7`, `target = 6` → `5`.

**Constraints that matter:** `1 ≤ target ≤ 10^4`. That's small — small enough that an `O(target · log target)` solution is instant, and even a well-pruned state search passes. But the number line is **infinite** and the speed **doubles without bound**, so the raw state space is infinite. The entire difficulty is (a) noticing the state is `(position, speed)` rather than just `position`, and (b) either bounding that space so search terminates, or replacing it with a DP over positions.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Shortest *sequence of moves* — that's not a DP reflex, that's a **BFS** reflex." Every instruction costs exactly 1, so the shortest sequence is the fewest edges in a graph, and BFS gives fewest-edges for free. Say that out loud in the room. It's the right first move and it's genuinely a solution.
- **Where it hurts:** what's a node? If you say "position," you're already wrong — arriving at position 3 at speed +4 and arriving at position 3 at speed −1 are completely different futures. So the node is `(position, speed)`. That's fine, but now count the nodes: positions run over all of ℤ and speed doubles forever. **The graph is infinite.** BFS never terminates on an unreachable-looking case unless you fence it in — and inventing that fence, and *justifying* it, is real interview work.
- **The leap:** stop and look at what the car can actually do. From `(0, +1)`, `k` consecutive `A`s always put you at exactly `1 + 2 + 4 + … + 2^(k-1) = 2^k − 1`, moving at speed `2^k`. Those `2^k − 1` milestones — 1, 3, 7, 15, 31 — are the *only* interesting places to turn around. And once you turn around, the problem restarts: you're at some position with speed ±1, needing to cover a **smaller remaining distance**, and the number line is translation- and reflection-symmetric. So "cost to cover distance `d` starting from speed 1" is a self-contained quantity. Call it `dp[d]`. The infinite 2-D state space collapses into one array of length `target + 1`.
- **Pattern trigger:** **"shortest sequence of moves" → BFS over states.** Then, the follow-up trigger: **when the reachable states have algebraic structure (here, powers of two), the BFS collapses into a DP over one coordinate.** That two-step — search first, then compress the search — is the transferable move, and it's exactly how you should narrate it live.

---

## ① Brute Force

BFS over the state `(position, speed)`, fenced into a sane window so it terminates.

```python
from collections import deque

def racecar_bfs(target):
    limit = 2 * target                    # the fence — justified below
    seen = {(0, 1)}
    queue = deque([(0, 1, 0)])            # position, speed, instructions used

    while queue:
        pos, spd, steps = queue.popleft()
        if pos == target:                 # first pop of the goal = shortest sequence
            return steps
        nxt = ((pos + spd, spd * 2),      # 'A' : move, then double
               (pos, -1 if spd > 0 else 1))  # 'R' : flip speed, stay put
        for npos, nspd in nxt:
            if 0 <= npos <= limit and abs(nspd) <= limit and (npos, nspd) not in seen:
                seen.add((npos, nspd))
                queue.append((npos, nspd, steps + 1))
    return -1                             # unreachable inside the fence (never happens)
```

**Why it's the natural first attempt:** "fewest instructions" is literally "fewest edges," and BFS is the reflex. This is the version you should put on the board first — it's correct, it passes on LeetCode, and it proves you modelled the state right. Compare it to the *truly* naive idea, generating every instruction string of length 1, 2, 3, … and simulating each: that's `O(2^L)` with `L` up to ~30, hopeless. BFS is already an enormous win because it dedupes states instead of re-walking prefixes.

**Why the fence is safe — say this out loud, don't just type it.** Let `k` be the smallest exponent with `2^k − 1 ≥ target`. Minimality means `2^(k-1) − 1 < target`, i.e. `2^(k-1) ≤ target`, so `2^k − 1 < 2·target`. That milestone `2^k − 1` is the *first* place a pure run of `A`s reaches or passes the target — driving beyond it only costs instructions and adds distance you must undo, so no optimal sequence needs a position past `2·target`. Symmetrically, never go left of 0: the start is 0 with speed +1, and any state at a negative position must be undone. Speeds are always `±2^i`, so capping `|speed| ≤ 2·target` clips exactly the runs that would leave the window anyway.

**Why it's not enough:** it works, but it's heavy. The frontier holds up to `~4·target·log(target)` states with tuple hashing on every one; for `target = 10^4` that's hundreds of thousands of hashed tuples. Worse, the *correctness* now rests on a bound you had to argue for. An interviewer who pushes — *"prove your window can't cut the optimal path"* — is pushing on the weakest joint in the solution. There's a version with no fence to defend at all.

**Complexity:** Time `O(target · log target)`, Space `O(target · log target)`.

---

## ② Optimised Solution

Define **`dp[t]` = the minimum number of instructions to travel a distance of `t`, starting from speed +1 facing that direction.** Because the line is translation- and reflection-symmetric, this one array answers every sub-journey, in either direction, from anywhere.

Let `k` be the smallest exponent with `2^k − 1 ≥ t`. There are exactly three shapes an optimal sequence can take.

**Case 1 — you land exactly.** If `2^k − 1 == t`, then `k` accelerations put you on the target with nothing wasted:

```
dp[t] = k
```

**Case 2 — overshoot, then come back.** Run `k` `A`s to `2^k − 1` (past the target), spend one `R` to flip to speed −1, and you now face a fresh sub-journey of distance `2^k − 1 − t`:

```
dp[t] = k + 1 + dp[2^k - 1 - t]
```

**Case 3 — undershoot, back up a bit, then come again.** Run only `k−1` `A`s, stopping **short** at `P = 2^(k-1) − 1 < t`. Spend an `R` (speed −1). Now reverse for `j` accelerations — that walks you back `1 + 2 + … + 2^(j-1) = 2^j − 1`. Spend a second `R` to face forward again at speed +1. Let's count both the instructions and the arithmetic carefully:

| Phase | Instructions | Position after | Speed after |
|---|---|---|---|
| `k−1` × `A` | `k − 1` | `P = 2^(k-1) − 1` | `2^(k-1)` |
| `R` | `1` | `P` | `−1` |
| `j` × `A` | `j` | `P − (2^j − 1)` | `−2^j` |
| `R` | `1` | `P − (2^j − 1)` | `+1` |

Instructions so far: `(k − 1) + 1 + j + 1 = k + j + 1`. Remaining distance to cover, forward, from speed +1:

```
t - [P - (2^j - 1)]  =  t - (2^(k-1) - 1) + (2^j - 1)
```

So:

```
dp[t] = min over j in 0..k-2 of  ( k + j + 1 + dp[ t - (2^(k-1) - 1) + (2^j - 1) ] )
```

*Why `j` stops at `k−2`:* backing up `2^j − 1` with `j = k−1` would retreat exactly `P` and dump you at position 0 with speed +1 — the start state, `2k` instructions poorer. Never useful. And `j = 0` **is** useful: it's `R R`, which resets your speed to +1 without moving at all.

```python
def racecar(target):
    dp = [0] * (target + 1)                 # dp[0] = 0: already there

    for t in range(1, target + 1):
        k = t.bit_length()                  # smallest k with 2^k - 1 >= t

        if (1 << k) - 1 == t:               # case 1: pure acceleration lands exactly
            dp[t] = k
            continue

        # case 2: overshoot to 2^k - 1, reverse, cover the gap coming back
        dp[t] = k + 1 + dp[(1 << k) - 1 - t]

        # case 3: stop short at 2^(k-1) - 1, reverse, back up 2^j - 1, reverse again
        for j in range(k - 1):              # j = 0 .. k-2
            rest = t - ((1 << (k - 1)) - 1) + ((1 << j) - 1)
            dp[t] = min(dp[t], k + j + 1 + dp[rest])

    return dp[target]
```

> `t.bit_length()` is exactly the `k` we want: for `t` in `[2^(k-1), 2^k - 1]` it returns `k`, and that range is precisely where `2^(k-1) − 1 < t ≤ 2^k − 1`. (Verified for all `t < 5000`; no loop needed.)

**Walk `target = 6` by hand.** Build the table bottom-up:

| `t` | `k` | Case 1? | Case 2 | Case 3 (`j = 0 … k−2`) | `dp[t]` |
|---|---|---|---|---|---|
| 1 | 1 | `2^1−1 = 1` ✅ | — | — | **1** (`A`) |
| 2 | 2 | `3 ≠ 2` | `2+1+dp[1] = 4` | `j=0`: `2+0+1+dp[2−1+0] = 3+dp[1] = 4` | **4** (`AARA`) |
| 3 | 2 | `2^2−1 = 3` ✅ | — | — | **2** (`AA`) |
| 4 | 3 | `7 ≠ 4` | `3+1+dp[3] = 6` | `j=0`: `3+0+1+dp[4−3+0] = 4+dp[1] = 5`; `j=1`: `3+1+1+dp[4−3+1] = 5+dp[2] = 9` | **5** (`AARRA`) |
| 5 | 3 | `7 ≠ 5` | `3+1+dp[2] = 8` | `j=0`: `4+dp[2] = 8`; `j=1`: `5+dp[3] = 7` | **7** |
| 6 | 3 | `7 ≠ 6` | `3+1+dp[1] = **5**` | `j=0`: `4+dp[3] = 6`; `j=1`: `5+dp[4] = 10` | **5** |

`dp[6] = 5`, delivered by case 2 — overshoot to 7, reverse, then `dp[1] = 1` more instruction. That's `AAA` + `R` + `A` = **`AAARA`**, exactly the sequence in the problem statement. ✅ And `dp[4] = 5` comes from case 3 with `j = 0`: `AA` (to 3), `R`, zero backward `A`s, `R` (now at 3, speed +1), then `dp[1] = A`. That's `AARRA` — the double reverse that looks like a wasted move is the optimal play.

**Why it's correct — and why the table order is safe.** Every optimal sequence must, at its first turn-around, have executed some run of `A`s from the start, landing on `2^i − 1` for some `i`. Three possibilities: `i = k` and it hits exactly (case 1), `i ≥ k` (case 2 — and `i > k` is strictly worse, since you'd pass `2^k − 1` and still have to come all the way back), or `i ≤ k − 1` (case 3 — and `i < k − 1` is dominated, since stopping even shorter leaves more distance for the same or more instructions). After the turn, symmetry lets us charge the rest to `dp[·]` of the remaining distance.

The recursion is well-founded because **both cases index strictly smaller values**:
- Case 2: `2^k − 1 − t < t`, because `2^(k-1) − 1 < t` implies `2^k − 1 < 2t`.
- Case 3: `t − (2^(k-1) − 1) + (2^j − 1) ≤ t − 2^(k-2)` for `j ≤ k − 2`, which is `< t`.

So a simple ascending loop over `t` always reads entries that are already final.

**Complexity:** Time `O(target · log target)` — `target` values of `t`, each doing at most `k ≤ log₂(target) + 1` work. Space `O(target)`.

---

## ③ Space Optimization

**Already optimal at `O(target)` — and here's the honest reason you can't roll it down.**

The tempting move in a DP section is the rolling window: "I only look back a few cells, so keep two variables." That fails here, and you should be able to say *why* in one sentence: **the subproblems are reached out of order, and the reach is unbounded.** Look at `dp[6]`: it reads `dp[1]` (case 2) and `dp[3]`, `dp[4]` (case 3). `dp[10000]` reads `dp[6383]` and a spray of indices scattered from `dp[1809]` upward. There is no fixed window `[t − c, t)` that covers the dependencies — case 2 jumps to `2^k − 1 − t`, which can be anywhere from `0` to nearly `t`. You genuinely need the whole table live.

```python
# No rolling-variable variant exists. The dependency set of dp[t] is scattered
# across [0, t), not confined to a constant-width window, so every entry
# computed so far can still be read later. O(target) is the floor.
```

What you *can* trim: the BFS's `O(target · log target)` visited set drops to `O(target)` the moment you switch to the DP — that's the real memory win of this problem, and it's worth naming out loud. Going below `O(target)` would mean recomputing entries on demand (memoized recursion with a dictionary), which stores the *reachable* subset rather than all of `[0, target]` — usually smaller in practice, still `O(target)` in the worst case, and slower.

**Complexity:** Time `O(target · log target)`, Space `O(target)`.

---

## Java (for Java interviewers)

`Integer.numberOfLeadingZeros` gives you `bit_length` for free — `32 - nlz(t)` is the smallest `k` with `2^k - 1 >= t`.

```java
public int racecar(int target) {
    int[] dp = new int[target + 1];                    // dp[0] = 0

    for (int t = 1; t <= target; t++) {
        int k = 32 - Integer.numberOfLeadingZeros(t);  // smallest k with 2^k - 1 >= t

        if ((1 << k) - 1 == t) {                       // case 1: lands exactly
            dp[t] = k;
            continue;
        }

        // case 2: overshoot to 2^k - 1, one R, then cover the gap
        dp[t] = k + 1 + dp[(1 << k) - 1 - t];

        // case 3: stop short at 2^(k-1) - 1, R, back up 2^j - 1, R again
        for (int j = 0; j < k - 1; j++) {              // j = 0 .. k-2
            int rest = t - ((1 << (k - 1)) - 1) + ((1 << j) - 1);
            dp[t] = Math.min(dp[t], k + j + 1 + dp[rest]);
        }
    }
    return dp[target];
}
```

And the BFS, for when you want the safe-but-slower answer on the board first:

```java
public int racecarBfs(int target) {
    int limit = 2 * target;
    Set<Long> seen = new HashSet<>();
    Deque<int[]> q = new ArrayDeque<>();
    q.offer(new int[]{0, 1, 0});                       // position, speed, steps
    seen.add(((long) 0 << 20) ^ 100001L);

    while (!q.isEmpty()) {
        int[] cur = q.poll();
        int pos = cur[0], spd = cur[1], steps = cur[2];
        if (pos == target) return steps;               // first pop = shortest
        int[][] nexts = {{pos + spd, spd * 2},         // 'A'
                         {pos, spd > 0 ? -1 : 1}};     // 'R'
        for (int[] nx : nexts) {
            int np = nx[0], ns = nx[1];
            if (np < 0 || np > limit || Math.abs(ns) > limit) continue;
            long key = ((long) np << 20) ^ (ns + 100000L);
            if (seen.add(key)) q.offer(new int[]{np, ns, steps + 1});
        }
    }
    return -1;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Enumerate all instruction strings | O(2^L), L ≈ 30 | O(L) |
| BFS over `(position, speed)` with a `2·target` fence | O(target · log target) | O(target · log target) |
| DP over distance, `dp[t]` | O(target · log target) | O(target) |

*(target ≤ 10^4, so `log target ≈ 14`. Both working solutions run instantly; the DP wins on memory and on not needing a bound you must defend.)*

---

## Say it out loud (interview narration)

> *"Shortest **sequence of instructions** means fewest edges, so my first instinct is BFS — but the node can't just be position, because being at 3 at speed +4 is nothing like being at 3 at speed −1. So the state is `(position, speed)`. Problem: that graph is infinite, so I have to fence it. Let `k` be the smallest exponent with `2^k − 1 ≥ target`; minimality gives `2^(k-1) ≤ target`, so that first milestone past the target is under `2·target`, and going further right is never useful. That fence makes BFS terminate, and it's `O(target log target)`.*
>
> *Now, can I do better than searching? Look at the structure: from a standing start, `k` accelerations always land you exactly on `2^k − 1`. Those are the only sensible turn-around points. And once I turn around, I'm facing a smaller distance from speed 1 again — same problem, smaller input. So let `dp[t]` be the minimum instructions to cover distance `t` from speed +1. Three cases: `2^k − 1` equals `t`, so `dp[t] = k`; or I overshoot to `2^k − 1`, reverse, and pay `dp[2^k − 1 − t]`; or I stop short at `2^(k-1) − 1`, reverse, back up `2^j − 1` for some `j`, reverse again, and pay `dp` of what's left. Both recursive calls are on strictly smaller distances, so a bottom-up loop works. That's `O(target log target)` time and `O(target)` space — and no bound to argue about, because the recursion is exact.*
>
> *One thing I'd flag: I can't roll the DP down to constant space. `dp[t]` reads indices scattered all over `[0, t)`, not a fixed window, so the whole table has to stay live."*

Before you write a line, ask the clarifying question that proves you read the spec: *"Reverse sets the speed to exactly ±1, not just negates it — so a reverse throws away all my accumulated speed, right?"* That's the rule everyone misreads, and it's the reason `RR` (a pure speed reset) is a legitimate optimal move.

## Related / follow-ups
- **Shortest Path in a Grid with Obstacles Elimination (LC 1293)** — the same "BFS is right, but the naive node is too small" lesson; there the extra coordinate is a budget, here it's speed.
- **Open the Lock (LC 752)** — shortest sequence of moves over an abstract state graph; pure BFS with no DP collapse available, a clean contrast for *when* the structure lets you compress.
- **Word Ladder (LC 127)** — the canonical "shortest sequence of transformations = BFS on states" problem. If Race Car felt alien, do this one first.
- **Perfect Squares (LC 279)** — the same duality in miniature: it's a legitimate BFS over remainders *and* a one-dimensional DP over `n`. Solving it both ways is the cheapest way to internalize the collapse this problem demands.
