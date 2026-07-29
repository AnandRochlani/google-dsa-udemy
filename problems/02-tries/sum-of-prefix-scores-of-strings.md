# Sum of Prefix Scores of Strings

> **LeetCode:** 2416. Sum of Prefix Scores of Strings · **Difficulty:** 🔴 Hard · **Pattern:** Trie · **Google frequency:** ⭐ high

---

## Problem

You're given an array of strings `words`. For any string `s`, define its **score** as the number of words in `words` that have `s` as a **prefix** (a word is a prefix of itself). Now, for each `words[i]`, take **every non-empty prefix** of it, look up each prefix's score, and add them all up. Return an array `answer` where `answer[i]` is that sum for `words[i]`.

**Example:** `words = ["abc","ab","bc","b"]` → `[5,4,3,2]`

For `"abc"`, its prefixes are `"a"`, `"ab"`, `"abc"`. Score of `"a"` = 2 (both `"abc"` and `"ab"` start with `"a"`). Score of `"ab"` = 2. Score of `"abc"` = 1 (only itself). Sum = 2 + 2 + 1 = **5**.

**Constraints that matter:** `words.length` up to `1000`, and each word up to `1000` chars — so the total character count `N` can be around `10^6`. Comparing every prefix of every word against every word is `O(N²)`-ish and blows up. The signal "score = how many words share this prefix" + "sum over all prefixes" is screaming **prefix tree**: a Trie counts shared prefixes for free.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For each word, generate all its prefixes. For each prefix, scan the whole array and count how many words start with it. Add those counts up." That's a direct translation of the definition — and it's correct. It's also brutally slow.
- **Where it hurts:** you keep re-answering the *same question*. "How many words start with `"ab"`?" gets recomputed for `"ab"`, for `"abc"`, for `"abcd"`… every word that passes through `"ab"` re-scans the array. The prefix `"a"` alone might be counted hundreds of times. That repeated counting is pure waste.
- **The leap:** the score of a prefix `s` is *just* "how many words pass through `s` on their way down." If I lay all the words into a **Trie**, then a node represents exactly one prefix, and the number of words passing through that node **is** the score of that prefix. So instead of counting per query, I count **once, at build time**: every time I insert a word and step onto a node, I bump that node's counter. Insert step = "one more word passes through here."
- **Pattern trigger:** **"count shared prefixes" + "sum over every prefix of every word"** → **Trie with pass-through counts**. The transferable move: *don't count prefixes on demand — bake the count into each node as you build.* Then answering a word is a single walk down, summing counters.

---

## ① Brute Force

For each word, take each of its prefixes, then scan all words to count how many have that prefix.

```python
def sum_prefix_scores_brute(words):
    answer = []
    for w in words:
        total = 0
        # every non-empty prefix of w
        for end in range(1, len(w) + 1):
            prefix = w[:end]
            # score(prefix) = how many words start with it
            score = sum(1 for other in words if other.startswith(prefix))
            total += score
        answer.append(total)
    return answer
```

**Why it's the natural first attempt:** it's the definition typed out verbatim — build each prefix, count the matches, add them. Nothing to get clever about, so it's the first thing you'd write to make sure you understand the problem.

**Why it's not enough:** for one word of length `L`, that's `L` prefixes, and each prefix scans all `n` words comparing up to `L` chars — `O(n · L²)` per word, `O(n² · L²)` overall. With `n = 1000` and `L = 1000`, that's astronomically over budget. And the waste is obvious: the score of `"a"` is recomputed from scratch for every word that starts with `"a"`.

**Complexity:** Time `O(n² · L²)` (n words, L max length), Space `O(1)` beyond the output.

---

## ② Optimised Solution

Build a **Trie** over all the words. Every node carries a `count` — the number of words that **pass through** it. Increment `count` on **every node you step onto during insert** (not just the last one). Then `answer[i]` = walk `words[i]` down the trie and sum the `count` at each node you visit — because each node is one prefix, and its `count` is that prefix's score.

```python
class TrieNode:
    def __init__(self):
        self.children = {}   # char -> TrieNode
        self.count = 0       # how many words pass through this node

def sum_prefix_scores(words):
    root = TrieNode()

    # ── build: insert every word, bumping count on every step ──
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1          # one more word passes through this prefix

    # ── query: walk each word down, summing the counts it visits ──
    answer = []
    for w in words:
        node = root
        total = 0
        for ch in w:
            node = node.children[ch]  # guaranteed to exist — we inserted w
            total += node.count       # this node = one prefix, count = its score
        answer.append(total)
    return answer
```

**Walk the example** `words = ["abc","ab","bc","b"]`. First we insert all four, bumping `count` on every node stepped onto:

| Insert | Nodes touched (count after) |
|---|---|
| `"abc"` | `a`→1, `ab`→1, `abc`→1 |
| `"ab"`  | `a`→2, `ab`→2 |
| `"bc"`  | `b`→1, `bc`→1 |
| `"b"`   | `b`→2 |

Final node counts: `a`=2, `ab`=2, `abc`=1, `b`=2, `bc`=1. Now query each word:

| Word | Prefix walk (node.count) | Sum |
|---|---|---|
| `"abc"` | `a`(2) + `ab`(2) + `abc`(1) | **5** |
| `"ab"`  | `a`(2) + `ab`(2) | **4** |
| `"bc"`  | `b`(2) + `bc`(1) | **3** |
| `"b"`   | `b`(2) | **2** |

