# 🎬 Recording Script — Word Ladder
**Pattern: Graphs (BFS shortest path over an implicit word graph) · LeetCode 127 · Hard · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** every earlier graph was *handed* to us. Here we have to *build* the graph ourselves — and BFS still finds the shortest path.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: the word "hit" morphs one letter at a time — hit → hot → dot → dog → cog. A "Hard" badge glints.]**

> This one's marked **Hard**, and it rattles people: *"Turn `hit` into `cog`, changing one letter at a time, where every step has to be a real word from this list. What's the shortest chain?"*
>
> There's no grid. There's no graph object. Just a bag of words. And your job is to realize those words *secretly form a graph* — and then not fall into the trap that makes it time out on the big test cases. Two leaps to make. Let's take them one at a time.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: the inputs, then the answer chain highlighted:]**

```
beginWord = "hit"
endWord   = "cog"
wordList  = [hot, dot, dog, lot, log, cog]
```

> One line: **find the length of the shortest chain from `beginWord` to `endWord`, where each step changes exactly one letter and lands on a word in the list.** Return `0` if it's impossible.
>
> The shortest chain here is `hit → hot → dot → dog → cog` — five words. So the answer is **5** — we count the words, including both ends. Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:30`
*(worked example — feel the mechanism)*

**[VISUAL: starting from "hit", branches fan out to every word one letter away, then those branch again — a spreading tree, depth labeled 1, 2, 3…]**

> Let's think it through. From `hit`, which listed words are one letter away? Only `hot`. From `hot`, one letter away: `dot`, `lot`. From `dot`: `dog`. From `lot`: `log`. From `dog`: `cog` — found it.
>
> **[VISUAL: the tree lights up level by level; "cog" appears at level 5, a burst.]**
>
> Notice *how* we searched: level by level. All words one step from `hit`, then all words two steps away, then three. The **first** time `cog` appears, we're at the shortest depth. That expand-in-levels search — that's **BFS.** And "first time you reach the target is the shortest path" is BFS's defining promise on an unweighted graph.

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(generation effect — first pause)*

**[VISUAL: for one word, arrows shooting out to compare against ALL 5000 words in a list. A "comparisons" counter exploding. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** BFS is clearly right. But here's the hidden cost that makes this Hard. At each word, I need its neighbors — the words one letter away. The obvious way? Compare this word against *every other word* in the list and count letter differences.
>
> **LEARNER:** And with up to 5000 words, that's 5000 comparisons per word, times thousands of words popped… that's `N`-squared. That's the time-out, isn't it?
>
> **TEACHER:** That's exactly it. `N` words, each scanned against `N` words, each comparison costing `L` characters — `N`-squared times `L`. It melts on the big cases. So pause and predict: **is there a way to find a word's one-letter neighbors *without* scanning the whole list?** Three seconds.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:30`
*(elaboration + analogy — words as graph + wildcard buckets)*

**[VISUAL: two panels. Left: "words as graph" — words as nodes, edges between one-letter-apart pairs. Right: the wildcard bucket idea.]**

> **TEACHER:** Two leaps. First, the reframe you already felt: **each word is a node; two words share an edge if they differ by exactly one letter.** A transformation chain is a *path*; shortest chain is *shortest path*; unweighted, so — BFS. Same engine as every graph before.
>
> The second leap is the clever one — building edges cheaply. Here's the trick: two words are neighbors if and only if they match a **wildcard pattern** with one position starred. `hot` and `dot` both match `*ot`. `hit` and `hot` both match `h*t`.
>
> **[VISUAL: "hot" spawns three patterns: `*ot`, `h*t`, `ho*`. Each drops into a labeled bucket.]**
>
> So *pre-bucket* every word by all its wildcard patterns. `hot` goes into buckets `*ot`, `h*t`, and `ho*`. Now to find a word's neighbors, I don't scan 5000 words — I generate my `L` patterns and grab whoever's already sitting in those buckets. Every word in bucket `h*t` differs from `hit` at exactly that one position. Neighbor lookup drops from "scan `N` words" to "check `L` buckets."
>
> **[VISUAL: bucket `*ot` shown holding {hot, dot, lot} — "instant neighbors, no scan."]**
>
> **LEARNER:** Wait — doesn't `h*t` also match the word to *itself*? `hit` matches `h*t`... no wait, `hit` is `h`, `i`, `t` — pattern `h*t` needs `h_t`. `hit` matches it. So does `hot`. So the bucket includes the word itself?
>
> **TEACHER:** Sharp — yes, a word lands in its own buckets. But that's harmless: our `visited` set already blocks revisiting a word, so "neighbor equals myself" just gets skipped like any seen word. The buckets can be generous; `visited` keeps us honest.

---

## 6. THE KEY MOVE (signaling) — `5:15`
*(one crisp, repeatable line)*

**[VISUAL: boxed line: "Words = graph, one-letter edges. BFS for shortest. Wildcard buckets = O(L) neighbor lookup."]**

> Two lines to remember: **model states as nodes and edits as edges, then BFS for the shortest path. And when neighbors are expensive, pre-bucket by wildcard pattern so lookup is O(L), not O(N).**

---

## 7. CODE IT — LIVE & CHUNKED — `5:50`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> First, the early exit and the pattern buckets.

```python
from collections import deque, defaultdict

def ladder_length(beginWord, endWord, wordList):
    words = set(wordList)
    if endWord not in words:
        return 0                          # unreachable by definition
    L = len(beginWord)

    patterns = defaultdict(list)          # "h*t" -> [words matching it]
    for word in words:
        for i in range(L):
            patterns[word[:i] + '*' + word[i+1:]].append(word)
```

> **[VISUAL: add chunk 2, highlight.]** Set up BFS — queue carries the word and its depth.

