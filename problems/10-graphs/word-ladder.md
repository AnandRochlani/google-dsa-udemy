# Word Ladder

> **LeetCode:** 127. Word Ladder · **Difficulty:** 🔴 Hard · **Pattern:** Graph BFS/DFS (BFS over a word graph, shortest transformation) · **Google frequency:** medium

---

## Problem

Given `beginWord`, `endWord`, and a `wordList`, a **transformation sequence** is a chain `beginWord → w1 → w2 → … → endWord` where **each adjacent pair differs by exactly one letter** and every intermediate word is in `wordList`. Return the **length** of the *shortest* such sequence (counting both endpoints), or `0` if none exists.

**Example:**

```
beginWord = "hit"
endWord   = "cog"
wordList  = ["hot", "dot", "dog", "lot", "log", "cog"]
```

Shortest chain: `hit → hot → dot → dog → cog` — that's **5** words.

```
hit
 |  (change i→o)
hot
 |  (change h→d)          (change h→l)
dot ---------------------- lot
 |  (t→g)                   |  (t→g)
dog                        log
 |  (d→c)                   |  (l→c)
 +---------> cog <----------+
```

**Constraints that matter:** words up to length 10, `wordList` up to 5000 words. `endWord` must be in `wordList` or the answer is `0`. "**Shortest** transformation" + "each step differs by one letter" = shortest path in an unweighted graph → **BFS**. The trap is how you find neighbors efficiently: comparing every word to every other is `O(N²·L)` and often too slow.

---

## 🧠 Intuition — how you'd actually arrive at this

> Two leaps: (1) see the words as a graph, (2) build neighbors cheaply with wildcard patterns.

- **First instinct:** "From `beginWord`, what words can I reach in one change? Then from those, what's reachable? Keep going until I hit `endWord`, tracking how many steps." That step-by-step, expand-the-frontier search *is* BFS.
- **The reframe — words as graph nodes:** each word is a **node**; put an edge between two words if they differ by exactly one letter. A transformation sequence is a **path** in this graph, and "shortest sequence" is the **shortest path**. Since every edge is one step (unweighted), **BFS from `beginWord` finds the shortest path** — the level at which `endWord` first appears is the answer.
- **Where it hurts — finding neighbors:** the naive way to get a word's neighbors is to compare it against all `N` words in the list (`O(N·L)` per word, `O(N²·L)` overall). At `N=5000` that bites.
- **The neighbor trick — wildcard patterns:** two words are neighbors iff they share a pattern like `h*t` (one position replaced by `*`). Pre-bucket every word by all `L` of its wildcard patterns: `"hot"` goes into buckets `*ot`, `h*t`, `ho*`. To find a word's neighbors, generate its `L` patterns and grab everyone in those buckets — `O(L)` pattern lookups instead of scanning `N` words. This turns neighbor discovery from `O(N)` into `O(L·26)`-ish.
- **BFS, not DFS:** shortest path in an unweighted graph is BFS's signature. DFS would explore full depth first and can't guarantee the first time it reaches `endWord` is via the fewest steps without extra machinery.
- **Pattern trigger:** **"shortest transformation / fewest steps between states, each step a small edit"** → model states as graph nodes, edits as edges, and **BFS** for the shortest path.

---

## ① Brute Force

BFS over the word graph, but discover neighbors by scanning the whole word list and counting letter differences for each candidate.

```python
from collections import deque

def ladderLength_brute(beginWord, endWord, wordList):
    words = set(wordList)
    if endWord not in words:
        return 0

    def differs_by_one(a, b):
        return sum(x != y for x, y in zip(a, b)) == 1

    q = deque([(beginWord, 1)])
    visited = {beginWord}
    while q:
        word, steps = q.popleft()
        if word == endWord:
            return steps
        for cand in list(words):                 # scan EVERY remaining word
            if cand not in visited and differs_by_one(word, cand):
                visited.add(cand)
                q.append((cand, steps + 1))
    return 0
```

**Why it's the natural first attempt:** the BFS skeleton is exactly right — expand level by level, return the depth when `endWord` appears. Comparing every pair of words is the obvious way to know who's adjacent.

**Why it's not enough:** for each of up to `N` dequeued words you scan all `N` words and do an `O(L)` comparison → **`O(N²·L)`**. With `N=5000, L=10` that's `~2.5×10⁸` char comparisons in the worst case — slow, and it re-scans the list repeatedly.

**Complexity:** Time `O(N² · L)`, Space `O(N)`.

---

## ② Optimised Solution

BFS with **wildcard-pattern buckets** for `O(L)` neighbor lookup.

```python
from collections import deque, defaultdict

def ladderLength(beginWord, endWord, wordList):
    words = set(wordList)
    if endWord not in words:
        return 0

    L = len(beginWord)

    # pre-bucket: pattern "h*t" -> [all words matching it]
    patterns = defaultdict(list)
    for word in words:
        for i in range(L):
            patterns[word[:i] + '*' + word[i+1:]].append(word)

    q = deque([(beginWord, 1)])
    visited = {beginWord}
    while q:
        word, steps = q.popleft()
        if word == endWord:
            return steps
        for i in range(L):
            pat = word[:i] + '*' + word[i+1:]
            for nei in patterns[pat]:            # all one-letter neighbors, O(bucket)
                if nei not in visited:
                    visited.add(nei)
                    q.append((nei, steps + 1))
            patterns[pat] = []                   # optional: clear bucket so it's not rescanned
    return 0
```

**Walk the example** (`hit` → `cog`):

