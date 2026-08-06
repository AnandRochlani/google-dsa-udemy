# Longest String Chain

> **LeetCode:** 1048. Longest String Chain · **Difficulty:** 🟡 Medium · **Pattern:** Dynamic Programming / DP over a hash map (longest chain in an implicit DAG) · **Google frequency:** ⭐ high

*The previous problem asked "can you make a DP transition fast?" This one asks something sneakier: **can you even see that it's a DP?** It arrives dressed as a graph problem — words, edges, longest path — and the whole lesson is the two moves that strip the graph away: sort into dependency order, and **generate** your predecessors instead of hunting for them.*

---

## Problem

You're given a list of `words`. `wordA` is a **predecessor** of `wordB` if you can insert **exactly one character** anywhere into `wordA` — without reordering anything else — and get `wordB`. So `"abc"` is a predecessor of `"abac"`, but not of `"abcd e"`-style reorderings, and never of a word that isn't exactly one character longer.

A **word chain** is a sequence `word_1, word_2, …, word_k` where each word is a predecessor of the next. A single word is a chain of length 1. Return the **length of the longest possible chain** you can build from the given words.

**Example:** `words = ["a","b","ba","bca","bda","bdca"]` → `4` *(the chain `"a" → "ba" → "bda" → "bdca"`; each step inserts one character)*

**Constraints that matter:** `words.length ≤ 1000`, `words[i].length ≤ 16`, lowercase letters only. Two numbers drive every decision here. `N = 1000` means an `O(N²)` pairwise scan is 10⁶ comparisons — survivable, but it's the wrong instinct and it dies instantly if the interviewer bumps `N` to 10⁵. `L ≤ 16` is the real gift: a word only has **16 possible predecessors**, and you can write all of them down. That tiny `L` is the constraint whispering *"stop searching, start generating."*

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** this smells like a graph. Draw an edge `A → B` whenever `A` is a predecessor of `B`, and the answer is the **longest path** in that DAG. That framing is *correct* — say it out loud, it earns credit. But to build the graph you compare every pair of words, and then you need a memoized DFS on top. Two heavyweight phases for a problem whose answer is one number.
- **Where it hurts:** the pair loop. For every word you interrogate all 999 others — "are you one insertion away from me?" — and almost every answer is *no*. Worse, most of those pairs are rejected on the very first check (`len(B) != len(A) + 1`), so we're paying 10⁶ comparisons to discover something the *lengths alone* already told us. We're searching an entire haystack for needles we could have manufactured.
- **The first leap — sort by length.** A chain climbs by exactly one character per step. So if I process words **shortest first**, then by the time I reach a word, every word that could possibly precede it has already been fully solved. That single ordering turns a longest-path-in-a-DAG problem into a plain left-to-right DP with no recursion, no visited set, no topological sort. *Sorting by length **is** the topological order — for free.*
- **The second leap — generate, don't search.** Instead of asking "which of the other 999 words is my predecessor?", ask *"what would my predecessors look like?"* For a word of length `L`, delete character 0, delete character 1, … delete character `L-1`. That's `L` candidate strings — an exhaustive list, because inserting one char into `A` to get `B` is *exactly* the inverse of deleting one char from `B` to get `A`. Then just look each one up in a hash map. `16` lookups instead of `999` comparisons.
- **Pattern trigger:** **when a DP's dependency is "one step smaller," sort into dependency order first — and when the neighbor space is tiny and enumerable, generate the neighbor key instead of scanning for it.** Both halves transfer. The first is why Longest Increasing Subsequence and Largest Divisible Subset both start with a sort. The second is the same reflex behind Word Ladder's `h*t` wildcard buckets: build the key, hit the map.

---

## ① Brute Force

Treat it as a literal graph: compare every ordered pair to build an adjacency list, then memoized-DFS for the longest path.

```python
def longestStrChain_brute(words):
    n = len(words)

    def is_pred(a, b):                       # is `a` a predecessor of `b`?
        if len(b) != len(a) + 1:
            return False
        i = j = 0
        while i < len(a) and j < len(b):     # subsequence check, one skip allowed
            if a[i] == b[j]:
                i += 1
            j += 1
        return i == len(a)

    succ = [[] for _ in range(n)]            # succ[i] = words a chain can step to
    for i in range(n):                       # ── the bottleneck: every pair ──
        for j in range(n):
            if i != j and is_pred(words[i], words[j]):
                succ[i].append(j)

    memo = {}
    def longest_from(i):                     # longest chain STARTING at word i
        if i in memo:
            return memo[i]
        best = 1
        for j in succ[i]:
            best = max(best, 1 + longest_from(j))
        memo[i] = best
        return best

    return max(longest_from(i) for i in range(n))
```

