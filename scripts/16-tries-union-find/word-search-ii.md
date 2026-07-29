# 🎬 Recording Script — Word Search II
**Pattern: Tries & Union-Find · LeetCode 212 · Hard · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Implement Trie (LC 208) — the character tree we're about to weaponize. Also grid-DFS backtracking (Word Search I).

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a 4×4 grid of letters. A word list with 30,000 entries scrolling on the side. A brute-force DFS animation frantically re-walking the grid over and over, a "TLE" banner looming.]**

> Here's an Google Hard that breaks people: a grid of letters, and a dictionary of *tens of thousands* of words. Find every word you can spell by walking adjacent cells.
>
> You already know Word Search I — DFS the grid for one word. So the "obvious" move is: loop it over all thirty thousand words. And it will **time out**, spectacularly, because you re-walk the entire grid from scratch for every single word — sharing nothing between "eat", "ear", and "earn".
>
> The fix is gorgeous: flip it around. Put the *dictionary* into a trie, and search the grid **once**, letting the trie prune every dead path the instant it starts. By the end you'll own it. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:45`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below, the 4×4 board and a short word list.]**

> One line: **return every dictionary word that can be traced through adjacent cells — up, down, left, right — using each cell at most once per word.**
>
> Tiny example:

```
board = o a a n        words = ["oath","pea","eat","rain"]
        e t a e
        i h k r
        i f l v
```

> "oath" traces a path through the grid. "eat" traces one too. "pea" and "rain" have no valid path. So the answer is `["oath","eat"]`. Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:30`
*(worked example — let them feel the waste)*

**[VISUAL: for each word, a fresh DFS floods the grid from every cell. The same cells get re-visited word after word; a "grid walks" counter explodes.]**

> The brute force: take Word Search I's single-word DFS and run it once per word. For "oath", DFS from every cell. For "pea", DFS from every cell again. For "eat", again.
>
> **[VISUAL: the grid re-flooding 4 times, counter climbing per word.]**
>
> Two problems. One: with 30,000 words, that's 30,000 independent grid searches — O(W × cells × 4^L). Dead. Two — and this is the deeper waste — a search for "pea" starts wandering the board looking for a `p`, exploring far, before discovering nothing spells "pea". No pruning. And "eat", "ear", "earn" all re-walk the same `e-a` start with zero sharing.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight "eat"/"ear"/"earn" all re-walking the same "ea" grid cells. A 5-second "🤔 your turn" timer.]**

> **TEACHER:** The waste is doubled: we re-walk the grid per word, *and* words sharing prefixes share zero work.
>
> **LEARNER:** So I want all the words that share a prefix to be searched together, in one grid walk. But the words are just a flat list — how do I make the search "know" about shared prefixes as it moves?
>
> **TEACHER:** That's the whole leap. You already built the structure that shares prefixes last lesson. Pause and predict: **if the dictionary lived in a trie, and I walked the grid one cell at a time, how could the trie tell me instantly whether to keep going or give up on this path?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:25`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a trie of {oath, pea, eat, rain} on the right. The grid on the left. A DFS cursor on the grid moves in lockstep with a cursor descending the trie.]**

> Here's the aha: **put all the words in a trie, then DFS the grid once — but move the grid cursor and a trie cursor in lockstep.**
>
> The rule: at each cell, only step forward **if the current letter is a child of the trie node you're standing on.** That single condition is the magic. It means the board exploration and the dictionary are *matched* — the moment the path you're spelling isn't the prefix of *any* word, the trie has no child for that letter, and you stop dead. The trie **prunes** the search.
>
> **[VISUAL: DFS starts at cell `(0,0)='o'`. Root has an `o` child (start of "oath")? Yes → descend. Follow o→a→t→h in both grid and trie → hit a node marked with a word → record "oath".]**
>
> Start at the `p`-less cells that would begin "pea"? There's no path, so the very first step that leaves the trie gets pruned instantly. We never wander.
>
> Two more tricks that make it clean:
> - **Store the whole word on the terminal trie node** — so when we arrive, we emit it directly, no reconstructing the path.
> - **Mark a cell visited by overwriting it** with `#`, and restore it on the way back — so we don't reuse a cell within one word.

---

