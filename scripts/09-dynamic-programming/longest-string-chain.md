# 🎬 Recording Script — Longest String Chain
**Pattern: DP over a hash map (longest chain / implicit DAG) · LeetCode 1048 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the row DP from *Maximum Number of Points with Cost* — there we made a transition faster; here we make a whole graph disappear.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a whiteboard covered in word bubbles with arrows scribbled between them — a messy tangled graph. A hand draws yet another arrow. Then the whole drawing fades to grey and ONE clean sorted list slides in over the top.]**

> Here's the trap in this problem, and almost everyone falls in it.

> You read the words. You see "predecessor." You start drawing arrows between words. Congratulations — you've just built a graph, and now you owe yourself a topological sort, a DFS, a memo, and a visited set. In a 40-minute interview.

> There's a version of this where none of that exists. No graph. No recursion. Twelve lines. And it comes from two moves you'll use for the rest of your DP life — **sort into dependency order**, and **generate your neighbours instead of hunting for them**.

> By the end of this video you'll know exactly why the graph was never necessary. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below it, six word-cards laid out:]**

```
words = ["a", "b", "ba", "bca", "bda", "bdca"]
```

> The whole problem in one line: **find the longest chain of words where each word is the previous one with exactly one character inserted.**

> Inserted — *anywhere* — but nothing reordered. So `"ba"` is a predecessor of `"bda"`: slip a `d` into the middle, done. `"ba"` is **not** a predecessor of `"ab"` — that's a reshuffle, not an insertion.

> **[VISUAL: `"ba"` → `"b_a"` → `"bda"` animates, the `d` dropping into the gap. Then `"ba"` → `"ab"` with a red ✗.]**

> One consequence to bank right now, because the entire solution hangs off it: **a predecessor is always exactly one character shorter.** Always. No exceptions.

> Six words on screen. The answer is **4**. Hold that number — we'll earn it by hand before we write a line of code.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: the six words in a circle. A "comparisons" counter, top-right, at 0. An arrow shoots from `"bdca"` to every other word in turn; each one lights up, gets checked, and 5 of them flash red ✗.]**

> Let's do what your brain does first. For each word, ask every *other* word: "are you one insertion away from me?" Draw an arrow when the answer's yes. Then find the longest path through the arrows.

> Take `"bdca"`. Is `"a"` my predecessor? Different length — no. `"b"`? No. `"ba"`? No. `"bca"`? **Yes.** `"bda"`? **Yes.** Five questions, two arrows. **[counter → 5]**

> Now do that for all six words. Thirty comparisons for six words.

> **[VISUAL: the counter spins up to 30. Then the words multiply into a dense blob and the counter rockets to 999,000.]**

> Six words is nothing. But the constraint says up to **a thousand** words — and a thousand words means about a **million** pairs, every one of them a character-by-character subsequence check.

> Now look at *what* we spent it on. Watch the rejections.

> **[VISUAL: replay the `"bdca"` scan in slow motion. Over `"a"`, `"b"`, `"ba"` a badge pops: "rejected on LENGTH ALONE".]**

> Three of those five rejections never looked at a single character. They died on `len(b) != len(a) + 1`. We paid for a search that the *lengths* had already answered.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — pause #1)*

**[VISUAL: freeze on `"bdca"` with its five arrows. Three arrows greyed and stamped "length says no". A 5-second "🤔 your turn" timer.]**

> **TEACHER:** Name the waste out loud: we're **searching** a haystack for predecessors. Nine hundred and ninety-nine questions, and almost every answer is no.

> **LEARNER:** But how else would I find them? "Predecessor" is a *relationship between two words* — don't I have to look at both to know?

> **TEACHER:** That's the assumption to break, and it's a good one. Here's the flip. Stop asking *"which word out there is my predecessor?"* and ask *"what would my predecessor **look like**?"*

> Pause the video right here. Take the word `"bdca"`. Without looking at the list at all — write down every string that could possibly be its predecessor. How many are there?

> *(pause — 5 seconds)*

---

