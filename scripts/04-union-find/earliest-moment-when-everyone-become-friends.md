# 🎬 Recording Script — The Earliest Moment When Everyone Become Friends
**Pattern: Union-Find (Disjoint Set Union) · LeetCode 1101 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** basic graph connectivity (BFS from a source) — but watch how much of it we throw away.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A clean "add edge, then BFS the whole graph" solution is typed out. A red "Time Limit Exceeded — 61 / 74" banner slams in.]**

> Google phone screen. The interviewer says: *"People become friends over time. Tell me the earliest moment the whole group is one big friend-circle."*
>
> You build a graph. After every new friendship, you run a BFS to check if everyone's connected yet. It's **correct**. It passes the small tests. You run the big one and… Time Limit Exceeded.
>
> Your code isn't wrong — it's doing almost the same work thousands of times. By the end of this video you'll throw away every one of those BFS calls and replace them with a single ticking counter. The pattern is called Union-Find, and it's one of the highest-leverage tools in the interview. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:30`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below, four person-dots labelled 0,1,2,3, all separate. A list of logs beside them.]**

> The whole problem in one line: **friendships arrive with timestamps, friendship is transitive, and we want the earliest time everyone is connected into one group — or -1 if that never happens.**
>
> Transitive is the key word. If 0 knows 1, and 1 knows 2, then 0 is acquainted with 2 — even though they never directly met.
>
> Here's our tiny example — four people, and these logs, *out of time order*:

```
logs = [ [4, 0, 1], [1, 2, 3], [2, 2, 3], [3, 1, 2] ]     n = 4
```

> Hold onto this. We'll solve it by hand before we write a line of code. The answer is going to be **4** — but don't take my word for it yet.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the logs sort themselves by timestamp. A "BFS calls" counter, top-right, starts at 0. After each edge, a BFS sweep animates over the whole graph.]**

> First instinct: process friendships in time order, and after each one, run a BFS from person 0 to see if it reaches all four.
>
> Sort by timestamp first: `[1,2,3]`, `[2,2,3]`, `[3,1,2]`, `[4,0,1]`.
>
> Edge at t=1 joins 2–3. BFS from 0 reaches only {0}. Not everyone. **Counter ticks.**
>
> Edge at t=2 joins 2–3 *again* — they're already friends. BFS from 0 anyway: still {0}. **Counter ticks.**
>
> Edge at t=3 joins 1–2. BFS from 0: still just {0}. **Counter ticks.**
>
> **[VISUAL: each BFS sweep re-lights the entire graph; counter climbing, turning orange.]**
>
> Every single edge, we re-walk the whole graph from scratch — even the t=2 edge that changed *nothing*. With ten thousand logs, that's ten thousand full traversals. That's your Time Limit Exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect + misconception — first pause)*

**[VISUAL: freeze. Two BFS sweeps side by side, nearly identical, one edge different. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Look at what's wasteful. Between two BFS runs, the connectivity picture barely moved — one edge changed, and sometimes, like t=2, *nothing* changed. Yet we recompute the entire thing.
>
> **LEARNER:** Can't I just count edges? Four people need to be connected — once I've added three friendships, three edges, everyone's linked, right?
>
> **TEACHER:** Tempting, and *wrong* — that's the trap. Three edges only connect four people if none of them is redundant. Our t=2 edge was a repeat; it added an edge but connected nobody new. Edge count lies. What never lies is the number of **separate groups**.
>
> So here's your think: instead of asking "is everyone connected?" over and over — **what single number could I track that tells me, instantly, how many separate friend-groups are left?** Pause the video.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the four dots, each in its own coloured bubble. A big "groups = 4" counter. As edges arrive, bubbles merge and the counter drops.]**

> **TEACHER:** Here's the move. Forget the whole graph. Track **one number: how many groups are there?** Everyone starts alone — four people, four groups.
>
> Think of it like clumps of friends at a party. Each friendship either **merges two separate clumps into one** — the number of clumps drops by one — or it's two people *already in the same clump*, and nothing changes.
>
> **[VISUAL: t=1 edge merges bubbles {2} and {3} → "groups = 3". t=2 edge tries to merge {2,3} with itself → bubble flashes, counter STAYS "3".]**
>
> Watch t=2 — persons 2 and 3 are already in the same bubble. The merge is a no-op. The counter doesn't move. *That's* the wasted BFS the brute force ran for nothing.
>
> **[VISUAL: t=3 merges {1} into {2,3} → "groups = 2". t=4 merges {0} into {1,2,3} → "groups = 1", the whole thing glows.]**
>
> The instant the counter hits **1**, there's a single clump — everyone's acquainted. And that happened at t=**4**. That's our answer.
>
> **LEARNER:** Wait — why did we have to *sort* the logs first? Why not process them as they come?
>
> **TEACHER:** Because we want the *earliest* moment in real time. If I merge groups in random order, the timestamp where my counter hits 1 is meaningless — it wouldn't line up with the real-world clock. Sorting by timestamp means the very first log that drops the counter to 1 is, by definition, the earliest moment it could have happened. Time order in, time answer out.

---

## 6. THE KEY MOVE (signaling) — `4:15`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "start with n groups · each real merge −1 · answer = the timestamp count hits 1."]**

> Burn this one line in: **start with `n` groups; every genuine merge drops the count by one; the timestamp it reaches 1 is your answer.**
>
> The tool that does the merging and the "are they already together?" check in near-constant time is **Union-Find** — Disjoint Set Union. Any time a problem is a *stream of connect-these-two* operations, this is your reflex.

---

## 7. CODE IT — LIVE & CHUNKED — `4:50`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First the two arrays that *are* the Union-Find: `parent`, where everyone starts as their own root, and `rank`, a hint about tree height we'll use to keep things flat.

```python
def earliestAcq(logs, n):
    parent = list(range(n))     # each person is its own group's root
    rank = [0] * n
