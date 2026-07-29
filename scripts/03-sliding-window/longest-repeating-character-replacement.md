# 🎬 Recording Script — Longest Repeating Character Replacement
**Pattern: Sliding Window (dynamic) · LeetCode 424 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the grow-then-shrink dynamic window from LC 3 / LC 209. New here: "valid" is defined by a *frequency* condition, and a famously subtle trick about not decrementing a stale max.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A red "Time Limit Exceeded" banner over a double loop.]**

> Google loves this one because it *looks* like it needs something clever, and it hides a trick that trips up even strong candidates.
>
> The problem: you can change up to `k` characters of a string to anything you want. What's the longest run of a *single repeated* letter you can create?
>
> The brute force — check every substring — times out. But the real story is a one-line reframe that turns "which characters do I change?" into a simple counting question. And then a stale-variable trick that makes people gasp. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence on top. Below: tiles `A A B A B B A`, indices 0–6, and `k = 1`.]**

> The whole problem in one line: **after changing at most `k` characters, return the length of the longest substring that's all one letter.**
>
> Tiny example: `"AABABBA"`, `k = 1`. You get *one* change. The answer is 4 — take a window like `"AABA"`, change its single `B` to `A`, and you've got four `A`s in a row. Hold that: **4**.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the tiles. A start-marker, a mini frequency tally, a "recount" counter.]**

> Brute force reads the definition literally: for every substring, find its most common letter, and count the *others* — those are the ones you'd have to change. If that count is `≤ k`, this substring is achievable.
>
> Start at 0: `"A"` — 0 to change, fine. `"AA"` — 0, fine. `"AAB"` — most common is A (twice), one `B` to change, that's ≤ 1, fine, length 3. `"AABA"` — three A's, one B, still one change, length 4.
>
> **[VISUAL: marker jumps to index 1; the tally resets to empty.]**
>
> Now restart at index 1 and rebuild the whole tally: `"A"`, `"AB"`, `"ABA"`…
>
> **[VISUAL: highlight the re-tallied letters glowing — counted one pass ago.]**
>
> Every restart recomputes a frequency table over characters we *just* tallied. `n` starts times up to `n` extension = `O(n²)`. At 10⁵ characters, that's Time Limit Exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Overlapping tallies pulsing across two restarts. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste is the same villain as always — every restart rebuilds a frequency count over letters we already counted.
>
> **LEARNER:** Okay, but even inside one window, figuring out "how many do I change" means finding the most common letter. Isn't *that* the expensive part, not just the restart?
>
> **TEACHER:** Great instinct — so let's nail the reframe first, then kill the restart. Pause and think about this: for any window, if I keep the **most frequent letter** and change everything else, how many changes is that? Write the formula. **What has to be true about that number for the window to be achievable with budget `k`?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a window over the tiles; a bar labeled "window length" splitting into "keep (max letter)" + "replace (everyone else)".]**

> Here's the reframe, and it's the whole problem. In any window, the cheapest way to make it all one letter is: **keep the most frequent letter, change all the rest.** So the number of changes you need is:
>
> **changes needed = window length − count of the most frequent letter.**
>
> And the window is **valid** exactly when that number is `≤ k`. That's it. We never ask "which characters do I change" — just "how many," and we get it by subtraction.
>
> **[VISUAL: on window `"AABA"`: length 4, max letter A appears 3 times, 4 − 3 = 1 ≤ k=1. Valid.]**
>
> Now the sliding part. Keep one window and a running count of all 26 letters inside it. Grow `right`. If the window goes invalid — `length − max_count > k` — nudge `left` forward by one and drop that letter from the count. Track the best length.
>
> **LEARNER:** Wait — you said "nudge left by one," a single `if`, not a shrink loop like last lesson. Why only one step?
>
> **TEACHER:** Because we only care about the *longest* window ever. Once we've found a valid window of length 4, we never want a *shorter* one — so we never shrink below the best size. We just slide it rightward, keeping its width, hunting for a chance to grow. A single `if` that moves `left` one step exactly preserves the width. And that sets up the trick everyone misses…

---

## 6. THE KEY MOVE (signaling) — `4:20`
*(one crisp, repeatable sentence + the subtle trick)*

**[VISUAL: a boxed line: "Window valid ⇔ (length − max_count) ≤ k."  Below it, a second box: "Don't bother decrementing max_count."]**

> Burn this in: **a window is valid when its length minus its most-frequent-letter count is within `k`.**
>
> And the trick that makes this famous: **we never decrement `max_count` when the window slides.** We let it go stale — keep the highest frequency we've *ever* seen. Sounds like a bug. It isn't, and here's the intuition: a stale, too-high `max_count` can only make us *think* a window is valid. But we only ever accept a window if it's *longer* than our best — and a genuinely longer valid window requires `max_count` to *actually* rise to a new real high. A stale value can't invent a longer answer out of thin air. It can only fail to shrink a *same-length* window, which never changes the maximum. So the answer stays correct, and the code stays clean.

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. A 26-slot count array, `left`, the running `max_count`, and `best`.

```python
def character_replacement(s, k):
    count = [0] * 26
    left = 0
    max_count = 0          # highest single-letter frequency ever seen
    best = 0
```

> **[VISUAL: add chunk 2, highlight it.]** Grow `right`: bump the new letter's count, and refresh the running max.

```python
    for right in range(len(s)):
        count[ord(s[right]) - ord("A")] += 1
        max_count = max(max_count, count[ord(s[right]) - ord("A")])
```

> **[VISUAL: add chunk 3 — the single-step slide.]** If the window now needs more than `k` changes, slide `left` forward one and drop that letter.

