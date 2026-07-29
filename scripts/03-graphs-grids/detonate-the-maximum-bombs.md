# 🎬 Recording Script — Detonate the Maximum Bombs
**Pattern: Directed graph + DFS/BFS · LeetCode 2101 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Number of Islands / Number of Provinces gave you grid + union-find. Watch the one word that breaks union-find here.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an editor. A clean Union-Find solution is typed out — `find`, `union`, count the biggest component. A LeetCode "Wrong Answer — 142 / 160" banner slams in red.]**

> Here's a way to fail a Google interview while writing *beautiful* code.
>
> The problem's a chain reaction — bombs setting off nearby bombs. Your brain screams **union-find**: group the bombs that touch, return the biggest group. You write it clean. It passes the examples. Then — Wrong Answer.
>
> Your code isn't buggy. It's solving the **wrong problem**. There's a single word in this spec that makes union-find illegal — and if you catch it in the room, that catch alone is a strong-hire signal. By the end of this video you'll see the word, and you'll know the one-line reflex that replaces union-find. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, two circles on a grid: bomb 0 at (2,1) radius 3, bomb 1 at (6,1) radius 4. Draw each blast circle faintly.]**

```
bombs = [[2,1,3],
         [6,1,4]]      # each is [x, y, radius]
```

> The whole problem in one line: **you press exactly one bomb; it sets off every bomb whose center sits inside its blast; those set off theirs; how many go off at most?**
>
> Tiny example — two bombs. Bomb 0 sits at `(2,1)` with radius 3. Bomb 1 at `(6,1)` with radius 4. A bomb triggers another when the **other bomb's center** lands inside its circle.
>
> Hold this: the answer here is **2**. But *which* bomb you press to get 2 — that's where it gets interesting.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the trap)*

**[VISUAL: the two blast circles. First light up bomb 0's radius-3 circle; bomb 1's center clearly OUTSIDE it. Then bomb 1's radius-4 circle; bomb 0's center INSIDE it.]**

> Let's reach for union-find, the way most people do, and watch it wobble.
>
> Union-find asks: *are bomb 0 and bomb 1 in the same group?* To answer, it'd check — do they touch? Draw bomb 0's circle, radius 3. Does it reach bomb 1's center? The centers are 4 apart. Radius 3 falls short. **No.**
>
> **[VISUAL: bomb 0's circle glows; a dashed line to bomb 1's center, stamped "4 > 3 ✗".]**
>
> Now bomb 1's circle, radius 4. Does *it* reach bomb 0's center? Same 4 apart, radius 4. **Yes — just barely.**
>
> **[VISUAL: bomb 1's circle glows; dashed line to bomb 0's center, stamped "4 ≤ 4 ✓".]**
>
> Feel the problem? Bomb 1 reaches bomb 0. Bomb 0 does **not** reach bomb 1. The relationship points **one way**. But union-find only knows "connected" or "not" — it has no arrows. It'd smush these into one group and quietly claim pressing bomb 0 sets off bomb 1. That's a lie.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The two bombs with a single one-way arrow from 1 → 0. A big "?" over a would-be arrow 0 → 1. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** There's the word from the cold open: **"its"** radius. Bomb `i` triggers `j` when `j` is inside **i's** radius. Each bomb judges with its *own* reach — and the reaches differ. So "i reaches j" and "j reaches i" are two separate facts.
>
> **LEARNER:** Okay but — that's just how far apart they are, right? Distance is distance. Why would the arrow only go one way?
>
> **TEACHER:** Because the *distance* is symmetric — but the *radius you compare it against isn't*. Same 4 apart, but bomb 1 owns a bigger circle. Big bomb swallows the small one; small one can't reach back. So here's your think: **if the relationship has a direction, what data structure has directions?** Pause. What are we actually building — and how would we count the answer on it?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration — derive it, don't hand it over)*

**[VISUAL: the bombs turn into graph nodes. Draw a directed edge 1 → 0. Then a caption: "edge i → j  ⟺  j is inside i's blast."]**

