# 🎬 Recording Script — Text Justification
**Pattern: Strings / Greedy · LeetCode 68 · Hard · Target length ~14 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** none needed — but we lean hard on the idea of *splitting one messy job into two clean ones*.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a clean code editor. A block of text is being typed and then snaps into a perfectly aligned newspaper column — both edges flush. Then a red "Wrong Answer — expected 16, got 17" banner slides in.]**

> This one shows up in real Google onsites, and it's marked **Hard** — but not for the reason you think.
>
> There's no fancy algorithm here. No dynamic programming, no graph. You could explain the idea to your grandma in one sentence: *fill each line with words, then spread the spaces so both edges line up.*
>
> And yet people **fail** it. They pass the example, hit submit, and get "Wrong Answer" — off by one space, on one line, out of forty. By the end of this video you'll know the one structural trick that turns this from a bug-hunt into fifteen clean lines. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, seven word-tiles: `This  is  an  example  of  text  justification.` and a ruler marked `maxWidth = 16`.]**

> The whole problem in one line: **pack words onto lines of a fixed width, and pad each line with spaces so both the left and right edges are flush.** Like a newspaper column.
>
> Here's our tiny example — seven words, and every line has to come out to **exactly 16 characters**. Not 15. Not 17. Sixteen.
>
> Hold onto this exact set. We'll build the answer by hand first, then in code.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the trap)*

**[VISUAL: the ruler at 16. Words drop onto line 1 one at a time; a running counter shows letters + spaces.]**

> Let's do what your brain does first. Fill line one greedily — keep adding words while they fit.
>
> `This` — 4. `is` — that's 4, a space, 2, so 7. `an` — 7, a space, 2, that's 10. Try `example` — that'd need 10, a space, then 7 more. Eighteen. Too big. Stop. Line one is **This, is, an.**
>
> **[VISUAL: line 1 shows `This is an` with a bracket: "8 letters, only 2 real gaps, need to hit 16".]**
>
> Now the hard part. I've got 8 letters and I need 16 characters. That's **8 spaces to sprinkle** — but only into **2 gaps** between three words. 8 divided by 2 is 4. So four spaces in each gap. `This····is····an`. Sixteen. 
>
> **[VISUAL: line 2 fills: `example of text` — bracket: "13 letters, 2 gaps, 3 spaces to spread".]**
>
> Line two: `example`, `of`, `text` — 13 letters. Sixteen minus 13 is **3 spaces**, but again only **2 gaps**. And 3 doesn't split evenly into 2…

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(the tiebreak — first pause + generation effect)*

