# 🎬 Recording Script — The Number of Weak Characters in the Game
**Pattern: Sort + running max (greedy sweep) · LeetCode 1996 · Medium · Target length ~11 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** custom sort keys (My Calendar's "sort by start" reflex) — plus one new twist: the tie-break *is* the algorithm.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a game roster of characters, each with an ⚔️ attack and 🛡️ defense stat. A nested for-loop appears; a LeetCode "Time Limit Exceeded — 71 / 82" banner slams in red.]**

> A hundred thousand game characters. Each one has an attack stat and a defense stat. The interviewer asks: *"How many of them are dominated — some other character beats them on both stats at once?"*
>
> You write the honest answer — check every character against every other character. It's correct. It passes the samples. And on the big test it burns ten *billion* comparisons and dies.
>
> Here's the promise: by the end of this video, you'll count every weak character in **one pass with one integer** — and the entire trick lives in a tie-break most people get backwards. Get that tie-break wrong and your code passes the examples and fails hidden tests. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below, three character cards:]**

```
properties = [[1,5], [10,4], [4,3]]
              atk,def  atk,def  atk,def
```

> The whole problem in one line: **a character is weak if some *other* character has a strictly bigger attack AND a strictly bigger defense — count the weak ones.**
>
> Both comparisons are **strict**. Bigger attack but equal defense? Not weak. That word "strictly" is going to matter more than anything else in this video — hold onto it.
>
> Here's our tiny example — three characters. `[1,5]`, `[10,4]`, `[4,3]`. The answer is **1**: only `[4,3]` is weak, because `[10,4]` out-attacks it, ten versus four, *and* out-defends it, four versus three. Nobody dominates the other two. Keep these three cards on screen — we'll earn that answer by hand.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the three cards in a row. A "comparisons" counter, top-right, at 0. An arrow sweeps from each card to every other card.]**

> Let's do what your brain does first: for each character, scan everyone else and ask, "does anybody beat me on both?"
>
> Character `[1,5]`. Check `[10,4]` — attack 10 beats 1, but defense 4 loses to 5. Not dominated. Check `[4,3]` — 4 beats 1, but 3 loses to 5. Safe. Two comparisons.
>
> **[VISUAL: counter ticks to 2.]**
>
> Character `[10,4]`. Check both others — nobody's attack tops 10. Safe. Four comparisons.
>
> Character `[4,3]`. Check `[1,5]` — no. Check `[10,4]` — attack 10 > 4 *and* defense 4 > 3. **Dominated.** Weak count: one. Six comparisons total.
>
> **[VISUAL: counter shows 6, then morphs into "n² ≈ 10¹⁰" with a red glow and a thought bubble: "n = 100,000".]**
>
> Six comparisons for three characters — cute. But this is n² work, and the constraints say n goes to a hundred thousand. That's ten billion comparisons. Tens of seconds. Guaranteed Time Limit Exceeded. And notice *what* we kept doing: re-scanning the entire unsorted pile, asking the same question over and over.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. The question "is there anyone with bigger attack AND bigger defense?" stamped over the pile three times. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Here's the waste, named precisely. For every character, we re-answer the same global question from scratch: "does someone out there beat me on *both* stats?" Two conditions at once is what makes it feel hard. So — what if we could make one of the two conditions just… disappear?
>
> **LEARNER:** You mean sort? If I sort by attack, at least I'd know who out-attacks whom without scanning.
>
> **TEACHER:** Exactly the right instinct. So here's your think: **if the characters were sorted by attack, descending — biggest attacker first — and you walked the line left to right, what single piece of information would you need to carry to decide "weak or not" instantly?** Pause the video. One variable. What is it?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the three cards rearrange into sorted order: [10,4] → [4,3] → [1,5]. A crown labeled "max defense seen" floats above the line, updating as a cursor walks left to right.]**

> **TEACHER:** Sort by attack, **descending**. Our line becomes `[10,4]`, then `[4,3]`, then `[1,5]`. Now walk it left to right and think about what sorting bought you: by the time you're standing on any character, **everyone behind you has attack greater than or equal to yours.**
>
> The attack condition is basically handled for free. The only question left is defense: *did anyone back there carry a bigger defense than mine?* And "biggest defense among everyone seen so far" is just a **running maximum**. One variable, updated as you walk.
>
> Think of it like a receiving line at a tournament. The champions walk past you in order of attack, strongest first. You only need to remember one thing: the biggest shield you've seen go by. When you step up and your own shield is smaller than that record — somebody ahead of you had a bigger sword *and* a bigger shield. You're weak.
>
> **[VISUAL: cursor on [4,3]; the crown reads "max def = 4"; the card flashes red "WEAK — 3 < 4". Cursor moves to [1,5]; 5 ≥ 4, crown updates to 5, card stays green.]**
>
> Walk it: `[10,4]` — nothing seen yet, record the 4. `[4,3]` — defense 3 is *below* the record 4, and the record was set by someone with strictly more attack. Weak. `[1,5]` — 5 beats the record, so update it to 5, not weak. Count: one. Same answer, and the counter barely moved.
>
> **LEARNER:** Wait — "everyone behind you has attack greater than **or equal**." Equal is the problem, right? Weak needs *strictly* bigger attack. What if the character behind me has the *same* attack but a bigger defense — your running max would call me weak, and I'm not.
>
> **TEACHER:** *That* is the trap that fails hidden test cases, and you just found it before the code did. Ties in attack can poison the running max. So we defuse them with the sort itself: **for equal attacks, sort defense ascending** — smallest shield first. Now inside any group of equal-attack characters, defenses only *climb* as we walk. An earlier same-attack character can never hold a bigger defense than a later one, so it can never falsely inflate the max. The only way your defense is below the running max is if someone with **strictly** greater attack put it there. Which is exactly, word for word, the definition of weak.

