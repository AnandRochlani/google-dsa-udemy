# 🎬 Recording Script — Sum of Prefix Scores of Strings
**Pattern: Trie · LeetCode 2416 · Hard · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** basic Trie insert (Implement Trie / LC 208) — but here we add one tiny counter that changes everything.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A clean double-loop solution is typed out. A LeetCode "Time Limit Exceeded — 61 / 78" banner slams in red.]**

> The interviewer says: *"For each word, add up the scores of all its prefixes. A prefix's score is how many words start with it. Go."*
>
> You write the obvious thing — for every prefix, count the matching words. It's *correct*. It passes the small tests. You run the big one and… Time Limit Exceeded.
>
> Your code isn't wrong. It's just counting the **same prefix thousands of times**. By the end of this video you'll fix it with one data structure and a single `+= 1` in exactly the right place. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, four word-tiles: `abc  ab  bc  b`.]**

> The whole problem in one line: **for each word, sum the scores of all its non-empty prefixes — where a prefix's score is how many words in the list start with it.** A word counts as a prefix of itself.
>
> Here's our tiny example — four short words: `abc`, `ab`, `bc`, `b`.
>
> Take `abc`. Its prefixes are `a`, `ab`, `abc`. How many words start with `a`? Two — `abc` and `ab`. Start with `ab`? Also two. Start with `abc`? Just one. So `abc` scores `2 + 2 + 1 = 5`.
>
> Hold that number — **five**. The full answer is `[5, 4, 3, 2]`. We'll earn all four by hand before we write code.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the four words. A "prefix counts" tally on the right, ticking up. Arrows scan the whole list for each prefix.]**

> Let's do what your brain does first. For each prefix, scan **all four words** and count who starts with it.
>
> For `abc`: check prefix `a` — scan all four, count 2. Check `ab` — scan all four, count 2. Check `abc` — scan all four, count 1.
>
> **[VISUAL: for prefix `a`, arrows sweep across all four tiles; tally ticks 2.]**
>
> Now `ab`: prefix `a` — scan all four again, count 2. Prefix `ab` — scan again, count 2.
>
> **[VISUAL: highlight that we just re-scanned for `a` a *second* time; a red "again!" flashes.]**
>
> See it? We counted "how many words start with `a`" for `abc`, and then **again** for `ab`. Same question, same answer, recomputed from scratch.
>
> **[VISUAL: tally morphs into "O(n² · L²)" with a red glow.]**
>
> With a thousand words up to a thousand characters each, that repetition explodes. That's your Time Limit Exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Spotlight the prefix `a` being counted from two different words. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So where's the waste? The score of a prefix like `a` never changes — it's a fact about the whole list. But we recompute it for every word that owns `a` as a prefix.
>
> **LEARNER:** Okay, but the words genuinely share prefixes. Isn't re-counting the shared part just unavoidable?
>
> **TEACHER:** They share prefixes — but the *count* for a shared prefix is one number. So here's your think: **what if we counted each prefix exactly once, up front, and stored that count somewhere the words could all read?** Pause the video. Where would you store a count that's shared across words that start the same way?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the four words start threading into a branching tree from a single root — `a` splits into a path, `b` into another. Each node shows a small counter badge.]**

> **TEACHER:** Here's the move. Stack all the words into a **Trie** — a prefix tree. Every path from the root spells out a prefix. The path `r → a → b` *is* the prefix `ab`. One node, one prefix.
>
> Now the magic. Give every node a counter. **Every time a word passes through a node while we insert it, bump that counter by one.** Think of each node as a turnstile — every word walking through clicks it forward.
>
> **[VISUAL: insert `abc` — nodes `a`, `ab`, `abc` each click to 1. Insert `ab` — `a` clicks to 2, `ab` clicks to 2.]**
>
> After inserting `abc` then `ab`, the `a` node reads **2** and the `ab` node reads **2**. That's not a coincidence — that counter *is* the number of words that start with `a`. It's the score. We never scanned the list; the turnstile counted for us.
>
> **LEARNER:** Wait — do I bump only the last node of each word, or every node along the way?
>
> **TEACHER:** **Every node.** That's the whole trick, and it's the line people get wrong. If you only bump the last node, you're counting exact-word matches, not prefixes. Bump on *every* step of the insert, because passing through node `ab` means this word has `ab` as a prefix — so `ab`'s score goes up.
>
> **[VISUAL: highlight the insert loop; the `count += 1` sits *inside* the per-character step, glowing.]**

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Insert = bump count on EVERY node. node.count = that prefix's score."]**

> Burn this one line in: **when you insert a word, increment the counter on every node you step onto — and that counter becomes the prefix's score for free.**
>
> Then answering a word is trivial: walk it down the tree and add up the counters you pass. Each node is one prefix; each counter is its score. Sum them — done.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First the node: a dictionary of children, and a counter starting at zero.

```python
class TrieNode:
    def __init__(self):
        self.children = {}   # char -> TrieNode
        self.count = 0       # words passing through this prefix
```

> **[VISUAL: add chunk 2, highlight it.]** Now insert every word — and watch *where* the `count += 1` lives.

```python
def sum_prefix_scores(words):
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1          # ← bump on EVERY step, not just the last
```