**[VISUAL: freeze on line 2. Two gaps blinking. "3 spaces → 2 gaps → ???". A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the moment people trip. Three spaces, two gaps. One gap gets 2, one gets 1 — fine. But **which** gap gets the extra one? The left gap, or the right?
>
> **LEARNER:** Does it even matter? It's one space. It looks basically the same either way.
>
> **TEACHER:** It matters *completely* — the judge checks it character for character. And here's the thing I want you to feel: this is a **rule you cannot derive.** You have to be *told* it. So in a real interview, this is the exact question you ask out loud before writing a single line.
>
> Pause the video. Predict: when spaces don't split evenly, do the extra ones go **left** or **right**?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:15`
*(the real unlock — split one job into two)*

**[VISUAL: the spec line highlights: "...leftmost slots get the extra space." Line 2 renders `example··of·text`.]**

> **TEACHER:** The rule is: **leftmost gaps win.** Extra spaces pile onto the left. So line two is `example`, **two** spaces, `of`, **one** space, `text`. And that's the kind of thing you'd only know by asking — which is why asking it scores you points.
>
> But that's not the real lesson. The real reason people fail this problem isn't the rule — it's *structure.* Watch what most people do: they try to pick words **and** space them out in the same tangled loop. Words go in, spaces get guessed, widths get patched at the end. Bug city.
>
> **[VISUAL: a messy loop with tangled arrows, crossed out. Then two clean boxes appear: "① WHICH words?" and "② HOW to space them?"]**
>
> **LEARNER:** So what do you do instead?
>
> **TEACHER:** You split it into **two separate jobs.** Job one: *which words go on this line?* That's pure greedy packing — nothing else. Job two: *given this frozen set of words, how do I lay out the spaces?* That's pure arithmetic — total spaces, divided by gaps, remainder to the left.
>
> The moment you stop doing both at once, every bug in this problem just… evaporates. Two small jobs, each easy. That's the whole trick.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Pack the words, THEN render the line. Two jobs, never one."]**

> Burn this in: **pack first, render second. Never both at once.**
>
> And the spacing formula, one line: **spaces ÷ gaps for everyone, remainder to the leftmost gaps.** That's `divmod` — quotient to all, remainder to the left. Say those two sentences and you've basically written the solution.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. Outer loop — one pass per line. `i` marks where the current line's words start.

```python
def full_justify(words, maxWidth):
    res = []
    i, n = 0, len(words)
    while i < n:
```

> **[VISUAL: add chunk 2, highlight it.]** Job one — greedy packing. Slide `j` forward while the words still fit. That `(j - i)` is the minimum one-space-per-word we owe.

```python
        j = i
        line_len = 0                     # letters only, no spaces yet
        while j < n and line_len + len(words[j]) + (j - i) <= maxWidth:
            line_len += len(words[j])
            j += 1
        num_words = j - i
        gaps = num_words - 1
```

> **[VISUAL: add chunk 3.]** Job two, first branch — the two special cases. Last line, or a single word? **Left-justify.** Just join with single spaces and pad the right.

```python
        if j == n or gaps == 0:
            line = " ".join(words[i:j])
            line += " " * (maxWidth - len(line))
```

> **[VISUAL: add chunk 4, highlight the divmod line.]** Otherwise — full justify. Here's the arithmetic. `divmod` gives `base` to every gap and `extra` left over for the leftmost gaps.

```python
        else:
            total_spaces = maxWidth - line_len
            base, extra = divmod(total_spaces, gaps)
            line = words[i]
            for k in range(1, num_words):
                spaces = base + (1 if k <= extra else 0)   # leftmost gaps get +1
                line += " " * spaces + words[i + k]
        res.append(line)
        i = j
    return res
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> The fit test — `line_len + len(words[j]) + (j - i)`. `line_len` is just the letters. `(j - i)` is how many words we've already committed, which is exactly how many **minimum** single spaces we need between them. Add the next word's length, and if it's still ≤ 16, it fits. That one line *is* job one.
>
> **LEARNER:** Wait — why `k <= extra` and not `k < extra`? That looks like a place to get an off-by-one.
>
> **TEACHER:** Great catch, that's the exact line people fumble. The gaps are numbered `k` from 1 up to `num_words − 1`. I want the **first** `extra` of them to get a bonus space. Gap 1, gap 2, up to gap `extra`. So the condition is `k <= extra` — inclusive, because gap number `extra` should still get the bonus. Use `<` and your leftmost gap silently loses a space. That's a "Wrong Answer" on test 30-something.
>
> And the `divmod` — this is why we split the jobs. Because the word set is already frozen, `total_spaces` is an *exact* number. There's no guessing mid-loop. Quotient to all gaps, remainder to the left. Clean.
>
> The `if j == n or gaps == 0` branch — that's the last line and the single-word line, sharing one behavior: left-justify, pad the right. Two edge cases, one branch. No duplicated code.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: the seven words with a trace table filling row by row; each output line snapped against the 16-char ruler.]**

> Let's run the real code on our seven words and watch it land.

| i | packs → j | line_len | branch | output (·= space) |
|---|---|---|---|---|
| 0 | `This is an` (+`example`=18 ✗) | 8 | full: 8÷2 → 4,4 | `This····is····an` |
| 3 | `example of text` (+`justif…`=30 ✗) | 13 | full: 3÷2 → **2,1** (left) | `example··of·text` |
| 6 | `justification.` (j hits n) | 14 | **last line** → left-justify | `justification.··` |

> Three lines. Every one lands at exactly 16 characters. Line two put the extra space on the **left** gap — just like the rule said. And the last line got left-justified with two trailing spaces. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: one row — Time: O(n). Space: O(n). A note: "n = total characters".]**

> **TEACHER:** Say it the way you'd say it in the room: *"There's no algorithmic trick to chase — I touch each character a constant number of times, so it's O(n) time over the total characters. Space is O(n), but that's the output I'm required to return."*
>
> Notice what's different about this problem. On most Hards, the interviewer wants to see you find the clever speedup. Here? There isn't one. **The signal they're grading is whether your code is clean and correct under a pile of edge rules.** That's a different skill, and Google tests it on purpose.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: the output list of strings, highlighted. A crossed-out "🧠 clever trick?" with "N/A".]**

> Quick and honest. Can we shrink the space? **No — and knowing why is the point.**
>
> The output *is* every character of every line. You're asked to **return** that whole justified block, so building `O(n)` of it isn't waste, it's the deliverable. Beyond that, I only ever hold **one line** in a buffer before I append it — so my extra working memory is O(1).
>
> Say that out loud in the interview: *"Space is O(n), but that's the required output, not overhead — my auxiliary memory is O(1), just one line at a time."* Naming *why* you can't do better — instead of inventing a fake optimization — is a strong-hire move.

---

## 12. YOUR TURN (active recall) — `10:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Rearrange Spaces Between Words (LC 1592)". A blank editor.]**

> Before the next video, try **Rearrange Spaces Between Words**, LeetCode 1592. Same DNA: count your total spaces, divide evenly between words, and — you guessed it — figure out where the leftovers go.
>
> Don't peek. Struggle for ten minutes. That struggle is what turns "I watched a video" into "I can write this cold in an interview."

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Split the job in two** — pick the words, *then* space them. Never both at once.
> 2. **`divmod` is the whole spacing rule** — quotient to every gap, remainder to the **leftmost** gaps.
> 3. **Two edge cases share one branch** — last line and single-word line both just left-justify.
>
> And the memory peg — when a string problem has *no algorithm but a mountain of rules*, don't be clever. Be **boringly clean**: **pack, then render.** That phrase is the whole solution.

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "String to Integer (atoi)".]**

