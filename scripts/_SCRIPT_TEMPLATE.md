# 🎬 Recording Script Template — Engineered for Retention

This is the template every per-problem **video recording script** follows. It's built on how humans actually learn and remember — not just "explain the solution." Authors (and agents) must follow the beat order and honor the learning-science notes.

**Audience:** college students + working IT professionals. Smart, busy, easily bored. They've maybe seen the problem, definitely felt the panic. Talk *with* them, never *at* them.

**Two on-screen tracks:** every beat has **[VISUAL: …]** (what's on screen) and the spoken narration. Humans learn better from words + matching visuals shown together (dual coding / Mayer's multimedia principle). Never narrate one thing while showing another.

---

## 🎙️ Two-voice convention (TEACHER + LEARNER) — use sparingly

Scripts use **two voices**, because a tutor–learner dialogue with sharp questions out-retains a monologue (vicarious learning; Chi's ICAP; AutoTutor trialogue research). But constant back-and-forth adds extraneous cognitive load (Mayer's coherence principle), so the LEARNER voice is a **scalpel, not a co-host**.

- **TEACHER:** the through-line. Carries ~85% of the words. Warm, senior-dev-to-a-friend.
- **LEARNER:** a **smart peer**, never a novice or a strawman. Asks the *exact* sharp question the viewer is already forming. Appears **only 3–5 times per script**, at these high-value moments:
  1. **The predict beat** (the pain point) — LEARNER voices the doubt, TEACHER turns it into "pause and think."
  2. **One code-explanation objection** — "wait, why `< right` and not `<=`?" — the question a real learner asks.
  3. **One common misconception** — LEARNER states the wrong-but-tempting idea; TEACHER corrects it. (Confronting a misconception out loud is one of the strongest retention moves.)
- **Rules:** LEARNER never explains the solution (that's TEACHER's job); LEARNER questions must be *authentic and sharp* (a dumb question insults an IT/college audience and kills trust); keep exchanges to 1–3 lines; everywhere else, single TEACHER voice for clean load.

Format lines as `**TEACHER:**` and `**LEARNER:**`. Beats with no dialogue are just TEACHER.

---

## The learning-science rules (non-negotiable)

| Principle | What it means for the script |
|---|---|
| **Curiosity gap (Zeigarnik)** | Open a loop early ("watch this time out"), close it later. Unfinished questions stick. |
| **Concrete before abstract** | Always a *tiny* real example (4–6 elements) before any general rule. The brain grabs the concrete first. |
| **Worked example + hand dry-run** | We trace a small input BY HAND, on screen, before any code. Seeing the mechanism beats being told it. |
| **Generation effect / predict-first** | Pause and ask the learner to predict before we reveal. Effortful guessing > passive watching, even when they're wrong. |
| **Manage cognitive load** | One new idea at a time. Chunk. Never show 20 lines at once — build the code in small pieces. |
| **Dual coding** | Verbal + visual together, always matched. Pointers move, cells highlight, counters tick. |
| **Elaboration / analogy** | Tie the idea to something they already know (bookshelf, two hands, a queue at a counter). |
| **Desirable difficulty** | A short pause-and-think beat is a *feature*, not dead air. |
| **Emotion & stakes** | A relatable feeling (the interview freeze, the timed-out submission) tags the memory. |
| **Retrieval at the end** | "Your turn" recall problem + 3 takeaways + a one-line memory peg. |
| **Spacing / interleaving** | Call back to earlier patterns ("remember the squeeze from the pair-sum lesson?"). |
| **Conversational voice** | First and second person. Contractions. Short sentences. A senior dev, not a textbook. |

---

## Beat sheet (target ~10–13 min for a Medium)

### 1. COLD OPEN / HOOK — `0:00` *(curiosity gap + emotion)*
Content on screen at second zero. A relatable, high-stakes micro-moment. Open a loop.
> *"You write the obvious solution. It passes the example. You hit submit — and the screen says Time Limit Exceeded on test 47. Let me show you why, and the one idea that fixes it."*