- Buckets include `*ot: [hot,dot,lot]`, `h*t: [hot]`, `d*t: [dot]`, `do*: [dot,dog]`, `*og: [dog,log,cog]`, `co*: [cog]`, etc.
- **Level 1:** dequeue `("hit", 1)`. Patterns `*it, h*t, hi*`. `h*t` bucket → `hot`. Enqueue `("hot", 2)`.
- **Level 2:** dequeue `("hot", 2)`. Patterns `*ot → [dot,lot]`, `h*t → []` (hot visited), `ho* → []`. Enqueue `("dot", 3)`, `("lot", 3)`.
- **Level 3:** dequeue `("dot", 3)` → `do*` gives `dog`; enqueue `("dog", 4)`. dequeue `("lot", 3)` → `lo*` gives `log`; enqueue `("log", 4)`.
- **Level 4:** dequeue `("dog", 4)` → `*og` gives `cog`; enqueue `("cog", 5)`. (`log` also reaches `cog` but it's already visited.)
- **Level 5:** dequeue `("cog", 5)` → `word == endWord` → **return 5.** ✅

**Why it's correct:** BFS explores words in increasing distance from `beginWord`, so the first time `endWord` is dequeued it's via a shortest chain. The `visited` set prevents revisiting (and cycles). Wildcard buckets enumerate *exactly* the one-letter neighbors — any word sharing pattern `h*t` differs from `hit` only at that position — so we never miss or over-count an edge.

**Complexity:** Time `O(N · L²)` — `N` words, each generating `L` patterns of length `L` (string slicing is `O(L)`); each edge processed once overall. Space `O(N · L²)` for the pattern buckets and visited set.

---

## ③ Space Optimization

The big extra structure is the pattern-bucket map, `O(N · L²)`. You *can* trade it away by generating neighbors **on the fly**: for each position, try all 26 letters and check membership in the word set — no precomputed buckets.

```python
from collections import deque
import string

def ladderLength_26(beginWord, endWord, wordList):
    words = set(wordList)
    if endWord not in words:
        return 0
    L = len(beginWord)
    q = deque([(beginWord, 1)])
    visited = {beginWord}
    while q:
        word, steps = q.popleft()
        if word == endWord:
            return steps
        for i in range(L):
            for ch in string.ascii_lowercase:
                nxt = word[:i] + ch + word[i+1:]
                if nxt in words and nxt not in visited:
                    visited.add(nxt)
                    q.append((nxt, steps + 1))
    return 0
```

**Complexity:** Time `O(N · L · 26)` neighbor generations, each an `O(L)` slice + set lookup → `O(N · L² · 26)`; Space `O(N · L)` for the word set and visited (no bucket map). This drops the `O(N·L²)` bucket storage — lower space, same asymptotic time class, slightly higher constant from the 26× letter sweep.

> The real pro move on a **Hard** follow-up: **bidirectional BFS** — search forward from `beginWord` and backward from `endWord`, alternating and always expanding the smaller frontier, stopping when they meet. It roughly halves the explored radius (from `b^d` to `2·b^(d/2)`), a big practical speedup, though same worst-case class. Mention it out loud even if you don't code it fully.

---

## Java (for Java interviewers)

```java
public int ladderLength(String beginWord, String endWord, List<String> wordList) {
    Set<String> words = new HashSet<>(wordList);
    if (!words.contains(endWord)) return 0;

    int L = beginWord.length();
    Queue<String> q = new ArrayDeque<>();
    q.offer(beginWord);
    Set<String> visited = new HashSet<>();
    visited.add(beginWord);
    int steps = 1;

    while (!q.isEmpty()) {
        for (int sz = q.size(); sz > 0; sz--) {
            String word = q.poll();
            if (word.equals(endWord)) return steps;
            char[] arr = word.toCharArray();
            for (int i = 0; i < L; i++) {
                char original = arr[i];
                for (char ch = 'a'; ch <= 'z'; ch++) {
                    arr[i] = ch;
                    String next = new String(arr);
                    if (words.contains(next) && !visited.contains(next)) {
                        visited.add(next);
                        q.offer(next);
                    }
                }
                arr[i] = original;
            }
        }
        steps++;
    }
    return 0;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (compare all pairs) | O(N² · L) | O(N) |
| Optimised (wildcard buckets) | O(N · L²) | O(N · L²) |
| On-the-fly 26-letter BFS | O(N · L² · 26) | O(N · L) |
| Bidirectional BFS | ~O(N · L²) but far smaller frontier | O(N · L) |

---

## Say it out loud (interview narration)

> *"Each word is a graph node, and two words share an edge if they differ by one letter. A transformation sequence is a path, and 'shortest' in an unweighted graph means BFS from beginWord — the level where endWord first appears is the answer. The naive way to find neighbors is comparing every pair, O(N²·L). Instead I pre-bucket words by wildcard patterns like h*t, so a word's one-letter neighbors are just the union of its L pattern buckets — neighbor lookup in O(L) instead of O(N). BFS with a visited set gives the shortest length. To save the bucket memory I can generate neighbors on the fly by trying all 26 letters per position and checking a word-set. And on a hard variant I'd reach for bidirectional BFS — search from both ends and meet in the middle — to roughly halve the search radius."*

## Related / follow-ups
- **Word Ladder II** (LC 126) — return *all* shortest sequences (BFS to build the graph, then DFS to reconstruct paths)
- **Minimum Genetic Mutation** (LC 433) — the identical pattern with a 4-letter alphabet
- **Open the Lock** (LC 752) — BFS over 4-digit states, each turn a one-step edit
- **Shortest Path in Binary Matrix** (LC 1091) — BFS shortest path on a grid graph
