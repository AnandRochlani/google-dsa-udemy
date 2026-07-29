# Similar String Groups

> **LeetCode:** 839. Similar String Groups · **Difficulty:** 🔴 Hard · **Pattern:** Union-Find (DSU) · **Google frequency:** ⭐ high

---

## Problem

You're given a list `strs` where every string is an **anagram** of every other one — same letters, possibly reordered. Call two strings **similar** if they're *equal*, or if you can make them equal by swapping **exactly two** characters in one of them. Group strings that are connected by this similarity (directly or through a chain), and return **how many groups** there are.

"Connected through a chain" is the key: if `A` is similar to `B` and `B` is similar to `C`, then `A`, `B`, and `C` all live in the same group — even if `A` and `C` aren't similar to each other directly. That's a **connected-components** question in disguise.

**Example:** `strs = ["tars","rats","arts","star"]` → `2`

- `tars` ↔ `rats` — swap positions 0 and 2 (`t`↔`r`) → similar.
- `rats` ↔ `arts` — swap positions 0 and 1 (`r`↔`a`) → similar.
- `star` is similar to none of them (differs in all 4 spots from each).

So `{tars, rats, arts}` chain together into one group, `{star}` is alone → **2 groups**.

`strs = ["omv","ovm"]` → `1` *(swap the last two chars → equal → one group)*.

**Constraints that matter:** `1 <= strs.length (n) <= 300`, each word length `1 <= m <= 300`, all lowercase, all anagrams of each other. `n` is small enough that an `O(n²)` pass over all pairs is fine — `300² = 90,000`. The real decision is **how you compare two strings** and **how you track the groups without an explicit graph**. That's what pushes this toward Union-Find.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Build a graph. Put an edge between every pair of similar strings, then count connected components with DFS or BFS." That's completely correct — and it's the honest starting point. Comparing all pairs is `O(n²)` comparisons, and each comparison walks the `m` characters, so `O(n² · m)` to discover the edges.
- **Where it hurts:** the *graph itself*. To flood-fill components you built an adjacency list — up to `O(n²)` edges of storage — plus a visited array plus a recursion/queue. You're materializing the entire relationship graph just to answer one number: *how many blobs?* You never need the edges again after you've merged two nodes.
- **The leap:** you don't need the graph. You need **"are these two already in the same blob, and if not, merge them."** That's *exactly* the two operations Union-Find gives you — `find` (which blob?) and `union` (merge two blobs) — in near-constant amortized time, using a single `parent` array of size `n`. Start with `n` groups; every time you union two strings that weren't already together, groups drop by one. The count falls out for free.
- **Pattern trigger:** **"count connected components / group things by an equivalence relation, and I only ever ask *same group?* and *merge*"** → **Union-Find (Disjoint Set Union)**. The transferable move: when the *edges are disposable* and you only care about *membership*, skip the graph and reach for DSU. It turns `O(n²)` edge storage into `O(n)`.

---

## ① Brute Force

Build the similarity graph explicitly (adjacency list), then DFS from each unvisited node to count connected components.

```python
def num_similar_groups_brute(strs):
    n = len(strs)

    def similar(a, b):
        # anagrams: they're similar iff they differ in 0 or exactly 2 spots
        diff = 0
        for x, y in zip(a, b):
            if x != y:
                diff += 1
                if diff > 2:            # early exit — can't be a single swap
                    return False
        return diff == 0 or diff == 2

    # 1. materialize every edge
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if similar(strs[i], strs[j]):
                adj[i].append(j)
                adj[j].append(i)

    # 2. flood-fill to count components
    seen = [False] * n
    groups = 0
    for start in range(n):
        if seen[start]:
            continue
        groups += 1
        stack = [start]
        seen[start] = True
        while stack:
            node = stack.pop()
            for nxt in adj[node]:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append(nxt)
    return groups
```

**Why it's the natural first attempt:** "similar strings = edges, count the blobs" is the textbook connected-components recipe. It's correct and it reads clearly.

**Why it's not enough:** it *works*, but it hoards an adjacency list that can hold up to `O(n²)` edges (a fully-similar input makes a complete graph), plus the visited array and the DFS stack. You built the whole graph only to throw it away after counting. The edges are scaffolding — and the scaffolding is bigger than the answer.

**Complexity:** Time `O(n² · m)` (all pairs × char compare), Space `O(n²)` for the adjacency list in the worst case.

---

## ② Optimised Solution

