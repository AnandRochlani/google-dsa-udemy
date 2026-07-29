# 🎬 Recording Script — Longest Substring Without Repeating Characters
**Pattern: Sliding Window (dynamic) · LeetCode 3 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the grow-then-shrink dynamic window from Minimum Size Subarray Sum (LC 209). This time we shrink on a *rule violation*, not a numeric threshold — and a hash map joins in.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. Two nested loops with a `set()` rebuilt inside. A red "Time Limit Exceeded" banner.]**

> This one shows up in Google interviews constantly: *"Longest stretch of a string with no repeated character."*
>
> You reach for the obvious thing — from every start, extend until a letter repeats, remember the length. Correct. And on a long string, painfully slow, because every restart re-checks characters you *just* verified.
>
> By the end of this video you'll do it in one pass with a trick that lets the left edge *teleport* — no crawling — using a map that remembers where it last saw each character. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, the string as tiles: `a b c a b c b b`, indices 0–7.]**

> The whole problem in one line: **find the length of the longest substring with all distinct characters.** Substring means contiguous — a solid run, not cherry-picked letters.
>
> Our tiny example: `"abcabcbb"`. The answer is 3 — `"abc"` — because the moment you'd extend to a fourth character you hit a repeat. Hold that: **3**.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the tiles. A start-marker, a `seen` set box, a "checks" counter top-right.]**

> Brute force: from each start, extend right while every character stays unique.
>
> Start at index 0. `a` — new. `b` — new. `c` — new. `"abc"`, length 3. Next is `a` at index 3 — already in the set. Stop.
>
> **[VISUAL: marker jumps to index 1; the `seen` set empties and rebuilds.]**
>
> Start at index 1. `b` — new. `c` — new. `a` — new. `"bca"`, length 3. Next is `b` — repeat. Stop.
>
> **[VISUAL: highlight `b, c` — glowing: they were JUST verified unique in the previous pass.]**
>
> Freeze. I just re-checked `b` and `c` — I confirmed those were unique *one pass ago*. Every restart empties the set and re-walks characters it already cleared. Six restarts, mountains of repeated checks. On tens of thousands of characters that's `O(n²)` and it drags.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The re-checked `b,c` pulsing across two passes. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste, named: every new start wipes the `seen` set and re-verifies characters we already knew were unique.
>
> **LEARNER:** But when a duplicate `a` shows up at index 3, the *only* fix is to move past the old `a`, right? So I have to restart somewhere after it. What's left to reuse?
>
> **TEACHER:** Almost — but you don't restart from *scratch*, you restart from *just past the old `a`*, and you keep everything after it. So pause and think: instead of a `left` pointer that crawls forward one step at a time, **what if a duplicate could tell `left` exactly where to jump — in a single move?** What would you need to remember to make that jump?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:00`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a single window `[left, right]` over the tiles, and a small map box: `char → last index`.]**

> Here's the leap. Keep **one** window `[left, right]` that is *always* duplicate-free. And keep a **map**: for each character, the last index where we saw it.
>
> Now walk `right` forward one character at a time:
> - If the new character isn't in the window — great, extend, and update the best length.
> - If it *is* a duplicate that's inside the window — **jump `left`** to just past where that character last appeared. In one move, the duplicate is evicted and the window is clean again.
>
> **[VISUAL: right lands on the second `a` at index 3; an arrow snaps `left` from 0 to 1, skipping over the old `a`.]**
>
> That jump is the upgrade over last lesson. In Minimum Size Subarray Sum, `left` crept forward one step per shrink. Here, the map lets `left` *teleport* straight past the collision.
>
> Think of it like reading a sentence with your finger, and a rule: no letter twice. The instant you hit a repeat, you don't back up letter by letter — you slide your finger to *right after* the earlier copy and keep going. The map is your memory of where that earlier copy sat.

---

## 6. THE KEY MOVE (signaling) — `4:20`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "On a duplicate inside the window, jump left to (last index of that char) + 1."]**

> Burn this in: **remember each character's last position; on a repeat inside the window, jump `left` to one past it.**
>
> Grow by default. Only the duplicate forces a jump. That's the whole engine.

---

## 7. CODE IT — LIVE & CHUNKED — `4:55`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. The map of last-seen indices, plus `left` and `best`.

```python
def length_of_longest(s):
    last_seen = {}          # char -> most recent index
    left = 0
    best = 0
```

> **[VISUAL: add chunk 2, highlight it.]** Walk `right` across the string, pulling out both index and character.

```python
    for right, ch in enumerate(s):
```

> **[VISUAL: add chunk 3 — the jump.]** If this character was seen *and* its last spot is inside our window, teleport `left` past it.

```python
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
```

> **[VISUAL: add chunk 4.]** Record this character's position, then update the best length.

```python
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:10`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as named.]**