> Here's a thing worth saying: Google doesn't just grade whether your code *works* — they grade **how you think out loud** while you build it. They literally have a rubric line for it: *General Cognitive Ability.* And the single move that scored me points on this exact problem? Asking, before I wrote anything: *"When the spaces don't divide evenly — extra ones go left, right?"* That one clarifying question told the interviewer I'd actually read the spec. Do that.
>
> Next up, another problem with zero algorithm and a *swamp* of rules — `atoi`, turning a messy string into a number. Leading spaces, signs, overflow, junk characters. Same lesson, nastier edge cases. Same fix: stay boringly clean. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public List<String> fullJustify(String[] words, int maxWidth) {
    List<String> res = new ArrayList<>();
    int i = 0, n = words.length;
    while (i < n) {
        // job 1: greedily pack the widest window [i, j) that fits
        int j = i, lineLen = 0;
        while (j < n && lineLen + words[j].length() + (j - i) <= maxWidth) {
            lineLen += words[j].length();
            j++;
        }
        int numWords = j - i, gaps = numWords - 1;
        StringBuilder sb = new StringBuilder();

        // job 2a: last line OR single word → left-justify
        if (j == n || gaps == 0) {
            for (int k = i; k < j; k++) {
                if (k > i) sb.append(' ');
                sb.append(words[k]);
            }
            while (sb.length() < maxWidth) sb.append(' ');
        // job 2b: fully justify; leftmost `extra` gaps get one more space
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
