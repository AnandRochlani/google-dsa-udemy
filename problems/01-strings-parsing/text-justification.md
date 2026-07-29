# Text Justification

> **LeetCode:** 68. Text Justification · **Difficulty:** 🔴 Hard · **Pattern:** Strings / Greedy line-packing · **Google frequency:** ⭐ high

---

## Problem

Given a list of `words` and a width `maxWidth`, format the text so each line is **exactly** `maxWidth` characters and **fully justified** (padded on both sides). Pack as many words as fit on each line, greedily. Then spread the extra spaces evenly between words. If the spaces don't divide evenly across the gaps, the **leftmost** gaps take the extra spaces. The **last line** — and any line holding a **single word** — is **left-justified** with trailing spaces on the right to reach `maxWidth`. Every word is at least one character and no word is longer than `maxWidth`.

**Example:** `words = ["This","is","an","example","of","text","justification."]`, `maxWidth = 16` →

```
[
  "This    is    an",
  "example  of text",
  "justification.  "
]
```

*(Line 1: 8 letters, 8 spaces over 2 gaps → 4 and 4. Line 2: 13 letters, 3 spaces over 2 gaps → 2 and 1, leftmost gap gets the extra. Line 3 is the last line → left-justified, pad the right.)*

**Constraints that matter:** the total character count is what you traverse — call it `n`. There's no clever asymptotic win to chase here; both a naive and a careful solution are `O(n)`. The **entire difficulty is correctness under a pile of edge rules**: the uneven-spaces tiebreak, the last line, the single-word line. This is a "can you write clean, bug-free code under pressure" problem — which is exactly why Google likes it.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "Walk the words, keep adding to the current line while they fit, then when the next word won't fit, format the line and start a new one." That greedy packing instinct is *correct* — hold onto it. The trap is what happens **inside** each line.
- **Where it hurts:** the naive version tries to build the justified line in one messy pass — appending words and guessing at spaces as it goes, then patching the width at the end. That's where the bugs breed: off-by-one on the gap count, forgetting the leftmost-gaps rule, mishandling the single-word line, treating the last line like a normal one. It's not *slow*, it's *fragile*.
- **The leap:** separate the two decisions cleanly. **Decision 1 — which words go on this line?** Pure greedy packing: keep a running total and stop the moment the next word plus its minimum single spaces would overflow. **Decision 2 — how do I lay out this fixed set of words?** Now the word set is frozen, so the spacing is pure arithmetic: `total_spaces = maxWidth − sum_of_word_lengths`, divide by the number of gaps, and the remainder gets handed to the leftmost gaps one at a time.
- **Pattern trigger:** **"fixed-width lines + greedy fill + a formatting rule per line"** → **greedy line-packing**. The transferable move is *split packing from rendering*. The instant you stop trying to do both at once, the edge cases fall out as three tidy branches instead of one tangled loop.

---

## ① Brute Force

Greedily collect words, but build each justified line the messy way — append words into a buffer, sprinkle spaces as you go, then hack the width to fit at the end.

```python
def full_justify_brute(words, maxWidth):
    res = []
    line = []
    length = 0  # letters only, no spaces
    for w in words:
        # would this word (plus one space per existing word) overflow?
        if length + len(w) + len(line) > maxWidth:
            # --- messy: build the justified line right here ---
            if len(line) == 1:
                s = line[0] + " " * (maxWidth - length)
            else:
                spaces_needed = maxWidth - length
                gaps = len(line) - 1
                s = ""
                for idx, word in enumerate(line):
                    s += word
                    if idx < gaps:
                        # guess the space count for this gap... error-prone
                        q = spaces_needed // gaps
                        r = spaces_needed % gaps
                        s += " " * (q + (1 if idx < r else 0))
            res.append(s)
            line, length = [], 0
        line.append(w)
        length += len(w)
    # ...and now a *separate* copy-pasted block for the last line
    last = " ".join(line)
    last += " " * (maxWidth - len(last))
    res.append(last)
    return res
```

**Why it's the natural first attempt:** it mirrors how you'd do it by hand — read words onto a line until it's full, then space it out.

**Why it's not enough:** it *works*, but look at it. The line-formatting logic is duplicated (once inside the loop, once for the last line), the space math is recomputed inside the per-word loop, and the whole thing is one nervous edit away from an off-by-one. In an interview this is the version that compiles, passes the example, and then fails a hidden case — the single-word line, or a last line that's also full-width. The problem isn't speed; it's that this structure **invites bugs**.

**Complexity:** Time `O(n)` over total characters, Space `O(n)` for the output.

---

## ② Optimised Solution

Same greedy packing — but **separate "which words" from "how to space them."** Find the word range for a line with a clean fit check, then render that fixed range with pure arithmetic.

```python
def full_justify(words, maxWidth):
    res = []
    i, n = 0, len(words)
    while i < n:
        # ── 1. greedily pack: find the widest window [i, j) that fits ──
        j = i
        line_len = 0                     # sum of word lengths only
        while j < n and line_len + len(words[j]) + (j - i) <= maxWidth:
            line_len += len(words[j])    # (j - i) = one min-space per prior word
            j += 1

        num_words = j - i
        gaps = num_words - 1

        # ── 2. render: last line OR single word → left-justify ──
        if j == n or gaps == 0:
            line = " ".join(words[i:j])
            line += " " * (maxWidth - len(line))
        # ── otherwise fully justify: spread spaces, leftmost gaps get extra ──
        else:
            total_spaces = maxWidth - line_len
            base, extra = divmod(total_spaces, gaps)
            line = words[i]
            for k in range(1, num_words):
                spaces = base + (1 if k <= extra else 0)   # leftmost `extra` gaps get +1
                line += " " * spaces + words[i + k]

        res.append(line)
        i = j
    return res
```