## 5b. WHY THE TRIE IS THE RIGHT TOOL — `4:40`
*(the misconception: "isn't a hash set of words enough?")*

**[VISUAL: a hash set of words with a "?" — can it answer "is 'oat' a prefix of something?" — a red X. The trie answers it with a green check.]**

> Quick misconception to kill: *"why not just a hash set of the words?"* Because a set can answer "is this a complete word?" but it *cannot* answer "is this string a prefix of some word?" — and that prefix question is exactly what lets us prune mid-path. A set would force us to walk to full word length before knowing we're wasting our time. The trie answers "keep going?" at *every single letter*. That's why it, and only it, gives us the pruning.

---

## 6. THE KEY MOVE (signaling) — `5:20`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Trie of all words + DFS the grid once. Only recurse if the cell's letter is a trie child — that's the prune."]**

> The key move: **build a trie of every word, DFS the board once, and only step to a cell whose letter is a child in the trie — the trie prunes every non-prefix path.**
>
> Trigger phrase: *"match many dictionary words against a grid or stream at once"* → Trie plus backtracking. One prefix tree replaces W independent searches.

---

## 7. CODE IT — LIVE & CHUNKED — `6:00`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 — node + build.]**

> The node stores children and, on a terminal, the full word. Build the trie from all words.

```python
class TrieNode:
    __slots__ = ("children", "word")
    def __init__(self):
        self.children = {}
        self.word = None          # set on a terminal node = the full word

def findWords(board, words):
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            node = node.children.setdefault(ch, TrieNode())
        node.word = w
```

> **[VISUAL: add chunk 2 — setup + the DFS signature.]** Grid dimensions, a result list, and a DFS that carries the *parent* trie node.

```python
    m, n = len(board), len(board[0])
    res = []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent.children.get(ch)
        if node is None:          # trie prune: no word uses this prefix
            return
```

> **[VISUAL: add chunk 3 — the word hit + de-dupe.]** If this trie node holds a word, we found it — record and null it out so we never add it twice.

```python
        if node.word is not None:
            res.append(node.word)
            node.word = None      # de-dupe
```

> **[VISUAL: add chunk 4 — the four-direction recursion with in-place marking.]**

```python
        board[r][c] = "#"         # mark visited
        for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != "#":
                dfs(nr, nc, node)
        board[r][c] = ch          # restore on backtrack
```

> **[VISUAL: add chunk 5 — leaf pruning + the driver loop.]** Prune dead leaves so the trie shrinks as we succeed, then launch DFS from every cell.

```python
        if not node.children:     # exhausted leaf → remove it
            parent.children.pop(ch, None)

    for r in range(m):
        for c in range(n):
            dfs(r, c, root)
    return res
```

---

## 8. EXPLAIN THE CODE (the WHY) — `8:30`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight lines.]**

> Why each piece.
>
> `node = parent.children.get(ch); if node is None: return` — *this is the prune*, the whole speedup. If the current letter isn't a trie child, no word has this prefix, so we abandon the path immediately.
>
> `node.word` stores the full string on terminal nodes — so on a hit we just append it, no rebuilding from the DFS path.
>
> `node.word = None` after a hit — the same word might be reachable by another route; nulling it prevents duplicate entries.
>
> `board[r][c] = "#"` then restore — this is the visited mark. It stops a word reusing a cell, and it costs *zero* extra memory because we mutate the board itself.
>
> **LEARNER:** The `parent.children.pop(ch)` at the end — why delete trie nodes *during* the search? Isn't that dangerous?
>
> **TEACHER:** It's the pro move. Once a node has no children left — its word's been found and nothing branches below it — it's dead weight. Popping it means every *later* DFS from other cells has a smaller trie to check, so the search literally shrinks as it succeeds. It's safe because we only pop a leaf we've fully finished exploring. That one line is what turns a passing solution into a fast one.

---

## 9. DRY-RUN THE CODE — `9:50`
*(worked example — prove it, close the loop)*

**[VISUAL: the board with the DFS path for "oath" highlighted cell by cell, trie descending alongside.]**

> Trace it on the example. Trie holds oath, pea, eat, rain.

