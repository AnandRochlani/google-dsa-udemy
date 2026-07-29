# 🎬 Recording Script — Permutation in String
**Pattern: Sliding Window (fixed size) · LeetCode 567 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the *fixed*-size roll from Maximum Average Subarray (LC 643) meets the frequency-count thinking from LC 424. Here the window is locked to `len(s1)`, and we match letter counts.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: two strings on screen: `s1 = "ab"`, `s2 = "eidbaooo"`. A red "Time Limit Exceeded" banner over a nested loop.]**

> *"Does `s2` contain a permutation of `s1`?"* — an anagram of `s1`, hiding somewhere as a substring.
>
> The instinct: slide a window and, for each position, sort or recount it and compare to `s1`. Correct, and slow — you rebuild a full count for every window from scratch.
>
> By the end of this video you'll compare two 26-letter fingerprints in *constant* time per step, using a single clever counter that only ever looks at the two letters that changed. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence on top. `s1 = "ab"` boxed; `s2 = "eidbaooo"` as tiles, indices 0–7.]**

> The whole problem in one line: **is some contiguous window of `s2` a rearrangement of `s1`?**
>
> Two facts unlock everything. First, a permutation of `s1` has *exactly* `len(s1)` characters — here, 2 — so we only ever look at windows of `s2` that are **exactly 2 wide**. Fixed size. Second, two strings are permutations of each other **if and only if their letter counts are identical.** Same letters, same quantities, any order.
>
> The answer here is True — `"ba"` at indices 3–4 is a rearrangement of `"ab"`. Hold that.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example — let them feel the waste)*

**[VISUAL: `need = {a:1, b:1}` in a box. A 2-wide window sliding over `s2`, rebuilding a fresh count each stop.]**

> Brute force: build `s1`'s count once — `a:1, b:1`. Then slide a 2-wide window across `s2` and, at each spot, **recount** the window and compare.
>
> Window `"ei"` — count e:1, i:1. Compare to need. Nope.
> Window `"id"` — recount i:1, d:1. Nope.
> Window `"db"` — recount d:1, b:1. Nope.
>
> **[VISUAL: highlight that each window shares one character with its neighbor — glowing — yet gets recounted fully.]**
>
> Freeze. Every window overlaps the previous one by a character, but I threw away the whole count and rebuilt it. Rebuilding costs `m` = `len(s1)` per window, across `n` windows — `O(n·m)`. When both strings are large, that drags.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Two adjacent windows, one char leaving, one entering, both pulsing. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste, named: when the fixed window slides one step, only *one* character leaves and *one* enters — but I recount all `m` from scratch.
>
> **LEARNER:** Sure, I can update the count incrementally like the average problem. But then I still have to compare 26 numbers to `need` every step to know if it matches. Isn't *that* the slow part now?
>
> **TEACHER:** Sharp — you've found the *second* bottleneck. So pause and think: instead of re-comparing all 26 counts each step, **could I keep a single number that tracks how many letters already agree with `need` — and only fix it up for the two letters that changed?** What would that number have to hit for a full match?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: two 26-slot bars, `need` and `window`, side by side. A `matches` dial reading 0–26.]**

