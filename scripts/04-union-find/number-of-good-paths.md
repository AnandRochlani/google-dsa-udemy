# 🎬 Recording Script — Number of Good Paths
**Pattern: Union-Find + process by increasing value · LeetCode 2421 · Hard · Target length ~14 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** plain Union-Find (Number of Provinces / Redundant Connection) — but here we don't just connect, we *sweep* the connecting in a deliberate order.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a tree of circles with numbers inside. A clean double-`for`-loop brute force is typed below it. A LeetCode "Time Limit Exceeded — 58 / 63" banner slams in red.]**

> Google onsite. Interviewer draws a tree, drops a number in every node, and says: *"Count the good paths. A good path is one where both ends have the same value, and nothing in between is bigger. Go."*
>
> You do the natural thing. Every pair with the same value, walk the path, check it. It's *correct*. It passes the small tests. You hit run on the big one and… Time Limit Exceeded.
>
> Here's the twist: your code isn't wrong, it's just doing enormous repeated work. By the end of this video you'll fix it with **Union-Find** — but with one clever ordering choice that makes the whole thing click. And that ordering is the entire lesson. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, this exact tree (node index : value):]**

```
        1(3)
         |
        0(1)
         |
        2(2)
        / \
     3(1) 4(3)
```

> The whole problem in one line: **count paths whose two endpoints have equal value, where every node on the path is ≤ that value.** And a single node counts too — same value at both ends, trivially.
>
> Tiny example — five nodes. `vals = [1,3,2,1,3]`. It's a **tree**, so between any two nodes there's *exactly one* path. Hold onto that — no path-hunting, the path is handed to us.
>
> The answer here is **six**. Don't chase it yet. Just hold: six.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: the tree. A "pairs checked" counter, top-right, at 0. Same-valued nodes glow in matching colors: nodes 0 & 3 blue (value 1), nodes 1 & 4 red (value 3).]**

> Let's do what your brain does first. Five singles — that's 6 minus... hold on, that's five good paths for free. Now hunt for same-valued **pairs**.
>
> **Value 3:** nodes 1 and 4. Path is `1 → 0 → 2 → 4`. Values along it: 3, 1, 2, 3. Both ends are 3, and 1 and 2 are below 3. Clean. ✅ That's our sixth.
>
> **[VISUAL: the red path lights green, a ✓ pops.]**
>
> **Value 1:** nodes 0 and 3. Path is `0 → 2 → 3`. But node 2 is a **2** — bigger than 1. The path climbs above the endpoints. ❌
>
> **[VISUAL: the blue path lights up, node 2 flashes red, a ✗ pops.]**
>
> Five singles plus one pair — six. Good. But *feel* the cost: for every same-valued pair I re-walked a path from scratch. On a big tree with tons of repeated values, that's a pair count exploding toward n-squared, each one a full walk. That's your TLE.
>
> **[VISUAL: counter morphs into "≈ n³" with a red glow.]**

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Spotlight the blue path `0 → 2 → 3` with node 2 flashing. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So what's the real question I keep re-answering? It's always the same shape: *"can these two same-valued nodes reach each other without stepping on anything bigger?"* Reach each other. Connectivity. That word should be ringing a bell.
>
> **LEARNER:** Connectivity screams Union-Find — but Union-Find just tells me if two nodes are connected. It doesn't know anything about a *value ceiling*. How do I stop it from connecting through node 2 when I'm asking about value 1?
>
> **TEACHER:** *Exactly* the right objection — that's the whole puzzle. Here's your think: what if I don't hand Union-Find the whole tree at once? What if I let nodes into the graph **in a specific order**, so that when I ask my value-1 question, node 2 simply *isn't allowed in yet*? Pause. What order would make that work?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:35`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a horizontal "ceiling" slider labeled `v`, starting at 1. Nodes below the ceiling are solid; nodes above are ghosted/greyed. Edges switch on only when BOTH endpoints are solid.]**

> **TEACHER:** Here's the move. Imagine a rising **ceiling**. Only nodes whose value is ≤ the ceiling are "switched on." Start the ceiling at the smallest value and raise it, one value at a time.
>
> Think of flooding a valley. The water level rises. Low nodes surface first and connect into little islands; higher nodes only join once the water reaches them.
>
> **[VISUAL: ceiling = 1. Only nodes 0 and 3 are solid (both value 1). But the edge between them runs through node 2, which is ghosted — so they're NOT connected. Two separate islands.]**
>
> Ceiling at 1: nodes 0 and 3 are on, but node 2 (value 2) is still ghosted, so the edge path between them is broken. They're in *different* islands. So the value-1 pair 0–3? Not connected → not a good path. The ceiling did our dirty work — it refused to connect them through the too-big node.
>
> **[VISUAL: raise ceiling to 2. Node 2 solidifies. Edges 0–2 and 2–3 switch on. Nodes 0, 2, 3 merge into one island.]**
>
> Raise to 2: node 2 wakes up, its edges fire, and now 0, 2, 3 are one blob.
>
> **[VISUAL: raise ceiling to 3. Nodes 1 and 4 solidify. Edges 0–1 and 2–4 fire. Everything is one big blob. Nodes 1 and 4 — both value 3 — now sit together.]**
>
> Raise to 3: nodes 1 and 4 join, and now they're in the *same* blob. And here's the beautiful part — **every node in that blob is ≤ 3**, because we only ever let in nodes ≤ the ceiling. So the path between 1 and 4 *cannot* exceed 3. Same blob **means** clean path. For free.
>
> **LEARNER:** Wait — so I never actually check the path? I just trust that "same blob" already guarantees nothing on it is too big?
>
> **TEACHER:** That's the magic. Because I built the blob only from nodes ≤ the current ceiling, the unique tree-path between any two of them stays *inside* the blob — so it's all ≤ the ceiling. The ordering **is** the check. No path walk, ever.

---

## 6. THE KEY MOVE (signaling) — `5:10`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "process values LOW → HIGH; union edges as their ceiling is reached; same blob ⇒ clean path."]**

> Burn this in: **sweep the value ceiling from low to high, union each edge the moment both its ends are under the ceiling, and then 'same component' automatically means 'good path.'**
>
> And the counting piece: when a merge joins two blobs at ceiling `v`, count how many value-`v` nodes are on each side — say `a` and `b`. The new good paths are `a × b`. Every value-`v` node on the left pairs with every value-`v` node on the right.

---

## 7. CODE IT — LIVE & CHUNKED — `5:50`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, Union-Find setup — and instead of a plain parent array, each root carries a little **histogram**: how many nodes of each value live in its component. Seed every node with just itself.

```python
from collections import Counter

