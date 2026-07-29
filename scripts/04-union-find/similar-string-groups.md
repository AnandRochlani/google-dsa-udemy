# 🎬 Recording Script — Similar String Groups
**Pattern: Union-Find · LeetCode 839 · Hard · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** you've counted connected components before (Number of Islands) — here the "grid" is a pile of scrambled words, and the edges are invisible.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: four word-tiles drop onto a dark screen — `tars` `rats` `arts` `star`. Faint dotted lines flicker between some of them, then vanish.]**

> Four words. All the same letters, just shuffled. The interviewer says: *"Two words are friends if you can swap two letters in one and get the other. Friends-of-friends count too. How many friend-groups are there?"*
>
> Your brain screams **"build a graph!"** — and you're not wrong. But watch: you'll spend all your effort storing edges you throw away three seconds later. By the end of this video you'll count those groups with **one array** and no graph at all. That's Union-Find. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below, the four tiles with their indices `0 1 2 3`.]**

```
0: tars   1: rats   2: arts   3: star
```

> The whole problem in one line: **group the strings where each is one swap away from another — directly or through a chain — and count the groups.**
>
> Every word here is an **anagram** of the others — same letters, reordered. Hold onto that word "anagram," it's going to save us later.
>
> The answer for these four is **two**. Don't chase it yet — just park it: two groups.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the shape)*

**[VISUAL: the four tiles. As we compare a pair, arrows light up and a "diffs" badge counts mismatched positions.]**

> Let's do what the brain does first: check every pair, and if they're "similar," draw an edge.
>
> `tars` vs `rats` — line them up: `t·a·r·s` over `r·a·t·s`. Position 0 differs, position 2 differs. **Two** mismatches. One swap fixes it → **edge.**
>
> **[VISUAL: green edge 0—1.]**
>
> `rats` vs `arts` — `r·a·t·s` over `a·r·t·s`. Positions 0 and 1 differ. Two mismatches → **edge.**
>
> **[VISUAL: green edge 1—2.]**
>
> `tars` vs `star` — every single position differs. Four mismatches. That's *not* one swap → no edge. Same story for `star` against everyone.
>
> **[VISUAL: `star` sits alone, no lines. The other three form a connected chain 0—1—2.]**
>
> So `{tars, rats, arts}` chain into one blob, `star` is its own. Two groups. To *count* blobs I'd now DFS the graph… but hold on.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The adjacency list balloons on the right — arrays of neighbors, a visited[] array, a DFS stack — all glowing, then a red "wait…" stamp. A 4-second 🤔 timer.]**

> **TEACHER:** Look at everything I just built to answer one number. An adjacency list — up to `n²` edges if every word is similar to every other. A visited array. A DFS stack. All of it… scaffolding. Once I've merged two words into a blob, I never look at that edge again.
>
> **LEARNER:** But that's just how you count connected components, right? Graph, then DFS. What else *is* there?
>
> **TEACHER:** That's the exact question. Here's your think: I only ever ask two things — *"are these two already in the same blob?"* and *"merge them."* Pause the video. If those are the **only** two operations I need… do I actually need the graph at all?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: each word-tile gets a tiny "points-to" arrow. At first every tile points at itself.]**

> **TEACHER:** Here's the move. Forget edges. Give every word a single pointer that says *"my group's leader is…"* — and at the start, everyone is their own leader. Four words, four groups.
>
> Think of it like people at a party finding their friend-circles. To merge two circles, the two leaders just shake hands — one becomes the other's leader. Done. To ask *"same circle?"*, you follow the chain of leaders up to the top and see if you land on the same person.
>
> **[VISUAL: `tars` and `rats` are similar → `rats`'s arrow re-points to `tars`. Group count ticks 4 → 3.]**
>
> `tars` and `rats` are similar → point one at the other. Two circles became one. **Every time two separate circles merge, the total group count drops by one.** That's the whole counter.
>
> **[VISUAL: `arts` similar to `rats` → follow `rats` up to leader `tars`, re-point `arts` to `tars`. Count 3 → 2.]**
>
> **LEARNER:** Wait — when `arts` merges in, why doesn't the count drop *again* if I also compare it to `tars` later? Won't I double-count the merge?
>
> **TEACHER:** Beautiful worry. It *won't*, and that's the safety of this structure: before merging, I check if they already share a leader. `arts` and `tars` will already be in the same circle by then — the handshake is skipped, the counter doesn't move. **A merge only counts when it truly joins two separate circles.** That's the invariant that keeps us honest.
>
> This structure has a name: **Union-Find**, also called Disjoint Set Union. One array of leaders. Two operations: `find` the leader, `union` two circles.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "start with n groups; every real union drops the count by 1."]**

