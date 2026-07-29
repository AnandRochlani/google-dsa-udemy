# 🎬 Recording Script — Minimum Window Substring
**Pattern: Sliding Window (dynamic, need/have) · LeetCode 76 · Hard · Target length ~15 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** everything so far — the grow-then-shrink window (LC 209), frequency counting (LC 424, LC 567). This is the boss level that fuses them into the *need/have* template.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. `s = "ADOBECODEBANC"`, `t = "ABC"`. A red "Time Limit Exceeded" banner over a double loop.]**

> This is the sliding-window problem Google interviewers reach for when they want to *separate* candidates. It's marked Hard, and most people freeze.
>
> The task: find the *shortest* substring of `s` that contains *all* of `t`'s characters — duplicates included. The brute force — every substring, check coverage — is `O(n²)` and dies.
>
> But here's the promise: this problem has a *template*. Learn its shape once — expand to become valid, contract to become minimal, with two counters called `formed` and `required` — and you'll own an entire family of "hard" string problems. By the end of this video, Hard will feel like a pattern you recognize. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one sentence on top. `s = "ADOBECODEBANC"` as tiles; `t = "ABC"` boxed.]**

> The whole problem in one line: **the shortest window of `s` that covers every character of `t`, counting duplicates.** If none exists, return the empty string.
>
> Our example: `s = "ADOBECODEBANC"`, `t = "ABC"`. We want the tiniest stretch of `s` holding at least one A, one B, and one C.
>
> One detail that changes everything: `t` can have **repeats**. If `t` were `"AABC"`, we'd need *two* A's in the window, not one. So this is about matching **counts**, not just "is the letter present." The answer here is `"BANC"` — hold that. It has A, B, C, and nothing shorter does.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:25`
*(worked example — let them feel the waste)*

**[VISUAL: the tiles. A start-marker `i`, an end-marker `j`, a "coverage check" recomputed each step.]**

> Brute force reads the definition literally: try every substring, check if it covers `t`, keep the shortest.
>
> Start `i` at 0. Extend `j`: `"A"` — has A, missing B, C. `"AD"` — still missing. `"ADO"`, `"ADOB"` — now has A and B, missing C. `"ADOBE"` — still missing C. `"ADOBEC"` — A, B, C all present! Length 6. Record it.
>
> **[VISUAL: marker `i` jumps to 1; coverage check resets, re-scans from scratch.]**
>
> Now restart at `i = 1` and rebuild coverage from nothing: `"D"`, `"DO"`, `"DOB"`…
>
> **[VISUAL: highlight the re-scanned overlap glowing — checked one pass ago.]**
>
> Freeze. Checking `[i..j]` then `[i..j+1]` re-scans almost the same characters. And every new start rebuilds the coverage check from zero. `O(n²)` substrings, each an `O(n)`-ish check. On 10⁵ characters, hopeless.

---

## 4. THE PAIN POINT + PREDICT — `2:45`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Overlapping re-scans pulsing across restarts. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste is our old villain, dressed up: every restart recomputes "does this window cover `t`?" from scratch, re-scanning characters we already accounted for.
>
> **LEARNER:** But "covering" is more than one number this time — it's *multiple* letters, each with its own required count. With the sum problem I tracked one running total. How do I track "am I covered yet" incrementally when there are several requirements at once?
>
> **TEACHER:** *That's* the exact question this problem is built to answer. So pause and think: suppose I know `t` needs 1 A, 1 B, 1 C — three distinct requirements. As I add characters, **could I keep a single count of how many of those requirements are *fully met right now*? When would the window be valid, and once it is, what should I do to make it shorter?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:30`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a checklist: `A ☐  B ☐  C ☐`. A `formed` counter and `required = 3` label. A window with `left`/`right` edges.]**

