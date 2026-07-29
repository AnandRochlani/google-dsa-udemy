# 🎬 Recording Script — Find And Replace in String
**Pattern: Strings / Simulation · LeetCode 833 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A tidy `for` loop calls `s.replace(...)` once per operation. Below, two test cases: the first shows a green ✓, the second shows a red ✗ with expected `"eeecd"` vs got `"eecd?"` garbled.]**

> You get a string, and a list of "replace this with that at position `k`" jobs. Easy, right? You write the obvious loop — for each job, do the replacement. First test passes. You feel good.
>
> Then the second test comes back **wrong** — and not a little wrong, *scrambled* wrong. Characters landing in the wrong place.
>
> Here's the twist: your logic is fine. What betrayed you is one word in the problem you skimmed past. By the end of this video you'll know the word, why it wrecks the naive loop, and the one reorder-and-sweep trick that makes the whole thing bulletproof. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, the string `"abcd"` as four tiles indexed 0,1,2,3, and two operation cards.]**

```
s = "a b c d"
       0 1 2 3

op @ 0:  if s here starts with "a"  → replace with "eee"
op @ 2:  if s here starts with "cd" → replace with "ffff"
```

> The whole problem in one line: **at each given position, if the string starts with this source, swap that piece for the target.**
>
> Tiny example — four letters, two jobs. Job one at index 0: does `"abcd"` start with `"a"`? Yes — become `"eee"`. Job two at index 2: does `"cd"` start with `"cd"`? Yes — become `"ffff"`.
>
> Hold the answer in your head: `eee`, then the leftover `b`, then `ffff` → **`"eeebffff"`**. We'll earn it, not guess it.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste... and the bug)*

**[VISUAL: `"abcd"`. Apply op @ 0 in place. The string visibly grows: `"eeebcd"`. Then a red pointer drops onto index 2 of the NEW string.]**

> Let's do what your brain does first: take the string, apply job one right on it, then apply job two.
>
> Job one at index 0: `"abcd"` → replace `"a"` with `"eee"` → now the string is **`"eeebcd"`**. Six characters.
>
> **[VISUAL: index 2 of `"eeebcd"` highlights the second `e`.]**
>
> Now job two says "at index **2**." But look where index 2 *is* now — it's sitting on an `e`, deep inside the word we just inserted. The `"cd"` we were supposed to find has slid down to index 4. We check index 2, see `"eb"`, no match — and silently do nothing. Answer comes out `"eeebcd"`. **Wrong.**
>
> **[VISUAL: the wrong answer `"eeebcd"` flashes red next to the correct `"eeebffff"`.]**

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Spotlight the word "**original**" glowing in the problem statement. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** There's the word from the cold open. The indices point into the **original** string — the one you were handed — and all the jobs happen *simultaneously*. Job two's "index 2" always meant the `c` in the *original* `"abcd"`. But the moment we mutated the string for job one, we moved the ground under job two's feet.
>
> **LEARNER:** Wait — so if I just process them in reverse, back-to-front, the earlier edits don't shift the later ones. Doesn't that fix it?
>
> **TEACHER:** Sharp — and reverse order *does* dodge the shift. But you're still rebuilding the whole string on every edit, and you're still doing index arithmetic in your head. Hold that instinct though, because it's a clue. Pause the video: **what if we never mutated the string at all — what would we read from, and what would we build?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it from the dry-run)*

**[VISUAL: the original `"abcd"` stays FIXED and untouched at the top. Below it, an empty "result" tray. A single cursor `i` sits under index 0 of the original.]**

