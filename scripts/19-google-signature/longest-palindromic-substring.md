# 🎬 Recording Script — Longest Palindromic Substring
**Pattern: Expand Around Center · LeetCode 5 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the two-pointer "squeeze" from the pair-sum lesson — but this time the pointers move *outward*.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A tangle of nested loops with an `is_palindrome` helper. A red "Time Limit Exceeded — 987/1000" banner slides in.]**

> The interviewer types one line: *"Return the longest substring that reads the same both ways."*
>
> You do the obvious thing — check every substring, test each one, keep the longest. It's correct. You hit run… and it crawls. Time Limit Exceeded.
>
> The idea wasn't wrong. It just does a pile of work it doesn't need to. By the end of this video you'll have a solution that's shorter, faster, *and* uses no extra memory — and you'll know exactly why it works. One image will carry the whole thing. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, five letter tiles: `b  a  b  a  d`.]**

> The whole problem in one line: **find the longest chunk that reads the same forwards and backwards.**
>
> Here's our tiny example — just five letters, `b a b a d`. Keep your eye on these; we'll solve this exact string by hand before we write a single line of code.
>
> There's a palindrome of length three hiding in here. Don't hunt for it yet — just hold that the answer is three letters long.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the five tiles. A bracket sweeping over every substring: `b`, `ba`, `bab`, `baba`… A "checks" counter climbing top-right.]**

> Let's do what your brain does first: look at *every* substring and ask "is this one a palindrome?"
>
> `b`? Yes, trivially. `ba`? No. `bab`? Compare the outer `b`s — match — then the middle. Palindrome! `baba`? Check outer, check inner… no. And on, and on.
>
> **[VISUAL: bracket keeps sliding; counter ticks 4, 7, 11, 15…]**
>
> Here's the ugly part. To test `bab` I compared the outer pair. To test `babad` I compare the outer pair *again*, from scratch. I keep re-deriving the same facts.
>
> Five letters is instant. But there are about n-squared substrings, and each check is another O(n) walk — that's O(n cubed). At a thousand characters —
>
> **[VISUAL: counter morphs into "≈ 1,000,000,000"]**
>
> A billion operations. There's your Time Limit Exceeded.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight the outer `b…b` pair being re-compared across three different substrings. A 4-second "🤔 your turn" timer appears.]**

> **TEACHER:** So where's the waste? Look — I keep starting every palindrome check *from the ends and working in*, re-testing pairs I've already confirmed on shorter strings.
>
> **LEARNER:** Right, but a palindrome kind of *is* an outside-in thing. How else would you even check it?
>
> **TEACHER:** That's the instinct to flip. Pause the video and sit with this: instead of grabbing a substring and checking from the outside in… **what if you started in the *middle* and grew outward?** What would that give you for free?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the tile `a` in `bab` glows as a center. Two arrows push outward from it: left hits `b`, right hits `b`.]**

> **TEACHER:** Here's the reframe. Every palindrome has a **center** — a middle point it mirrors around. So forget substrings. Stand on the center and *grow*: push one finger left, one finger right. Same letter on both sides? You're still inside a palindrome — keep going. Different, or you fall off the edge? Stop. You just found the biggest palindrome for that center.
>
> Think of it like a zipper opening from the middle, or ripples spreading from where a stone hits water. You don't guess-and-check — you build the answer outward.
>
> **[VISUAL: on `bab`, center `a`: fingers step out to `b`/`b` (match ✓), step again → off both edges. Palindrome `bab` locks in green.]**
>
> Watch it on our string. Center on the `a` in the middle. Left finger `b`, right finger `b` — match. Step again — we run off both ends. Done: `bab`, length three. We *grew* it in two comparisons. No re-checking every substring.

---

## 6. THE MISCONCEPTION — WHY 2n−1 CENTERS? — `4:15`
*(confront the wrong-but-tempting idea — the key retention beat)*

**[VISUAL: the string `cbbd`. A single finger hovering over `b`, `b`, then confused. Then a marker drops into the *gap between* the two `b`s.]**

