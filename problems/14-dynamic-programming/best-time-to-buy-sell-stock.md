# Best Time to Buy and Sell Stock (I & II)

> **LeetCode:** 121. Best Time to Buy and Sell Stock (one transaction) & 122. Best Time to Buy and Sell Stock II (unlimited) · **Difficulty:** 🟢 Easy / 🟡 Medium · **Pattern:** Dynamic Programming · **Google frequency:** ⭐ high

---

## Problem

You're given `prices`, where `prices[i]` is the stock price on day `i`.

- **LC 121 — one transaction:** buy on one day, sell on a **later** day, at most **once**. Return the max profit (0 if no profit is possible).
- **LC 122 — unlimited transactions:** buy and sell as many times as you like (but hold at most one share at a time — you must sell before buying again). Return the max total profit.

**Example (121):** `prices = [7, 1, 5, 3, 6, 4]` → `5`. Buy at 1 (day 1), sell at 6 (day 4).
**Example (122):** `prices = [7, 1, 5, 3, 6, 4]` → `7`. Buy 1→sell 5 (+4), buy 3→sell 6 (+3), total 7.
**Example (122):** `prices = [1, 2, 3, 4, 5]` → `4`. One clean run 1→5, or equivalently sum every up-step.

**Constraints that matter:** `1 ≤ prices.length ≤ 10⁵`. `O(n²)` (try every buy/sell pair) times out — you need a single `O(n)` pass with `O(1)` extra space.

---

## 🧠 Intuition — how you'd actually arrive at this

Both problems are DP over "what state am I in each day," and both collapse to a one-pass scan. Let's walk the discovery for each.

### LC 121 — at most one transaction

**(a) The decision.** Profit from selling on day `i` is `prices[i] - (min price before i)`. So on each day, you either **sell today** (locking in `today - cheapest-so-far`) or you don't. The best answer is the max over all sell days.

**(b) Overlapping work.** Brute force recomputes "the min price before day i" for every `i` — that's the repeated work.

**(c–e) Collapse.** You don't need a table at all: sweep left to right carrying **one variable** `min_price` (cheapest day seen so far) and one `best`. Each day, update `best = max(best, price - min_price)`, then `min_price = min(min_price, price)`. **O(n) time, O(1) space.**

> **State (DP view):** `dp[i]` = max profit achievable by selling on or before day `i`. `dp[i] = max(dp[i-1], prices[i] - minSoFar)`. Collapses to two scalars.

### LC 122 — unlimited transactions

**(a) The decision each day: hold or don't.** Model two states: `cash` = max money if I hold **no** share today; `hold` = max money if I **do** hold a share today.
- `cash` today = better of (stay in cash) or (sell the share I held): `max(cash, hold + price)`.
- `hold` today = better of (keep holding) or (buy today from cash): `max(hold, cash - price)`.

**(b) Overlapping subproblems / (c–d).** This is the classic **state-machine DP**: `dp[i][0/1]` for not-holding / holding on day `i`. Each depends only on day `i-1`.

**(e) Collapse to two rolling scalars** `cash`, `hold`. **O(n) time, O(1) space.**