> Let's walk *why*.
>
> `last_seen[ch] >= left` — this guard is the crux, and it's the part people get wrong. It has *two* conditions folded together: the character was seen before (`ch in last_seen`), **and** that sighting is still *inside* the current window (`>= left`).
>
> **LEARNER:** Why the `>= left` part? If I've seen the character at all, isn't it a duplicate? Why check where it was?
>
> **TEACHER:** Because a character seen *before* `left` is already *outside* the window — it's not in our current substring, so it's not a real duplicate for us. Imagine `"abba"`: when the final `a` arrives, the earlier `a` sat at index 0, but `left` has already moved past it to index 2. That old `a` is gone from the window. If we blindly jumped, we'd shove `left` *backwards* — corrupting everything. The `>= left` check says "only jump if the collision is actually inside the room."
>
> `left = last_seen[ch] + 1` — jump to just *past* the old copy, evicting it and only it.
>
> `last_seen[ch] = right` — update *after* the jump check, so the character now points at its newest position.
>
> `right - left + 1` — current window length, both ends inclusive.

---

## 9. DRY-RUN THE CODE — `7:25`
*(worked example — prove it, close the loop)*

**[VISUAL: `"abcabcbb"` with a trace table filling row by row.]**

> Let's run the code on `"abcabcbb"`.

| right (ch) | seen inside window? | left after | window | best |
|---|---|---|---|---|
| 0 (a) | no | 0 | `a` | 1 |
| 1 (b) | no | 0 | `ab` | 2 |
| 2 (c) | no | 0 | `abc` | 3 |
| 3 (a) | yes, idx 0 ≥ 0 → jump | 1 | `bca` | 3 |
| 4 (b) | yes, idx 1 ≥ 1 → jump | 2 | `cab` | 3 |
| 5 (c) | yes, idx 2 ≥ 2 → jump | 3 | `abc` | 3 |
| 6 (b) | yes, idx 4 ≥ 3 → jump | 5 | `cb` | 3 |
| 7 (b) | yes, idx 6 ≥ 5 → jump | 7 | `b` | 3 |

> Answer: 3. Exactly the `"abc"` we called at the start. And notice `left` never once moved backward — the `>= left` guard held the line every time. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:30`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n²). Ours: O(n).]**

> **TEACHER:** Say it to the interviewer: *"Brute force restarts a `seen` set from every index and re-verifies characters it already cleared — O(n²). Instead I keep one duplicate-free window plus a map of each character's last index. When a duplicate lands inside the window, I jump `left` one past the previous copy — one move, no crawling. Each character is processed once, so O(n) time."*
>
> That word — *jump* — is what signals you've gone past the textbook version. Cheaper than the crawl, and it's the detail interviewers listen for.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:05`
*(depth + honesty)*

**[VISUAL: the map, capped at "≤ alphabet size". A fixed `int[128]` array shown as the swap.]**

> The map holds at most one entry per *distinct* character — so space is O(min(n, Σ)), bounded by the alphabet, not the string. Lowercase English? ≤ 26 entries. ASCII? ≤ 128. For a fixed alphabet that's effectively O(1).
>
> A tighter variant: swap the hash map for a **fixed array** indexed by character code — `int[128]`, initialized to −1, storing last-seen index. Same asymptotic space, smaller constant, faster lookups. And be honest about the floor: you *can't* go below O(Σ) — you fundamentally must remember where each in-window character last appeared. Naming that limit is the strong-hire move.

---

## 12. YOUR TURN (active recall) — `9:40`
*(retrieval practice)*

**[VISUAL: "Your turn → Longest Substring with At Most K Distinct Characters (LC 340)". A blank editor.]**

> Before the next video, try **Longest Substring with At Most K Distinct Characters**. Same dynamic window, but the shrink rule changes: instead of "no duplicates," it's "at most `k` different characters." You'll track a count of distinct chars and shrink when it exceeds `k`.
>
> Build the grow / jump-or-shrink skeleton from memory first. The struggle is the point.

---

## 13. LOCK IT IN — `10:15`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **"Longest substring where a rule holds" → dynamic window + a hash structure** that describes the window's contents.
> 2. **Grow by default; shrink only on violation.** Here the violation is a repeated character.
> 3. **The `>= left` guard is non-negotiable** — it stops `left` from ever moving backward when the duplicate is already outside the window.
>
> Memory peg: **finger reading, no letter twice** — hit a repeat, and your finger jumps to just after the earlier copy instead of backing up.

---

## 14. CLIFFHANGER — `10:45`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Longest Repeating Character Replacement".]**

> Here a single repeat *killed* the window. But what if repeats were the *goal* — and you had a budget to change a few characters to force a longer run of one letter? Now "valid" isn't "no duplicates," it's "the number of misfits I'd have to replace fits my budget." Same window, a counter of the most frequent letter, and one surprisingly subtle trick about a stale maximum. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int lengthOfLongestSubstring(String s) {
    int[] lastSeen = new int[128];      // ASCII; last index of each char
    java.util.Arrays.fill(lastSeen, -1);
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        char ch = s.charAt(right);
        if (lastSeen[ch] >= left) {
            left = lastSeen[ch] + 1;    // jump past the previous copy
        }
        lastSeen[ch] = right;
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```
