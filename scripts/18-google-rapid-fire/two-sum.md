# 🎬 Recording Script — Two Sum

**Pattern: Hash Map (complement lookup) · LeetCode 1 · Easy ⭐ · Target length ~10 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none — this is the "why hash maps matter" origin story.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. Two nested `for` loops typed out. A phone-screen clock ticking in the corner.]**

> This is the most-asked interview question on the planet. *"Find the two numbers that add up to the target."*
>
> And almost everyone writes the same first answer — two loops, check every pair. It works. But there's a reason this "easy" problem shows up in Google phone screens: they're not testing whether you can *solve* it. They're testing whether you can spot the **one wasteful thing** your loops are doing — and replace it with a trick you'll then reuse in a dozen harder problems.
>
> By the end of this, you'll never write those two loops again. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:30`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below: four tiles `2  7  11  15`, and "target = 9".]**

> The whole problem in one line: **return the indices of the two numbers that add up to the target.**
>
> Tiny example — four numbers, `2, 7, 11, 15`, target `9`. The answer is indices `[0, 1]`, because `2 + 7 = 9`.
>
> Two things the interviewer sneaks in: return the **indices**, not the values. And the array is **not sorted** — that matters more than it looks.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:05`
*(worked example — let them feel the waste)*

**[VISUAL: the four tiles. A marker `i` and a marker `j`. A "checks" counter, top-right.]**

> Let's do what the brain does first. Pin `i` on the first number and let `j` try everyone after it.
>
> `i` on `2`. `j` on `7`: `2 + 7 = 9`? Yes — but pretend we're unlucky and the answer's later. `j` on `11`: `2 + 11`? No. `j` on `15`? No. Now `i` moves to `7`, and `j` re-scans `11`, `15`... then `i` on `11`, `j` on `15`...
>
> **[VISUAL: markers jump through pairs, counter ticking 1, 2, 3, 4, 5, 6.]**
>
> For every single number, we re-scan the rest of the array. Four numbers is fine. But at ten thousand numbers, that's fifty million checks — and notice *what* those checks are: over and over, we're asking **"is `target minus this number` somewhere in the array?"** and never remembering the answer.

---

## 4. THE PAIN POINT + PREDICT — `2:15`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight the repeated inner scan. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** There's the waste. For each number we ask a question — *"have I got the partner that completes the target?"* — and we answer it by scanning. Every. Single. Time.
>
> **LEARNER:** But the array's unsorted, so I can't binary-search it. What else is there? It kind of *has* to look through everything, doesn't it?
>
> **TEACHER:** That's the instinct to break. Pause and think: **"is this specific value somewhere in my collection, instantly?" — what data structure answers that in one step, no scanning, sorted or not?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `2:55`
*(elaboration + analogy — derive it)*

**[VISUAL: the phrase "look something up by value, instantly" morphs into the word "HASH MAP".]**

> **TEACHER:** "Look something up by value, instantly" — that *is* the definition of a hash map. So instead of re-scanning, let's **remember**.
>
> As I walk the array, I write down every number I've seen — value → its index. Now for the current number `x`, the partner I need is `complement = target − x`. And the question "have I already seen the complement?" is now a single hash-map lookup. O(1).

**[VISUAL: walk `2, 7, 11, 15`. At 2: "need 7 — seen? no. Remember 2." At 7: "need 2 — seen? YES, at index 0!" Both light up.]**

> Walk it. First number `2`, target `9`, so I need `7`. Seen a 7 yet? No. **Remember 2.** Next number `7` — I need `2`. Seen a 2? **Yes — at index 0.** Return `[0, 1]`. One pass. Never scanned ahead.
>
> **LEARNER:** Wait — I only stored `2` before I got to `7`. What if the partner comes *later* in the array, not earlier?
>
> **TEACHER:** Beautiful question, and here's why one pass is enough: whichever of the pair you reach **second** finds the first one already waiting in the map. The order doesn't matter — you only need one of them to be recorded by the time you arrive at the other.

---

## 6. THE KEY MOVE (signaling) — `4:10`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "For each number, check for its complement BEFORE storing it."]**

> Burn this in: **for each number, look for its complement in the map first — then store the current number.**
>
> "Check before store" isn't a style choice — it's what stops you from pairing a number with *itself*. That one ordering is the entire trick.

---

## 7. CODE IT — LIVE & CHUNKED — `4:45`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type the setup.]**

> Five lines. Start with the map.

```python
def two_sum(nums, target):
    seen = {}                      # value -> index
```

> **[VISUAL: add the loop.]** Walk the array with both index and value.

```python
    for i, x in enumerate(nums):
        complement = target - x