## 5. BUILD THE INTUITION (the aha) — `3:20`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: `b d c a` in four boxes. One at a time, a box is lifted out and the rest close the gap, producing `dca`, `bca`, `bda`, `bdc` stacked below.]**

> Did you get four? Because that's all there are.

> Inserting one character into `A` to get `B` is exactly the **inverse** of deleting one character from `B` to get `A`. So the complete set of possible predecessors of `"bdca"` is: delete the `b` → `"dca"`. Delete the `d` → `"bca"`. Delete the `c` → `"bda"`. Delete the `a` → `"bdc"`. Four strings. That's the *whole universe*. Nothing else can be a predecessor. Ever.

> **[VISUAL: the four candidates drop into a hash-map lookup slot. `dca` → ✗. `bca` → ✓. `bda` → ✓. `bdc` → ✗.]**

> And a word is at most **16 characters** — the constraint says so. So every word has **at most 16 possible predecessors**, and I can write all sixteen down and just *look them up in a hash set*. Sixteen lookups instead of nine hundred and ninety-nine comparisons.

> Think of it like a locksmith. The searching version walks a hallway of a thousand doors trying your key in every one. The generating version reads the shape of your key and **cuts the four doors it could possibly open**.

> **[VISUAL: the six words re-arranging themselves into length order: a, b | ba | bca, bda | bdca. Columns labelled "len 1", "len 2", "len 3", "len 4".]**

> Now the second move, and it's the quieter one. When I look up `"bca"`, I need its answer to *already be computed*. Is it? Every predecessor is exactly one character shorter — so if I process the words **shortest first**, then by the time I reach any word, everything that could feed it is already done. Finished. Final.

> That's it. **Sorting by length IS the topological order.** For free. One `sort` call, and the graph, the DFS, the visited set — all of it evaporates.

---

## 6. THE KEY MOVE (signaling) — `4:40`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Sort by length. Delete one char → look it up. dp[w] = 1 + best predecessor."]**

> Burn this line in: **sort by length so predecessors are already solved, then delete one character at a time and look the result up.**

> `dp[word]` means one thing all the way through: *the length of the longest chain that **ends at** this word.* And the rule is `dp[word] = 1 + the best dp among my deleted-by-one candidates that actually exist` — and if none exist, I'm a chain of one, all by myself.

> The transferable half: **when a DP's dependency is "one step smaller," sort into dependency order first — and when the neighbour space is tiny, *generate* the key instead of scanning for it.**

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only, highlighted.]**

> Let's build it. Line one is the whole first leap.

```python
def longestStrChain(words):
    words.sort(key=len)          # shortest first = dependency order
    dp = {}                      # word -> longest chain ending at that word
    best = 0
```

> `sort(key=len)`. That's our topological sort. `dp` is a plain dict — word in, chain length out.

> **[VISUAL: add chunk 2, highlight the slice.]** Now, for each word, generate its predecessors.

```python
    for w in words:
        cur = 1                          # a lone word is already a chain of 1
        for i in range(len(w)):
            pred = w[:i] + w[i + 1:]     # delete character i
```

> `w[:i] + w[i+1:]` — everything before position `i`, everything after position `i`. That's the word with character `i` removed. Loop `i` over the whole word and you've generated every candidate.

> **[VISUAL: add chunk 3, highlight `if pred in dp`.]** Look it up. Take the best.

```python
            if pred in dp:               # exists AND is already solved
                cur = max(cur, dp[pred] + 1)
        dp[w] = cur
        best = max(best, cur)

    return best
```

> `if pred in dp` is doing two jobs at once — hold that thought, it's the next beat. Then we record `dp[w]`, keep a running best, and return it. Twelve lines. No recursion, no graph, no visited set.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:50`
*(elaboration — why each line exists)*