```

> **[VISUAL: add chunk 2, highlight it.]** Now `find` — who's the root of your group? We climb parent pointers, and as we climb we do **path compression**: point each node at its grandparent, flattening the chain.

```python
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving — flatten as we climb
            x = parent[x]
        return x
```

> **[VISUAL: add chunk 3.]** Now `union` — the heart. Find both roots. **Same root? Return False — no merge.** Different roots? Hang the shorter tree under the taller one and return True.

```python
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False                 # already one group
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra              # taller tree becomes the parent
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        return True                      # a real merge happened
```

> **[VISUAL: add chunk 4, highlight the sort line and the `-1` counter.]** Finally the driver: **sort by timestamp**, start the counter at `n`, and on every real merge drop it — the moment it's 1, return that timestamp.

```python
    logs.sort(key=lambda log: log[0])    # earliest first
    components = n
    for t, a, b in logs:
        if union(a, b):
            components -= 1
            if components == 1:
                return t
    return -1
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:30`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `union` returns a **boolean** — and that return value is the whole trick. `True` means two different groups just fused, so we decrement. `False` means they were already together — the no-op case, the one the brute force wasted a BFS on. We just skip it.
>
> `logs.sort(...)` — without this, "earliest" is a lie. Sorted time in means the first count-hits-1 is the true earliest.
>
> `parent[x] = parent[parent[x]]` — path compression. Every `find` shortens the tree, so future finds are faster. Paired with union-by-rank, each operation is amortised near-constant.
>
> **LEARNER:** One thing — why is the answer *the timestamp when the count becomes 1*? Why not something after, once things settle?
>
> **TEACHER:** Because `count == 1` is *exactly* the definition of done — one group means every person is reachable from every other, transitively. And we're feeding logs in time order, so the merge that pushes count from 2 to 1 is the **first instant** the whole group is connected. One tick earlier there were still two islands; this log is the bridge. Everything after it is redundant — that's why we return immediately.
>
> `return -1` — if the loop finishes and count never reached 1, some people are permanently islanded. No moment exists.

---

## 9. DRY-RUN THE CODE — `7:40`
*(worked example — prove it, close the loop)*

**[VISUAL: the four dots with parent pointers; a trace table filling row by row.]**

```
logs sorted: [1,2,3] · [2,2,3] · [3,1,2] · [4,0,1]     n = 4
```

> Let's run the actual code. Start: `components = 4`.

| t | union(a,b) | roots | real merge? | components |
|---|---|---|---|---|
| 1 | (2,3) | 2≠3 | ✅ True | 3 |
| 2 | (2,3) | same root | ❌ False | 3 (unchanged) |
| 3 | (1,2) | 1≠2 | ✅ True | 2 |
| 4 | (0,1) | 0≠1 | ✅ True → **1** | **return 4** |

> t=2 does nothing — `union` returns False, counter frozen at 3, exactly like our party clumps. At t=4 the last island joins and count hits 1. We return **4** — the four we promised at the very start. Loop closed.
>
> **[VISUAL: quick flash — drop the t=4 log. Counter stops at 2 → "return -1".]** And if that last log never came? Count sticks at 2, loop ends, we return -1. Two friend-groups that never meet.

---

## 10. COMPLEXITY, OUT LOUD — `8:40`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(m·(n+m)). Ours: O(m log m). A note: "sort dominates; unions are near-constant".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force is `O(m·(n+m))` — a full BFS after every one of the m logs. With Union-Find, sorting the logs is `O(m log m)`, and each union is amortised near-constant — inverse Ackermann — so the sort dominates. Total time `O(m log m)`, space `O(n)` for the parent and rank arrays."*
>
> That's the sentence that turns a Medium from "I think so" into "I've got this."

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:10`
*(depth + honesty)*

