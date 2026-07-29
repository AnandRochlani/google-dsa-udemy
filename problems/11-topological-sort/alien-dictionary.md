# Alien Dictionary

> **LeetCode:** 269. Alien Dictionary · **Difficulty:** 🔴 Hard · **Pattern:** Topological Sort · **Google frequency:** ⭐ high

---

## Problem

There's a new language that uses lowercase English letters, but in an **unknown alphabetical order**. You're given a list of words that are sorted according to that alien order. Derive a possible ordering of the letters as a string. If no valid order exists (the input is contradictory), return `""`. If multiple orders are valid, return any.

**Example:** `words = ["wrt","wrf","er","ett","rftt"]` → `"wertf"`.
`words = ["z","x"]` → `"zx"`. `words = ["z","x","z"]` → `""` *(contradiction: z<x and x<z).*

**Constraints that matter:** the words themselves give you no complete ordering — only **pairwise hints**. Comparing two adjacent words tells you the order of exactly *one* pair of letters (the first position where they differ). The whole problem is: gather those hints into a directed graph, then topologically sort the letters. There are at most 26 letters, so the graph is tiny; the subtlety is *building it correctly*.

---

## 🧠 Intuition — how you'd actually arrive at this

- **What does "sorted" actually tell me?** If `word1` comes before `word2` in the list, scan them character by character. At the **first position where they differ**, `word1`'s letter must come *before* `word2`'s letter in the alien alphabet. That single comparison is one directed edge `c1 → c2`. Every character *after* that first difference tells you nothing.
- **Reframe as a graph:** each letter is a node; each "first-difference" comparison is a directed edge. Finding a consistent alphabet = finding a topological order of this graph. So this is Course Schedule II with a **graph-building preamble.**
- **The two Hard-level traps:**
  1. **The prefix contradiction.** If `word1` is longer than `word2` but `word2` is a prefix of `word1` — e.g. `["abc", "ab"]` — that's impossible in a real dictionary (a prefix must sort first). You must detect this and return `""`. Miss it and you'll wrongly produce an answer.
  2. **Cycle = contradiction.** If the hints imply `a < b` and `b < a`, topo sort can't include all letters → return `""`.
- **Don't forget lonely letters:** every character that appears in any word is a node, even if it never gets an edge (e.g. it only ever appears in equal positions). Seed the graph with all of them first.
- **Pattern trigger:** **"derive an ordering from pairwise 'this before that' evidence"** → **build a directed graph, then Topological Sort.**

Recall: **in-degree** = number of edges pointing *into* a node — here, how many letters are known to come before this one.

---

## ① Brute Force

There's no meaningfully different "naive" algorithm — you still must extract the edges. The brute-force *flavor* is to resolve the ordering by repeated scanning instead of tracking in-degrees: after building the pairwise constraints, repeatedly pick any letter that has no unplaced predecessor, append it, and rescan.

```python
def alien_order_brute(words):
    # 1) collect nodes and pairwise "before" constraints
    letters = set("".join(words))
    before = {c: set() for c in letters}      # before[c] = letters that must precede c
    for w1, w2 in zip(words, words[1:]):
        if len(w1) > len(w2) and w1.startswith(w2):
            return ""                          # prefix contradiction
        for a, b in zip(w1, w2):
            if a != b:
                before[b].add(a)
                break

    # 2) repeatedly place any letter whose predecessors are all placed
    placed, result = set(), []
    while len(result) < len(letters):
        progress = False
        for c in letters:
            if c not in placed and before[c] <= placed:
                placed.add(c); result.append(c); progress = True
        if not progress:
            return ""                          # cycle
    return "".join(result)
```

**Why it's the natural first attempt:** it directly encodes "keep placing whatever letter is currently unblocked."

**Why it's not enough:** the graph-building is fine, but the placement loop rescans all letters every round — `O(k²)` in the number of distinct letters `k`. With `k ≤ 26` it's harmless here, but it doesn't scale as a *pattern* and hides the clean in-degree formulation an interviewer wants to see.

**Complexity:** Time `O(C + k²)` where `C` = total characters across all words, `k` = distinct letters. Space `O(k + unique edges)`.

---

## ② Optimised Solution

Build the graph, compute in-degrees, run Kahn's BFS.