> Two leaps, stacked.
>
> **Leap one — slide the count, don't rebuild it.** Keep one running `window` count. When the frame moves right: decrement the letter that left, increment the letter that entered. Two updates, not `m`. Exactly the "minus what leaves, plus what enters" roll from the average lesson — but on letter counts instead of a sum.
>
> **Leap two — track agreement with a single dial.** Comparing 26 slots every step is wasteful when only two changed. So keep a counter, `matches`: **how many of the 26 letters currently have the same count in `window` as in `need`.** When `matches` hits 26, every letter agrees — the window *is* a permutation.
>
> **[VISUAL: a letter's count ticks up; the dial checks just that letter — "was it equal before? is it equal now?" — and adjusts by ±1.]**
>
> The bookkeeping is delightfully local. When a letter's count changes, only *that* letter's agreement can flip. So before the change, ask "were we equal?" — if yes, we're about to break it, so `matches--`. After the change, ask "are we equal now?" — if yes, `matches++`. Two letters touched per slide, a couple of checks each. O(1).
>
> Think of it like two combination locks side by side. You're not re-reading all the dials every second — you only glance at the dial you just turned, and keep a tally of how many already line up.

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Slide the count (−leaving, +entering); track `matches`; permutation ⇔ matches == 26."]**

> Burn this in: **slide the count instead of rebuilding it, and track a single `matches` dial — when all 26 letters agree, you've found the anagram.**
>
> That `matches` counter is the tightening that turns an O(26)-per-step compare into O(1).

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. Guard the impossible case, then count what `s1` needs.

```python
def check_inclusion(s1, s2):
    m, n = len(s1), len(s2)
    if m > n:
        return False

    need = [0] * 26
    window = [0] * 26
    for ch in s1:
        need[ord(ch) - ord("a")] += 1
```

> **[VISUAL: add chunk 2, highlight it.]** Initialize `matches` — for every letter where `need` and `window` already agree. Both start at zero, so all 26 agree out of the gate.

```python
    matches = 0
    for i in range(26):
        if need[i] == window[i]:
            matches += 1
```

> **[VISUAL: add chunk 3 — the entering character.]** March `right`. Add the entering letter, fixing `matches` around the change.

```python
    for right in range(n):
        r = ord(s2[right]) - ord("a")
        if window[r] == need[r]:
            matches -= 1        # was equal, about to break it
        window[r] += 1
        if window[r] == need[r]:
            matches += 1        # became equal
```

> **[VISUAL: add chunk 4 — the leaving character.]** Once the window is wider than `m`, evict the leftmost letter, again fixing `matches`.

```python
        if right >= m:
            l = ord(s2[right - m]) - ord("a")
            if window[l] == need[l]:
                matches -= 1
            window[l] -= 1
            if window[l] == need[l]:
                matches += 1

        if matches == 26:
            return True
    return False
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:10`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each block.]**

> Let's walk *why*.
>
> The init loop sets `matches = 26` — because before we've read any of `s2`, both counts are all zeros, so every letter trivially agrees. We build up from a known-good baseline.
>
> The entering block is the ±1 dance. Before touching a letter, "were we equal? then I'm about to break it, `matches--`." Bump the count. "Equal now? `matches++`." Only that one letter's agreement can change, so those are the only checks we need.
>
> `if right >= m` — this is what keeps the window a *fixed* size `m`. When `right` reaches index `m`, the window would be `m+1` wide, so we evict the character that entered `m` steps ago: index `right - m`.
>
> **LEARNER:** Why `right >= m` and not `right > m`? I always second-guess that boundary.
>
> **TEACHER:** Count it out. At `right = m - 1`, the window spans indices 0 through `m-1` — exactly `m` characters. Perfect size, nothing to evict. The *first* time it overflows is `right = m`, spanning 0 through `m`, which is `m+1` wide. So we start evicting at `right == m` — that's `>=`. Evict index `right - m = 0`, the oldest. Off-by-one dodged.
>
> `matches == 26` — every one of the 26 letters agrees, so the window's fingerprint equals `s1`'s. It's a permutation. Return True.

---

## 9. DRY-RUN THE CODE — `8:30`
*(worked example — prove it, close the loop)*

**[VISUAL: `s1="ab"`, `s2="eidbaooo"`, m=2. Trace table of the 2-wide window.]**

> Let's run it. `need = {a:1, b:1}`. Watch the 2-wide window as `right` advances.

| right (ch) | window (size ≤ 2) | a,b vs need | matches == 26? |
|---|---|---|---|
| 0 (e) | `"e"` | a:0 b:0 | no |
| 1 (i) | `"ei"` | a:0 b:0 | no |
| 2 (d) | `"id"` (evict e) | a:0 b:0 | no |
| 3 (b) | `"db"` (evict i) | a:0 b:1 | no |
| 4 (a) | `"ba"` (evict d) | a:1 ✓ b:1 ✓ | **yes → return True** |

