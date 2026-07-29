# 🎬 Recording Script — Group Anagrams

**Pattern: Hash Map (canonical key) · LeetCode 49 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Two Sum's "hash a derived key" reflex.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: six word-tiles scattered — eat, tea, tan, ate, nat, bat. Faint lines try to connect the ones that are rearrangements of each other, tangling into a mess.]**

> Here's a deceptively deep Google question: *"Group these words so all the anagrams sit together."* eat, tea, ate — same letters, different order.
>
> The tempting move is to compare every word against every other word — "are these two anagrams?" — over and over. That's a quadratic tangle. The elegant move is to realize you shouldn't be **comparing** words at all. You should be giving each word a *label* that anagrams automatically share.
>
> The whole lesson is: **when comparing pairs is slow, invent a key.** Learn it here and you'll reach for it constantly. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below, the six tiles and the target grouping: [eat, tea, ate] · [tan, nat] · [bat].]**

> One line: **group the words that are anagrams** — same letters, same counts, any order. Return the groups in any order.
>
> Tiny example — six words. The answer is three groups: `eat, tea, ate` together; `tan, nat` together; `bat` alone. Keep these six in view; we'll build those groups by hand.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: each new word compared against the "representative" of each existing group; arrows re-sorting words to check.]**

> Brute force: keep a list of groups. For each new word, walk the existing groups and check "is this an anagram of that group's first word?" — by sorting both and comparing. If none match, start a new group.
>
> `eat` — no groups yet, start one. `tea` — compare to `eat`: sort both to `aet`, match, join. `tan` — compare to `eat`, no match, new group. `ate` — compare to `eat` (`aet`=`aet`), join...

**[VISUAL: a "sort operations" counter climbing fast as each word re-sorts against multiple group reps.]**

> It works. But notice: every word gets compared against multiple groups, and every comparison **re-sorts**. We keep recomputing the same sorted forms and re-scanning groups. Worst case — all distinct — that's roughly O(n² · k log k). Slow, and wasteful.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on "eat" and "tea" both being sorted to "aet" — separately, redundantly. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste: we ask "are these two anagrams?" thousands of times, and re-sort to answer each one. Look — `eat` and `tea` both sort to the same thing, `aet`, but we compute that separately every time they meet.
>
> **LEARNER:** So if they both *sort to the same string*... couldn't that sorted string just be the group's name? Then anagrams would drop into the right group without any comparison.
>
> **TEACHER:** That is the entire insight — you've got it. Pause and make it precise: **what's a transformation I can apply to a word so that two words give the *identical* result exactly when they're anagrams?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(elaboration + analogy — derive it)*

**[VISUAL: eat → aet, tea → aet, ate → aet, all funneling into a bucket labeled "aet". tan/nat → "ant". bat → "abt".]**

> **TEACHER:** Anagrams differ only in letter *order*, never letter *content*. So we need a **canonical form** — a fingerprint that ignores order. Two natural ones:
>
> **Sorted letters.** `eat → aet`, `tea → aet`, `ate → aet`. All anagrams sort to the identical string. That sorted string is the fingerprint.
>
> **Letter counts.** A length-26 tally: how many a's, b's, c's. Anagrams have identical tallies. Same fingerprint, computed in one linear pass instead of a sort.
>
> **[VISUAL: the canonical form dropping into a hash map as a KEY; each word appended to map[key].]**
>
> Now the reflex — use that fingerprint as a **hash-map key**, and append each word to `map[fingerprint]`. Anagrams collide into the same bucket *by definition*. One pass over the words, and the map's values *are* the groups. No pairwise comparison, ever.
>
> **LEARNER:** So the sorting doesn't disappear — it just moves from "compare pairs" to "make a key once per word"?
>
> **TEACHER:** Exactly. We sort each word *once* to label it, instead of re-sorting it against every group. That's the difference between n² and n.

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed line: "Map each item to an order-independent key; group by the key in one pass."]**

> The key move: **give every item a canonical key that collapses away what shouldn't matter, then group by that key in a single hash-map pass.** Here, "what shouldn't matter" is letter order. The whole skill is spotting *what to normalize away* — and then the map does the grouping for free.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. The sorted-key version.]**

> Sorted-key version first — cleanest to write.

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))      # canonical form: sorted letters
        groups[key].append(s)
    return list(groups.values())
```

> Three lines of logic. `defaultdict(list)` means a missing key auto-creates an empty list, so we just append.
>
> **[VISUAL: the count-key variant appears beside it.]** The faster variant — avoid the sort with a 26-length count signature.

```python
from collections import defaultdict