### 2. WHAT WE'RE SOLVING (made concrete) — `~0:30` *(concrete before abstract)*
State the problem in one plain sentence + a TINY example on screen. No formal spec dump.
> *"Here's the whole problem in one line… and here's a tiny example — just six numbers."*

### 3. DRY-RUN THE OBVIOUS IDEA (by hand, small example) — `~1:15` *(worked example)*
Trace the brute force on the tiny example, by hand, on screen. Let them FEEL the wasted work.
> *"Let's do what your brain does first. Check every pair… watch how many times I re-scan the same numbers."*
**[VISUAL: the tiny array, arrows re-scanning, a growing 'comparisons' counter]**

### 4. THE PAIN POINT + PREDICT — `~2:30` *(curiosity gap close #1 + generation effect)*
Name exactly what's wasteful. Then ask them to predict the fix before revealing.
> *"See it? Every pass I re-scan numbers I've already looked at. Pause the video — what information am I throwing away that could save me?"*
**[VISUAL: highlight the repeated/wasted work; a 3-second 'think' timer]**

### 5. BUILD THE INTUITION (the aha, from the dry-run) — `~3:15` *(elaboration + analogy)*
Derive the optimal idea *from* what we just saw — not handed down. Use an analogy. Hand-trace the SAME tiny example the new way so the contrast is visceral.
> *"The array's sorted — that's the clue we ignored. Put one finger at each end, like squeezing a book onto a shelf…"*
**[VISUAL: two pointers as two hands; trace the same example, comparisons counter stays tiny]**

### 6. THE KEY MOVE (signaling) — `~4:30` *(signaling + chunking)*
State the reusable rule in one crisp, repeatable line. This is the sentence they'll remember.
> *"The key move: sum too big → move the right pointer in; too small → move the left in. That's the whole trick."*

### 7. CODE IT — LIVE & CHUNKED — `~5:15` *(cognitive load management)*
Write the code in small pieces, teacher-paced, each chunk explained as it lands. Never paste a wall.
> *"Two variables — left at 0, right at the end. Now the loop…"* (build 3–4 lines, pause, build the next)
**[VISUAL: code typed line-by-line, current chunk highlighted]**

### 8. EXPLAIN THE CODE (the WHY, not the what) — `~7:00` *(elaboration)*
Walk the finished code explaining *why each line exists* and what would break without it.
> *"Why `while left < right` and not `<=`? Because a number can't pair with itself here…"*

### 9. DRY-RUN THE CODE — `~8:15` *(worked example, closing the loop)*
Trace the actual code on the tiny example with a step table. Prove it produces the answer.
**[VISUAL: trace table — left, right, sum, action — filling row by row]**

### 10. COMPLEXITY, OUT LOUD — `~9:15` *(transfer to interview)*
Say time AND space the way they'd say it to an interviewer. Compare to the brute force.

### 11. CAN WE USE LESS MEMORY? (space) — `~9:45` *(depth + honesty)*
The space-optimization beat. Or, if already optimal, say why — naming the absence is a skill.

### 12. YOUR TURN (active recall) — `~10:15` *(retrieval practice)*
A near-twin problem to attempt before the next video. Effortful recall locks it in.

### 13. LOCK IT IN — `~10:45` *(retrieval + memory peg)*
3 takeaways + ONE memorable peg (a phrase, an image) that recalls the whole pattern.
> *"When you see 'sorted' and 'find a pair,' your hand should already be reaching for two pointers."*

### 14. CLIFFHANGER — `~11:15` *(open loop to next lesson)*
Why the next problem breaks this approach — and the itch to find out how it's fixed.

---

## Writing rules for authors/agents

- **Every `>` line is spoken aloud** — read it back; if it sounds like a textbook, rewrite it.
- **Every code chunk is real, runnable code** (Python primary, Java optional at the end).
- **Tiny examples only** for dry-runs (4–6 elements) — big inputs overwhelm working memory.
- **Mark [VISUAL: …] on every beat** so the video editor knows what's on screen.
- **Insert at least two explicit "pause and predict" beats** (the generation effect is the single biggest retention lever).
- **Keep sentences short.** One idea per line. Contractions. Warmth.
- **End on an open loop.** The brain finishes what it started — that's what pulls them to the next video.
