# 🎬 Recording Script — Course Schedule II
**Pattern: Topological Sort · LeetCode 210 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Course Schedule I (Kahn's BFS, draining in-degrees) — previous lesson.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: last lesson's function on screen, returning `True`. A cursor hovers over the line `taken += 1`. A speech bubble: "…but which order?"]**

> Last video, we answered *"can you finish all the courses?"* — yes or no. We built the graph, drained the in-degrees, counted, done.
>
> Now the interviewer leans in: *"Great. Now give me the actual order to take them in."*
>
> Here's the beautiful part — the order was already flowing through our code. We just weren't writing it down. One line changes. Let me show you exactly which one, and why it's guaranteed correct.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:30`
*(concrete before abstract)*

**[VISUAL: "numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]" → "[0, 1, 2, 3]". A note: "or [0,2,1,3] — any valid order."]**

> The problem in one line: **return a valid order to take all the courses.** If it's impossible — a cycle — return an empty array.
>
> Same four courses as last time. A valid answer is `[0, 1, 2, 3]`. So is `[0, 2, 1, 3]` — course 0 first, course 3 last, and the middle two can swap. Any legal order counts.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:05`
*(worked example — let them feel the waste)*

**[VISUAL: courses {0,1,2,3}, a "placed" list building up, a "passes" counter.]**

> The brute-force reflex, same as before: repeatedly scan for any course whose prerequisites are all already placed, append it, rescan.
>
> Pass 1: 0 is free → place it. Rescan. Pass 2: 1 and 2 are free → place both. Rescan. Pass 3: 3 is free → place it.
>
> **[VISUAL: each pass re-sweeps the full remaining set; counter climbs.]**
>
> It produces `[0, 1, 2, 3]` — correct. But it's the same sin as last lesson: every pass re-checks every remaining course's *entire* prerequisite set from scratch. Quadratic. We already know the cure.

---

## 4. THE PAIN POINT + PREDICT — `2:00`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the repeated rescans. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** We fixed exactly this waste last time with in-degrees — take a course, decrement only what it unlocks, no rescans.
>
> **LEARNER:** Right, but that version just *counted* how many we took. It threw the order away. Do I need a whole new algorithm to capture the order?
>
> **TEACHER:** That's the question. Pause and predict: **in Kahn's algorithm, the courses come off the queue in some sequence. Is that pop sequence already a valid order — or do we need extra bookkeeping to sort them?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `2:40`
*(elaboration — derive it)*

**[VISUAL: the graph draining. As each course pops, it drops into a growing "order" list on the right: [0] → [0,1] → [0,1,2] → [0,1,2,3].]**

> **TEACHER:** Here's the insight, and it's lovely: a course is popped from the queue **only after every one of its prerequisites was already popped.** That's baked into how in-degree works — a course only reaches in-degree zero once all its blockers are gone, and they're gone because we already took them.
>
> So the pop order *is* a valid topological order, for free. When I append course 3, courses 1 and 2 are guaranteed to already sit earlier in the list.
>
> **LEARNER:** So the fix is literally… record what I pop?
>
> **TEACHER:** That's the entire change. Replace the counter with a list. Instead of `taken += 1`, do `order.append(course)`. The algorithm was already doing the hard part.

---

## 6. THE KEY MOVE (signaling) — `3:45`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "The dequeue order IS the topological order — just append as you pop."]**

> The key move: **the order courses leave the queue is a valid schedule — so append each one as you pop it.** No sorting, no extra pass. The queue hands you the answer in order.

---

## 7. CODE IT — LIVE & CHUNKED — `4:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Chunk 1 — identical to last lesson, highlighted "same as before".]**

> Setup is word-for-word Course Schedule I: build the graph, count in-degrees.

```python
from collections import deque

def find_order(numCourses, prerequisites):
    graph = [[] for _ in range(numCourses)]   # b -> courses b unlocks
    indegree = [0] * numCourses
    for a, b in prerequisites:                # edge b -> a
        graph[b].append(a)
        indegree[a] += 1
```

> **[VISUAL: chunk 2. The word `order = []` glows — "the one new idea".]** Seed the queue, and this time keep an `order` list instead of a counter.

```python
    queue = deque(c for c in range(numCourses) if indegree[c] == 0)
    order = []
```

> **[VISUAL: chunk 3. Highlight the single changed line `order.append(course)`.]** Drain — and record every pop.

```python
    while queue:
        course = queue.popleft()
        order.append(course)                  # dequeue order = topo order
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return order if len(order) == numCourses else []
```

---

## 8. EXPLAIN THE CODE (the WHY) — `5:45`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight the changed lines vs. last lesson.]**