def numberOfGoodPaths(vals, edges):
    n = len(vals)
    parent = list(range(n))
    cnt = [Counter({vals[i]: 1}) for i in range(n)]   # per-root value histogram
```

> **[VISUAL: add chunk 2, highlight it.]** Standard `find` with path compression — nothing exotic.

```python
    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:          # path compression
            parent[x], x = root, parent[x]
        return root
```

> **[VISUAL: add chunk 3, highlight the `sorted(...)` key.]** Here's the heart: seed the answer with `n` for the singles, then walk edges **sorted by their ceiling** — the *larger* of the two endpoint values. That's the low-to-high sweep, in one line.

```python
    ans = n                               # each node is a good path by itself
    for u, v in sorted(edges, key=lambda e: max(vals[e[0]], vals[e[1]])):
        ru, rv = find(u), find(v)
        peak = max(vals[u], vals[v])      # this edge's ceiling; one end equals it
```

> **[VISUAL: add chunk 4, highlight the `ans += ...` line.]** Before merging, cash in the new good paths: value-`peak` nodes on one side times value-`peak` nodes on the other. Then union, folding the smaller histogram into the larger.

```python
        ans += cnt[ru][peak] * cnt[rv][peak]    # cross-pairs of peak-valued nodes
        if len(cnt[ru]) < len(cnt[rv]):         # small-to-large merge
            ru, rv = rv, ru
        parent[rv] = ru
        cnt[ru].update(cnt[rv])                 # fold rv's counts into ru
        cnt[rv] = None
    return ans
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:45`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `sorted(edges, key=lambda e: max(...))` — this **one line is the entire algorithm.** Sorting by the larger endpoint value means we activate each edge exactly at the ceiling where both its ends become legal. Low to high. Remove this ordering and everything collapses back to brute force.
>
> `ans = n` — the five singles. Every node is a good path with itself. Seed it up front so we never special-case it.
>
> `peak = max(vals[u], vals[v])` — the ceiling for *this* edge, and it always equals at least one endpoint's value. That's why looking up `cnt[...][peak]` is the right question to ask.
>
> `ans += cnt[ru][peak] * cnt[rv][peak]` — cross-pairs only. Pairs already inside `ru` got counted when `ru` formed; same for `rv`. Merging creates *only* the left-times-right pairs. That's why we read the counts *before* we merge.
>
> **LEARNER:** Hold on — why sort by the **max** of the two endpoints and not the min? Feels arbitrary.
>
> **TEACHER:** Great catch. An edge is only usable when **both** ends are under the ceiling — so it comes alive at the *higher* of the two, not the lower. Sort by the min and you'd try to union through a node that isn't legal yet, and your "same blob means clean path" guarantee dies. The max is what keeps the invariant true.
>
> `cnt[ru].update(cnt[rv])` with the small-to-large swap above it — merge the smaller histogram into the bigger one. That's not cosmetic: it's what keeps total merge work at `O(n log n)` instead of `O(n²)`.

---

## 9. DRY-RUN THE CODE — `9:05`
*(worked example — prove it, close the loop)*

**[VISUAL: the tree, plus a trace table filling row by row. Histograms shown as `{value:count}` badges on each blob.]**

> Let's run the real code. Edge ceilings: `0-1→3`, `0-2→2`, `2-3→2`, `2-4→3`. Sorted: **`0-2`(2), `2-3`(2), `0-1`(3), `2-4`(3)**. Start `ans = 5`.

| Edge (peak) | roots | `cnt[ru][peak] × cnt[rv][peak]` | new | blob after | `ans` |
|---|---|---|---|---|---|
| `0-2` (2) | {0},{2} | `0 × 1` | 0 | `{1:1, 2:1}` | 5 |
| `2-3` (2) | {0,2},{3} | `1 × 0` | 0 | `{1:2, 2:1}` | 5 |
| `0-1` (3) | {0,2,3},{1} | `0 × 1` | 0 | `{1:2, 2:1, 3:1}` | 5 |
| `2-4` (3) | {0,1,2,3},{4} | `1 × 1` | **1** | `{1:2, 2:1, 3:2}` | **6** |

> Watch the payoff land on the **last** row. By then the big blob already holds one value-3 node — node 1. Node 4 walks in, also value 3, `1 × 1 = 1` new good path. That's the `1 → 0 → 2 → 4` we found by hand. `ans` ticks to **six**. Loop closed — exactly the six we promised at the start.
>
> And notice row 2: when node 3 (value 1) joins at ceiling 2, we ask about value-**2** nodes and get `1 × 0 = 0`. The bogus 0–3 value-1 pair *never* fires, because their path runs through node 2 and the ordering never let them meet under ceiling 1. The sort did the filtering, silently.

---

## 10. COMPLEXITY, OUT LOUD — `10:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n³). Ours: O(n log n). A note: "sort dominates; union-find is near-linear."]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force is O(n³) — up to n-squared same-valued pairs, each an O(n) path walk. With union-find swept by value, the cost is dominated by sorting the edges: O(n log n). The find operations are near-constant with path compression, and small-to-large histogram merging is O(n log n) total. So O(n log n) time, O(n) space."*
>
> That sentence is what turns a Hard from "I hope this passes" into "I know exactly why it's fast."

