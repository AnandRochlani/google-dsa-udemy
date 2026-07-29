# 🎬 Recording Script — Alien Dictionary
**Pattern: Topological Sort · LeetCode 269 · Hard · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Course Schedule II (Kahn's BFS returns the order) — previous lesson.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a leather-bound "Alien Dictionary". Words scroll past in gibberish order: wrt, wrf, er, ett, rftt. A caption: "sorted — but by WHAT alphabet?"]**

> This is one of Google's favorite Hard problems, and it looks impossible at first: *"Here's a dictionary from an alien language. The words are sorted — but by an alphabet you don't know. Figure out the alphabet."*
>
> No prerequisites given. No graph. Just a pile of words. It feels like you'd need to be a cryptographer.
>
> But here's the secret: it's the topo sort you already know, wearing a disguise. The *only* new skill is manufacturing the graph out of thin air — and it comes down to one tiny observation about what "sorted" really means. Let's crack it.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: "words = ['z', 'x']  →  'zx'". Below: "words = ['z', 'x', 'z']  →  '' (contradiction)".]**

> The problem in one line: **given words sorted in an unknown alphabet, return a possible ordering of the letters.** If the input contradicts itself, return an empty string.
>
> Tiniest example: `["z", "x"]`. Since "z" sorts before "x", z must come before x in their alphabet. Answer: `"zx"`.
>
> Now `["z", "x", "z"]` — z before x, but then x before z. Impossible. Return `""`. Hold that contradiction; it's one of two traps.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — build the real skill)*

**[VISUAL: two words stacked: `w r t` over `w r f`. A finger scans left to right.]**

> Let's figure out what "sorted" actually hands us. Take two adjacent words, `wrt` and `wrf`. Scan them together, letter by letter.
>
> `w` equals `w` — no info. `r` equals `r` — no info. `t` versus `f` — they differ! And since `wrt` sorts *before* `wrf`, that first difference tells us: **`t` comes before `f`** in the alien alphabet.
>
> **[VISUAL: an arrow t → f pops out. The remaining letters after the diff get grayed out with a label "irrelevant".]**
>
> Critical: everything *after* that first difference tells us nothing. Once `t` beats `f`, the rest of the word is irrelevant. One adjacent pair gives you exactly **one edge.**
>
> **[VISUAL: repeat quickly for all adjacent pairs, edges accumulating: t→f, w→e, r→t, e→r.]**

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: the loose edges floating: t→f, w→e, r→t, e→r, plus five lonely letter nodes. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So each pair of neighboring words gives me one "this letter before that letter" rule. Now I've got a fistful of these rules — `t` before `f`, `w` before `e`, and so on.
>
> **LEARNER:** Hang on — those are just directed "before" relationships between letters. That's… prerequisites. That's a graph.
>
> **TEACHER:** *There* it is. Pause and predict: **once I've collected every "before" edge, what algorithm from the last two lessons turns a pile of "this before that" constraints into a single valid ordering?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:30`
*(elaboration — derive it)*

**[VISUAL: the loose edges snap into a clean directed graph. In-degree badges appear: w:0, e:1, r:1, t:1, f:1.]**

> **TEACHER:** It's topological sort — the exact Kahn's drain from Course Schedule II. Each letter is a node. Each "before" rule is a directed edge. A valid alphabet is a topological order of this graph.
>
> Remember **in-degree** — the number of edges pointing *into* a node, here "how many letters are known to come before this one." Letter `w` has in-degree 0. Drain from there.
>
> So the shape of the whole solution: **build the graph from adjacent-word comparisons, then run Kahn's BFS.** The second half you already own.
>
> **LEARNER:** But this is a *Hard* problem. If it's just topo sort with a graph-building step, where's the difficulty?
>
> **TEACHER:** Two traps hide in the graph-building — and they're what separate a hire from a no-hire. Let me show you both before we code.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence + the two traps)*

**[VISUAL: boxed line: "First differing letter of each adjacent pair = one edge. Then topo-sort."] Then two red trap cards slide in.]**