def group_anagrams_counts(strs):
    groups = defaultdict(list)
    for s in strs:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - ord('a')] += 1
        groups[tuple(counts)].append(s)   # tuple is hashable → usable as a key
    return list(groups.values())
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:40`
*(elaboration — why each line exists)*

**[VISUAL: both versions; spotlight the key construction.]**

> Why it's correct: two words are anagrams **if and only if** their sorted forms — equivalently, their letter counts — are equal. That's the literal definition. So the key sends exactly the anagrams, and only them, into the same bucket. No false groupings possible.
>
> The count variant builds a 26-slot tally per word — `ord(ch) - ord('a')` maps `a`→0, `b`→1, and so on.
>
> **LEARNER:** Why `tuple(counts)` and not just the list? Why convert it?
>
> **TEACHER:** Because a hash-map key has to be **hashable**, and Python lists are mutable, so they can't be keys. A tuple is the frozen, immutable version of the same 26 numbers — same contents, but usable as a key. Small detail, but forget it and you get a `TypeError` in the interview.

---

## 9. DRY-RUN THE CODE — `7:30`
*(worked example — prove it)*

**[VISUAL: the sorted-key map filling row by row.]**

| word | key = sorted | map after |
|---|---|---|
| eat | aet | {aet:[eat]} |
| tea | aet | {aet:[eat,tea]} |
| tan | ant | {aet:[eat,tea], ant:[tan]} |
| ate | aet | {aet:[eat,tea,ate], ant:[tan]} |
| nat | ant | {aet:[eat,tea,ate], ant:[tan,nat]} |
| bat | abt | {aet:[...], ant:[tan,nat], abt:[bat]} |

> Result: `[[eat,tea,ate], [tan,nat], [bat]]` — exactly the three groups we predicted. Every word walked in once, dropped into its bucket by fingerprint, no comparisons. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:20`
*(transfer to interview)*

**[VISUAL: three rows — Brute O(n²·k log k); sorted key O(n·k log k); count key O(n·k). Space O(nk) all.]**

> Out loud: *"n words of length up to k. Brute force is O(n² · k log k) — every pair, re-sorting. The sorted-key map is O(n · k log k): one sort per word, then O(1) bucketing. The count-signature key drops the sort, giving O(n · k). Space is O(nk) either way — I have to store all the strings in the output."*
>
> That progression — from n² down to n·k — is the payoff of "key instead of compare."

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:00`
*(depth + honesty)*

**[VISUAL: the output regrouping ALL input strings — highlight "the answer IS all the data".]**

> Space is **inherently O(nk)** — the output literally contains every input string, just regrouped. There's no in-place trick; you can't return the groups without holding the words. So don't chase space here.
>
> The real optimization is on **time**, and it's the count-key: swap each word's O(k log k) sort for an O(k) tally, giving O(n·k) overall.
>
> Say it out loud: *"Sorted-string keys are the cleanest to write; the length-26 count tuple avoids the sort for O(n·k) time. Both use O(nk) space, which is unavoidable since the output holds every string."* Knowing which resource you *can* optimize — and which you can't — is the mark of clear thinking.

---

## 12. YOUR TURN (active recall) — `9:40`
*(retrieval practice)*

**[VISUAL: "Your turn → Group Shifted Strings (LC 249)".]**

> Before the next video, try **Group Shifted Strings** — group strings that are *shifts* of each other, like `abc`, `bcd`, `xyz`. Same exact pattern, but you invent a *different* canonical key: the sequence of gaps between consecutive letters. It tests whether you really understand that the skill is *choosing what to normalize*, not memorizing "sort the letters."
>
> Fifteen minutes before you peek.

---

## 13. LOCK IT IN — `10:15`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Pairwise comparison is slow → invent a canonical key** and group in one pass.
> 2. **Anagram key = sorted letters, or a 26-length count tuple** (count is faster, skips the sort).
> 3. **Keys must be hashable** — freeze the count list into a tuple.
>
> The memory peg — *"don't compare items, fingerprint them — anagrams share a fingerprint, so the map groups them for free."*

---

## 14. CLIFFHANGER — `10:45`
*(open loop to next lesson)*

**[VISUAL: a blurred array [1,2,3,4] transforming into [24,12,8,6].]**

> So far the map has been our hammer. Next problem takes it away entirely. You're asked for the product of *all other* elements at each index — no division allowed — and the trick isn't a map at all. It's realizing every answer splits into "everything to my left" times "everything to my right." A completely different tool: prefix and suffix products. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String s : strs) {
        char[] c = s.toCharArray();
        Arrays.sort(c);                 // canonical key
        String key = new String(c);
        groups.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}
```

*(Count-key variant: build an `int[26]`, then use `Arrays.toString(...)` or the counts as a string key to skip sorting — O(n·k).)*