Same `O(n² · m)` pairwise comparison — but replace the graph + DFS with **Union-Find**. No adjacency list, no visited array: just a `parent` array and a running group count.

```python
def num_similar_groups(strs):
    n = len(strs)
    parent = list(range(n))          # each string starts in its own group
    rank = [0] * n                   # tree-height hint for balanced unions

    def find(x):                     # root of x's group, with path compression
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # halve the path as we climb
            x = parent[x]
        return x

    def union(a, b):                 # merge; return True only if they were apart
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:      # attach shorter tree under taller
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        return True

    def similar(a, b):
        diff = 0
        for x, y in zip(a, b):
            if x != y:
                diff += 1
                if diff > 2:         # third mismatch → not one swap → bail
                    return False
        return diff == 0 or diff == 2

    groups = n                       # start: everyone is their own island
    for i in range(n):
        for j in range(i + 1, n):
            if similar(strs[i], strs[j]) and union(i, j):
                groups -= 1          # a real merge shrinks the group count
    return groups
```

**Walk the example** `strs = ["tars","rats","arts","star"]` (index them `0,1,2,3`):

| Pair | `similar?` (diffs) | `union` did work? | `parent` after | `groups` |
|---|---|---|---|---|
| start | — | — | `[0,1,2,3]` | 4 |
| (0,1) `tars`/`rats` | diff at 0,2 → **yes** | merge → yes | `[0,0,2,3]` | 3 |
| (0,2) `tars`/`arts` | diff at 0,1,2 → no | — | `[0,0,2,3]` | 3 |
| (0,3) `tars`/`star` | diff at all 4 → no | — | `[0,0,2,3]` | 3 |
| (1,2) `rats`/`arts` | diff at 0,1 → **yes** | merge (1→0, 2→0) → yes | `[0,0,0,3]` | 2 |
| (1,3) `rats`/`star` | diff 4 → no | — | `[0,0,0,3]` | 2 |
| (2,3) `arts`/`star` | diff 4 → no | — | `[0,0,0,3]` | 2 |

Final answer **2** — `{0,1,2}` rooted at `0`, and `{3}` alone. ✅

**Why it's correct:** `similar` counts differing positions and accepts only `0` or `2`. That's precisely the "at most one swap makes them equal" rule — a swap touches exactly two indices, so equal strings (0 diffs) or a single-swap pair (2 diffs) qualify, and nothing else does. Union-Find then maintains the invariant that *two strings share a root iff they're in the same component*: `find` collapses each string to its group's representative, and `union` only decrements `groups` when it genuinely joins two previously-separate roots — so double-counting a pair (like a redundant edge) can never over-merge. Path compression + union by rank keep every `find`/`union` at `O(α(n))`, effectively constant.

> **"Why 0 or 2 differing positions — never exactly 1?"** Because the strings are **anagrams**. If they differed in *exactly one* position, one string would have some letter `X` there and the other a different letter `Y`, while every *other* position matched. That means one string has an extra `X` and is missing a `Y` compared to the other — their letter multisets differ — so they *couldn't* be anagrams. Contradiction. A single mismatch is impossible; the smallest non-zero difference between two anagrams is **two** positions (the two endpoints of a swap). *(Note: anagrams can still differ in more than two spots — e.g. `abc` vs `bca` differ in 3 — those just aren't "similar," they'd need multiple swaps.)*

**Complexity:** Time `O(n² · m)`, Space `O(n)` — just `parent` and `rank`.

---

## ③ Space Optimization

The Union-Find version **already is** the space optimization over the brute force: it dropped the `O(n²)` adjacency graph down to two `O(n)` arrays. There's nothing below `O(n)` to chase — you must remember which group each of the `n` strings belongs to, and that's `n` slots by definition.

But there's a **time** trade worth knowing, because Google likes the "which approach, and why" conversation. There are two ways to find the similar pairs:

- **(A) Compare every pair directly** — `O(n² · m)`. What we did above. Best when the words are **long** (`m` large) relative to how many of them there are.
- **(B) Generate the swaps of each word** — for word length `m`, every string has only `C(m,2) = O(m²)` possible single-swap neighbors. Put all words in a hash map; for each word, generate its `O(m²)` swapped variants and union it with any variant that exists in the map. That's `O(n · m² · m) = O(n · m³)` (each variant costs `O(m)` to build and hash). Best when the words are **short** (`m` small).

