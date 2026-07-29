# Word Search II

> **LeetCode:** 212. Word Search II · **Difficulty:** 🔴 Hard · **Pattern:** Tries & Union-Find · **Google frequency:** ⭐ high

---

## Problem

Given an `m × n` board of characters and a list of `words`, return all words that can be formed by a path of **adjacent** (up/down/left/right) cells, where each cell is used **at most once per word**.

**Example:**
```
board = [["o","a","a","n"],
         ["e","t","a","e"],
         ["i","h","k","r"],
         ["i","f","l","v"]]
words = ["oath","pea","eat","rain"]
→ ["oath","eat"]      (order not important)
```
*("oath": o(0,0)→a(0,1)→... actually o(0,0)→a→t→h path exists; "eat": e(1,0)→a... exists; "pea" and "rain" have no valid path.)*

**Constraints that matter:** board up to 12×12, up to 3×10⁴ words each up to length 10. Running Word Search I (single-word DFS) once per word is O(W × cells × 4^L) — far too slow. A **trie of all the words** lets one DFS pass search for *every* word at once and prune dead branches instantly.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "I already have Word Search I — DFS the board for one word. Just loop it over all the words." That re-walks the board from scratch for each word and shares no work between words like `eat`, `ear`, `earn`.
- **Where it hurts:** words share prefixes, and each independent DFS re-explores the same board cells. Worse, a DFS for `zzzz` might wander far into the board before discovering no word starts that way.
- **The leap — put the *dictionary* in a trie, then DFS the board once against it.** Build a trie of all words. Walk the board; at each step, only continue if the current character is a **child in the trie** of the node you're at. That means the board exploration and the dictionary are matched in lockstep — the trie **prunes** any path that isn't the prefix of *some* word. When you reach a trie node marked as a word end, record it.
- **Key optimizations:** store the full word on the terminal trie node (so you emit it directly, no path reconstruction); mark a cell visited by mutating it (e.g. `#`) and restore on backtrack; and **prune the trie** by removing leaf nodes once their word is found, so the search shrinks as it succeeds.
- **Pattern trigger:** **"match many dictionary words against a grid/stream simultaneously"** → **Trie + backtracking.** One shared prefix tree replaces W independent searches.

---

## ① Brute Force

Run a single-word board DFS (Word Search I) once for each word.

```python
def findWords_brute(board, words):
    m, n = len(board), len(board[0])

    def dfs(r, c, word, k):
        if k == len(word):
            return True
        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[k]:
            return False
        tmp, board[r][c] = board[r][c], "#"
        found = (dfs(r+1, c, word, k+1) or dfs(r-1, c, word, k+1) or
                 dfs(r, c+1, word, k+1) or dfs(r, c-1, word, k+1))
        board[r][c] = tmp
        return found

    res = []
    for word in words:
        if any(dfs(r, c, word, 0) for r in range(m) for c in range(n)):
            res.append(word)
    return res
```

**Why it's the natural first attempt:** it reuses the Word Search I solution directly — correct and easy to reason about.

**Why it's not enough:** it's O(W × m × n × 4^L). With tens of thousands of words it times out, and it shares zero work between words that have common prefixes.

**Complexity:** Time `O(W × m·n × 4^L)`, Space `O(L)` recursion.

---

## ② Optimised Solution

Build a trie of the words; DFS the board once, guided (and pruned) by the trie.

```python
class TrieNode:
    __slots__ = ("children", "word")
    def __init__(self):
        self.children = {}
        self.word = None          # non-None on a terminal node = the full word

def findWords(board, words):
    root = TrieNode()
    for w in words:               # build the trie
        node = root
        for ch in w:
            node = node.children.setdefault(ch, TrieNode())
        node.word = w

    m, n = len(board), len(board[0])
    res = []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent.children.get(ch)
        if node is None:          # trie prune: no word uses this prefix
            return
        if node.word is not None: # found a complete word
            res.append(node.word)
            node.word = None      # de-dupe so we don't add it twice

        board[r][c] = "#"         # mark visited
        for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != "#":
                dfs(nr, nc, node)
        board[r][c] = ch          # restore

        if not node.children:     # prune dead leaf to shrink future search
            parent.children.pop(ch, None)

    for r in range(m):
        for c in range(n):
            dfs(r, c, root)
    return res
```

**Walk it** on the example: build a trie holding `oath, pea, eat, rain`. Start DFS at `(0,0)='o'` — `o` is a child of root (prefix of "oath"), so continue; follow `o→a→t→h`, reach a node with `word="oath"` → record "oath". Starting at `(1,0)='e'` — `e` is a child of root (prefix of "eat"), follow `e→a→t`, reach `word="eat"` → record. Any start whose character isn't a trie child of root (like the board cells that would begin "pea"/"rain" but can't complete) is pruned on the *first* step.

**Why it's correct:** the DFS only ever advances when the board character matches a trie child, so every path it explores spells a real word-prefix; reaching a `word`-bearing node means that exact path spells an inserted word using distinct cells (guaranteed by the `#` marking). Setting `node.word = None` after emitting prevents duplicates.

**Complexity:** Time `O(m·n × 4^(L−1))` in the worst case, but the trie prunes so aggressively that in practice it's dramatically faster; building the trie is `O(total chars in words)`. Space `O(total chars)` for the trie plus `O(L)` recursion.

---

## ③ Space Optimization

The trie is inherent — it's the mechanism that makes one pass search all words. Levers:

- **Store the word on the terminal node** (done above) instead of a boolean `is_end` — avoids reconstructing the string from the DFS path. A tiny space cost for a real simplicity win.
- **Prune exhausted leaves** (the `parent.children.pop(...)` step): once a word is found and a node has no children left, delete it. The trie *shrinks* as the search succeeds, so later starts explore less. This bounds work, not asymptotic space, but it's the optimization interviewers look for.
- **In-place visited marking** (`board[r][c] = "#"`, restored on backtrack) avoids an `O(m·n)` visited matrix — `O(1)` extra for the marking.

> The trie can't be removed without losing the whole speedup, so space is `O(total dictionary characters)` and that's the floor. The meaningful optimizations are runtime pruning and avoiding an auxiliary visited grid.

**Complexity:** Time bounded by the pruned DFS, Space `O(total chars)` trie.

---

## Java (for Java interviewers)

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

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute (Word Search I per word) | O(W × m·n × 4^L) | O(L) |
| Trie + backtracking | O(m·n × 4^(L−1)) worst, heavily pruned | O(total chars) |

---

## Say it out loud (interview narration)

> *"Running a board DFS per word re-walks the grid for every word and shares nothing between words with common prefixes. Instead I put all the words into a trie, then DFS the board once. At each cell I only recurse if that character is a child of my current trie node — so the trie prunes any path that isn't a prefix of some word. When I land on a node that stores a full word, I record it and null it out to avoid duplicates. I mark cells visited in place and restore on backtrack, and I prune trie leaves once their word is found so the search shrinks as it succeeds. The trie is O(total characters) and turns W independent searches into one."*

## Related / follow-ups
- **Word Search I** (LC 79 — single word, plain backtracking)
- **Implement Trie** (LC 208 — the underlying structure)
- **Add and Search Word** (LC 211 — trie DFS with wildcards)
- **Concatenated Words** (LC 472 — trie/DFS over a dictionary)