> Here's the template, and it's worth slowing down for. Four pieces:
>
> - **`need`** — how many of each character `t` requires. For `"ABC"`: `A:1, B:1, C:1`.
> - **`required`** — the number of *distinct* characters we must satisfy. Here, 3.
> - **`window`** — a running count of characters currently inside our window.
> - **`formed`** — how many distinct requirements are *fully met right now*.
>
> **[VISUAL: as characters enter, the checklist ticks A ☑, then B ☑, then C ☑; `formed` climbs 0→1→2→3.]**
>
> Now the two-phase dance:
>
> **Expand to become valid.** Push `right` forward, adding characters. Each time a character's window-count *reaches* its needed count, one more requirement is satisfied — `formed++`. When `formed == required`, every requirement is met: the window **covers `t`**. It's valid.
>
> **Contract to become minimal.** A valid window might be bloated with junk on the left. So pull `left` inward, dropping characters, as long as the window *stays* valid — recording the smallest valid window each time. The moment removing a character would break coverage (its count drops *below* what's needed, `formed--`), stop shrinking and go back to expanding.
>
> **[VISUAL: window inflates rightward to `"ADOBEC"` (valid), then the left edge presses in, trimming `A,D,O` until it can't.]**
>
> Think of it like packing a suitcase for a trip with a required list — one shirt, one charger, one passport. You keep tossing items in until every required thing is present (expand). Then you *remove* everything you can while the required list stays complete (contract), so the bag is as small as possible.

---

## 6. THE KEY MOVE (signaling) — `5:00`
*(one crisp, repeatable sentence)*

**[VISUAL: a boxed line: "Expand right until formed == required → contract left while still valid → record the smallest."]**

> Burn this in: **expand `right` until the window is valid (`formed == required`), then contract `left` while it stays valid — recording the smallest.**
>
> That's *the* need/have template. Same skeleton solves Find All Anagrams, Permutation in String, and half the "hard" window problems. This is the shape to memorize.

---

## 7. CODE IT — LIVE & CHUNKED — `5:40`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. Guard the empties, then set up `need`, `required`, and the tracking state.

```python
from collections import Counter

def min_window(s, t):
    if not s or not t:
        return ""

    need = Counter(t)
    required = len(need)      # distinct chars we must satisfy
    window = {}
    formed = 0                # how many distinct chars are fully satisfied
```

> **[VISUAL: add chunk 2, highlight it.]** Track the best answer as a length and a start index — infinity means "none found yet."

```python
    best_len = float("inf")
    best_left = 0
    left = 0
```

> **[VISUAL: add chunk 3 — the expand.]** March `right`, add each character, and bump `formed` when a requirement is exactly met.

```python
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            formed += 1       # this character just became fully covered
```

> **[VISUAL: add chunk 4 — the contract loop.]** While valid, record and shrink from the left.

```python
        while formed == required:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_left = left
            lch = s[left]
            window[lch] -= 1
            if lch in need and window[lch] < need[lch]:
                formed -= 1   # dropped below required → no longer valid
            left += 1

    return "" if best_len == float("inf") else s[best_left:best_left + best_len]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:30`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each block.]**

> Let's walk *why* — this is where the subtleties live.
>
> `required = len(need)` — the number of *distinct* letters, not the total length of `t`. For `"AABC"`, `required` is 3 (A, B, C), even though `t` is 4 long. The A's multiplicity is handled by the *count*, not by `required`.
>
> `if window[ch] == need[ch]` — note it's `==`, exact equality, not `>=`. We bump `formed` only at the *exact moment* a character reaches its needed count — the transition from "not enough" to "just enough." If we used `>=`, a fourth A in the window would wrongly bump `formed` again. Equality fires once, cleanly.
>
> **LEARNER:** In the contract loop, when I remove a character, why `window[lch] < need[lch]` — strictly less than? Why not `<=`?
>
> **TEACHER:** Beautiful catch, and it mirrors the expand. Say we need one A and the window has two. We drop one — now the window has *one* A, which still *satisfies* the requirement. We're still valid! `1 < 1` is false, so `formed` correctly stays put. Only when the count falls *below* need — from 1 down to 0 — does coverage actually break. `<` captures exactly that crossing. Using `<=` would wrongly declare us broken while we're still covered.
>
> The `while` — not an `if` — because after one expansion we might shrink several times. We squeeze until the window would go invalid.
>
> And we record *inside* the while, *before* shrinking, because that's when the window is valid and we want its length.

---

## 9. DRY-RUN THE CODE — `9:10`
*(worked example — prove it, close the loop)*

**[VISUAL: `s = "ADOBECODEBANC"`, `t = "ABC"`. A trace highlighting the key valid-then-contract moments.]**

> Let's run it. `need = {A:1, B:1, C:1}`, `required = 3`. I'll show the moments the window becomes valid and contracts.

| right | ch | event | window → contract | best so far |
|---|---|---|---|---|
| 5 | C | `formed` hits 3 at `"ADOBEC"` | contract: drop A → breaks coverage, stop | `"ADOBEC"` len 6 |
| 10 | B | valid again around `"...CODEBA"` | contract drops junk, records shorter windows | shrinking |
| 12 | C | valid at window ending `"BANC"` | contract: drop B → breaks, stop | **`"BANC"` len 4** |

> Trace the crux at `right = 5`: window is `"ADOBEC"`, all three present, `formed = 3`. We record length 6, then try to shrink — drop `A` at the left. Now the window has zero A's, `formed` drops to 2, coverage broken, the `while` exits. We expand again. Much later, at `right = 12`, the window tightens to `"BANC"` — A, B, C all present, length 4 — and dropping the `B` would break it, so 4 is the tightest here.
>
> Final answer: `"BANC"`. Exactly what we called at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `10:40`
*(transfer to interview)*

**[VISUAL: rows — Brute force: O(n²·Σ). Ours: O(|s| + |t|). Note: "each char enters once, leaves once".]**

> **TEACHER:** Say it to the interviewer: *"Brute force checks every substring for coverage — O(n²), too slow. Instead I use a dynamic window with need/have counts. I count what t requires; `required` is the number of distinct characters. I expand right, and each time a character reaches its needed count I bump `formed`. When `formed == required` the window covers t, so I contract from the left while it stays valid, recording the smallest. Every character enters once via right and leaves once via left — so despite the nested loop it's linear, O(|s| + |t|) time."*
>
> **LEARNER:** That inner `while` inside the `for` — how is that not O(n²)?
>
> **TEACHER:** Same amortized argument as the min-subarray lesson, and it's worth saying out loud: `right` advances `n` times total; `left` also advances at most `n` times total and never rewinds. Combined, at most `2n` pointer moves across the *entire* run. Each character is added once and removed at most once. Linear, guaranteed.

---

## 11. CAN WE USE LESS MEMORY? (space) — `11:35`
*(depth + honesty)*

**[VISUAL: `need` and `window` maps, capped at "≤ alphabet". A "filter s to t's letters" note.]**

> The two maps hold at most one entry per *distinct* character — so O(min(|s|, Σ)), bounded by the alphabet: ≤ 128 for ASCII, ≤ 52 for mixed-case letters. Effectively O(1) for a fixed alphabet. And you genuinely can't drop the counts — matching multiplicities *requires* remembering how many of each character you need and have.
>
> One honest optimization worth naming: if `s` is huge but `t`'s alphabet is tiny, you can **pre-filter** `s` down to just the positions whose characters appear in `t`, and slide over that shorter list. It doesn't change the Big-O, but it can be dramatically faster in practice. Mentioning it signals you think about real-world constants, not just asymptotics.

---

## 12. YOUR TURN (active recall) — `12:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Find All Anagrams in a String (LC 438)". A blank editor.]**

> Before the next video, try **Find All Anagrams in a String** — but this time force yourself to solve it with *this* need/have template, not the fixed-window trick from last lesson. It's a great test of whether you can *bend* the template: the window's max size is capped at `len(t)`, and you collect every start where it's fully formed.
>
> Even better: re-derive `min_window` from a blank editor, out loud, naming each of the four pieces — `need`, `required`, `window`, `formed`. If you can reconstruct the template cold, you own it.

---

## 13. LOCK IT IN — `12:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **"Shortest window that *covers* a target multiset" → dynamic window + need/have counts.** This is the template — memorize its four pieces.
> 2. **Expand to valid, contract to minimal.** `formed == required` is the validity gate; record on the valid side.
> 3. **The `==` on the way in and the `<` on the way out** are what make `formed` exact — bump only when a requirement is *just* met, drop only when it falls *below*.
>
> Memory peg: **pack the suitcase, then squeeze it shut.** Toss items in until the required list is complete, then remove everything you can while it stays complete.

---

## 14. CLIFFHANGER — `13:25`
*(open loop to next lesson)*

**[VISUAL: a new section title blurred in: "Hashing & Frequency Maps".]**

> Notice the quiet hero across this whole section: a hash map that answered "how many of this have I seen?" in O(1). Sliding windows *lean* on that. Next section, we put the hash map center stage — problems where the map *is* the algorithm: two-sum in one pass, grouping anagrams, spotting the first unique character. The window taught you to reuse work; hashing teaches you to *remember* it. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public String minWindow(String s, String t) {
    if (s.isEmpty() || t.isEmpty()) return "";

    int[] need = new int[128];
    int required = 0;
    for (char c : t.toCharArray()) {
        if (need[c]++ == 0) required++;   // new distinct char to satisfy
    }

    int[] window = new int[128];
    int formed = 0, left = 0;
    int bestLen = Integer.MAX_VALUE, bestLeft = 0;

    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        window[c]++;
        if (need[c] > 0 && window[c] == need[c]) formed++;

        while (formed == required) {
            if (right - left + 1 < bestLen) {
                bestLen = right - left + 1;
                bestLeft = left;
            }
            char lc = s.charAt(left);
            window[lc]--;
            if (need[lc] > 0 && window[lc] < need[lc]) formed--;
            left++;
        }
    }
    return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestLeft, bestLeft + bestLen);
}
```