> Burn this in: **start with n groups, and every union that joins two *different* circles drops the count by one. The number left is your answer.**
>
> No graph. No DFS. No visited array. One `parent` array of size `n`, and a counter. That's Union-Find's whole gift: when the edges are disposable and you only care about *membership*, you skip the graph entirely.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, everyone is their own leader — `parent[i] = i`. And a `rank` array to keep the trees short when we merge.

```python
def num_similar_groups(strs):
    n = len(strs)
    parent = list(range(n))      # each string starts as its own group leader
    rank = [0] * n               # tree-height hint for balanced merges
```

> **[VISUAL: add chunk 2, highlight it.]** Now `find` — climb to the leader. And as we climb, we flatten the path so next time it's instant.

```python
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path compression: halve the chain
            x = parent[x]
        return x
```

> **[VISUAL: add chunk 3.]** `union` — find both leaders; if they already match, do nothing and say so. Otherwise hang the shorter tree under the taller.

```python
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False                    # already same circle → no merge
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra                 # attach smaller under larger
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        return True
```

> **[VISUAL: add chunk 4, highlight the `diff > 2` bail.]** The similarity test — count mismatched positions, bail the instant we hit a third.

```python
    def similar(a, b):
        diff = 0
        for x, y in zip(a, b):
            if x != y:
                diff += 1
                if diff > 2:                # a third mismatch → not one swap
                    return False
        return diff == 0 or diff == 2
```

> **[VISUAL: add chunk 5, highlight `groups -= 1`.]** Now the driver: start at `n` groups, compare all pairs, and drop the count on every real merge.

