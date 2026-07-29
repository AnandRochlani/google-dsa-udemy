# 🎬 Recording Script — Course Schedule
**Pattern: Topological Sort · LeetCode 207 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** plain BFS/queue traversal (graphs lesson).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a university course catalog. Arrows drawn between courses: "Data Structures needs Intro CS," "Algorithms needs Data Structures." Then one sneaky arrow loops back — "Intro CS needs Algorithms." A red "?" pulses.]**

> Google phone screen: *"Here are your courses and their prerequisites. Can you actually finish all of them?"*
>
> Sounds like a scheduling puzzle. It's not. Hidden inside that innocent question is one of the most reusable graph patterns in the whole interview canon — and a single trap that turns "yes" into "impossible."
>
> By the end of this video you'll spot that trap instantly, and you'll have a five-line technique that Google asks about constantly. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below: "numCourses = 2, prerequisites = [[1,0]]". Two boxes labeled 0 and 1, an arrow 0 → 1.]**

> The whole problem in one line: **given courses and their prerequisites, return true if you can finish them all.**
>
> Tiny example. Two courses. The pair `[1, 0]` means *take course 0 before course 1.* Easy — take 0, then 1. True.
>
> Now watch this second case: `[[1,0],[0,1]]`. One says take 0 before 1. The other says take 1 before 0. Hold that image — it's the entire problem in miniature.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: four courses 0,1,2,3. Prereqs [[1,0],[2,0],[3,1],[3,2]]. A "remaining" set {0,1,2,3}. A "passes" counter top-right.]**

> Let's do what your brain does first. *"Which course can I take right now? One whose prerequisites are all already done."*
>
> Scan everybody. Course 0 has no prerequisites — take it. Now rescan from scratch: 1 is free, 2 is free — take both. Rescan again: now 3 is free — take it.
>
> **[VISUAL: each "rescan" sweeps all remaining courses, the passes counter ticking 1, 2, 3…]**
>
> It works. But look at what we're doing: every single round we re-examine *every* remaining course and re-check *all* its prerequisites from zero. With 2000 courses that's rescans on top of rescans.
>
> **[VISUAL: counter morphs to "≈ V² work".]**
>
> We're re-deriving "who's ready" from scratch, over and over. There's a smarter bookkeeping.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight the repeated full-list rescans. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the waste: after I take course 0, only the courses that *depended on 0* could possibly have become ready. Everything else is unchanged. But I rescanned all of them anyway.
>
> **LEARNER:** So instead of asking "who's ready?" every round from scratch… I should just update the few courses that were actually affected?
>
> **TEACHER:** Exactly the instinct. Pause the video: **what one number could you track per course so that finishing a course instantly tells you who just became takeable — no rescan?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it)*

**[VISUAL: the four courses as a directed graph. Each node gets a little counter badge. 0:(0), 1:(1), 2:(1), 3:(2).]**

> **TEACHER:** First, see it as a graph. Each prerequisite `[a, b]` — take b before a — is a directed arrow `b → a`, meaning *"b unlocks a."*
>
> Now the key number. For each course, count the arrows pointing *into* it. That count is its **in-degree** — literally *the number of prerequisites it still hasn't finished.* Course 0 has in-degree 0. Course 3 has in-degree 2.
>
> **LEARNER:** Wait — so a course is takeable exactly when its in-degree hits zero?
>
> **TEACHER:** That's the whole move. In-degree 0 means nothing is blocking you. Take it, then walk its outgoing arrows and *decrement* the in-degree of everything it unlocks. Anything that drops to zero just became takeable — throw it in a queue.
>
> **[VISUAL: take 0 → its badge grays out → arrows 0→1 and 0→2 fire → badges on 1 and 2 tick from 1 to 0 → both turn green and slide into a queue.]**
>
> This is called **Kahn's algorithm** — topological sort by draining in-degrees. It's just tasks-with-prerequisites: repeatedly take whatever has zero prerequisites left.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "In-degree 0 = takeable. Take it, decrement neighbors, repeat."]**

> Burn this in: **a course with in-degree zero is takeable — take it, drop the in-degree of everything it unlocks, and anything that hits zero is next.**
>
> And the punchline: if you manage to take *all* the courses this way, there's no cycle. If some get stuck, they were tangled in one.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Build the graph and the in-degree array first.

```python
from collections import deque

def can_finish(numCourses, prerequisites):
    graph = [[] for _ in range(numCourses)]   # b -> courses b unlocks
    indegree = [0] * numCourses               # unfinished prereqs per course
    for a, b in prerequisites:                # [a, b]: take b before a  (b -> a)
        graph[b].append(a)
        indegree[a] += 1
```

> **[VISUAL: add chunk 2, highlight it.]** Seed the queue with every course that starts free — in-degree zero.

```python
    queue = deque(c for c in range(numCourses) if indegree[c] == 0)
    taken = 0
```

> **[VISUAL: add chunk 3.]** Now the drain. Pop a course, count it, and relax its neighbors.