```python
        if (right - left + 1) - max_count > k:
            count[ord(s[left]) - ord("A")] -= 1
            left += 1
```

> **[VISUAL: add chunk 4.]** Record the best length and return.

```python
        best = max(best, right - left + 1)
    return best
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:45`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line.]**

> Let's walk *why*.
>
> `ord(s[right]) - ord("A")` — maps `'A'`→0, `'B'`→1, up to `'Z'`→25. That's our index into the count array.
>
> `(right - left + 1) - max_count > k` — window length minus the most common letter's count is exactly "how many I'd have to change." If that exceeds `k`, the window is unaffordable.
>
> `if`, not `while` — the deliberate choice from the key move. We slide the window rightward at constant width; we never collapse it, because we only want longer windows.
>
> And the line that *isn't* there: **we never decrement `max_count`** after dropping a left character. That's the stale-max trick. It stays as the all-time high.
>
> **LEARNER:** That still bugs me. If I drop a letter and `max_count` is now wrong — too high — couldn't I record a window that's secretly invalid?
>
> **TEACHER:** Follow the sizes. Suppose `max_count` is stale-high by the time we're at some window. The check `length − max_count > k` is now *too lenient*, so we might *not* slide when a fresh count would have. But `left` doesn't move, so the window length is unchanged — it's the *same size* as before. We only update `best` if this window is *longer* than the record, and it isn't longer. So a stale max can only ever "wrongly keep" a window that's no bigger than one we already had. It can never produce a new, larger answer. The maximum is safe.

---

## 9. DRY-RUN THE CODE — `8:05`
*(worked example — prove it, close the loop)*

**[VISUAL: `"AABABBA"`, `k=1`, trace table filling row by row.]**

> Let's run the code on `"AABABBA"`, `k = 1`.

| right (ch) | counts (A,B) | max_count | len | len − max | > k? slide | best |
|---|---|---|---|---|---|---|
| 0 (A) | A1 | 1 | 1 | 0 | no | 1 |
| 1 (A) | A2 | 2 | 2 | 0 | no | 2 |
| 2 (B) | A2 B1 | 2 | 3 | 1 | no | 3 |
| 3 (A) | A3 B1 | 3 | 4 | 1 | no | 4 |
| 4 (B) | A3 B2 | 3 | 5 | 2 | yes → drop A@0, left=1 | 4 |
| 5 (B) | A2 B3 | 3 | 5 | 2 | yes → drop A@1, left=2 | 4 |
| 6 (A) | A2 B3 | 3 | 5 | 2 | yes → drop B@2, left=3 | 4 |

> Answer: 4. Exactly the run of A's we predicted. Notice `max_count` sits at 3 from `right=3` onward and never drops — the stale max in action — and the answer is still correct. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:05`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n²). Ours: O(n). Note: "count array fixed at 26".]**

> **TEACHER:** Say it to the interviewer: *"The reframe is the key — a window is achievable when its length minus its most frequent letter's count is within k. Brute force recomputes frequencies for every substring, O(n²). Instead I slide one window with a 26-letter count. When length minus max-count exceeds k, I slide left forward by one. Because I only want the longest window, it's a single `if`, not a shrink loop — and I don't even decrement max-count, since a stale max can't fabricate a longer valid window. One pass, O(n) time, and the count array is fixed at 26 so O(1) space."*
>
> Explaining the stale-max out loud is a genuine strong-hire moment — most people either don't know it or can't justify it.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:50`
*(depth + honesty)*

**[VISUAL: the 26-slot array glowing, labeled "constant, regardless of n".]**

> The count array is 26 slots no matter how long the string is. That's O(1) — genuinely constant. There's nothing to trim: you need per-letter counts to know the dominant character, and there are only 26 letters.
>
> The one honest caveat: if the alphabet were arbitrary Unicode instead of A–Z, you'd swap the array for a hash map and space becomes O(min(n, Σ)). But for this fixed 26-letter alphabet, the array is both simpler and strictly constant. Say that and you've shown you know *why* it's O(1), not just that it is.

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Max Consecutive Ones III (LC 1004)". A blank editor.]**

> Before the next video, try **Max Consecutive Ones III**: you have a binary array and may flip up to `k` zeros to ones — find the longest run of ones. It's this exact "budget of changes" idea, stripped to two symbols. The valid-window condition becomes "zeros in the window ≤ k."
>
> Write the grow / single-slide skeleton from memory first. That recall is what cements it.

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **The reframe: changes needed = window length − most-frequent-letter count.** Valid when that's ≤ k.
> 2. **Chasing the longest → single-`if` slide, not a shrink loop.** The window never gets shorter than its best.
> 3. **Let `max_count` go stale.** A too-high max can only keep same-length windows — it can't invent a longer answer.
>
> Memory peg: **keep the king, replace the rest.** The dominant letter is the king; everyone else is a change you pay for out of your budget `k`.

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Permutation in String".]**

> So far our windows have grown and shrunk freely. Next up, the window is *locked* to one size — the length of a target word — and the question flips to: does any window of that exact size have the *same letter counts* as the target? That's anagram-hunting with a fixed frame, and it needs a slick way to compare 26 counts in O(1). See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int characterReplacement(String s, int k) {
    int[] count = new int[26];
    int left = 0, maxCount = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        int idx = s.charAt(right) - 'A';
        count[idx]++;
        maxCount = Math.max(maxCount, count[idx]);
        if ((right - left + 1) - maxCount > k) {   // too many replacements
            count[s.charAt(left) - 'A']--;
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```