Answer `[5,4,3,2]`. ✅

**Why it's correct:** a Trie node reached by the path `c₁c₂…cₖ` represents *exactly* the prefix `c₁c₂…cₖ`. During insert, we bump that node's `count` precisely once for each word whose path passes through it — i.e. once for each word that has this string as a prefix. So `node.count` *is* the score of that prefix, by construction. Summing the counts along a word's path adds up the scores of every one of its prefixes — which is the definition of the answer. The query walk can never hit a missing child, because the word itself was inserted, so its whole path exists.

**Complexity:** Time `O(N)` where `N` = total characters across all words (each char is touched once on insert, once on query), Space `O(N)` for the trie nodes.

---

## ③ Space Optimization

**Already optimal for a Trie — but here's the honest accounting.** The trie stores at most one node per distinct prefix, which is `O(N)` in the worst case (all words share nothing). You genuinely need to remember every prefix's count to answer queries, so `O(N)` structure is the floor for this approach — there's no rolling-variable trick, because the counts of *all* prefixes are consulted, not just recent ones.

What you *can* tune is the node itself. A `dict` of children is flexible and memory-light when the branching is sparse. If the alphabet is fixed lowercase `a–z`, a **26-slot array** per node makes lookups pointer-fast at the cost of a fixed 26-wide array even for near-empty nodes — a classic time-vs-space trade you should *name* in the interview:

```python
class ArrayTrieNode:
    __slots__ = ("children", "count")
    def __init__(self):
        self.children = [None] * 26   # fixed a–z fan-out
        self.count = 0

def sum_prefix_scores_arr(words):
    root = ArrayTrieNode()
    for w in words:
        node = root
        for ch in w:
            k = ord(ch) - 97
            if node.children[k] is None:
                node.children[k] = ArrayTrieNode()
            node = node.children[k]
            node.count += 1
    ans = []
    for w in words:
        node, total = root, 0
        for ch in w:
            node = node.children[ord(ch) - 97]
            total += node.count
        ans.append(total)
    return ans
```

**Complexity:** Time `O(N)`, Space `O(N)` (array-26 uses more constant memory per node than the dict, but the asymptotics are the same).

> If asked to shrink further: **you can't beat `O(N)` here** — the answer for a word depends on counts scattered across every prefix it owns, and those prefixes are shared arbitrarily across the input. There's no "keep only the last row" collapse like a 1-D DP, because dependencies fan out across the whole tree. Naming *why* `O(N)` is the floor is the strong-hire move.

---

## Java (for Java interviewers)

```java
class Solution {
    static class Node {
        Node[] children = new Node[26];   // fixed a–z fan-out
        int count = 0;                     // words passing through this prefix
    }

    public int[] sumPrefixScores(String[] words) {
        Node root = new Node();

        // build: bump count on every node stepped onto
        for (String w : words) {
            Node node = root;
            for (int i = 0; i < w.length(); i++) {
                int k = w.charAt(i) - 'a';
                if (node.children[k] == null) node.children[k] = new Node();
                node = node.children[k];
                node.count++;
            }
        }

        // query: sum counts along each word's path
        int[] answer = new int[words.length];
        for (int idx = 0; idx < words.length; idx++) {
            Node node = root;
            int total = 0;
            for (int i = 0; i < words[idx].length(); i++) {
                node = node.children[words[idx].charAt(i) - 'a'];
                total += node.count;
            }
            answer[idx] = total;
        }
        return answer;
    }
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (re-count every prefix) | O(n² · L²) | O(1) aux |
| Optimised (Trie with pass-through counts) | O(N) | O(N) |
| Space-optimised (array-26 node) | O(N) | O(N) — same asymptotics, different constant |

*(N = total characters across all words; n = number of words; L = max word length.)*

---

## Say it out loud (interview narration)

> *"The score of a prefix is just how many words share that prefix — so my instinct is a Trie. The naive version re-counts each prefix against the whole array, which is quadratic and recomputes 'how many words start with `ab`' over and over. The key move is to count at build time: I insert every word into the trie, and on every single node I step onto during insert, I increment a per-node counter. That counter is now exactly the score of that prefix — the number of words passing through it. To answer a word, I just walk it back down and sum the counter at each node, since each node on the path is one of its prefixes. Time is O(total characters) — one pass to build, one to query — and space is O(total characters) for the nodes. The one detail I'd flag out loud: increment on **every** node during insert, not just the leaf — that's the whole trick."*

The clarifying question that shows you read the spec: *"A word counts as a prefix of itself, right? So `words = ["a","a"]` gives score 2 for `"a"`?"* Asking that early is exactly what Google's rubric rewards.

## Related / follow-ups
- **Implement Trie (Prefix Tree) (LC 208)** — the base structure; build this reflex first.
- **Map Sum Pairs (LC 677)** — Trie nodes carry a summed value; same "aggregate along the path" idea.
- **Longest Common Prefix (LC 14)** — trivial with a trie, and a warm-up for prefix thinking.
- **Word Search II (LC 212)** — Trie + DFS on a grid; the heavyweight cousin.
- **Count Prefix and Suffix Pairs II (LC 3045)** — double trie for prefix *and* suffix matching.