```python
    q = deque([(beginWord, 1)])           # depth counts words, begin is 1
    visited = {beginWord}
```

> **[VISUAL: add chunk 3, highlight the neighbor lookup.]** The BFS loop, with O(L) neighbor lookup through the buckets.

```python
    while q:
        word, steps = q.popleft()
        if word == endWord:
            return steps
        for i in range(L):
            pat = word[:i] + '*' + word[i+1:]
            for nei in patterns[pat]:      # all one-letter neighbors, no full scan
                if nei not in visited:
                    visited.add(nei)
                    q.append((nei, steps + 1))
            patterns[pat] = []             # clear bucket so we never rescan it
    return 0
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:45`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight lines.]**

> `if endWord not in words: return 0` — cheap early exit. If the target isn't even in the list, no chain can end on it.
>
> The pattern pre-build is the whole speed win: pay `O(N·L)` once, up front, to make every later neighbor lookup `O(L)`.
>
> Carrying `steps` in the queue is how we count without a separate level loop — each neighbor is one deeper than its parent. `begin` starts at `1` because the problem counts *words*, both endpoints included.
>
> `visited.add(nei)` the moment we enqueue — not when we dequeue. Marking on enqueue stops the same word from being added twice by two different parents in the same wave.
>
> **LEARNER:** That `patterns[pat] = []` line — clearing the bucket. Is that just an optimization, or does it change correctness?
>
> **TEACHER:** Purely an optimization, but a meaningful one. Once we've expanded a bucket, everyone in it is now visited — revisiting it later would just loop over already-seen words and skip them all. Emptying it means later words sharing that pattern don't waste time rescanning it. Correctness is already guaranteed by `visited`; this just trims repeated work.

---

## 9. DRY-RUN THE CODE — `9:00`
*(worked example — prove it)*

**[VISUAL: BFS wave over the word tree; queue and depth shown; buckets emptying.]**

> Trace `hit → cog`. Relevant buckets: `h*t:[hit,hot]`, `*ot:[hot,dot,lot]`, `do*:[dot,dog]`, `lo*:[lot,log]`, `*og:[dog,log,cog]`.

| dequeue | patterns hit | enqueues (depth) |
|---|---|---|
| (hit,1) | h*t → hot | (hot,2) |
| (hot,2) | *ot → dot,lot | (dot,3),(lot,3) |
| (dot,3) | do* → dog | (dog,4) |
| (lot,3) | lo* → log | (log,4) |
| (dog,4) | *og → cog | (cog,5) |
| (cog,5) | word == endWord | **return 5** |

> There it is — `cog` dequeued at depth **5.** The first time we reach it, and BFS guarantees that's the shortest. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `10:00`
*(transfer to interview)*

**[VISUAL: Brute: O(N²·L). Ours: O(N·L²).]**

> Out loud: *"Naive neighbor-finding compares every pair of words — O(N-squared times L). With wildcard buckets, each of N words generates L patterns, and building each pattern is an O(L) string slice — so O(N times L-squared) to build, and each edge is processed once in BFS. For the real constraints, N-squared is the thing that times out, and L-squared is far smaller since words are short."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:45`
*(depth + honesty — two upgrades)*

**[VISUAL: panel A: 26-letter on-the-fly generation. panel B: two frontiers meeting in the middle.]**

> The buckets cost `O(N·L²)` memory. Two ways to do better.
>
> **First — generate neighbors on the fly.** Skip the bucket map entirely: for each position, try all 26 letters, and check "is this a real word?" against the set. Same time class, but no bucket storage — space drops to `O(N·L)`.

```python
import string

def ladder_length_26(beginWord, endWord, wordList):
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

> **Second — the real pro move on a Hard follow-up: bidirectional BFS.** Search *forward* from `beginWord` and *backward* from `endWord` at the same time, always expanding the smaller frontier, and stop the instant they meet.
>
> **[VISUAL: two expanding circles from opposite ends, colliding in the middle — the collision point flashes.]**
>
> Why it's a big deal: a one-directional search explores roughly `b^d` words; two searches meeting in the middle each go half the depth, `b^(d/2)`, so together `2·b^(d/2)` — dramatically smaller. Even if you don't code it fully, *say it out loud* — on a Hard, naming bidirectional BFS is a strong-hire signal.

---

## 12. YOUR TURN (active recall) — `12:00`
*(retrieval practice)*

**[VISUAL: "Your turn → Minimum Genetic Mutation (LC 433)". Blank editor.]**

> Your turn: **Minimum Genetic Mutation.** Identical pattern — shortest one-character-edit chain — but the alphabet is just `A C G T`, four letters. If you can retarget today's code to a 4-letter alphabet, you've truly internalized "states as nodes, edits as edges, BFS for shortest."

---

## 13. LOCK IT IN — `12:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Shortest chain of small edits → build an implicit graph and BFS.** States are nodes, edits are edges.
> 2. **When neighbors are expensive, precompute cheaply** — wildcard buckets turn O(N) lookup into O(L).
> 3. **On a Hard, mention bidirectional BFS** — meet in the middle to shrink the search radius.
>
> Memory peg: **"one edit at a time, shortest path — that's a hidden graph, and BFS walks it. Star out a letter to find your neighbors."**

---

## 14. CLIFFHANGER — `13:30`
*(open loop to next lesson)*

**[VISUAL: a graph with arrows pointing one-way, a course-prerequisite chart. Title blurred: "Course Schedule (LC 207)".]**

> Every graph so far let us wander freely and BFS the shortest path. But what if the edges point *one way* — task A must come before task B — and the real question is whether the whole thing is even *possible*, or whether it deadlocks in a cycle? That needs a different weapon: topological sort. That's where this section turns next. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