```python
from collections import deque

def alien_order(words):
    graph = {c: set() for w in words for c in w}   # every letter is a node
    indegree = {c: 0 for c in graph}

    for w1, w2 in zip(words, words[1:]):
        # prefix contradiction: "abc" before "ab" is invalid
        if len(w1) > len(w2) and w1.startswith(w2):
            return ""
        for a, b in zip(w1, w2):
            if a != b:
                if b not in graph[a]:              # avoid double-counting edges
                    graph[a].add(b)
                    indegree[b] += 1
                break                              # only the FIRST difference counts

    queue = deque(c for c in indegree if indegree[c] == 0)
    order = []
    while queue:
        c = queue.popleft()
        order.append(c)
        for nxt in graph[c]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return "".join(order) if len(order) == len(indegree) else ""  # "" if cycle
```

**Walk the example** `["wrt","wrf","er","ett","rftt"]`:

- `wrt` vs `wrf`: first diff at index 2 → `t → f`.
- `wrf` vs `er`: first diff at index 0 → `w → e`.
- `er` vs `ett`: first diff at index 1 → `r → t`.
- `ett` vs `rftt`: first diff at index 0 → `e → r`.
- Nodes: `{w,r,t,f,e}`. Edges: `t→f, w→e, r→t, e→r`. In-degrees: `w:0, e:1, r:1, t:1, f:1`.
- Queue `[w]` → pop `w`, decrement `e`→0, queue `[e]` → pop `e`, decrement `r`→0 → pop `r`, decrement `t`→0 → pop `t`, decrement `f`→0 → pop `f`.
- `order = "wertf"`, length 5 = number of letters → **`"wertf"`** ✅.

**Why it's correct:** each adjacent-word comparison contributes exactly the one edge the dictionary ordering guarantees (the first differing position); later positions carry no information and are skipped. Kahn's produces a valid order consistent with all edges, and a cycle (contradiction) surfaces as `len(order) < number of letters`. The prefix check catches the one impossibility the edge logic can't see.

**Complexity:** Time `O(C)` where `C` = total characters (building the graph dominates; the topo sort over ≤26 nodes is `O(1)`-ish). Space `O(1)` effectively — at most 26 nodes and 26² edges, i.e. `O(k + k²)` bounded by a constant.

---

## ③ Space Optimization

The graph is bounded by the alphabet — **at most 26 nodes and 26×25 edges** — so the working set is constant regardless of how many or how long the words are. You genuinely can't do better: you must at least read every character once to extract the constraints, so `O(C)` time and `O(1)` extra space (constant-bounded graph) is optimal.

The only thing to *not* waste is comparing beyond the first differing character, or comparing non-adjacent words — both add no information and would just cost time. Guarding the edge insertion with `if b not in graph[a]` avoids inflating in-degrees with duplicate edges (a classic bug that makes valid inputs return `""`).

> Already optimal — the graph is capped at the 26-letter alphabet, so it's constant space; you can only spend time on the unavoidable single pass over all characters.

---

## Java (for Java interviewers)

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
        if (w1.length() > w2.length() && w1.startsWith(w2)) return "";  // prefix
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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (rescan placement) | O(C + k²) | O(k + edges) |
| Kahn's BFS | O(C) | O(1) (≤26 nodes, constant-bounded) |

*(C = total characters across all words; k = number of distinct letters ≤ 26.)*

---

## Say it out loud (interview narration)

> *"Being 'sorted' only gives pairwise hints: for each adjacent pair of words, the first position where they differ tells me one letter comes before another — that's one directed edge. I build a graph over all letters that appear, guarding against duplicate edges, and I special-case the prefix trap: if a longer word precedes its own prefix, that's impossible, return empty string. Then it's just topological sort — Kahn's on in-degrees. If a cycle means I can't emit every letter, the constraints contradict, so I return empty string. The alphabet caps the graph at 26 nodes, so it's O(total characters) time and constant space."*

## Related / follow-ups
- **Course Schedule II** (the pure topo-sort core, once the graph is built)
- **Sequence Reconstruction** (is the derived order unique — does the queue ever hold >1 node?)
- **Verifying an Alien Dictionary** (LC 953 — check words are sorted given the order; the inverse problem)