---

## 6. THE KEY MOVE (signaling) — `4:55`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "sort attack DESC, defense ASC on ties → sweep once → defense < max_def ⇒ weak."]**

> Burn this in: **sort by attack descending — and on ties, defense ascending — then sweep once; anyone whose defense is below the running max is weak.**
>
> And tuck away the bigger lesson, because it transfers: **when a problem demands domination on two dimensions, sort one dimension away and sweep a running best on the other.** The tie-break isn't a detail — it's how you encode "strictly greater" into the sort itself.

---

## 7. CODE IT — LIVE & CHUNKED — `5:30`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, the sort — and look closely at the key, because this line *is* the algorithm.

```python
def numberOfWeakCharacters(properties):
    # attack DESC, and for equal attack, defense ASC (the crucial tie-break)
    properties.sort(key=lambda p: (-p[0], p[1]))
```

> Negating attack sorts it descending; leaving defense positive sorts it ascending within ties. One lambda, both rules.
>
> **[VISUAL: add chunk 2, highlight it.]** Two integers — the answer, and the crown: the best defense seen so far.

```python
    weak = 0
    max_def = 0                       # best defense among everyone seen so far
```

> **[VISUAL: add chunk 3.]** Now the whole sweep — and notice we don't even look at attack anymore. The sort already spent it.

```python
    for _, defense in properties:
        if defense < max_def:
            # someone earlier had a STRICTLY bigger attack (earlier group)
            # AND a strictly bigger defense → this character is dominated
            weak += 1
        else:
            max_def = defense         # new high-water mark for defense
    return weak
```

> That's the entire solution. A sort, a loop, an if. The hundred-thousand-character case that murdered the brute force? This strolls through it.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:50`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `key=lambda p: (-p[0], p[1])` — the minus sign flips attack to descending so the sweep meets strong attackers first. The *un*-flipped `p[1]` is the tie-break: equal-attack groups line up smallest defense first, so nobody inside your own group can sit ahead of you with a bigger shield.
>
> `if defense < max_def` — strict less-than. If your defense *equals* the record, you're not dominated — remember, weak needs strictly bigger on both.
>
> `else: max_def = defense` — on a tie or a new high, we take your defense as the new record. Safe either way, because the record only ever gets *used* against characters with strictly less attack, further down the line.
>
> **LEARNER:** Let me try to break it. Flip the tie-break — sort defense *descending* on ties. What actually goes wrong?
>
> **TEACHER:** Take `[2,1]` and `[2,2]` — same attack. Descending puts `[2,2]` first, so `max_def` becomes 2 before `[2,1]` arrives. Then `[2,1]` sees `1 < 2` and gets branded weak — dominated by a character with the *same* attack. That's flat-out wrong, and here's the evil part: the LeetCode sample inputs have no attack ties, so the bug sails through the examples and detonates on a hidden test. When a tie-break decides correctness, it's the first thing to check in your dry-run.

---

## 9. DRY-RUN THE CODE — `8:00`
*(worked example — prove it, close the loop)*

**[VISUAL: sorted cards [10,4] → [4,3] → [1,5]; a trace table filling row by row.]**

> Let's run the real code on our example and close the loop from the start. After the sort: `[10,4]`, `[4,3]`, `[1,5]`.

| Step | Character | `defense < max_def`? | Action | `max_def` after | weak |
|---|---|---|---|---|---|
| 1 | `[10,4]` | `4 < 0`? no | update max | `4` | 0 |
| 2 | `[4,3]`  | `3 < 4`? **yes** | weak++ | `4` | 1 |
| 3 | `[1,5]`  | `5 < 4`? no | update max | `5` | 1 |

> Returns **1** — exactly the answer we promised at second thirty-five, and exactly which character: `[4,3]`, dominated by `[10,4]`.
>
> Now the one that separates the passers from the failers — attack ties. `[[1,1],[2,1],[2,2],[1,2]]`. Sorted with our key: `[2,1]`, `[2,2]`, `[1,1]`, `[1,2]`.