```

> **[VISUAL: add the check-then-store.]** Check for the complement — if it's there, we're done. Otherwise remember this number and move on.

```python
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return []
```

> That's it. The whole optimized solution is shorter than the brute force.

---

## 8. EXPLAIN THE CODE (the WHY) — `5:45`
*(elaboration — why each line exists)*

**[VISUAL: the finished function; spotlight each line.]**

> Why each piece.
>
> `seen` maps *value to index* — value because we look up by the number's value, index because that's what we must return.
>
> `complement = target - x` — the exact partner that would complete the sum. We turn "find two things that add up" into "find one specific thing."
>
> `if complement in seen` comes **before** `seen[x] = i`. 
>
> **LEARNER:** Why does that ordering matter so much? Feels like it'd work either way.
>
> **TEACHER:** Say `target` is `6` and you land on a `3`. The complement is also `3`. If you stored the current `3` *first*, then checked, you'd find your own entry and return `[i, i]` — the same element twice, which the problem forbids. Check first, and you only match a `3` that came *earlier*. Order saves correctness.

---

## 9. DRY-RUN THE CODE — `6:45`
*(worked example — prove it)*

**[VISUAL: trace table filling row by row for `[2,7,11,15]`, target 9.]**

| i | x | complement (9−x) | in seen? | action |
|---|---|---|---|---|
| 0 | 2 | 7 | no | store 2→0 → seen = {2:0} |
| 1 | 7 | 2 | **yes (index 0)** | return **[0, 1]** ✅ |

> Two iterations. We reached `7` second; its partner `2` was already sitting in the map from the first step. Output `[0, 1]`. Loop closed — no ahead-scanning ever happened.

---

## 10. COMPLEXITY, OUT LOUD — `7:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute: O(n²) time, O(1) space. Hash map: O(n) time, O(n) space.]**

> Out loud to the interviewer: *"Brute force is O(n²) — every pair. The waste is repeatedly searching for the complement, and 'search by value' means a hash map. One pass, O(1) lookups, so O(n) time. The map costs O(n) space. I trade memory for speed."*
>
> That trade — spend O(n) space to buy O(n) time — is the entire lesson.

---

## 11. CAN WE USE LESS MEMORY? (space) — `7:55`
*(depth + honesty)*

**[VISUAL: "sorted?" fork — one branch "hash map, O(n) space", other "two pointers, O(1) space".]**

> Can we drop the O(n) space? Only by changing the problem's precondition — and that's the insight worth stating.
>
> To get O(1) space you'd **sort** first and use two pointers. But sorting is O(n log n) — slower — *and* it scrambles the positions, and we were asked for **indices**. So you'd have to store the original indices anyway, back to O(n) space.
>
> Contrast **Two Sum II**, where the input is *already sorted*: there, two pointers give O(n) time and O(1) space, strictly better. The whole difference is that one word — "sorted."
>
> Say it in the room: *"Unsorted and I must return indices, so the hash map's O(n) space buys the better O(n) time. If it were sorted, I'd switch to two pointers for O(1) space."* Choosing the structure to fit the precondition — that's the signal.

---

## 12. YOUR TURN (active recall) — `8:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Subarray Sum Equals K (LC 560)". Blank editor.]**

> Before the next video, try **Subarray Sum Equals K**. It looks different — count subarrays that sum to `k` — but it's the *exact same reflex*: you walk once, and for each running total you check the map for a complement you've already seen. Same move, one level deeper.
>
> Struggle with it ten minutes before peeking. That's what locks it in.

---

## 13. LOCK IT IN — `9:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **Repeated "is this value here?" → hash map.** That's the whole pattern.
> 2. **Turn "find two that combine" into "find one specific complement."**
> 3. **Check before you store** — it prevents matching an element with itself.
>
> The memory peg — when you see *"find two things that add up, unsorted,"* your hand reaches for a map: **remember what you've seen, look up what you need.**

---

## 14. CLIFFHANGER — `9:30`
*(open loop to next lesson)*

**[VISUAL: a blurred title: "Group Anagrams". A pile of scrambled words.]**

> Two Sum taught you to hash a *value*. But what if the thing you want to group by isn't a value at all — it's a *shape*? Next up: a pile of words, and you have to cluster the ones that are rearrangements of each other. The trick is inventing the right **key** to hash. Same reflex, sneakier key. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();   // value -> index
    for (int i = 0; i < nums.length; i++) {
        int complement = target - nums[i];
        if (seen.containsKey(complement)) {
            return new int[]{seen.get(complement), i};
        }
        seen.put(nums[i], i);
    }
    return new int[]{};
}
```