> **TEACHER:** A relationship with a direction is a **directed graph**. So let's build one. One rule for the arrows: **draw `i → j` when bomb j's center is inside bomb i's radius.** That arrow means "if i goes off, it directly sets off j."
>
> Once the arrows exist, the chain reaction is just... following arrows. Press a bomb, and everything you can *reach* by walking arrows explodes. So the answer to "how many go off if I start at i" is simply: **how many nodes are reachable from i.** That's a plain DFS or BFS.
>
> **[VISUAL: from node 1, a BFS ripple: 1 lights, arrow to 0, 0 lights. Counter shows "2".]**
>
> And since we don't know the best starting bomb, we try **all** of them and keep the biggest count.
>
> **LEARNER:** Wait — isn't that wasteful? Union-find gets the biggest group in basically one pass. Now you're saying run a whole traversal from *every single* bomb?
>
> **TEACHER:** Yep — n traversals. And that's completely fine here, because look at the constraint: **n is at most 100.** A hundred BFS runs over a hundred-node graph is nothing. We're not paying for speed we don't need — we're paying for *correctness* union-find can't give. Right tool beats fast-wrong tool every time.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "asymmetric reach ⇒ DIRECTED graph ⇒ DFS/BFS from every node."]**

> Burn this one in: **when the relationship points one way, it's a directed graph — draw the arrows, then traverse from every node and take the max.**
>
> That's the reflex. The tell is *asymmetry*: A affects B but not necessarily B affects A. The moment you spot it, undirected tools — union-find, "connected components" — are the wrong shape. Reach for directed edges.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Build it in two halves: make the graph, then walk it. First, the graph — an empty adjacency list per bomb.

```python
from collections import deque

def maximum_detonation(bombs):
    n = len(bombs)
    graph = [[] for _ in range(n)]
```

> **[VISUAL: add chunk 2, highlight the comparison line.]** Now fill it. For every ordered pair, ask: is j inside **i's** radius? Two things to nail here.

```python
    for i in range(n):
        xi, yi, ri = bombs[i]
        for j in range(n):
            if i == j:
                continue
            xj, yj, _ = bombs[j]
            dx, dy = xi - xj, yi - yj
            if dx * dx + dy * dy <= ri * ri:   # squared dist ≤ squared radius
                graph[i].append(j)
```

> **[VISUAL: add chunk 3, highlight it.]** Now the walk — a BFS that counts everything reachable from one start.

```python
    def reachable(start):
        seen = {start}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:          # only bombs u can trigger
                if v not in seen:
                    seen.add(v)
                    queue.append(v)
        return len(seen)
```

> **[VISUAL: add chunk 4.]** And the punchline — try every bomb as the start, keep the max.

```python
    return max(reachable(s) for s in range(n))
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight each line as it's named. Zoom the `ri * ri` comparison.]**

> Two lines carry this whole solution. Let's earn them.
>
> `if dx*dx + dy*dy <= ri * ri` — this is the arrow rule, and it's doing **two** clever things at once. One: I compare **squared** distance to **squared** radius. Never take a square root. Square roots give you floats, floats give you rounding, and rounding flips a borderline `≤` — remember our example landed *exactly* on `4 ≤ 4`. Integers keep that exact.
>
> **LEARNER:** Small thing — why `ri` and not `rj`? They're right next to each other, easy to swap.
>
> **TEACHER:** And that swap is *the* bug in this problem. `ri` is bomb **i's** radius — the bomb doing the reaching. We're asking "does i's blast cover j?" Use `rj` and you'd ask the reverse. That single character is the direction of the arrow. Get it backwards and every edge points the wrong way.
>
> **[VISUAL: flash `ri * ri` in green, a struck-out `rj * rj` in red beside it.]**
>
> The second star is quieter: `graph[i].append(j)` adds `i → j` but **not** `j → i`. That's what makes it directed. If I ever added both, I'd be back to union-find's undirected world — and back to Wrong Answer.
>
> One more: `dx*dx + dy*dy` on coordinates up to 10⁵ reaches ~4·10¹⁰. In Python, fine — big ints. **In Java you'd need `long`**, or it overflows a 32-bit int and silently corrupts the compare. Say that out loud in the room.

---

## 9. DRY-RUN THE CODE — `8:15`
*(worked example — prove it, close the loop)*

**[VISUAL: the two bombs; a graph-build table, then a traversal table.]**

> Run the real code on `[[2,1,3],[6,1,4]]`. Distance² between the centers is fixed at `(2−6)² + 0 = 16`. Build the edges:

| Pair tested | dist² | source's r² | dist² ≤ r²? | edge |
|---|---|---|---|---|
| 0 → 1 | 16 | `3² = 9` | 16 ≤ 9 ✗ | — |
| 1 → 0 | 16 | `4² = 16` | 16 ≤ 16 ✓ | **1 → 0** |

> So `graph = [[], [0]]`. One arrow, nothing back — exactly the asymmetry we drew by hand. Now traverse from each start:

| Start | BFS | reachable |
|---|---|---|
| 0 | `seen={0}`; `graph[0]` empty | **1** |
| 1 | `seen={1}` → visit 0 → `seen={1,0}` | **2** |

> `max(1, 2) = 2`. Loop closed — the answer's 2, and crucially, you only get it by **starting at bomb 1**. Press bomb 0 and you're alone. Union-find never knew the difference.

---

## 10. COMPLEXITY, OUT LOUD — `9:15`
*(transfer to interview)*

**[VISUAL: two rows — Build graph: O(n²). n traversals: O(n·(n+E)) → O(n³). Note: "n ≤ 100, so this flies".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Building the graph is O(n²) — every ordered pair. Then I traverse from all n starts, and each traversal is O(n + E) where E can be O(n²), so the whole thing is O(n³) worst case. Space is O(n²) for the adjacency list. With n capped at 100, that's tiny — well under a millisecond."*
>
> Notice I didn't apologize for O(n³). I *justified* it with the constraint. That's the move.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:45`
*(depth + honesty)*