| Step | Character | `defense < max_def`? | Action | `max_def` | weak |
|---|---|---|---|---|---|
| 1 | `[2,1]` | `1 < 0`? no | update | `1` | 0 |
| 2 | `[2,2]` | `2 < 1`? no | update | `2` | 0 |
| 3 | `[1,1]` | `1 < 2`? **yes** | weak++ | `2` | 1 |
| 4 | `[1,2]` | `2 < 2`? no | update | `2` | 1 |

> **[VISUAL: row 2 pulses — "[2,1] went FIRST, so [2,2] survives"; row 4 pulses — "2 < 2 is false: equal defense ≠ weak".]**
>
> Watch step 2: `[2,2]` shares its attack with `[2,1]`, but ascending defense put `[2,1]` *first* — the record was only 1, so `[2,2]` walks free. And step 4: `[1,2]` meets a record of 2, but `2 < 2` is false — equal defense, not dominated. Both strictness rules, honored by two characters in the code: one minus sign and one `<`. Answer: **1**, only `[1,1]`. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:10`
*(transfer to interview)*

**[VISUAL: two rows — Brute force: O(n²) ≈ 10¹⁰. Ours: O(n log n) sort + O(n) sweep.]**

> **TEACHER:** Say it the way you'd say it in the room: *"Brute force compares all pairs — O(n²), ten billion operations at n equals ten to the fifth, so it times out. I sort by attack descending with a defense-ascending tie-break — O(n log n) — then one linear sweep with a running max decides every character in O(1). The sort dominates: O(n log n) total."*
>
> And here's your GCA moment — remember, Google explicitly scores General Cognitive Ability, and half that rubric is *narration*: stating the brute force, naming the repeated work, asking the clarifying question before you code. Here, the question that proves you read the spec is: **"Both comparisons are strict, right — attack AND defense both strictly greater?"** That one question is what *drives* the ascending tie-break. Ask it out loud, then design the sort key in front of them — that's worth more than silently typing the right answer.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: the sweep variables — just `weak` and `max_def` — in a tiny box; next to them a "counting sort?" thought bubble with "O(10⁵) space" price tag.]**

> Quick one, and honesty scores here.
>
> The sweep carries exactly two integers — `weak` and `max_def`. We sort `properties` in place, so we allocate nothing that grows with n. Auxiliary space: **O(1)**.
>
> Can we beat O(n log n) *time*? Actually yes — and naming it is a bonus signal. Stats are capped at 10⁵, so you could counting-sort on attack and take a suffix-max of defense: O(n) time, but it costs O(10⁵) extra space for the buckets. Say the trade out loud: *"For these limits, sort-and-sweep at O(1) auxiliary is the clean answer; if the interviewer pushes for linear time, counting sort buys the log factor for O(10⁵) space."* Knowing the trade exists — and choosing not to take it — reads as judgment, not ignorance.

---

## 12. YOUR TURN (active recall) — `10:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Russian Doll Envelopes (LC 354)". A blank editor.]**

> Before the next video, try **Russian Doll Envelopes**. Same DNA — domination on two dimensions, envelopes instead of characters — and the same opening move: sort one dimension with a *deliberate* tie-break. But this time the second dimension needs more than a running max; it becomes Longest Increasing Subsequence. See how far the sort-one-sweep-one instinct carries you before it needs reinforcement.
>
> Don't peek. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `11:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **Two-dimension domination + n too big for n² → sort one dimension away, sweep a running max on the other.**
> 2. **The tie-break IS the algorithm:** attack descending, defense *ascending* on ties — it's how "strictly greater" gets encoded into the sort.
> 3. **The sweep is two integers** — O(n log n) time from the sort, O(1) auxiliary space.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "sort one stat away, sweep the other — ties sorted backwards."]**
>
> When you see "beats it on both stats," your hand should already be reaching for a sort key with a minus sign in it — and your first sanity check should be the tie-break.

---

## 14. CLIFFHANGER — `11:30`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Range Module" — a number line where ranges get painted in, punched out, and queried, fragments flying.]**

> Today, one sort and one sweep did everything, because the data held still. But what if the intervals *won't hold still*? Next up is **Range Module** — add a range, remove a *chunk out of the middle* of existing ranges, then answer "is this whole range covered?" — in any order, thousands of times. Ranges get split, merged, and shattered live. It's the hardest interval problem in this section, and everything the calendar problems taught you gets stress-tested at once. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int numberOfWeakCharacters(int[][] properties) {
    // attack DESC; for equal attack, defense ASC (the crucial tie-break)
    Arrays.sort(properties, (a, b) ->
        a[0] == b[0] ? a[1] - b[1] : b[0] - a[0]);

    int weak = 0;
    int maxDef = 0;                      // best defense among everyone seen so far
    for (int[] p : properties) {
        if (p[1] < maxDef) {
            weak++;                      // strictly bigger attack earlier + bigger defense
        } else {
            maxDef = p[1];               // new high-water mark
        }
    }
    return weak;
}
```

*(Watch the comparator: `a[1] - b[1]` on equal attack sorts defense **ascending** — flip it and same-attack characters corrupt the count. Stats are capped at 10⁵, so the int subtraction can't overflow here.)*