> At `right = 4` the window is `"ba"`, a and b both hit their needed count of 1, every letter agrees, `matches` reaches 26. True — exactly the `"ba"` we spotted at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:35`
*(transfer to interview)*

**[VISUAL: rows — Brute force: O(n·m). Ours: O(n). A note: "matches ⇒ O(1) compare".]**

> **TEACHER:** Say it to the interviewer: *"A permutation of s1 has exactly s1's letters and exactly s1's length, so I only look at fixed windows of length len(s1). Brute force recounts each window, O(n·m). Instead I slide one count — decrement the leaver, increment the enterer — and to avoid comparing 26 counts each step, I keep a single `matches` number, how many letters already agree with s1, fixing it only for the two touched letters. When matches hits 26, it's an anagram. O(n) time, O(1) space since the alphabet's fixed at 26."*
>
> The two-part story — slide the count *and* track matches — is what shows you optimized both bottlenecks, not just one.

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:15`
*(depth + honesty)*

**[VISUAL: two 26-slot arrays, `need` and `window`, labeled "constant".]**

> Two fixed 26-slot arrays plus a few scalars — O(1) space, independent of input length. You fundamentally need per-letter counts to compare frequencies, and there are only 26 letters.
>
> Honest trade-off worth naming: you *can* drop the `matches` counter and just compare `window == need` every step. Still O(n) time overall and the same O(1) space — but with a bigger constant, since each step re-checks 26 slots. It's the readable version; `matches` is the tightening. Mentioning both — and *why* you'd pick one — is the strong-hire signal.

---

## 12. YOUR TURN (active recall) — `10:50`
*(retrieval practice)*

**[VISUAL: "Your turn → Find All Anagrams in a String (LC 438)". A blank editor.]**

> Before the next video, try **Find All Anagrams in a String**. Identical machinery — fixed window, sliding count, `matches` dial — but instead of returning True on the first hit, you *collect every start index* where `matches == 26`. One tiny change: don't return, append and keep going.
>
> Rebuild the sliding-count-plus-matches skeleton from memory first. That recall is the whole point.

---

## 13. LOCK IT IN — `11:20`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Fixed target length + "anagram / permutation" → fixed-size window + frequency match.** The tell is that the target size is known and constant.
> 2. **Slide the count, don't rebuild it** — decrement the leaver, increment the enterer.
> 3. **Track `matches`** so each step is O(1); a full match is `matches == 26`.
>
> Memory peg: **two combination locks, side by side.** Only glance at the dial you just turned, and keep a tally of how many already line up.

---

## 14. CLIFFHANGER — `11:50`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Minimum Window Substring".]**

> Here the window was locked to one size and we asked "do the counts match *exactly*?" Next up, the boss level: the window can be *any* size, and we want the *shortest* one that merely *covers* a target — every required letter present, duplicates and all, extras allowed. It's the grow-then-shrink window plus need/have counting — the template that unlocks a whole family of hard problems. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public boolean checkInclusion(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    if (m > n) return false;

    int[] need = new int[26], window = new int[26];
    for (char c : s1.toCharArray()) need[c - 'a']++;

    int matches = 0;
    for (int i = 0; i < 26; i++) if (need[i] == window[i]) matches++;

    for (int right = 0; right < n; right++) {
        int r = s2.charAt(right) - 'a';
        if (window[r] == need[r]) matches--;
        window[r]++;
        if (window[r] == need[r]) matches++;

        if (right >= m) {
            int l = s2.charAt(right - m) - 'a';
            if (window[l] == need[l]) matches--;
            window[l]--;
            if (window[l] == need[l]) matches++;
        }
        if (matches == 26) return true;
    }
    return false;
}
```