**Why it's the natural first attempt:** "predecessor" literally defines edges, and "longest chain" literally means longest path. This is the honest translation of the English into code, and it produces the right answer.

**Why it's not enough:** the edge-building loop is `O(N² · L)` — with `N = 1000, L = 16` that's ~1.6 × 10⁷ character comparisons just to *discover* the graph, versus ~2.6 × 10⁵ for the whole optimised solution. Roughly 60× the work, before you've computed a single DP value. And it's fragile in two ways an interviewer will poke at: the adjacency list can hold `O(N²)` edges, and the recursive DFS needs a memo plus (in Java) recursion-depth care. Push `N` to 10⁵ — a completely reasonable follow-up — and the pair loop hits 10¹⁰ and dies, while the fix below barely notices.

**Complexity:** Time `O(N² · L)`, Space `O(N²)` for the edges.

---

## ② Optimised Solution

Two moves, both from the intuition. **Sort by length** so predecessors are always already computed, and for each word **generate its `L` predecessors by deletion** and look them up in a dict.

`dp[word]` = the length of the longest chain **ending at** `word`.

```python
def longestStrChain(words):
    words.sort(key=len)              # LEAP 1: shortest first = dependency order
    dp = {}                          # word -> longest chain ending at that word
    best = 0

    for w in words:
        cur = 1                      # a lone word is already a chain of length 1
        for i in range(len(w)):      # LEAP 2: generate all L predecessors
            pred = w[:i] + w[i + 1:] # delete character i
            if pred in dp:           # already solved — it's shorter, so it came first
                cur = max(cur, dp[pred] + 1)
        dp[w] = cur
        best = max(best, cur)

    return best
```

**Walk the example** `["a","b","ba","bca","bda","bdca"]`. Sorted by length: `a, b, ba, bca, bda, bdca`.

| Word | Generated predecessors (delete each char) | Found in `dp`? | `dp[word]` |
|---|---|---|---|
| `a` | `""` | — | **1** |
| `b` | `""` | — | **1** |
| `ba` | `"a"`, `"b"` | `a`→1, `b`→1 | 1 + 1 = **2** |
| `bca` | `"ca"`, `"ba"`, `"bc"` | `ba`→2 | 2 + 1 = **3** |
| `bda` | `"da"`, `"ba"`, `"bd"` | `ba`→2 | 2 + 1 = **3** |
| `bdca` | `"dca"`, `"bca"`, `"bda"`, `"bdc"` | `bca`→3, `bda`→3 | 3 + 1 = **4** |

Answer: `max(dp.values()) = 4` ✅ — the chain `a → ba → bda → bdca`. Notice what never happened: we never compared `"bdca"` against `"xyz"`, or against any other word at all. We manufactured four strings and did four dict lookups. That's the whole optimisation, visible in one row.

**Why it's correct:** two invariants.
1. **Completeness of generation.** `A` is a predecessor of `B` ⟺ `A` is `B` with exactly one character deleted. So the `L` strings we build by deleting each position of `w` are *exactly* the full set of possible predecessors — we can't miss one. (Duplicates among them are harmless; `max` doesn't care.)
2. **Availability.** Every predecessor of `w` has length `len(w) - 1`, strictly shorter, so the length-sort guarantees it was processed earlier and `dp[pred]` is already final. This is the "already solved" precondition that makes a single forward pass legal — no recursion needed.

Together: `dp[w] = 1 + max(dp[p] for valid predecessors p)`, defaulting to 1, is computed correctly for every word, and the longest chain ends *somewhere*, so the answer is the max over all `dp` values.

**Complexity:** Time `O(N log N + N · L²)` — the sort, then per word `L` deletions each costing `O(L)` to slice and hash. With `N=1000, L=16` that's ~2.6 × 10⁵. Space `O(N · L)` for the map — `O(N)` entries.

---

## ③ Space Optimization

Here's a case where the rolling trick from the last lesson **does exist**, but doesn't change the asymptotic answer — and being able to say both halves of that sentence is the point.

A predecessor is always **exactly one character shorter**. So once we've moved on to processing words of length `L+1`, every `dp` entry for length `L-1` and below is dead weight — nothing will ever look it up again. We only need the *immediately previous* length group. That's a real rolling optimisation, exactly like keeping one row of a DP table:

```python
def longestStrChain_rolling(words):
    words.sort(key=len)
    best = 0
    prev, cur = {}, {}               # dp for length L-1 and for length L
    cur_len = -1

    for w in words:
        if len(w) != cur_len:        # entering a new length group
            # predecessors are ALWAYS exactly one shorter, so only the
            # previous group survives; a gap in lengths breaks all chains
            prev = cur if len(w) == cur_len + 1 else {}
            cur = {}
            cur_len = len(w)

        val = 1
        for i in range(len(w)):
            p = w[:i] + w[i + 1:]
            if p in prev:            # look ONLY in the previous length group
                val = max(val, prev[p] + 1)
        cur[w] = val
        best = max(best, val)

    return best
```