> **[VISUAL: spotlight the indentation — `count += 1` is inside the `for ch` loop.]** That one line, at that one indent level, is the entire optimization.
>
> **[VISUAL: add chunk 3.]** Now the query — walk each word back down, summing the counters.

```python
    answer = []
    for w in words:
        node = root
        total = 0
        for ch in w:
            node = node.children[ch]   # exists — we inserted this word
            total += node.count        # this node = one prefix, count = its score
        answer.append(total)
    return answer
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `node.count += 1` **inside the insert loop** — this is the difference between a prefix-counter and a plain trie. Every character step means one more word passes through this prefix, so we click the turnstile. Move it outside the loop and you'd only count whole words — the answer collapses.
>
> **LEARNER:** In the query, you write `node = node.children[ch]` with no "is it there?" check. In insert you *did* check. Why is it safe to skip the check now?
>
> **TEACHER:** Sharp catch. It's safe because we only ever query words we already inserted. Every character of `w` carved a path into the trie during the build, so that exact path is guaranteed to exist when we walk it back down. No missing child is possible. If we were querying a *random* string, you'd absolutely need the guard.
>
> `total += node.count` — each node on `w`'s path is one of `w`'s prefixes, and its counter is that prefix's score. Adding them as we descend sums every prefix's score in one clean pass. That's the definition of the answer, computed in `O(length of w)`.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: the trie with counter badges; two trace tables filling row by row.]**

> Let's run the real code on `["abc","ab","bc","b"]`. **Build phase** first — bump on every step:

| Insert | Nodes clicked (count after) |
|---|---|
| `abc` | `a`→1, `ab`→1, `abc`→1 |
| `ab`  | `a`→2, `ab`→2 |
| `bc`  | `b`→1, `bc`→1 |
| `b`   | `b`→2 |

> Final badges: `a`=2, `ab`=2, `abc`=1, `b`=2, `bc`=1. Now the **query phase** — walk each word, sum the badges:

| Word | Path (node.count) | Sum |
|---|---|---|
| `abc` | `a`(2) + `ab`(2) + `abc`(1) | **5** |
| `ab`  | `a`(2) + `ab`(2) | **4** |
| `bc`  | `b`(2) + `bc`(1) | **3** |
| `b`   | `b`(2) | **2** |

> `[5, 4, 3, 2]`. Loop closed — and that leading **5** is exactly the number we promised for `abc` back at the start.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n² · L²). Ours: O(N), N = total characters. Note: "each char touched once to build, once to query".]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force is quadratic because it re-counts each prefix against the whole list. With a trie, I touch each character once to insert and once to query — so it's `O(N)` time, where `N` is the total number of characters across all words. Space is `O(N)` for the trie nodes."*
>
> That's the sentence that flips a Hard from "I hope" to "I've got this."

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: the trie; a "collapse to one row?" thought bubble appears, then a red ✗. Beside it, a node redrawn two ways: a dict vs a 26-slot array.]**

> Quick but important — and honesty scores here.
>
> Can we beat `O(N)` space? **No, and I can say why.** A word's answer depends on the counts of *all* its prefixes, and those prefixes are shared arbitrarily across the input — there's no "keep only the last row" collapse like a 1-D DP, because the dependencies fan out across the whole tree. The trie *is* the algorithm.
>
> What you *can* tune is the node. I used a dictionary — flexible, light when branching is sparse. If the alphabet is fixed `a` to `z`, you could use a **26-slot array** per node: pointer-fast lookups, but a fixed 26-wide array even on near-empty nodes. Same `O(N)` asymptotics, different constant.
>
> Say it out loud: *"Space is `O(N)` and that's the floor — every prefix's count is consulted. Dict node keeps constants low; array-26 trades memory for speed."* Naming the trade is a stronger signal than picking one silently.

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Map Sum Pairs (LC 677)". A blank editor.]**

> Before the next video, try **Map Sum Pairs**. Same skeleton — a trie where nodes carry a value along the path — but now you `insert(key, val)` and query the *sum of values* for all keys with a given prefix. It's this exact "aggregate along the path" idea, flipped slightly.
>
> Don't peek. Wrestle with it for ten minutes. That struggle turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **"Count shared prefixes" → reach for a Trie.** A node is a prefix; the tree counts sharing for free.
> 2. **Bump the counter on EVERY node during insert** — that counter *becomes* the prefix's score. Only the last node = you counted words, not prefixes.
> 3. **Answer a word by walking down and summing counters** — `O(word length)` per query.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "Every insert clicks every turnstile — the turnstile count is the score."]**
>
> When you see "score = how many words share this prefix," your hand should already be reaching for a trie with a counter on every node.
>
> *(GCA reminder — for the interview itself: state the brute force, name the repeated counting out loud, *then* reach for the trie. Google's General Cognitive Ability signal isn't the data structure — it's you narrating the path from naive to optimal. And ask the one clarifying question early: "a word counts as its own prefix, right?" That question is points on the rubric.)*

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Word Search II" — a letter grid with a trie overlaid on top.]**

> We built a trie and just *read* counts off it. But what happens when the trie meets a **grid** — when you have to hunt dozens of words at once by crawling a board of letters, and a plain search would re-walk the same paths forever? That's the next one: **Word Search II** — trie plus DFS, the heavyweight cousin. It's where this pattern earns its Hard badge. See you there.