**[VISUAL: the parent and rank arrays; a "shrink it?" thought bubble gets a red ✗.]**

> Quick and honest. Can we shrink the `O(n)` space? **No — and I can say exactly why.** The `parent` array *is* the disjoint-set structure; it's how each node knows its group. That's intrinsic.
>
> The `rank` array is another `O(n)` — could I drop it? I could, but then trees grow tall and `find` degrades toward `O(n)` per call. I'd save a little space and pay for it in time. Bad trade.
>
> Say that out loud in the interview: *"Space is `O(n)` and that's the floor — the parent array is the structure itself; keeping rank is what buys me near-constant finds."* Naming *why* you're optimal beats silence.

---

## 12. YOUR TURN (active recall) — `9:40`
*(retrieval practice)*

**[VISUAL: "Your turn → Number of Provinces (LC 547)". A blank editor.]**

> Before the next video, try **Number of Provinces**. Same friend-circles idea — but the friendships come as an `n × n` matrix, and instead of the earliest *time*, you just count the final number of groups.
>
> Same DSU skeleton: `parent`, `find`, `union`, count the roots. Don't peek. Wrestle with it for ten minutes — that struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:10`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Re-running BFS after every edge is redundant work** — the connectivity answer changes slowly, so track one number, not the whole graph.
> 2. **`components` starts at n, drops on every real merge** — `union` returning True is the signal. Count hits 1 → everyone's connected.
> 3. **Sort by timestamp first** — that's what makes "earliest connected" mean earliest in *time*.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "merging groups over time? count the clumps with Union-Find."]**
>
> When a problem is a *stream of connect-these-two* and you never split groups back apart, your hand should already be reaching for Union-Find.
>
> *(GCA reminder — for the interview itself: Google scores how you **think out loud**, not just the final code. State the brute-force BFS, name the repeated work, then reach for the counter. And ask the clarifying question up front — "friendship is transitive, so I want one connected component, right?" Narrating naive → optimal is the General Cognitive Ability signal.)*

---

## 14. CLIFFHANGER — `10:45`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Redundant Connection" — a graph with one extra edge glowing red, forming a cycle.]**

> Here, a repeat friendship — the t=2 edge — was harmless; we just ignored it. But what if that *redundant* union is the entire point? What if the interviewer hands you a graph with exactly one edge too many and asks: *"Which edge creates the cycle — find it."* Suddenly `union` returning False isn't noise to skip — it's the **answer**. That's the next one: Redundant Connection. Same Union-Find, flipped inside out. See you there.