---

## 11. CAN WE USE LESS MEMORY? (space) — `11:00`
*(depth + honesty)*

**[VISUAL: the parent array and the histograms; a "shrink below O(n)?" thought bubble gets a red ✗.]**

> Quick but important — honesty scores here.
>
> Can we go below `O(n)`? **No — and I can say exactly why.** I need the parent array, that's `O(n)`. And I need, per component, the count of each value — but across *all* components those counts sum to exactly `n`, so it's `O(n)` total, never more. The value counts *are* the algorithm's memory; they're what I reuse on every merge.
>
> Say it out loud: *"Space is O(n) and that's optimal — union-find plus per-component value counts, and those counts sum to n no matter how I organize them."* Naming *why* it can't shrink is a stronger signal than silently accepting it.

---

## 12. YOUR TURN (active recall) — `11:40`
*(retrieval practice)*

**[VISUAL: "Your turn → Checking Existence of Edge Length Limited Paths (LC 1697)". A blank editor.]**

> Before the next video, try **Checking Existence of Edge Length Limited Paths**. Same skeleton exactly: sort by a threshold, sweep it upward, union as you go, and answer questions at each level. Different dressing — edge weights instead of node-value ceilings — but the *same reflex*.
>
> Don't peek. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `12:20`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **"Can two nodes reach each other under a ceiling?" is a connectivity question → Union-Find.**
> 2. **Process values low → high.** Because a blob built from nodes ≤ v can't hide anything bigger — so "same blob" *means* "clean path," free.
> 3. **On each merge, `count[v] × count[v]` across the two sides** is the new good paths. Seed the answer at `n` for the singles.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "Rising ceiling: union low-to-high, same blob = good path."]**
>
> When a problem asks about reachability under a limit that only ever *rises*, your hand should already be reaching for Union-Find, sorted low to high.
>
> *(GCA reminder — for the interview itself: Google scores how you *think out loud*, not just the final code. Start by asking "it's a tree, so the path between two nodes is unique, right?" — that one clarifying question reframes everything. Then narrate the jump: brute force is O(n³), the repeated question is really connectivity, and the ceiling only rises so I sweep and union. Saying that path from naive to optimal is the General Cognitive Ability signal — say it before you write the sort line.)*

---

## 14. CLIFFHANGER — `13:15`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Accounts Merge" — a tangle of emails linking into clusters.]**

> Here we swept in a deliberate order and Union-Find just *counted*. But what happens when the things you're merging aren't nodes with a clean value — when they're **groups that share a hidden key**, like accounts that share an email, and you have to fuse them *and* reconstruct what each merged cluster contains? Same union-find muscle, aimed at a messier target. That's the next one: **Accounts Merge**. See you there.