**[VISUAL: the full function; a spotlight moves to each line as it's named.]**

> Let's walk *why*, not what.

> `words.sort(key=len)` — without this line the code is silently **wrong**, not slow. If `"bdca"` gets processed before `"bca"`, the lookup misses and we under-count. The sort is what makes "already solved" true.

> **LEARNER:** Hang on — most of those deleted strings aren't real words at all. `"bdc"` isn't in the list. Doesn't the dictionary fill up with garbage?

> **TEACHER:** Great catch, and that's the second job `if pred in dp` is doing. We **never insert** a generated string — we only ever *ask* about it. A candidate that isn't a real word simply isn't a key, the `in` check is False, and we move on. The map only ever holds actual input words. That's why it stays `O(N)` and not `O(N · L)` junk entries.

> `cur = 1` — the base case, and it's easy to lose. A word with no predecessors in the list is still a valid chain: itself. If you initialise to 0 you'll return one less than the answer on every single test.

> **LEARNER:** One more. Couldn't I check predecessors more cheaply — just confirm A's letters are all inside B with one left over?

> **TEACHER:** That's the tempting wrong turn, and interviewers watch for it. **Order matters.** `"ab"` and `"ba"` have identical letters, but `"ba"` is *not* a predecessor of `"abc"` — you'd have to reorder, and the problem forbids that. Any multiset or letter-count check quietly accepts anagrams and gives you wrong answers on cases you'll never think to test. Deletion is order-preserving by construction, which is exactly why generating beats hand-rolling a comparison.

> And the cost: one sort, then per word 16 deletions, each costing about 16 to build and hash. That's `N log N + N·L²` — about a quarter of a million operations for the full thousand-word input.

---

## 9. DRY-RUN THE CODE — `8:10`
*(worked example — pause #2, then close the loop)*

**[VISUAL: the six words sorted into a column on the left; an empty `dp` table on the right, filling row by row.]**

> Let's run the real code. Sorted by length: `a`, `b`, `ba`, `bca`, `bda`, `bdca`.

| Word | Generated predecessors | Found in `dp`? | `dp[word]` |
|---|---|---|---|
| `a` | `""` | none | **1** |
| `b` | `""` | none | **1** |
| `ba` | `"a"`, `"b"` | `a`→1, `b`→1 | 1+1 = **2** |
| `bca` | `"ca"`, `"ba"`, `"bc"` | `ba`→2 | 2+1 = **3** |
| `bda` | `"da"`, `"ba"`, `"bd"` | `ba`→2 | 2+1 = **3** |
| `bdca` | ? | ? | ? |

> **[VISUAL: the last row blanked out. A 5-second "🤔 your turn" timer over it.]**

> Stop the video. You've got `bca` at 3 and `bda` at 3 sitting in the map. Work out the last row yourself: what are `"bdca"`'s four candidates, which ones hit, and what's `dp["bdca"]`?

> *(pause — 5 seconds)*

> **[VISUAL: the row fills in.]**

> Candidates: `"dca"`, `"bca"`, `"bda"`, `"bdc"`. Two of them are real words — `bca` at 3 and `bda` at 3. So `dp["bdca"] = 3 + 1 = ` **4**.

> Final answer: **4**. Exactly the number we promised at the top. And the chain is `"a"` → `"ba"` → `"bda"` → `"bdca"` — one character inserted each step.

> **[VISUAL: the winning chain lights up in green across the word cards.]**

> Now notice what never happened in that entire table. We never once compared `"bdca"` to `"a"`. We never compared any word to any other word. Not a single pairwise check in the whole run. That's the win, made concrete.

---

## 10. COMPLEXITY, OUT LOUD — `9:25`
*(transfer to interview)*

**[VISUAL: two rows. Brute force: O(N² · L) — "~16,000,000". Ours: O(N log N + N · L²) — "~260,000". A 60× badge between them.]**

> Say it the way you'd say it in the room: *"The graph version costs O(N squared times L) just to find the edges — about sixteen million character comparisons at N equals a thousand. My version sorts in N log N, then does L deletions per word at L cost each: O(N log N plus N times L squared). Roughly two hundred sixty thousand. Sixty times less work, and I never materialise the graph, so I skip the O(N squared) edge list too."*

> And add the line that shows you're thinking past the given limits: *"If N grew to a hundred thousand, the pairwise version is ten to the tenth and dead. Mine is twenty-six million and fine — because my cost per word depends on the **word length**, not on how many other words exist."*

> That last sentence is the strong-hire sentence. It says you know *which* term you removed.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:00`
*(depth + honesty)*

**[VISUAL: the dp map drawn as columns by length — "len 1", "len 2", "len 3", "len 4". Older columns fade grey as the cursor moves right.]**

> **LEARNER:** Last lesson we rolled a 2-D DP down to one row. Predecessors are always exactly one shorter — so can't we throw away everything except the previous length group?

> **TEACHER:** You can, and you're right to reach for it. Once we're processing length-4 words, nothing will ever ask about length 2 again. Keep two dicts — previous group and current group — and swap them at each length boundary. It's a real optimisation and it's worth saying out loud.

> **[VISUAL: two small dicts, `prev` and `cur`, swapping at a length boundary.]**

> **But be honest about what it buys you: the constant, not the order.** Worst case, every word is length 8 or 9 — two adjacent groups holding all thousand words. You've rolled away nothing.

> So the floor stays `O(N)`, and here's why that floor is real: every word needs its own chain length remembered, and those `N` numbers are `N` independent facts. Nothing you can do.

> Say it in the room like this: *"Space is O(N) and that's optimal — I have to remember a chain length per word. I could drop all but the previous length group since predecessors are exactly one shorter, but that's a constant-factor win, not an asymptotic one, because one length group can be the entire input."*

> Naming which optimisation exists **and** why it doesn't move the exponent — that's the judgement they're scoring. Memory was never the problem in this one. Killing the N-squared edge set was.

---

## 12. YOUR TURN (active recall) — `10:45`
*(retrieval practice)*

**[VISUAL: "Your turn → Largest Divisible Subset (LC 368)". A blank editor.]**

> Before the next video, do **Largest Divisible Subset**, LeetCode 368. Same skeleton, different relation: sort the numbers ascending so every divisor comes before its multiple, then chain on divisibility instead of insertion.

> Two things to notice while you solve it. One: the sort is doing the *exact same job* it did here — putting dependencies first. Two: you can't "generate" divisors as cheaply as we generated predecessors, so that half of today's trick doesn't transfer. Feeling *which* half carries over is the point of the exercise.

> Don't peek. Ten minutes of wrestling beats an hour of watching.

---

## 13. LOCK IT IN — `11:20`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **"Longest chain" smells like a graph — check whether a sort makes the graph unnecessary.** If every edge goes from smaller to bigger by a fixed step, sorting *is* your topological order.
> 2. **Generate neighbours, don't search for them.** Deleting one character gives the complete predecessor set — at most 16 candidates, versus 999 comparisons.
> 3. **Order matters, letters aren't enough.** Any anagram-style shortcut accepts `"ba"` into `"abc"` and is silently wrong.

> And the memory peg — the one line that recalls the whole pattern:

> **[VISUAL: big box → "Sort into dependency order. Build the key, hit the map."]**

> When a DP's dependency is "one step smaller," your hand should reach for `sort` before it reaches for recursion.

> *(GCA reminder — for the interview itself: state the graph framing first, out loud, then say "but every edge goes from length L to length L plus one, so a sort by length gives me the order for free." That narration — naive framing, named observation, collapse — **is** the General Cognitive Ability signal. And ask the clarifying question before you code: "insert one character, no reordering, right?" It takes four seconds and it's the exact detail people get wrong.)*

---

## 14. CLIFFHANGER — `11:55`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Sort Integers by The Power Value — LC 1387". Behind it, a jagged line graph that shoots up, crashes down, spikes again — nothing like today's neat staircase.]**

> Today's chain only ever went **one step up**. That's why sorting worked — the dependency order was sitting right there in the lengths.

> Next problem, the chain goes the other way and it *misbehaves*. Take a number: if it's even, halve it; if it's odd, triple it and add one. Count the steps to reach 1. Start at 15 and the value climbs past 150 before it comes back down.

> So which order do you process the numbers in? You can't sort by size — the chain jumps **above** your range and back. There's no dependency order to find.

> Which means the trick we just learned doesn't apply — and the fix is the *other* half of dynamic programming, the half we've been quietly avoiding for two lessons. See you there.
