# Coin Change

> **LeetCode:** 322. Coin Change · **Difficulty:** 🟡 Medium · **Pattern:** Dynamic Programming (Unbounded Knapsack) · **Google frequency:** ⭐ high

---

## Problem

Given coin denominations `coins` (infinite supply of each) and an `amount`, return the **fewest number of coins** that sum to `amount`. If it's impossible, return `-1`.

**Example:** `coins = [1, 2, 5]`, `amount = 11` → `3`. Because `11 = 5 + 5 + 1`.

**Example:** `coins = [2]`, `amount = 3` → `-1`. No combination of 2s makes 3.

**Constraints that matter:** `1 ≤ amount ≤ 10⁴`, `coins.length ≤ 12`. Greedy ("always take the biggest coin") is **wrong** — for `coins = [1, 3, 4]`, `amount = 6`, greedy takes `4 + 1 + 1 = 3 coins` but the optimum is `3 + 3 = 2 coins`. You need DP.

---

## 🧠 Intuition — how you'd actually arrive at this

**(a) Find the decision at each step.** To make `amount`, your **last coin** was one of the denominations. If the last coin was `c`, then the rest must optimally make `amount - c`. You don't know which last coin is best, so try them all and take the minimum:

> **minCoins(a) = 1 + min over c in coins of minCoins(a - c)**   (for each `c ≤ a`)

Base: `minCoins(0) = 0` (zero coins make amount 0). If no coin leads to a solution, it's `-1` (represent as ∞ while computing).

**(b) Notice overlapping subproblems.** `minCoins(11)` needs `minCoins(10), minCoins(9), minCoins(6)`; `minCoins(10)` again needs `minCoins(9)`… the same amounts get recomputed across branches. Exponential blow-up → DP signal.

**(c) Add memoization (top-down).** Cache `minCoins(a)` by amount. Now each of the `amount+1` distinct amounts is solved once, each doing `O(len(coins))` work.

**(d) Convert to a bottom-up table.** Build `dp[a]` for `a = 0 … amount`, where `dp[a]` = fewest coins to make `a`. Initialize `dp[0] = 0` and everything else to ∞. For each amount, try every coin:
`dp[a] = min(dp[a], dp[a - c] + 1)` for every coin `c ≤ a`.

**(e) Space.** Here the table **is already 1-D** — `dp` has `amount+1` entries and each depends on smaller indices, so you can't collapse it to O(1); every earlier amount can still be needed. `O(amount)` space is the floor. (This is the honest answer for this problem — see ③.)

**State & recurrence (memorize this):**
- **State:** `dp[a]` = minimum coins to form amount `a`.
- **Recurrence:** `dp[a] = min(dp[a - c] + 1)` over all coins `c ≤ a`.
- **Base:** `dp[0] = 0`; unreachable amounts stay ∞ → return `-1`.

This is the **unbounded knapsack** shape: each coin reusable any number of times.

---

## ① Brute Force

Recurse on "which coin did I use last," trying every coin at every amount, no caching.

```python
def coin_change_brute(coins, amount):
    def helper(rem):
        if rem == 0:
            return 0
        if rem < 0:
            return float('inf')
        best = float('inf')
        for c in coins:
            best = min(best, helper(rem - c) + 1)
        return best
    ans = helper(amount)
    return ans if ans != float('inf') else -1
```

**Why it's the natural first attempt:** it directly asks "for each possible last coin, how few coins make the remainder?"

**Why it's not enough:** the recursion tree branches `len(coins)` ways at each level and depth up to `amount`, so it's exponential (`O(len(coins)^amount)`), recomputing the same remainders endlessly.

**Complexity:** Time `O(coins^amount)`, Space `O(amount)` (stack).

---

## ② Optimised Solution

Bottom-up table over amounts `0 … amount`.

```python
def coin_change(coins, amount):
    dp = [0] + [float('inf')] * amount   # dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != float('inf') else -1
```

**A small filled table** for `coins = [1, 2, 5]`, `amount = 11`:

| a | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dp[a] | 0 | 1 | 1 | 2 | 2 | 1 | 2 | 2 | 3 | 3 | 2 | 3 |

E.g. `dp[11] = min(dp[10]+1, dp[9]+1, dp[6]+1) = min(3, 4, 3) = 3`. ✅

**Why it's correct:** `dp[a]` considers every possible last coin `c` and adds 1 to the already-optimal `dp[a-c]`. Since all smaller amounts are finalized before `a`, the min over last-coin choices is globally optimal for `a`.

**Complexity:** Time `O(amount × len(coins))`, Space `O(amount)`.

---

## ③ Space Optimization

**The honest DP answer: it's already at the space floor — say so and explain why.** The table is a single 1-D array of length `amount + 1`, and `dp[a]` can depend on `dp[a-c]` for *any* coin `c`, which reaches as far back as `amount - min(coin)`. Unlike Fibonacci-style problems, the dependency window isn't a fixed constant — it spans the whole array — so you **cannot** collapse it to O(1) rolling variables. Every earlier amount may still be needed.

> *"Space is O(amount) and that's the floor here — a coin can be as small as 1, so dp[a] may reference all the way back to dp[0]. There's no fixed-size window to slide, unlike Climbing Stairs."*

One genuine micro-optimization: loop coins on the **outer** loop and amounts inner — same O(amount·coins) time and O(amount) space, but it's the exact template you reuse for the *count-combinations* variant (Coin Change II), so it's worth knowing:

```python
def coin_change(coins, amount):
    dp = [0] + [float('inf')] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

**Complexity:** Time `O(amount × len(coins))`, Space `O(amount)`.

---

## Java (for Java interviewers)

```java
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);   // sentinel for "infinity"
    dp[0] = 0;
    for (int a = 1; a <= amount; a++) {
        for (int c : coins) {
            if (c <= a) {
                dp[a] = Math.min(dp[a], dp[a - c] + 1);
            }
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (recursion) | O(coins^amount) | O(amount) |
| Memoized (top-down) | O(amount × coins) | O(amount) |
| Tabulated (bottom-up) | O(amount × coins) | O(amount) |
| Space-optimised | O(amount × coins) | O(amount) — already the floor |

---

## Say it out loud (interview narration)

> *"Greedy fails — [1,3,4] making 6 is 3+3, not 4+1+1. The real question is: what was my last coin? For each coin c, the answer is 1 + fewest coins for amount − c, and I take the min. Naive recursion recomputes remainders exponentially, so I tabulate dp[0..amount] in O(amount × coins). I can't shrink below O(amount) space because a coin of 1 means dp[a] can reach all the way back to dp[0] — there's no fixed window to roll."*

## Related / follow-ups
- **Coin Change II** (count *combinations* instead of minimizing — coins on the outer loop to avoid double-counting)
- **Perfect Squares** (same unbounded knapsack; "coins" are 1, 4, 9, 16, …)
- **Combination Sum IV** (count ordered sequences — amounts outer, coins inner)
- **Minimum Cost for Tickets** (knapsack-flavoured DP over days)
