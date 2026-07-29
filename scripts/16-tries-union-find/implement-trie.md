# 🎬 Recording Script — Implement Trie (Prefix Tree)
**Pattern: Tries & Union-Find · LeetCode 208 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none — this is the foundational data structure the next problems build on.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a search bar. Someone types "app" and a dropdown instantly fills: "apple, application, apply…". A timer shows "0.001s" while a million-word dictionary icon sits behind it.]**

> Every time you type into a search box and it autocompletes before your finger leaves the key — something is answering *"which words start with these letters?"* instantly, over a dictionary of millions of words.
>
> If you stored those words in a hash set, that prefix query would have to scan *every single word*. Slow, and it gets slower as the dictionary grows.
>
> The data structure that fixes this — the **Trie** — makes every operation depend only on the length of the word you're typing, *not* on how many words you've stored. By the end of this video you'll build one from scratch, and see the one flag that separates "is this a word" from "is this a prefix." Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: three method signatures on screen: `insert(word)`, `search(word)`, `startsWith(prefix)`. Below, a short script of calls with their expected results.]**

> We're *designing* a structure with three operations: `insert` a word, `search` for an exact word, and `startsWith` to check if any word begins with a prefix.
>
> Here's the behavior to nail:

```
insert("apple")
search("apple")   → true
search("app")     → false   ← "app" was never inserted as a full word
startsWith("app") → true    ← but "apple" does start with "app"
insert("app")
search("app")     → true    ← now it is a real word
```

> Feel that tension between `search("app") → false` but `startsWith("app") → true`? That gap is the whole lesson. Hold it.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — let them feel the waste)*

**[VISUAL: a hash set holding {"apple", "apply", "apricot", "banana"}. A `startsWith("app")` query fires arrows at every single word, checking each one.]**

> The obvious idea: store the words in a set. `search` is a clean O(1) lookup — great. `startsWith`? A one-liner: check if *any* stored word begins with the prefix.
>
> **[VISUAL: arrows hitting every word, a counter "words scanned" climbing to the full dictionary size.]**
>
> But watch `startsWith`. It has to scan *every word* to find one that matches — that's O(number of words × length). With a million words and someone typing fast, you re-scan the entire dictionary on every keystroke. And notice the waste: "apple", "apply", "apricot" all share the letters "ap", but the set stores and re-checks that shared prefix over and over.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight the shared "app" across "apple"/"apply". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste: shared prefixes are stored redundantly, and prefix queries can't exploit the sharing — they scan everything.
>
> **LEARNER:** So I want the words that share letters to *share storage* somehow. But words are just flat strings in a set — how do I make them share?
>
> **TEACHER:** Exactly the right question. Pause and predict: **if "apple" and "apply" both start with a-p-p-l, what structure lets them walk the same path for those four letters and only branch at the fifth?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a character tree grows. From `root`: `a → p → p → l → e`, then a branch `l → y` off the second `l`. Each node is a circle holding one letter.]**

> Here's the aha: **build a tree of characters.** Start at an empty root. Each letter of a word is a step down the tree. "apple" carves the path a → p → p → l → e. Now insert "apply" — it walks the *same* a-p-p-l path that already exists, and only branches at the last letter into a `y`.
>
> **[VISUAL: the shared trunk a-p-p-l glows; the tree branches e and y at the tip.]**
>
> That shared trunk *is* the compression — the prefix is stored once. Now every operation just walks a path:
> - **insert:** walk the letters, creating nodes that don't exist yet.
> - **search:** walk the letters — but reaching the end isn't enough. You need to know a *word actually ended here.*
> - **startsWith:** walk the letters — if the path exists at all, some word uses it. Done.
>
> And here's the one trick that makes it all work: each node carries a boolean flag, `is_end`, marking "a real word terminates here."

---

## 5b. THE `is_end` FLAG — THE WHOLE DIFFERENCE — `4:15`
*(confronting the misconception)*

**[VISUAL: the a-p-p node highlighted with `is_end=False`; the a-p-p-l-e node with `is_end=True`.]**

> This flag is the answer to that opening tension. After inserting only "apple", the path a-p-p *exists* — but no word ended there. So the "app" node has `is_end = False`.
>
> - `search("app")` walks to that node, checks `is_end` → it's False → **not a word.**
> - `startsWith("app")` walks to that same node, and just asks "does the path exist?" → yes → **true.**
>
> **Search and startsWith differ by exactly one thing:** whether you demand `is_end` at the final node. That's it. Internalize that and this problem is trivial.

---

## 6. THE KEY MOVE (signaling) — `4:55`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "A trie shares common prefixes in a tree of characters. is_end marks where a word ends."]**

> The key move: **share common prefixes in a tree of characters; an `is_end` flag marks where a real word ends.**
>
> Trigger phrase: *"prefix queries, autocomplete, a dictionary of words"* → reach for a Trie. It trades a little memory for prefix ops that don't depend on dictionary size.