> The key move: **for each adjacent word pair, the first position where they differ gives one edge; then topologically sort the letters.**
>
> Now the two traps.
>
> **[VISUAL: Trap 1 card — "abc" over "ab", a big red ✗.]**
>
> **Trap 1 — the prefix contradiction.** If a longer word comes *before* its own prefix — like `["abc", "ab"]` — that's impossible in any real dictionary. "ab" must sort before "abc". If you scan for a first difference, you never find one, and you'd wrongly move on. You must detect this and return `""`.
>
> **[VISUAL: Trap 2 card — a cycle a→b→a, red ✗.]**
>
> **Trap 2 — the cycle.** If the edges imply `a` before `b` *and* `b` before `a`, no order exists. Just like Course Schedule, a cycle means the topo sort can't emit every letter → return `""`.

---

## 7. CODE IT — LIVE & CHUNKED — `5:45`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Chunk 1.]**

> First, every letter that appears is a node — even lonely ones with no edges. Seed the graph and in-degrees with all of them.

```python
from collections import deque

def alien_order(words):
    graph = {c: set() for w in words for c in w}   # every letter is a node
    indegree = {c: 0 for c in graph}
```

> **[VISUAL: chunk 2, the prefix guard glowing red.]** Now compare adjacent words. Guard the prefix trap *first*, then find the single first difference.

```python
    for w1, w2 in zip(words, words[1:]):
        if len(w1) > len(w2) and w1.startswith(w2):
            return ""                              # Trap 1: prefix contradiction
        for a, b in zip(w1, w2):
            if a != b:
                if b not in graph[a]:              # avoid double-counting edges
                    graph[a].add(b)
                    indegree[b] += 1
                break                              # only the FIRST diff counts
```