> The only two differences from Course Schedule I: `order = []` instead of `taken = 0`, and `order.append(course)` instead of `taken += 1`. That's it.
>
> `order.append(course)` — every course leaves the queue *after* its prerequisites left, so appending here builds a legal order left to right.
>
> **LEARNER:** The cycle case — last time we returned `taken == numCourses`. Now we return a list. How does the cycle check survive?
>
> **TEACHER:** Same idea, read off the length. If a cycle traps some courses, they never reach in-degree zero, never get appended, so `len(order) < numCourses`. When that happens we return `[]`, exactly as the problem demands. The length check *is* the cycle detector — just like `taken` was.

---

## 9. DRY-RUN THE CODE — `6:45`
*(worked example — prove it, close the loop)*

**[VISUAL: graph 0→1, 0→2, 1→3, 2→3; in-degrees [0,1,1,2]; the `order` list filling.]**

> Run it.

| pop | order | decrements | new zeros → queue |
|---|---|---|---|
| 0 | [0] | 1→0, 2→0 | 1, 2 |
| 1 | [0,1] | 3→1 | — |
| 2 | [0,1,2] | 3→0 | 3 |
| 3 | [0,1,2,3] | — | — |

> `len(order) == 4` → return **`[0, 1, 2, 3]`.** ✅
>
> And notice: if the queue had popped 2 before 1, we'd get `[0, 2, 1, 3]` — also valid. Both are correct topological orders; the problem accepts any. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:45`
*(transfer to interview)*

**[VISUAL: O(V + E) time, O(V + E) space; note "same as Schedule I".]**

> Out loud: *"Identical to Course Schedule I — O(V plus E) time, since each course enqueues once and each edge relaxes once. O(V plus E) space for the graph, in-degree array, queue, and the output list. Returning the order costs nothing extra asymptotically."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:15`
*(depth + honesty)*

**[VISUAL: the output list highlighted — "this IS the answer, can't be removed".]**

> Space is already at the floor. The output list is O(V) — but that's the answer itself, unavoidable. The graph is O(E), the in-degree array and queue O(V). Nothing is slack.
>
> The alternative is **DFS post-order**: run DFS, push a node after exploring all its successors, then reverse the stack. Same O(V + E), recursion stack instead of a queue, plus you need three-color marking to catch cycles. Kahn's wins on the whiteboard because it returns the order forward — no final reverse — and the cycle check is just a length comparison.

---

## 12. YOUR TURN (active recall) — `8:45`
*(retrieval practice)*

**[VISUAL: "Your turn → Alien Dictionary (LC 269)". A blank editor.]**

> Before the next video, try **Alien Dictionary.** Here's the twist: nobody hands you the graph. You're given words sorted in an unknown alphabet, and you have to *derive* the edges yourself — then run this exact topo sort. The sorting logic you just wrote is the second half; the challenge is building the graph. Give it a real ten-minute fight.

---

## 13. LOCK IT IN — `9:15`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Course Schedule II = Schedule I + record the pops.** One line changes.
> 2. **Dequeue order is a valid topological order** — guaranteed, because a node pops only after all its prerequisites.
> 3. **`len(order) < numCourses` → cycle → return `[]`.**
>
> The peg: **the queue already knows the order — just write down what you pop.**

---

## 14. CLIFFHANGER — `9:45`
*(open loop to next lesson)*

**[VISUAL: two words stacked — "wrt" / "wrf" — with the 't' and 'f' glowing at the first difference.]**

> So far the graph was handed to us on a plate. But what if the interviewer gives you a list of words in an *alien* language, sorted by rules you don't know — and asks for the alphabet? No edges, no in-degrees, nothing. You have to *manufacture* the graph from the ordering of the words themselves. One comparison, one edge. That's the next one: Alien Dictionary — topo sort's Hard-mode boss. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
import java.util.*;

public int[] findOrder(int numCourses, int[][] prerequisites) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
    int[] indegree = new int[numCourses];
    for (int[] p : prerequisites) {        // p = [a, b], edge b -> a
        graph.get(p[1]).add(p[0]);
        indegree[p[0]]++;
    }

    Deque<Integer> queue = new ArrayDeque<>();
    for (int c = 0; c < numCourses; c++)
        if (indegree[c] == 0) queue.offer(c);

    int[] order = new int[numCourses];
    int idx = 0;
    while (!queue.isEmpty()) {
        int course = queue.poll();
        order[idx++] = course;
        for (int nxt : graph.get(course))
            if (--indegree[nxt] == 0) queue.offer(nxt);
    }
    return idx == numCourses ? order : new int[0];
}
```