> **LEARNER:** Okay, so one center per letter — n centers, one per character. Simple.
>
> **TEACHER:** Careful — that's the trap, and it's the number-one bug in this problem. Take `cbbd`. The answer is `bb`. Where's *its* center? It's not on a letter — there's no middle character. The center sits **between** the two `b`s.
>
> **LEARNER:** Ohh. So even-length palindromes have their center *in the gap*, not on a character.
>
> **TEACHER:** Exactly. Odd-length palindromes — `bab`, `aba` — center on a character. Even-length ones — `bb`, `abba` — center on the *gap* between two characters. So the centers are: **n characters, plus n−1 gaps between them. That's 2n−1 centers total.** Miss the gaps and you'll never find a single even-length palindrome. Check every one.
>
> **[VISUAL: `cbbd` with all 7 centers marked — 4 on letters, 3 in gaps (2·4−1 = 7). The gap between the two `b`s expands outward to grab `bb`.]**

---

## 7. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Every palindrome has a center — grow from all 2n−1 of them."]**

> Burn this one line in: **every palindrome has a center — grow from all 2n−1 of them.**
>
> One expand routine, called twice per position: once with both fingers on the same character (odd), once with them straddling the gap (even). That's the whole algorithm.

---

## 8. CODE IT — LIVE & CHUNKED — `5:35`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, the one routine that does all the work — expand from a center.

```python
def expand(s, left, right):
    # walk outward while it's still a palindrome
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return left + 1, right - 1   # step back to the last valid pair
```

> **[VISUAL: highlight the `return`.]** One gotcha: the loop stops *after* it fails, so `left` and `right` have each gone one step too far. Step them back — that's the `+1` and `−1`.
>
> **[VISUAL: add chunk 2.]** Now the driver: track the best answer so far as a `[start, end]` range.

```python
def longest_palindrome(s):
    if not s:
        return ""
    start, end = 0, 0
```

> **[VISUAL: add chunk 3, highlight the two `expand` calls.]** Loop every position, and call expand *twice* — odd center on the character, even center on the gap after it.

```python
    for i in range(len(s)):
        l1, r1 = expand(s, i, i)       # odd: center on character i
        if r1 - l1 > end - start:
            start, end = l1, r1
        l2, r2 = expand(s, i, i + 1)   # even: center in the gap i..i+1
        if r2 - l2 > end - start:
            start, end = l2, r2
    return s[start:end + 1]
```

> There's the `2n−1` in code: `n` odd calls, `n` even calls — the last even one just expands nothing and harmlessly does nothing.

---

## 9. EXPLAIN THE CODE (the WHY) — `7:10`
*(elaboration — why each line exists)*