> **[VISUAL: chunk 3 — the familiar Kahn's drain.]** And now the topo sort you already know.

```python
    queue = deque(c for c in indegree if indegree[c] == 0)
    order = []
    while queue:
        c = queue.popleft()
        order.append(c)
        for nxt in graph[c]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return "".join(order) if len(order) == len(indegree) else ""  # Trap 2: cycle
```

---

## 8. EXPLAIN THE CODE (the WHY) — `8:00`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight each line as named.]**

> Walk the *why*.
>
> `{c: set() for w in words for c in w}` — this seeds a node for *every* letter that ever appears. Miss this and a lonely letter — one that only shows up in equal positions — silently vanishes from your answer.
>
> The prefix guard runs *before* the difference scan, because the prefix case has *no* differing letter to find. It's the one impossibility the edge logic literally cannot see.
>
> `break` after the first difference — this is the heart. Only the first differing position carries ordering information. Keep comparing past it and you'd invent edges that don't exist.
>
> **LEARNER:** Why the `if b not in graph[a]` guard? If I add the same edge twice, isn't it still just... one relationship?
>
> **TEACHER:** Great catch, and it's a classic bug. The *set* would dedupe the edge fine — but `indegree[b] += 1` runs regardless. Add the same edge twice and b's in-degree inflates to 2 when only 1 letter precedes it. Then it never drains to zero, and a perfectly valid input returns `""`. The guard keeps the in-degree honest.
>
> Finally, `len(order) == len(indegree)` — the cycle check. If contradictory edges trap some letters, they never drain, `order` comes up short, and we return `""`.

---

## 9. DRY-RUN THE CODE — `9:45`
*(worked example — prove it, close the loop)*

**[VISUAL: `["wrt","wrf","er","ett","rftt"]`, edges being extracted pair by pair, then the drain.]**

> Run the full example. Extract edges from adjacent pairs:

| pair | first diff | edge |
|---|---|---|
| wrt, wrf | index 2: t vs f | t → f |
| wrf, er | index 0: w vs e | w → e |
| er, ett | index 1: r vs t | r → t |
| ett, rftt | index 0: e vs r | e → r |

> Nodes `{w, r, t, f, e}`. In-degrees: `w:0, e:1, r:1, t:1, f:1`. Now drain:

| pop | order | decrement → new zero |
|---|---|---|
| w | w | e → 0 |
| e | we | r → 0 |
| r | wer | t → 0 |
| t | wert | f → 0 |
| f | wertf | — |

> `order = "wertf"`, length 5 = number of letters → **`"wertf"`.** ✅ Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `11:15`
*(transfer to interview)*

**[VISUAL: "O(C) time, C = total characters. Graph capped at 26 nodes."]**

> Out loud: *"Let C be the total number of characters across all words. Building the graph reads every character once — O(C). The topo sort runs over at most 26 nodes and 26-squared edges, which is constant. So it's O(C) time. Space is effectively constant — the alphabet caps the graph at 26 nodes."*
>
> That "capped at 26" line is a strong detail — it shows you noticed the alphabet bounds the whole graph regardless of how many words come in.

---

## 11. CAN WE USE LESS MEMORY? (space) — `12:00`
*(depth + honesty)*

**[VISUAL: a 26×26 grid, mostly empty — "constant-bounded".]**

> Space is already optimal, and here's the honest framing: the graph can *never* exceed 26 letters and 26×25 edges, no matter how many or how long the words are. That's constant. You can't beat O(C) time either — you must read every character at least once to extract the constraints.
>
> The only thing to *avoid wasting* is effort: don't compare past the first differing character, and don't compare non-adjacent words — both add zero information. And keep that duplicate-edge guard, or you'll manufacture false contradictions.

---

## 12. YOUR TURN (active recall) — `12:45`
*(retrieval practice)*

**[VISUAL: "Your turn → Sequence Reconstruction (LC 444)". A blank editor.]**

> Before the next video, try **Sequence Reconstruction.** The question becomes: is the topological order *unique*? Here's the hint that unlocks it — the order is unique only if, at every step of Kahn's drain, the queue holds *exactly one* node. If it ever holds two, you had a choice, and the order isn't forced. Ten minutes, no peeking.

---

## 13. LOCK IT IN — `13:15`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **First differing letter of an adjacent pair = one edge.** Everything after it is noise.
> 2. **Two traps:** the prefix contradiction (`"abc"` before `"ab"`) and the cycle. Both return `""`.
> 3. **Guard duplicate edges** so in-degrees stay honest.
>
> The peg: **compare neighbors, take the first difference, then it's just topo sort.**

---

## 14. CLIFFHANGER — `13:45`
*(open loop to next lesson)*

**[VISUAL: a tree with branches, a red pin hunting for its "center". A blurred title: "Minimum Height Trees".]**

> Every topo sort so far drained a *directed* graph by in-degree. But what if the graph is undirected — a plain tree — and instead of "who has no prerequisites," you want to find its *center*? Turns out you peel it from the outside in, trimming leaves layer by layer, and it's the same Kahn's rhythm with one word swapped: degree instead of in-degree. That's the next one: Minimum Height Trees. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
import java.util.*;

public String alienOrder(String[] words) {
    Map<Character, Set<Character>> graph = new HashMap<>();
    Map<Character, Integer> indegree = new HashMap<>();
    for (String w : words)
        for (char c : w.toCharArray()) {
            graph.putIfAbsent(c, new HashSet<>());
            indegree.putIfAbsent(c, 0);
        }

    for (int i = 0; i + 1 < words.length; i++) {
        String w1 = words[i], w2 = words[i + 1];
        if (w1.length() > w2.length() && w1.startsWith(w2)) return "";  // prefix trap
        int len = Math.min(w1.length(), w2.length());
        for (int j = 0; j < len; j++) {
            char a = w1.charAt(j), b = w2.charAt(j);
            if (a != b) {
                if (graph.get(a).add(b)) indegree.merge(b, 1, Integer::sum);
                break;                          // only first difference
            }
        }
    }

    Deque<Character> queue = new ArrayDeque<>();
    for (char c : indegree.keySet())
        if (indegree.get(c) == 0) queue.offer(c);

    StringBuilder sb = new StringBuilder();
    while (!queue.isEmpty()) {
        char c = queue.poll();
        sb.append(c);
        for (char nxt : graph.get(c))
            if (indegree.merge(nxt, -1, Integer::sum) == 0) queue.offer(nxt);
    }
    return sb.length() == indegree.size() ? sb.toString() : "";
}
```