**Walk the example** `["This","is","an","example","of","text","justification."]`, `maxWidth = 16`:

| Line | Fit check | Words picked | `line_len` | Branch | Result |
|---|---|---|---|---|---|
| 1 | `This`+`is`+`an`=8+2 spaces=10 ✓; +`example` → 18 ✗ | `This is an` | 8 | full: 8 spaces / 2 gaps → 4,4 | `"This    is    an"` |
| 2 | `example`+`of`+`text`=13+2 spaces=15 ✓; +`justification.` → 30 ✗ | `example of text` | 13 | full: 3 spaces / 2 gaps → 2,1 | `"example  of text"` |
| 3 | only `justification.` fits (14) | `justification.` | 14 | last line → left-justify | `"justification.  "` |

Every line lands at exactly 16 characters. ✅

**Why it's correct:** the fit test `line_len + len(words[j]) + (j - i) <= maxWidth` counts the letters plus *exactly one* space between every pair already chosen — the minimum a line needs — so we never pack a set that can't physically fit. Once the window `[i, j)` is frozen, `total_spaces = maxWidth − line_len` is exact, and `divmod` splits it so `extra` leftmost gaps get `base + 1` and the rest get `base`. That sums back to `total_spaces` precisely, so the line is always exactly `maxWidth` wide. The `k <= extra` check is what steers the remainder to the **leftmost** gaps (gaps are numbered 1…gaps as `k` runs 1…num_words−1).

**Complexity:** Time `O(n)`, Space `O(n)`.

---

## ③ Space Optimization

**Already optimal — and here's the honest version of why.** The output *is* every character of every line: `n` letters plus the padding spaces needed to reach `maxWidth` per line. You are required to **return** that fully-built text, so materializing `O(total output)` characters isn't a wasteful choice — it's the deliverable. There's no rolling-variable trick that makes the answer smaller, because the answer is the big string list itself.

```python
# No space-optimised variant exists: the O(n) output IS the required result.
# We only hold one line's characters at a time before appending — the extra
# working memory beyond the output is O(maxWidth), i.e. O(1) relative to n.
```

**Complexity:** Time `O(n)`, Space `O(n)` (output-bound; `O(1)` auxiliary beyond the output).

> Say it out loud: *"Space is O(n), but that's the output I'm asked to produce, not overhead — I only keep one line in a buffer at a time, so my extra working memory is O(1)."* Naming *why* you can't do better is the strong-hire move. Don't pretend there's a trick when the problem definition sets the floor.

---

## Java (for Java interviewers)

```java
public List<String> fullJustify(String[] words, int maxWidth) {
    List<String> res = new ArrayList<>();
    int i = 0, n = words.length;
    while (i < n) {
        // 1. greedily pack the widest window [i, j) that fits
        int j = i, lineLen = 0;
        while (j < n && lineLen + words[j].length() + (j - i) <= maxWidth) {
            lineLen += words[j].length();
            j++;
        }
        int numWords = j - i, gaps = numWords - 1;
        StringBuilder sb = new StringBuilder();

        // 2. last line OR single word → left-justify
        if (j == n || gaps == 0) {
            for (int k = i; k < j; k++) {
                if (k > i) sb.append(' ');
                sb.append(words[k]);
            }
            while (sb.length() < maxWidth) sb.append(' ');
        // otherwise fully justify; leftmost `extra` gaps get one more space
        } else {
            int totalSpaces = maxWidth - lineLen;
            int base = totalSpaces / gaps, extra = totalSpaces % gaps;
            sb.append(words[i]);
            for (int k = 1; k < numWords; k++) {
                int spaces = base + (k <= extra ? 1 : 0);
                for (int s = 0; s < spaces; s++) sb.append(' ');
                sb.append(words[i + k]);
            }
        }
        res.add(sb.toString());
        i = j;
    }
    return res;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (messy inline build) | O(n) | O(n) |
| Optimised (pack, then render) | O(n) | O(n) |
| Space-optimised | — (none exists) | O(n) output-bound, O(1) auxiliary |

*(n = total characters across all words + the padding required to fill each line.)*

---

## Say it out loud (interview narration)

> *"This isn't a speed problem — it's a correctness-under-edge-cases problem, so my plan is to keep the code boringly clean. Two separate jobs. First, greedy packing: I walk words onto a line while the letters plus one minimum space each still fit. Second, once that word set is frozen, rendering is just arithmetic — total spaces divided by the number of gaps, and the remainder goes to the leftmost gaps. Two special cases get their own branch: the last line and any single-word line are left-justified with trailing spaces. Time is O(n) over the characters, space is O(n) — but that space is the output I'm required to return, not overhead; my working memory per line is O(1)."*

Before you write a line, ask the interviewer the one clarifying question that proves you read the spec: *"When the spaces don't divide evenly, the extra ones go to the leftmost gaps, right?"* That's the detail people miss, and asking it early is exactly what Google's rubric rewards.

## Related / follow-ups
- **Text Justification with a single space cap** — the common "one space between words, no full-justify" variant (word-wrap).
- **String to Integer (atoi)** — same DNA: no algorithmic trick, pure careful edge-case handling under an interviewer's eye.
- **Reorganize String / Rearrange spaces between words (LC 1592)** — more even-space-distribution arithmetic.
- **Valid Number** — another "spec is the whole difficulty" Google-signature string problem.