```python
def num_similar_groups_swaps(strs):
    # Alternative pair-finding: enumerate swaps instead of comparing all pairs.
    # Faster than (A) when m is small — precisely when m^2 < n.
    n = len(strs)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
        return True

    first = {}                       # distinct word -> its first index
    groups = n
    for i, w in enumerate(strs):
        if w in first:               # identical string → already similar
            if union(i, first[w]):
                groups -= 1
            continue
        first[w] = i
        chars = list(w)
        m = len(chars)
        for p in range(m):           # try every single swap of this word
            for q in range(p + 1, m):
                if chars[p] == chars[q]:
                    continue         # swapping equal chars yields the same word
                chars[p], chars[q] = chars[q], chars[p]
                cand = "".join(chars)
                if cand in first and union(i, first[cand]):
                    groups -= 1
                chars[p], chars[q] = chars[q], chars[p]   # swap back
    return groups
```

**When to pick which:** compare the exponents. (A) is `O(n² · m)`, (B) is `O(n · m³)`. Divide: (B)/(A) `= m² / n`. So **(B) wins when `m² < n`** (short words, many of them); **(A) wins when the words are long.** With LC 839's caps (`n, m ≤ 300`) either passes — but *stating this trade-out loud* is the senior move.

**Complexity:** (A) Time `O(n² · m)`, Space `O(n)`. (B) Time `O(n · m³)`, Space `O(n)` (plus the hash map of words).

> Say it out loud: *"Space is `O(n)` — I only need one `parent` array to remember group membership; there's no graph to store. For time I've got two choices for finding the pairs, and I'd pick based on whether the words are long or short."*

---

## Java (for Java interviewers)

```java
class Solution {
    private int[] parent, rank;

    public int numSimilarGroups(String[] strs) {
        int n = strs.length;
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;   // each its own group

        int groups = n;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (similar(strs[i], strs[j]) && union(i, j)) {
                    groups--;                         // a real merge shrinks count
                }
            }
        }
        return groups;
    }

    // anagrams: similar iff they differ in exactly 0 or 2 positions
    private boolean similar(String a, String b) {
        int diff = 0;
        for (int k = 0; k < a.length(); k++) {
            if (a.charAt(k) != b.charAt(k)) {
                if (++diff > 2) return false;         // third mismatch → not one swap
            }
        }
        return diff == 0 || diff == 2;
    }

    private int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];            // path compression
            x = parent[x];
        }
        return x;
    }

    private boolean union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return false;                   // already together
        if (rank[ra] < rank[rb]) { int t = ra; ra = rb; rb = t; }
        parent[rb] = ra;
        if (rank[ra] == rank[rb]) rank[ra]++;
        return true;
    }
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (build graph + DFS) | O(n² · m) | O(n²) |
| Union-Find, pairwise compare (primary) | O(n² · m) | O(n) |
| Union-Find, swap-generation (m small, m² < n) | O(n · m³) | O(n) |

*(n = number of strings, m = length of each string. Union/find are `O(α(n))` — amortized near-constant.)*

---

## Say it out loud (interview narration)

> *"This is a connected-components problem: 'similar' defines edges, and I need the number of blobs. The clarifying question I'd ask first — 'the strings are all anagrams of each other, right?' — because that's what makes 'similar' clean: two anagrams can never differ in exactly one position, so 'differs in exactly two spots' is precisely 'one swap apart.' My first idea is build the graph and DFS, but that stores up to O(n²) edges I throw away. So instead I reach for Union-Find: a `parent` array, `find` with path compression, `union` by rank. I start with n groups and drop the count by one on every genuine merge. Comparing all pairs is O(n²·m), and the DSU makes the bookkeeping O(n) space and near-constant per operation. If the words were short I'd mention the swap-generation alternative — O(n·m³) — which wins when m² is under n."*

Leading with that anagram clarifying question, then narrating brute-force → why-it-wastes-space → Union-Find, is exactly the **GCA (General Cognitive Ability)** signal Google's rubric rewards — they score *how you reason toward the answer*, not just the final code.

## Related / follow-ups
- **Number of Provinces (LC 547)** — the same "count connected components with Union-Find" skeleton, edges given as a matrix.
- **Accounts Merge (LC 721)** — DSU where you union by shared emails; the grouping payoff is bigger.
- **Number of Islands (LC 200)** — components on a grid; DFS or DSU, great contrast to this one.
- **Redundant Connection (LC 684)** — DSU where the *first union that fails* is the answer.
- **Sentence Similarity II (LC 737)** — union words by given similar-pairs, then query transitively.