**[VISUAL: the adjacency list; a thought bubble "skip the graph?" → arrow to O(n) space.]**

> Quick honest beat. Can I cut the O(n²) graph? **Yes — I could skip storing it and recompute each distance check *inside* the traversal.** That drops memory to O(n) — just the visited set — at the cost of redoing those in-range tests on every walk.
>
> But here's the judgment call: with n ≤ 100 that graph is at most 10,000 tiny entries. I'd **keep** the graph. It cleanly splits "build the model" from "use the model," which is far easier to explain out loud. Say it in the interview: *"I could inline the checks to get O(n) space if memory were tight — but at this scale the explicit graph reads cleaner, so that's my call."* Naming the trade you chose **not** to make is its own signal of judgment.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Number of Provinces (LC 547)". A blank editor.]**

> Before the next video, do **Number of Provinces**. It's the same "count the reachable group" flavor — but the relationship is **symmetric**: if city A connects to B, B connects to A. So here union-find is *right*.
>
> The whole exercise: feel *why* it flips. What's different about the relation that makes the undirected tool legal there and illegal here? Wrestle with it for ten minutes. That contrast is what locks the pattern in.

---

## 13. LOCK IT IN — `10:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **"i reaches j" ≠ "j reaches i"** — the radii differ, so the relationship has a direction. That kills union-find.
> 2. **Directed graph + DFS/BFS from every start**, take the max. Edge `i → j` when j sits in i's blast.
> 3. **Squared distance vs squared radius, integer math** — no square roots, no floats; and use `long` in Java or it overflows.
>
> The memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "asymmetric reach ⇒ directed graph, not union-find."]**
>
> When a chain reaction reaches **one way**, your hand should reach for arrows — a directed graph — not a union-find blob.
>
> *(GCA reminder — for the interview itself: the win here isn't the code, it's the *clarifying question*. Ask "does i triggering j mean j triggers i?" out loud, watch yourself answer "no — different radii," and reject union-find in front of the interviewer. Narrating your way from the wrong tool to the right one is exactly the General Cognitive Ability signal Google scores. Say the direction insight before you write a single edge.)*

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Course Schedule" — a directed graph with a red cycle looping back on itself.]**

> We built a directed graph and just... walked it, no worries. But we got lucky — our arrows never looped back. What happens when a directed graph **can** cycle — when following the arrows might trap you in an endless loop, and the *entire question* becomes "is there a cycle at all?" That's the next one: Course Schedule. Same directed-graph muscle, but now the loop is the enemy. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int maximumDetonation(int[][] bombs) {
    int n = bombs.length;
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());

    // build the DIRECTED graph: edge i -> j if j's center is in i's radius
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            long dx = (long) bombs[i][0] - bombs[j][0];   // long! ~4e10 overflows int
            long dy = (long) bombs[i][1] - bombs[j][1];
            long r  = bombs[i][2];                        // i's OWN radius — directional
            if (dx * dx + dy * dy <= r * r) graph.get(i).add(j);
        }
    }

    int best = 0;
    for (int start = 0; start < n; start++) {
        boolean[] seen = new boolean[n];
        Deque<Integer> queue = new ArrayDeque<>();
        seen[start] = true;
        queue.add(start);
        int count = 1;
        while (!queue.isEmpty()) {
            int u = queue.poll();
            for (int v : graph.get(u)) {
                if (!seen[v]) { seen[v] = true; count++; queue.add(v); }
            }
        }
        best = Math.max(best, count);
    }
    return best;
}
```