| DFS start | trie step | outcome |
|---|---|---|
| `(0,0)='o'` | root has `o` (prefix of "oath") | descend → follow o→a→t→h → node.word="oath" → **record "oath"** |
| `(1,0)='e'` | root has `e` (prefix of "eat") | descend → follow e→a→t → node.word="eat" → **record "eat"** |
| cell starting "pea" | root has no matching path from that cell | pruned on step 1 |
| cell starting "rain" | no valid adjacent path | pruned early |

> Output: `["oath","eat"]`. Exactly the two words we predicted. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `10:50`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(W × m·n × 4^L). Trie+DFS: O(m·n × 4^(L−1)), heavily pruned.]**

> Say it: *"Running Word Search I per word is O(W × cells × 4^L) — the number of words multiplies everything. Building the trie is O(total characters in the dictionary). Then I DFS the board once; worst case it's O(cells × 4^(L−1)), but the trie prunes so aggressively that in practice it's dramatically faster. Space is O(total characters) for the trie plus O(L) recursion depth."*
>
> The headline: *"the trie turns W independent searches into one, and prunes every dead path at the first wrong letter."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `11:35`
*(depth + honesty)*

**[VISUAL: three labeled levers — "word on node", "prune leaves", "in-place visited".]**

> The trie is inherent — it's the mechanism, can't remove it. So the space floor is O(total dictionary characters). But there are three real levers worth naming:
>
> - **Store the word on the terminal node** instead of a boolean — trades a few bytes to avoid reconstructing strings. A clean simplicity win.
> - **Prune exhausted leaves** — bounds *runtime*, not asymptotic space, but it's the optimization interviewers hunt for.
> - **In-place visited marking** (`board[r][c]='#'`) — avoids an O(m·n) visited matrix entirely, O(1) extra.
>
> Say it: *"The trie is the floor at O(total chars). The meaningful optimizations are runtime pruning and skipping an auxiliary visited grid."*

---

## 12. YOUR TURN (active recall) — `12:20`
*(retrieval practice)*

**[VISUAL: "Your turn → Concatenated Words (LC 472)". A word split into two dictionary pieces.]**

> Before the next video, try **Concatenated Words**, LC 472 — find words that are built by joining two or more shorter dictionary words. It's another trie-plus-DFS: walk the trie over a word, and whenever you hit a word-end mid-string, recurse on the rest. Same "trie guides the search" idea.
>
> Ten minutes of struggle first.

---

## 13. LOCK IT IN — `12:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Put the dictionary in a trie, search the grid once** — not once per word.
> 2. **The prune is the whole point** — only recurse if the letter is a trie child.
> 3. **Store the word on the node, mark cells in place, prune dead leaves.**
>
> Memory peg: **many words against a grid? Trie the words, walk the grid once, let the trie say "stop."**

---

## 14. CLIFFHANGER — `13:30`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Number of Provinces" — dots connected into clusters.]**

> Tries were about *sharing prefixes*. The rest of this chapter is about a completely different superpower: *grouping things that are connected*. How many friend-clusters are in a social network? Which accounts belong to the same person? For that we need a new tool that merges sets in near-constant time — **Union-Find**. Next up: Number of Provinces. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class Solution {
    static class Node { Node[] ch = new Node[26]; String word = null; }
    private List<String> res = new ArrayList<>();
    private char[][] board;
    private int m, n;

    public List<String> findWords(char[][] board, String[] words) {
        this.board = board; m = board.length; n = board[0].length;
        Node root = new Node();
        for (String w : words) {
            Node node = root;
            for (char c : w.toCharArray()) {
                int i = c - 'a';
                if (node.ch[i] == null) node.ch[i] = new Node();
                node = node.ch[i];
            }
            node.word = w;
        }
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                dfs(r, c, root);
        return res;
    }

    private void dfs(int r, int c, Node parent) {
        if (r < 0 || r >= m || c < 0 || c >= n) return;
        char cur = board[r][c];
        if (cur == '#') return;
        Node node = parent.ch[cur - 'a'];
        if (node == null) return;
        if (node.word != null) { res.add(node.word); node.word = null; }
        board[r][c] = '#';
        dfs(r+1, c, node); dfs(r-1, c, node);
        dfs(r, c+1, node); dfs(r, c-1, node);
        board[r][c] = cur;
    }
}
```