> **TEACHER:** Here's the move. The original string is **read-only** — we treat it like a printed page we're never allowed to write on. We build the answer in a *separate* tray, left to right.
>
> Think of it like copying a document while making tracked edits: you don't scribble on the original, you retype it into a new doc, and when you hit a spot marked "replace," you type the new text instead. One finger — the cursor — slides across the original once.
>
> **[VISUAL: sort the two op cards by index — they're already 0 then 2. A label appears: "sorted by index → sweep left to right."]**
>
> First, sort the jobs by their position, so we meet them in the order the cursor reaches them. Now sweep:
>
> **[VISUAL: cursor at 0. Op @ 0 fires. Copy nothing before it, drop `"eee"` into the tray, cursor jumps to index 1.]**
>
> Cursor's at 0, job one's at 0 — nothing to copy first. Does the *original* `"abcd"` start with `"a"` at index 0? Yes. Drop `"eee"` in the tray. Then **skip past the source** — `"a"` is one character — so the cursor jumps to index 1.
>
> **[VISUAL: cursor at 1. Op @ 2 next. Copy `s[1:2]="b"` into the tray, then drop `"ffff"`, cursor jumps to 4.]**
>
> Next job's at index 2, cursor's at 1 — so copy the untouched gap `"b"` into the tray. Check the *original* at index 2: starts with `"cd"`? Yes. Drop `"ffff"`. Skip the two source chars, cursor lands at 4 — the end.
>
> Tray reads `eee` · `b` · `ffff`. **`"eeebffff"`.** No mutation, no shifting, no offset math — because we only ever *read* the frozen original and only ever *append* to the tray.
>
> **LEARNER:** But the problem lists the jobs in some given order. If I sort them, am I not changing which replacement wins when two collide?
>
> **TEACHER:** Beautiful worry — and the spec already answered it. The operations are **guaranteed not to overlap**. No two ever touch the same characters. So sorting them by position can't change any outcome; it just lets one cursor visit them in reading order. The guarantee is what makes the sweep legal.

---

## 6. THE KEY MOVE (signaling) — `4:50`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Don't mutate — sort by index, sweep the original once: copy the gap, splice or skip."]**

> Burn this in: **when edits reference fixed positions in an original string, don't edit in place — sort by position and rebuild in one left-to-right pass.**
>
> Copy the untouched gap, test the match against the *original*, splice in the target and skip the source — or move on. That's the entire trick.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, zip the three arrays into triples and sort by index — that's the left-to-right order.

```python
def findReplaceString(s, indices, sources, targets):
    ops = sorted(zip(indices, sources, targets))   # (index, source, target), by index
    res = []
    i = 0                                           # cursor into the ORIGINAL s
```

> **[VISUAL: add chunk 2, highlight it.]** Now the sweep. For each job: copy the untouched gap from the cursor up to this job's index.

```python
    for idx, src, tgt in ops:
        res.append(s[i:idx])                        # untouched gap before this op
```

> **[VISUAL: add chunk 3 — the match test, highlight the `s[idx:...]` slice.]** Test the match — and notice we test the **original** `s`, always.

```python
        if s[idx:idx + len(src)] == src:            # does the ORIGINAL match here?
            res.append(tgt)                         # yes → write the replacement
            i = idx + len(src)                      # skip past the matched source
        else:
            i = idx                                 # no → leave chars for the next copy
```

> **[VISUAL: add chunk 4, highlight the tail line.]** After the loop, copy whatever's left of the original, and join.

```python
    res.append(s[i:])                               # the tail after the last op
    return "".join(res)
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:00`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `sorted(zip(...))` — tuples sort by their first element, which is the index. That's what guarantees the cursor meets jobs in reading order. Skip this sort and a job to the left of the cursor would force us to copy a *negative* gap — chaos.
>
> `res.append(s[i:idx])` — this copies everything between where we stopped and where this job starts, straight from the original. It's how untouched characters — the `"b"` — survive.
>
> `s[idx:idx + len(src)] == src` — the heart. We slice the **original** at the job's own index and compare. Not the result, not a mutated copy — the original. That's the "simultaneous" rule made literal: earlier replacements live only in `res`, so they can never poison this test.
>
> **LEARNER:** In the `else` branch you set `i = idx`, not `i = idx + 1`. If it didn't match, why don't we skip the character?
>
> **TEACHER:** Because on a *miss*, nothing gets replaced — those original characters must survive untouched. Setting `i = idx` means the next `s[i:idx]` copy, or the final tail, will scoop them up verbatim. If we jumped past them we'd delete characters the problem told us to keep. On a *match*, though, we set `i = idx + len(src)` — we skip the source precisely because the target replaced it.
>
> `res.append(s[i:])` — the tail. Easy to forget, and if you do, you silently drop the end of the string. The last job rarely reaches the final character.

---

## 9. DRY-RUN THE CODE — `8:10`
*(worked example — prove it, close the loop)*

**[VISUAL: original `"abcd"` fixed on top; a trace table filling row by row; the `res` tray growing.]**

```
s = "abcd"   indices=[0,2]  sources=["a","cd"]  targets=["eee","ffff"]
ops sorted = (0,"a","eee"), (2,"cd","ffff")
```

| Op | `s[i:idx]` copied | match test | emit | new `i` | `res` |
|---|---|---|---|---|---|
| (0,"a","eee") | `s[0:0]`=`""` | `s[0:1]`=`"a"` == `"a"` ✓ | `"eee"` | `1` | `["", "eee"]` |
| (2,"cd","ffff") | `s[1:2]`=`"b"` | `s[2:4]`=`"cd"` == `"cd"` ✓ | `"ffff"` | `4` | `[…, "b", "ffff"]` |
| tail | `s[4:]`=`""` | — | — | — | `[…, ""]` |

> Join it: `"" + "eee" + "b" + "ffff" + ""` = **`"eeebffff"`**. Exactly the answer we promised at second thirty-five. Loop closed.
>
> **[VISUAL: quick second trace — swap op two's source to `"ec"`. Row shows `s[2:4]="cd" != "ec"` → red ✗, emit nothing, `i=2`, tail copies `"cd"`.]**
>
> And the miss case: if that second source were `"ec"`, the test fails, we emit nothing, `i` stays at 2, and the tail copies `"cd"` straight through. A failed match costs nothing — the cursor just doesn't move, and the original flows on.

---

## 10. COMPLEXITY, OUT LOUD — `9:10`
*(transfer to interview)*

**[VISUAL: two rows — Brute (mutate + offset): O(m·n). Ours: O(n + m log m). Note: "one sweep of s, m jobs sorted".]**

> **TEACHER:** Say it the way you'd say it in the room: *"The naive mutate-in-place is O(m·n) — every replacement rebuilds the whole string. My version sorts the m operations, O(m log m), then makes a single linear sweep of the string, reading each character once — O(n). So O(n + m log m) time. Space is O(n) for the output string I have to return."*
>
> With m tiny — around a hundred jobs — that sort is basically free, and you're really just paying for one pass over `s`.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:45`
*(depth + honesty)*

**[VISUAL: the `res` tray; a "rewrite s in place?" thought bubble appears, then gets a red ✗ next to "strings are immutable".]**

> Quick, and honesty scores points here.
>
> Can we do it without the O(n) buffer — edit `s` in place? **No, and I can say exactly why.** Strings are immutable in Python and Java; you *can't* rewrite them in place. And even if you could, the result has a different length than the input, so you need a fresh string anyway.
>
> Say it out loud: *"Space is O(n), but that's the output I'm required to return, not overhead. Beyond it I only keep the sorted operations — O(m), and m is small. There's no in-place trick because strings are immutable — this is the floor."* Naming *why* it can't shrink is the strong-hire move.

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Merge Intervals (LC 56)". A blank editor.]**

> Before the next video, try **Merge Intervals**. Feels unrelated? It's the *same skeleton*: sort by position, then one left-to-right sweep with a cursor deciding "extend or start fresh." If you can see 833 and 56 as the same move, you've got the pattern, not just the problem.
>
> Wrestle with it for ten minutes before you peek. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **The indices point into the *original* string, applied simultaneously.** Mutating in place shifts later jobs — that's the whole trap.
> 2. **Don't mutate — sort by index and rebuild** in one sweep: copy the gap, splice or skip.
> 3. **Always test the match against the original `s`**, and don't forget the tail copy at the end.
>
> The memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "Fixed positions? Freeze the original, sort by index, sweep once."]**
>
> When edits are keyed to fixed positions in a string, your hand should already be reaching to sort by index and rebuild — never to edit in place.
>
> *(GCA reminder — for the interview itself: ask the clarifying question first — "these indices are all into the original string, and the ops happen simultaneously, right?" Then narrate the naive mutate-and-shift, name why it breaks, and reach for the sort-and-sweep. Google's General Cognitive Ability signal isn't the final code — it's you catching the "original string" trap out loud before you write a line.)*

---

## 14. CLIFFHANGER — `11:15`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Merge Intervals" — two overlapping bars merging into one, drawn in red.]**

> We leaned hard on one gift from the problem: the operations **never overlap**. One cursor, no conflicts. But what happens when the pieces *do* overlap — when two of them collide and you have to *fuse* them into one? That's the next problem: Merge Intervals. Same sort-and-sweep spine, but now overlap is the entire game. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public String findReplaceString(String s, int[] indices, String[] sources, String[] targets) {
    int m = indices.length;

    // sort operation slots by their index into s
    Integer[] order = new Integer[m];
    for (int k = 0; k < m; k++) order[k] = k;
    Arrays.sort(order, (a, b) -> indices[a] - indices[b]);

    StringBuilder sb = new StringBuilder();
    int i = 0;                                   // cursor into the ORIGINAL s
    for (int k : order) {
        int idx = indices[k];
        String src = sources[k], tgt = targets[k];
        sb.append(s, i, idx);                    // untouched gap before this op
        if (s.startsWith(src, idx)) {            // match against ORIGINAL s (bounds-safe)
            sb.append(tgt);
            i = idx + src.length();              // skip past the matched source
        } else {
            i = idx;                             // no match → leave chars for next copy
        }
    }
    sb.append(s, i, s.length());                 // the tail
    return sb.toString();
}
```