```python
    while queue:
        course = queue.popleft()
        taken += 1
        for nxt in graph[course]:             # this course unlocks nxt
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return taken == numCourses                # all taken ⇒ no cycle
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as named.]**

> Let's walk *why*.
>
> `graph[b].append(a)` and `indegree[a] += 1` — one prerequisite, two updates: record that b unlocks a, and add one to a's blocked count. This is the entire model.
>
> The queue starts with in-degree-zero courses — the ones with no prerequisites, ready on day one.
>
> `taken += 1` — every course that comes off the queue is a course we legally took. That counter is secretly our cycle detector.
>
> The inner loop is the payoff for tracking in-degree: when we finish `course`, we touch *only* the courses it unlocks — no full rescan. Each drops by one; each that hits zero is now free.
>
> **LEARNER:** So where exactly does a cycle get caught? I don't see an `if cycle` anywhere.
>
> **TEACHER:** Sharp — there isn't one. A course in a cycle waits on another course that waits back on it, so its in-degree *never* reaches zero. It never enters the queue, never gets counted. So `taken` comes out short. `taken == numCourses` is the cycle test — no special case needed.

---

## 9. DRY-RUN THE CODE — `8:15`
*(worked example — prove it, close the loop)*

**[VISUAL: graph 0→1, 0→2, 1→3, 2→3. In-degrees [0,1,1,2]. A trace table fills row by row; badges tick down live.]**

> Run it on our four courses.

| pop | taken | decrements | new zeros → queue |
|---|---|---|---|
| 0 | 1 | 1→0, 2→0 | 1, 2 |
| 1 | 2 | 3→1 | — |
| 2 | 3 | 3→0 | 3 |
| 3 | 4 | — | — |

> Queue empties, `taken = 4 = numCourses` → **True.** ✅
>
> Now the deadlock `[[1,0],[0,1]]`: in-degrees `[1,1]`, so the queue starts *empty*. `taken` stays 0, `0 ≠ 2` → **False.** The cycle trapped everyone. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute force rescans: O(V²). Kahn's: O(V + E).]**

> Say it the way you would in the room: *"Building the graph is O(E). Each course enters the queue at most once — O(V) — and each edge is relaxed exactly once — O(E). So O(V plus E) time, and O(V plus E) space for the adjacency list, in-degree array, and queue."*
>
> Versus the rescan brute force at roughly O(V squared). We traded repeated full scans for one number per node that updates incrementally.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: the three stored structures — graph, in-degree, queue — each labeled "required".]**

> Can we shrink the space? Honestly, no — and saying *why* is a skill.
>
> You must store the adjacency list to know what each course unlocks — that's O(E). The in-degree array is O(V). You can't answer "is there a cycle?" without materializing the dependency graph, so O(V + E) is the floor.
>
> The one real alternative is **DFS with three-color marking** — white, gray, black — where revisiting a gray node on the current path means a back-edge, a cycle. Same O(V + E) time and space; the recursion stack just replaces the queue. It's a style choice, not a memory win. Kahn's narrates cleaner because "in-degree zero equals takeable" *is* the story.

---

## 12. YOUR TURN (active recall) — `10:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Course Schedule II (LC 210)". A blank editor.]**

> Before the next video, try **Course Schedule II.** Same graph, same drain — but instead of returning true or false, return the *actual order* you'd take the courses in. Ninety percent of the code is what you just wrote. Find the one line that changes.
>
> Don't peek. That struggle is what moves this from "I watched it" to "I own it."

---

## 13. LOCK IT IN — `11:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Prerequisite `[a, b]` = edge `b → a`.** Model it as a directed graph first.
> 2. **In-degree = unfinished prerequisites.** Zero means takeable.
> 3. **`taken < numCourses` means a cycle** — no separate cycle check needed.
>
> The memory peg — when you hear *"dependencies," "prerequisites," or "order these tasks,"* your hand should already be reaching for it: **drain the zeros.**

---

## 14. CLIFFHANGER — `11:30`
*(open loop to next lesson)*

**[VISUAL: the same graph, but now the popped courses line up in a row: 0, 1, 2, 3.]**

> Notice something in that dry-run? The courses came off the queue in a *legal* order — 0, then 1 and 2, then 3. We threw that order away and just counted. What if the interviewer wants the order itself — the real schedule? Turns out it's already sitting in our queue, one append away. That's the next one: Course Schedule II. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
import java.util.*;

public boolean canFinish(int numCourses, int[][] prerequisites) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
    int[] indegree = new int[numCourses];
    for (int[] p : prerequisites) {       // p = [a, b], edge b -> a
        graph.get(p[1]).add(p[0]);
        indegree[p[0]]++;
    }

    Deque<Integer> queue = new ArrayDeque<>();
    for (int c = 0; c < numCourses; c++)
        if (indegree[c] == 0) queue.offer(c);

    int taken = 0;
    while (!queue.isEmpty()) {
        int course = queue.poll();
        taken++;
        for (int nxt : graph.get(course))
            if (--indegree[nxt] == 0) queue.offer(nxt);
    }
    return taken == numCourses;
}
```