**[VISUAL: the full two functions; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `expand(s, i, i)` — both fingers start on the *same* character. That's the odd case: `bab`'s center is the single `a`.
>
> `expand(s, i, i + 1)` — fingers straddle a gap. That's the even case: `bb`'s center is between the two `b`s. This one line is what makes even-length palindromes findable — it's the misconception, fixed.
>
> `left >= 0 and right < len(s)` — the edge guards. Without them the fingers walk off the string and crash. These come *first* in the `and`, before we touch `s[left]` — short-circuit order matters.
>
> **LEARNER:** Quick one — why `return left + 1, right - 1`? Why the step-back?
>
> **TEACHER:** Sharp catch. The `while` only exits *after* a mismatch — either the characters differed or a finger fell off the edge. So on exit, `left` and `right` are one past the last *good* pair. We nudge them back inward by one to land on the real palindrome. Forget that and you'll grab garbage on the ends.
>
> And `r - l > end - start` — that's just "is this palindrome longer than my current best?" Range width is the length, minus one, but the comparison still works.

---

## 10. DRY-RUN THE CODE — `8:25`
*(worked example — prove it, close the loop)*

**[VISUAL: `b a b a d` with a trace table filling row by row; fingers animating outward on each call.]**

> Let's run the actual code on `babad` and watch it land.

| i | call | expands to | palindrome | best so far |
|---|---|---|---|---|
| 0 | odd (0,0) | (0,0) | `b` | `b` (len 1) |
| 0 | even (0,1) | `b≠a` → nothing | — | `b` |
| 1 | odd (1,1) → (0,2) | `b==b` ✓, then off edge | `bab` | **`bab` (len 3)** |
| 1 | even (1,2) | `a≠b` → nothing | — | `bab` |
| 2 | odd (2,2) → (1,3) | `a==a` ✓ → (0,4) `b≠d` ✗ | `aba` | still len 3 → keep `bab` |
| 3–4 | — | nothing beats 3 | — | `bab` |

> Output: `bab`. Exactly the length-three palindrome we said was hiding at the start. And notice `aba` was *also* length three — either answer is accepted; we just kept the first. Loop closed.

---

## 11. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n³). Ours: O(n²). A note: "2n−1 centers × O(n) expand".]**

> **TEACHER:** Say it the way you would to the interviewer: *"Brute force is O(n cubed) — n-squared substrings times an O(n) check. Expand-around-center is O(n squared): there are 2n−1 centers, and each expands at most O(n). Space is O(1) — I'm only holding a few indices."*
>
> That sentence — the naive cost, the improvement, *and* the space — is what earns the checkmark.

---

## 12. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: a big `O(n²)` DP grid on the left, crossed out; our four little integer variables on the right.]**

> Quick but important — and here it's about *not* over-engineering.
>
> There's a classic DP-table solution to this problem: an n-by-n grid marking which substrings are palindromes. Same O(n squared) time — but O(n squared) *space*.
>
> We don't need it. Expand-around-center holds two fingers and a best-so-far range. That's it. **O(1) extra space.** Say it out loud: *"It's already O(1) space — the DP version would cost me an n-by-n table for the same time, so this is strictly leaner."* Naming why there's nothing left to cut is a strong-hire move.
>
> **LEARNER:** And if they push for faster than O(n²)?
>
> **TEACHER:** Then you name **Manacher's algorithm** — true O(n) — reuses mirror symmetry so each center is amortized O(1). Nobody expects you to code it live; naming it is the win.

---

## 13. YOUR TURN (active recall) — `10:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Palindromic Substrings (LC 647)". A blank editor.]**

> Before the next video, try **Palindromic Substrings**, LeetCode 647. Same exact move — expand from all 2n−1 centers — but instead of tracking the longest, you *count* every palindrome you pass through.
>
> Don't peek at the solution. Struggle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 14. LOCK IT IN — `11:05`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Grow, don't check.** Expand outward from a center beats testing every substring.
> 2. **2n−1 centers** — n on characters (odd), n−1 in the gaps (even). The gaps are the bug everyone hits.
> 3. **Step back on exit** — the loop overshoots by one, so `return left+1, right-1`.
>
> And the memory peg — the whole pattern in one image: **every palindrome has a center; grow from all 2n−1 of them.**

---

## 15. CLIFFHANGER — `11:35`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Longest Palindromic *Subsequence*".]**

> We grew palindromes that were *contiguous* — solid runs of characters. But what if the letters don't have to be next to each other? "Longest palindromic *subsequence*" lets you skip characters — and suddenly expanding from a center falls apart, because there's no fixed center to grow from. That one needs a completely different weapon: a 2-D table. Same word "palindrome," a whole new pattern. See you there.

---

## 📌 GCA reminder
Before recording: **G**et the tiny example on screen first (`babad`), **C**hunk the code into the four pieces above (never paste the wall), **A**lways read every `>` line out loud — if it sounds like a textbook, rewrite it warmer.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public String longestPalindrome(String s) {
    if (s == null || s.isEmpty()) return "";
    int start = 0, end = 0;
    for (int i = 0; i < s.length(); i++) {
        int[] odd = expand(s, i, i);       // odd-length center
        if (odd[1] - odd[0] > end - start) { start = odd[0]; end = odd[1]; }
        int[] even = expand(s, i, i + 1);  // even-length center
        if (even[1] - even[0] > end - start) { start = even[0]; end = even[1]; }
    }
    return s.substring(start, end + 1);
}

private int[] expand(String s, int left, int right) {
    while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
        left--;
        right++;
    }
    return new int[]{left + 1, right - 1};  // step back to last valid pair
}
```