---

## 7. CODE IT — LIVE & CHUNKED — `5:35`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 — the node.]**

> First, the node: a map from character to child, plus the end flag.

```python
class TrieNode:
    __slots__ = ("children", "is_end")
    def __init__(self):
        self.children = {}      # char -> TrieNode
        self.is_end = False
```

> **[VISUAL: add chunk 2 — the Trie shell and insert.]** The Trie holds a root. Insert walks the word, creating nodes as needed, and flags the final one.

```python
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
```

> **[VISUAL: add chunk 3 — a shared `_walk` helper.]** Both queries walk a path; factor that out. Return the final node, or `None` if the path breaks.

```python
    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

> **[VISUAL: add chunk 4 — the two queries, the punchline.]** And here's the payoff — they differ by one check.

```python
    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end   # must be a real word end

    def startsWith(self, prefix):
        return self._walk(prefix) is not None     # path existing is enough
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:15`
*(elaboration — why each line exists)*

**[VISUAL: full class; spotlight lines.]**

> Why each piece.
>
> `children = {}` — a dict keyed by character. Only the letters that actually appear get stored, so sparse tries stay lean.
>
> `insert`'s `if ch not in node.children: create` — this is where prefix sharing happens. If the path already exists from an earlier word, we *reuse* it and don't recreate nodes.
>
> `node.is_end = True` at the end — plants the flag that says "a word terminates right here."
>
> **LEARNER:** In `search`, why the `node is not None` check *before* `node.is_end`? Isn't checking the flag enough?
>
> **TEACHER:** Sharp — and no. `_walk` returns `None` when the path doesn't even exist — say you search "xyz" and there's no `x` child at all. If you tried `None.is_end`, you'd crash. So you must first confirm the path exists, *then* ask whether a word ended there. Two separate questions: does the road go there, and is there a house at the end.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: the character tree after `insert("apple")`, then flag flips after `insert("app")`.]**

> Trace it. After `insert("apple")` the tree is:

```
root → a → p → p → l → e(is_end=True)
```

| call | walk result | is_end? | answer |
|---|---|---|---|
| `search("apple")` | reaches `e` node | True | **true** ✅ |
| `search("app")` | reaches second `p` | False | **false** ✅ |
| `startsWith("app")` | reaches second `p` (exists) | — | **true** ✅ |
| `insert("app")` | flips second `p`'s `is_end` → True | — | — |
| `search("app")` | reaches second `p` | now True | **true** ✅ |

> Every case matches the spec from the opening. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:15`
*(transfer to interview)*

**[VISUAL: a table — Set: startsWith O(N×L). Trie: every op O(L).]**

> Say it: *"With a set, insert and search are O(L) in the word length, but `startsWith` is O(N times L) — it scans every stored word. A trie makes **every** operation O(L), completely independent of how many words are stored. That's the whole win — prefix queries that don't care about dictionary size."*
>
> That last clause — *independent of dictionary size* — is the sentence that lands it.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: two node designs side by side — a 26-slot array vs a hash map, sparse slots highlighted.]**

> The node tree itself is the point of a trie — you can't drop it. But there's one real design dial: **how do you store children?**
>
> - A fixed **26-slot array** per node gives O(1) indexing and is a hair faster, but wastes slots on letters that never appear.
> - A **hash map** (what we used) stores only the letters actually present — leaner for sparse tries or big alphabets.
>
> Say it: *"For lowercase-only input the 26-array is the textbook choice; for large or unicode alphabets the map wins. And note the prefix sharing already *is* the compression — 'app', 'apple', 'apply' share three nodes instead of storing three full strings."* Space is O(total inserted characters), and that's the honest floor.

---

## 12. YOUR TURN (active recall) — `10:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Add and Search Word (LC 211)". A search with a `.` wildcard.]**

> Before the next video, try **Add and Search Words**, LC 211. Same trie, but `search` can contain a `.` that matches *any* letter. That one wildcard forces `search` to branch — DFS over all children when it hits a dot. Build on today's trie.
>
> Ten minutes before you peek.

---

## 13. LOCK IT IN — `11:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **A trie is a tree of characters** — shared prefixes, shared nodes.
> 2. **`is_end` is the whole trick** — it separates a word from a mere prefix.
> 3. **Every op is O(L)** — independent of how many words you've stored.
>
> Memory peg: **walk the letters; `search` needs the flag, `startsWith` just needs the road.**

---

## 14. CLIFFHANGER — `11:35`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Word Search II" — a letter grid with a trie overlaid.]**

> A trie is powerful on its own. But watch what happens when you point it at a *grid* of letters and ask it to find thousands of dictionary words at once. Instead of searching the board once per word, you search it *once* — and the trie prunes every dead path instantly. Next up, a Hard one: Word Search II. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

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