**The famous shortcut for 122:** because there's no transaction limit, the state machine's answer equals simply **summing every positive day-to-day increase** — grab every uphill step. `sum(max(0, prices[i] - prices[i-1]))`. (This does *not* work for 121, which is capped at one transaction — that's why the two problems live together, to sharpen the distinction.)

> **State (122):** `cash[i]` / `hold[i]` = best profit not-holding / holding at end of day `i`. `cash = max(cash, hold + p)`, `hold = max(hold, cash - p)`. Answer `cash`.

---

## ① Brute Force

**LC 121 — try every buy/sell pair:**

```python
def max_profit_one_brute(prices):
    best = 0
    n = len(prices)
    for buy in range(n):
        for sell in range(buy + 1, n):
            best = max(best, prices[sell] - prices[buy])
    return best
```

**Why it's the natural first attempt:** the definition is literally "best (sell − buy) over all buy < sell."

**Why it's not enough:** `O(n²)` pairs — ~10¹⁰ at n = 10⁵ → **TLE**. It recomputes "cheapest buy before each sell" from scratch every time.

**Complexity:** Time `O(n²)`, Space `O(1)`.

---

## ② Optimised Solution

**LC 121 — one pass, track the running minimum:**

```python
def max_profit_one(prices):
    min_price = float('inf')
    best = 0
    for p in prices:
        best = max(best, p - min_price)   # sell today at best-so-far buy
        min_price = min(min_price, p)     # update cheapest buy day
    return best
```

**Walk** `[7, 1, 5, 3, 6, 4]`:

| price | min_price (before) | p − min | best |
|---|---|---|---|
| 7 | ∞ | — | 0 |
| 1 | 7 | −6 | 0 |
| 5 | 1 | 4 | 4 |
| 3 | 1 | 2 | 4 |
| 6 | 1 | 5 | **5** |
| 4 | 1 | 3 | 5 |

Answer `5`. ✅

**LC 122 — state machine (cash / hold):**

```python
def max_profit_many(prices):
    cash, hold = 0, float('-inf')         # start: no share, or "impossible" hold
    for p in prices:
        cash = max(cash, hold + p)        # sell today (or stay in cash)
        hold = max(hold, cash - p)        # buy today (or keep holding)
    return cash
```

**Why it's correct:** each day the two states capture the only two positions (holding / not), each transition is the best of "act" vs "wait," and every future decision depends only on today's two values — so the greedy-looking scan is provably optimal.

**Complexity:** Time `O(n)`, Space `O(1)` (both).

---

## ③ Space Optimization

Both are **already O(1) space** — and that's the teaching point: state-machine DPs whose transitions only reference **yesterday** never need a table, just a fixed set of rolling scalars.

For **122**, the state machine simplifies to the one-liner "sum the uphills," which is the same O(1):

```python
def max_profit_many_greedy(prices):
    return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))
```

`[7,1,5,3,6,4]` → up-steps are `(1→5)=4` and `(3→6)=3`, sum `7`. ✅ Every profitable segment `a→b→c` (increasing) telescopes: `(b−a)+(c−b) = c−a`, so summing adjacent gains equals doing the big trades — no transaction limit means you can decompose freely.

> Say it out loud: *"For 121 I keep a running min and best — O(1). For 122 there's no cap, so I take every uphill move; that's equivalent to the cash/hold state machine but reads as a one-liner. Both are O(n) time, O(1) space — no DP table needed because each day only looks at yesterday."*

**Complexity:** Time `O(n)`, Space `O(1)`.

---

## Java (for Java interviewers)

```java
// LC 121 — at most one transaction
public int maxProfit(int[] prices) {
    int minPrice = Integer.MAX_VALUE, best = 0;
    for (int p : prices) {
        best = Math.max(best, p - minPrice);
        minPrice = Math.min(minPrice, p);
    }
    return best;
}

// LC 122 — unlimited transactions
public int maxProfitII(int[] prices) {
    int profit = 0;
    for (int i = 1; i < prices.length; i++) {
        if (prices[i] > prices[i - 1]) {
            profit += prices[i] - prices[i - 1];
        }
    }
    return profit;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (all pairs, 121) | O(n²) | O(1) |
| One-pass min tracking (121) | O(n) | O(1) |
| State machine / sum-of-uphills (122) | O(n) | O(1) |

---

## Say it out loud (interview narration)

> *"For one transaction, I sweep once keeping the cheapest price seen and the best profit if I sold today — O(n), O(1). For unlimited transactions, I model two states each day, holding or not: cash = max(cash, hold+price), hold = max(hold, cash−price). With no transaction cap that's the same as just adding up every day-over-day price increase, so it's a clean one-liner. Both are linear time and constant space, since each day only depends on the previous."*

## Related / follow-ups
- **Best Time to Buy and Sell Stock III** (at most **2** transactions — 4-state DP)
- **Best Time to Buy and Sell Stock IV** (at most **k** transactions — 2-D DP over k and day)
- **With Cooldown (309)** (add a "rest" state after selling)
- **With Transaction Fee (714)** (subtract a fee on each sell in the cash transition)