**Complexity:** Time `O(N log N + N · L²)`, Space `O(N)` — still.

> **And that's the honest verdict: `O(N)` is the floor, and the rolling version doesn't beat it.** Say why out loud, because it's the interesting part. In the worst case *every* word lives in two adjacent length groups — 500 words of length 8 and 500 of length 9 — and you're holding all 1000 anyway. The rolling trick shrinks the *constant* on inputs with a wide spread of lengths; it cannot shrink the *order*, because a single length group can be the entire input. Can we go below `O(N)`? No: each word needs its own chain length remembered, and `N` of them are independent facts. The win in this problem was never memory — it was killing the `O(N²)` edge set. Naming which optimisation was available and which wasn't is exactly the judgement Google is scoring.

---

## Java (for Java interviewers)

Two Java-specific notes: sort with `Comparator.comparingInt(String::length)` (never `a.length() - b.length()` on untrusted ints, though it's safe here), and build the deleted string with a reusable `StringBuilder` rather than allocating substrings twice per position.

```java
public int longestStrChain(String[] words) {
    Arrays.sort(words, Comparator.comparingInt(String::length));  // dependency order
    Map<String, Integer> dp = new HashMap<>();                    // word -> chain ending here
    int best = 0;

    for (String w : words) {
        int cur = 1;                                   // a lone word is a chain of 1
        StringBuilder sb = new StringBuilder(w);
        for (int i = 0; i < w.length(); i++) {
            char removed = sb.charAt(i);
            sb.deleteCharAt(i);                        // generate predecessor i
            cur = Math.max(cur, dp.getOrDefault(sb.toString(), 0) + 1);
            sb.insert(i, removed);                     // restore for the next deletion
        }
        dp.put(w, cur);
        best = Math.max(best, cur);
    }
    return best;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (pairwise edges + memoized DFS) | O(N² · L) | O(N²) |
| Optimised (length sort + generate predecessors) | O(N log N + N · L²) | O(N · L) ≡ O(N) |
| Space-optimised (roll one length group) | O(N log N + N · L²) | O(N) — same order, smaller constant |

*(N ≤ 1000 words, L ≤ 16 characters per word.)*

---

## Say it out loud (interview narration)

> *"My first framing is a graph: an edge from A to B when A is a predecessor of B, and I want the longest path in that DAG. That works, but building the edges compares every pair — O(N² · L) — and I don't think I need the graph at all. Two observations kill it. First, a chain always grows by exactly one character, so if I sort the words by length, every predecessor of a word is already fully solved by the time I reach it — the sort **is** my topological order, and the DP becomes one forward pass. Second, instead of searching for predecessors I'll generate them: deleting one character from a word gives exactly the set of its possible predecessors, and there are only 16 of them since L ≤ 16. So `dp[word] = 1 + the best dp among those 16 candidates that actually exist in my map`, defaulting to 1, and the answer is the max value in the map. That's O(N log N + N·L²) time and O(N) space. I could roll away all but the previous length group since predecessors are always exactly one shorter — but that's a constant-factor win, not an asymptotic one, since every word could sit in two adjacent length groups."*

Before you code, ask the one clarifying question that proves you read the spec: *"Predecessor means insert exactly one character with **no reordering** — so `"abc"` → `"acb"` doesn't count, right?"* People lose this problem by writing an anagram-ish check. Asking locks the definition before you commit a line.

## Related / follow-ups

- **Longest Increasing Subsequence (LC 300)** — the same skeleton stripped to numbers: sort/scan in dependency order, `dp[i] = 1 + best earlier valid dp`. Do it first if this one felt fast; the `O(n log n)` patience-sort variant is the natural next escalation.
- **Largest Divisible Subset (LC 368)** — the closest twin. Sort ascending so every divisor comes first, then chain on divisibility. Same "sort into dependency order" move, different relation.
- **Maximum Length of Pair Chain (LC 646)** — chain again, but the relation is interval ordering, and here a **greedy** by end-time beats the DP. Great contrast: knowing when the chain problem *doesn't* need DP is its own signal.
- **Solving Questions With Brainpower (LC 2140)** — a linear DP where each state's dependency sits a *computed* distance away, so you iterate right-to-left to guarantee it's ready. Same core lesson as leap 1: **choose the processing order that makes dependencies already-solved**, and the recursion disappears.
- **Word Ladder (LC 127)** — the other half of this lesson's technique. There you generate neighbor keys with a wildcard (`h*t`) instead of scanning the dictionary. Same reflex: **build the key, hit the map.**