```python
    groups = n
    for i in range(n):
        for j in range(i + 1, n):
            if similar(strs[i], strs[j]) and union(i, j):
                groups -= 1
    return groups
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `return diff == 0 or diff == 2` — this is the heart of "similar." Equal strings are 0 diffs. A single swap touches exactly two positions → 2 diffs. Nothing else qualifies.
>
> **LEARNER:** Hang on — why `0 or 2`, but never *exactly 1*? Couldn't two words differ in just one spot?
>
> **TEACHER:** Not these words — and this is where "anagram" pays off. If two anagrams differed in *exactly one* position, one would have some letter `X` there and the other a different letter `Y`, with everything else identical. That means one word has an extra `X` and is missing a `Y` — their letter bags don't match — so they *couldn't* be anagrams. Contradiction. The smallest non-zero gap between two anagrams is **two** — the two ends of a swap. So "exactly 1" is simply impossible here.
>
> **LEARNER:** Then why bail at `diff > 2` — couldn't a valid pair differ in more?
>
> **TEACHER:** No — *similar* means **one** swap, and one swap moves exactly two letters. Anagrams can differ in more spots — `abc` and `bca` differ in three — but those need multiple swaps, so they're not similar. The moment we see a third mismatch, we're done: bail early, save the rest of the scan.
>
> `if ra == rb: return False` — the double-count guard. If they already share a leader, we merged them before; `groups` must not move.
>
> `parent[x] = parent[parent[x]]` — path compression. Every `find` flattens the chain, so leaders stay one hop away. With union-by-rank, that's what makes each operation amortized `O(α(n))` — basically constant.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: the four tiles with leader-arrows; a trace table filling row by row. `parent` shown as an array.]**

> Let's run the real code on `["tars","rats","arts","star"]`. `groups` starts at **4**, `parent = [0,1,2,3]`.

| Pair | diffs | union does work? | parent after | groups |
|---|---|---|---|---|
| (0,1) tars/rats | 0,2 → **2** | yes → merge | `[0,0,2,3]` | 3 |
| (0,2) tars/arts | 0,1,2 → 3 | not similar | `[0,0,2,3]` | 3 |
| (0,3) tars/star | 4 | not similar | `[0,0,2,3]` | 3 |
| (1,2) rats/arts | 0,1 → **2** | yes → merge | `[0,0,0,3]` | 2 |
| (1,3) rats/star | 4 | not similar | `[0,0,0,3]` | 2 |
| (2,3) arts/star | 4 | not similar | `[0,0,0,3]` | 2 |

> Final: `parent = [0,0,0,3]`. Words 0, 1, 2 all climb to leader `0`; word 3 stands alone. **Two groups** — exactly the number we parked at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute (graph+DFS): Time O(n²·m), Space O(n²). Ours (Union-Find): Time O(n²·m), Space O(n). A note: "union/find ≈ O(α(n)) ≈ constant".]**

> **TEACHER:** Say it the way you'd say it in the room: *"I compare all pairs — that's `O(n²)` — and each comparison walks `m` characters, so `O(n²·m)` time. The Union-Find operations are amortized near-constant, so they don't change that. But space drops from the brute force's `O(n²)` adjacency graph to just `O(n)` — one `parent` array. Same time, far less memory, and no graph to manage."*
>
> That contrast — *same speed, but I killed the O(n²) space* — is the sentence that lands the point.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: the `parent` array; a "smaller than O(n)?" bubble gets a red ✗. Then a second panel: "or trade TIME — compare pairs vs. generate swaps".]**

> Can we go below `O(n)` space? **No — and here's the honest why.** I have to remember which group each of the `n` words belongs to. That's `n` facts. You can't store `n` distinct memberships in less than `O(n)`. Union-Find is already the space win — it's what took us *down* from the graph's `O(n²)`.
>
> But there's a **time** trade worth naming. Two ways to find the similar pairs:
> - **Compare every pair** — `O(n²·m)`. Great when the words are **long**.
> - **Generate each word's swaps** — every word has only `O(m²)` single-swap neighbors; hash all words, look the swaps up. That's `O(n·m³)`, and it wins when the words are **short** — precisely when `m² < n`.
>
> Say that out loud: *"I'd pick pairwise or swap-generation based on whether the words are long or short."* Naming the trade — not just coding one path — is a senior signal.

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Accounts Merge (LC 721)". A blank editor.]**

> Before the next video, try **Accounts Merge**. Same Union-Find skeleton — but now you union accounts that *share an email*, and the payoff is rebuilding the merged accounts, not just counting them.
>
> Don't peek. Wrestle with the "what do I union on?" question for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Counting connected components + you only ask "same group?" and "merge" → Union-Find.** Skip the graph.
> 2. **Start at n groups; every *real* union drops the count by one.** The `ra == rb` check stops double-counting.
> 3. **Anagrams can't differ in exactly one spot** — so "similar" is cleanly "0 or 2 diffs," and you bail at the third.
>
> The memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "disposable edges + membership questions ⇒ Union-Find, one array, no graph."]**
>
> When you hear *"group these, friends-of-friends count, how many groups?"* — your hand should already be reaching for a `parent` array.
>
> *(GCA reminder — for the interview itself: ask "these are all anagrams, right?" first, then say the brute-force graph idea, then name the wasted O(n²) edges *out loud*, then reach for Union-Find. Google's General Cognitive Ability signal isn't the DSU trick — it's you narrating the path from naive to lean. Say the "I don't need the graph" insight before you write `parent`.)*

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Redundant Connection" — a graph with one extra edge glowing red, closing a cycle.]**

> Here, every union *helped* — it merged two circles. But what if a union tries to join two nodes that are **already in the same circle**? That's not a merge… that's a **cycle**. And detecting the exact edge that closes it is the entire next problem: Redundant Connection. Same `find`, same `union` — but this time the union that *fails* is the answer. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class Solution {
    private int[] parent, rank;

    public int numSimilarGroups(String[] strs) {
        int n = strs.length;
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;   // each its own leader

        int groups = n;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                if (similar(strs[i], strs[j]) && union(i, j))
                    groups--;                         // real merge → drop count
        return groups;
    }

    private boolean similar(String a, String b) {
        int diff = 0;
        for (int k = 0; k < a.length(); k++)
            if (a.charAt(k) != b.charAt(k))
                if (++diff > 2) return false;         // third mismatch → not one swap
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
