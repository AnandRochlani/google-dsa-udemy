# Lesson 02: Think-Out-Loud — The 6-Step Framework for Any Problem
**Section 0: Orientation | Duration: ~10 min**

---

# PART 1: WHY PROCESS BEATS ANSWERS (~4 min)

## HOOK (0:00)

> Two candidates get the exact same problem. Both write a correct, optimal solution.
>
> One gets "strong hire." The other gets "no hire."
>
> The difference? The first one *talked*. Clarified the input, stated the brute force, named the tradeoff, tested the edges — out loud. The second one went silent for eight minutes and produced a correct answer the interviewer couldn't follow. Google scores your **process**, and if they can't hear it, it didn't happen.

---

## THE STORY (0:45)

> Think of it like a pilot landing a plane. The plane could land itself. But the pilot *calls out* every step — "gear down, flaps 30, on glidepath" — so the co-pilot knows exactly what's happening and can catch a mistake early.
>
> In an interview, **you're the pilot and the interviewer is the co-pilot.** They're not there to watch you land in silence. They're there to follow your calls, nudge you when you drift, and write down that you fly well. Narrate the landing.

**[SLIDE: Cockpit callouts ↔ interview narration]**

---

## THE FRAMEWORK (2:00)

> Six steps. Same six, every problem, in order. Memorize the shape until it's automatic — then all your brainpower goes to the *problem*, not to "what do I do now?"
>
> **1. Clarify** — repeat it back, ask what changes the answer.
> **2. Examples** — one small case by hand, one nasty edge.
> **3. Brute force + complexity** — the obvious solution and its Big-O.
> **4. Optimise** — "what am I repeating?" → name the pattern.
> **5. Code** — narrate as you type.
> **6. Test & edges** — trace it, then break it.
>
> Notice steps 3 and 4: **brute force always comes first.** Never jump to clever. The brute force proves you can always ship something, and the optimization is just "remove the repeated work" from there.

---

## QUICK CHECK (3:30)

> You're handed: *"Return the length of the longest substring without repeating characters."* What's the **very first thing** out of your mouth?
>
> *(pause)*
>
> Not code. A **clarifying question**: *"Are these ASCII or full Unicode? Is an empty string a valid input — should it return 0?"* Step 1, always. You clarify before you solve.

---

# PART 2: THE FRAMEWORK ON A REAL PROBLEM (~6 min)

> Let's run all six steps on one problem — *"Two Sum on a sorted array"* — so you hear what each step sounds like. (We solve this fully in L08; here we're watching the *narration*.)

## STEP 1 — CLARIFY (4:00)

> *"Let me make sure I've got it. I'm given an array of integers, sorted ascending, and a target. I return the indices of the two numbers that add to the target. Questions: Is there always exactly one answer? Can I assume it's sorted — yes? Can the same element be used twice? Are there negatives?"*
>
> Every one of those answers can change your code. Ask them **before** you write, not after you've built the wrong thing.

## STEP 2 — EXAMPLES (5:00)

> *"Quick example: `[1, 3, 4, 6]`, target 10 → 4 + 6 = 10, indices `[2, 3]`. And an edge case — what if no pair exists, like target 100? I'll return `[-1, -1]`. What about an empty array? Also `[-1, -1]`."*
>
> The edge case you name here is the test case you *pass* later. Interviewers love a candidate who surfaces edges early.

## STEP 3 — BRUTE FORCE + COMPLEXITY (6:00)

> *"The obvious approach: check every pair with two nested loops. That's O(n²) time, O(1) space. It'll work but it times out for large inputs — so let me use the fact that the array is **sorted**."*
>
> One sentence of brute force. Its Big-O. Why it's not enough. That's the whole step. **Do not skip it** — it's the setup for looking smart in step 4.

## STEP 4 — OPTIMISE (6:45)

> *"What am I repeating? For each element I re-scan the whole rest of the array. But since it's sorted, I can start one pointer at each end: if the sum's too big, move the right pointer down; too small, move the left up. That's two pointers — O(n) time, O(1) space."*
>
> "What am I repeating?" is the magic question. The answer is almost always the pattern.

## STEP 5 — CODE (7:30)

> *"I'll set `left = 0`, `right = last index`. While they haven't crossed, compute the sum. If it equals the target, return the indices. If it's less, `left += 1`; if more, `right -= 1`…"*
>
> Talk while you type. Name your variables clearly. If you go quiet, the interviewer loses the thread — and the score.

## STEP 6 — TEST & EDGES (8:30)

> *"Let me trace `[1,3,4,6]`, target 10: left=0(1)+right=3(6)=7, too small, left→1. 3+6=9, too small, left→2. 4+6=10 — return `[2,3]`. Now the empty array: the while loop never runs, returns `[-1,-1]`. Good. Single element: same. Negatives work because the sum logic doesn't care about sign."*
>
> Trace the happy path, then *hunt for the break*: empty, one element, no answer, duplicates, overflow. Finding your own bug beats the interviewer finding it.

---

## ACTIVE RECALL (9:15)

> **Your turn.** Take any problem you've solved before — even Two Sum — and narrate all six steps *out loud*, to your webcam or a rubber duck. Time yourself. If steps 1–4 take more than ~3 minutes, you're over-thinking; if you skipped brute force, do it again. This narration is a muscle. Reps build it.

---

## 3-POINT SUMMARY (9:40)

> 1. **Six steps, every time:** Clarify → Examples → Brute force + Big-O → Optimise → Code → Test.
> 2. **Brute force is never optional.** It proves you can always produce a solution, and it's the launchpad for the optimization.
> 3. **Narrate everything.** A silent correct answer scores worse than a spoken one. The interviewer grades what they can hear.

---

## CLIFFHANGER (9:55)

> You've got the script. Now you need the *tools* the script plugs into. Before any pattern, we spend five short lessons on the fundamentals every pattern leans on — Big-O you can feel, the hash map that shows up everywhere, and the array tricks that trip people up. That's Section 1, starting with why exactly O(n²) times out.
