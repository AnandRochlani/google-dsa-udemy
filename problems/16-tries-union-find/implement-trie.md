# Implement Trie (Prefix Tree)

> **LeetCode:** 208. Implement Trie (Prefix Tree) · **Difficulty:** 🟡 Medium · **Pattern:** Tries & Union-Find · **Google frequency:** ⭐ high

---

## Problem

Design a **trie** (prefix tree) supporting:
- `insert(word)` — add a word.
- `search(word)` — return `true` if the exact word was inserted.
- `startsWith(prefix)` — return `true` if any inserted word begins with `prefix`.

**Example:**
```
insert("apple")
search("apple")   → true
search("app")     → false   (inserted "apple", never "app" as a full word)
startsWith("app") → true    ("apple" starts with "app")
insert("app")
search("app")     → true
```

**Constraints that matter:** up to ~3×10⁴ calls, words of lowercase letters up to length ~2000. A trie makes every operation **O(L)** in the word length `L` — independent of how many words are stored. That's the reason to build a tree of characters instead of a hash set of strings.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Store all words in a set. `search` is a set lookup, `startsWith` scans every stored word for the prefix." Search is fine, but `startsWith` becomes O(number of words × length) — you re-examine unrelated words on every prefix query.
- **Where it hurts:** words that share a prefix (`app`, `apple`, `apply`) store that prefix over and over, and prefix queries can't exploit the sharing.
- **The leap:** **share common prefixes in a tree of characters.** Each node has up to 26 children (one per letter) and an `is_end` flag marking where a real word terminates. Insert walks/creates one node per character; search walks the same path and checks `is_end`; `startsWith` walks the path and just checks the path *exists*. `search` vs `startsWith` differ by exactly one thing: whether you require `is_end` at the last node.
- **Pattern trigger:** **"prefix queries / autocomplete / dictionary of words / shared string prefixes"** → **Trie.** A trie trades a bit of memory for prefix operations that don't depend on the dictionary size.

---

## ① Brute Force

Keep a set of words. `startsWith` scans them all.

```python
class TrieBrute:
    def __init__(self):
        self.words = set()

    def insert(self, word):
        self.words.add(word)

    def search(self, word):
        return word in self.words

    def startsWith(self, prefix):
        return any(w.startswith(prefix) for w in self.words)
```

**Why it's the natural first attempt:** a set gives O(1) exact search for free, and `startsWith` is a one-liner.

**Why it's not enough:** `startsWith` is O(N × L) — it re-scans every stored word on each prefix query, ignoring shared prefixes. With many words and frequent prefix queries (autocomplete), that's the bottleneck the trie exists to fix.

**Complexity:** insert O(L); search O(L) (hashing); `startsWith` **O(N × L)**. Space O(total characters).

---

## ② Optimised Solution

A tree of character nodes, each with children and an end-of-word flag.

```python
class TrieNode:
    __slots__ = ("children", "is_end")
    def __init__(self):
        self.children = {}      # char -> TrieNode
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end   # must be a real word end

    def startsWith(self, prefix):
        return self._walk(prefix) is not None     # path existing is enough
```

**Walk the example** after `insert("apple")`:

```
root → a → p → p → l → e(is_end=True)
```
- `search("apple")`: walk a-p-p-l-e, last node `is_end=True` → **true**.
- `search("app")`: walk a-p-p, that node exists but `is_end=False` (we never ended a word there) → **false**.
- `startsWith("app")`: walk a-p-p, path exists → **true**.
- After `insert("app")`, the a-p-p node's `is_end` becomes `True`, so `search("app")` → **true**.

**Why it's correct:** each word maps to exactly one root-to-node path; `is_end` distinguishes "a word ends here" from "this is merely a prefix of some word." That single flag is what separates `search` (needs `is_end`) from `startsWith` (needs only the path).

**Complexity:** every operation is **O(L)** in the query length, independent of how many words are stored. Space O(total characters inserted), worst case O(N × L).

---

## ③ Space Optimization

The tree of nodes is inherent to a trie — that's the data structure. Two honest levers:

- **Dict vs fixed array children:** a 26-slot array per node (`children[26]`) gives slightly faster O(1) indexing but wastes slots on sparse tries; a hash map (used above) stores only the letters actually present. For lowercase-only inputs the array is the textbook choice; for large/unicode alphabets the map wins.
- **You can't drop the nodes:** prefix sharing already *is* the compression — `app`/`apple`/`apply` share their first three nodes instead of storing three full strings. A radix/compressed trie (merging single-child chains into one edge) can shrink node count further, but that's an optimization beyond what LC 208 asks.

> So: already near-optimal. The node tree is the point of a trie; the only real dial is dict-children vs array-children, a constant-factor space/speed trade.

**Complexity:** Space O(total inserted characters).

---

## Java (for Java interviewers)

```java
class Trie {
    private static class Node {
        Node[] children = new Node[26];
        boolean isEnd = false;
    }
    private final Node root = new Node();

    public void insert(String word) {
        Node node = root;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (node.children[i] == null) node.children[i] = new Node();
            node = node.children[i];
        }
        node.isEnd = true;
    }

    private Node walk(String s) {
        Node node = root;
        for (char c : s.toCharArray()) {
            int i = c - 'a';
            if (node.children[i] == null) return null;
            node = node.children[i];
        }
        return node;
    }

    public boolean search(String word) {
        Node n = walk(word);
        return n != null && n.isEnd;
    }

    public boolean startsWith(String prefix) {
        return walk(prefix) != null;
    }
}
```

---

## Complexity Summary

| Operation | Set (brute) | Trie |
|---|---|---|
| insert | O(L) | O(L) |
| search | O(L) | O(L) |
| startsWith | O(N × L) | O(L) |
| Space | O(total chars) | O(total chars) |

---

## Say it out loud (interview narration)

> *"A set handles exact search but makes `startsWith` scan every word, O(N×L). A trie fixes that by sharing common prefixes in a tree of characters — each node has up to 26 children and an is-end flag. Insert creates one node per character; search walks the path and checks is-end; `startsWith` walks the path and just confirms it exists. The only difference between search and startsWith is whether I require the is-end flag at the final node. Every operation is O(L), independent of the dictionary size — that's the whole win."*

## Related / follow-ups
- **Add and Search Word / Design Add and Search Words Data Structure** (LC 211 — `.` wildcard needs DFS branching over children)
- **Word Search II** (LC 212 — a trie over the dictionary drives grid backtracking)
- **Replace Words** (LC 648 — walk the trie to find the shortest root prefix)
- **Map Sum Pairs** (LC 677 — trie nodes carry summed values)
