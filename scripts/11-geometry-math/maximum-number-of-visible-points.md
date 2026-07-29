# 🎬 Recording Script — Maximum Number of Visible Points
**Pattern: Angles + Sliding Window · LeetCode 1610 · Hard · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** sliding window on a sorted array (longest subarray within a limit) — same sweep, new coordinate.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a person-icon standing at a point. A pie-slice "field of view" wedge sweeps around them. Scattered dots light up as the wedge passes. A red "TLE — test 61 / 84" banner slams in.]**

> You're standing still. You can spin in place, and you've got a cone of vision — a fixed angle. Points inside the cone, you see. The question: spin to the *best* direction — how many can you catch at once?

> You write the obvious thing: for every direction, count what's visible. It's correct. You submit… and it dies. Time Limit Exceeded on a hundred-thousand-point test.

> Here's the fix, and it's a two-step combo you'll reuse forever: **turn every point into an angle, then slide a window.** Plus one weird trick with the number 360 that makes the whole circle behave. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence up top. Below, a grid with "you" at (1,1) and three dots at (2,1), (2,2), (3,3). A 90° wedge.]**

> The whole problem in one line: **you're fixed at a location, you have an `angle`-degree field of view, and you can rotate freely — see the most points you can.**

> Tiny example. You're at (1,1). Three points out there. Your view is 90 degrees wide.

> Two rules. One: a point sitting *exactly* on you is always visible — it's on your nose, doesn't matter where you face. Two: everything else, you see it only if it falls inside your wedge.

> Hold this example. The answer here is **three** — but don't take my word yet. Let's earn it.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the wedge snapping to point after point, re-counting all dots each time. A "counts done" tally climbing.]**

> Your brain's first move: the best wedge, you can always rotate it until its *leading edge* lines up with some actual point. Sliding it past that only loses points. So you don't need infinite directions — just `n` of them, one per point.

> So: aim the wedge's left edge at point one. Count everyone inside. Now aim it at point two. Count everyone inside — *again, from scratch.* Now point three. Count everyone — *again.*

> **[VISUAL: highlight the same cluster of dots being re-counted on every pass; tally jumps in chunks of n.]**

> Three points, three full scans. Feel that? Every placement re-counts the same neighbors from zero. `n` placements times `n` points each…

> **[VISUAL: tally morphs into "n × n = n²" with a red glow, then "10⁵ → 10¹⁰".]**

> …is n-squared. At a hundred thousand points that's ten billion operations. That's your TLE.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the three re-scans stacked side by side. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So name the waste. We keep re-scanning the same points, in roughly the same order around the circle, over and over. What are we ignoring that could turn `n` scans into *one*?

> **LEARNER:** The points don't move… so their positions around me never change. Feels like I should sort them once and reuse that.

> **TEACHER:** That's exactly the thread. Pause the video — if each point were just a **single number** you could sort, what number would you pick, and what would the wedge become on that sorted line?

> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: each dot shoots a ray back to "you"; a protractor overlays; each ray gets labeled with its angle in degrees.]**

> **TEACHER:** Here's the number: each point's **angle** relative to you. Draw the line from you to the point, measure its direction. In code that's `atan2` of `(dy, dx)`, converted to degrees.

> Our three points become **0°, 45°, 45°.** Suddenly they're not scattered dots — they're marks on a dial.

> **[VISUAL: the three angles drop onto a horizontal number line: 0, 45, 45.]**

> Sort them. Now "points inside a 90° wedge" means "a **run of marks that spans at most 90°.**" And *widest run within a limit on a sorted line*? That's a **sliding window.** One sweep, not `n` scans.

> **[VISUAL: a 90°-wide bracket slides along the line; it covers 0, 45, 45 all at once → "3".]**

> **LEARNER:** Wait. Angles wrap around a circle. What about a point at 170° and one at −170°? On my sorted line those look 340° apart, but through the back they're only 20° apart. Won't the window miss that?

> **TEACHER:** *That's* the sharp question, and it's the whole trick. Angles live on a circle; the seam is at ±180°. So after sorting, I **copy every angle and add 360.** A point at −170° also shows up as 190°. Now a wedge that straddles the seam appears as an ordinary, contiguous window in the extended list.

> **[VISUAL: line [−170, 170]; a ghost copy appears at [190, 530]; a 20°-wide bracket now cleanly covers 170 and 190.]**

> The circle got unrolled into a straight line. No seam special-case. The number 360 did all the work.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: one boxed line: "point → angle (atan2) · sort · +360 to unwrap · slide the window."]**

> Burn this in: **turn each point into an angle, sort, duplicate everything plus 360 to kill the wraparound, then slide a window for the widest arc that fits.**

> That sentence *is* the solution. Everything left is typing it without tripping.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Chunk one — angles, and the always-visible on-you points counted aside.

```python
import math

def visiblePoints(points, angle, location):
    same = 0
    angles = []
    lx, ly = location
    for x, y in points:
        if x == lx and y == ly:
            same += 1                      # sits on you → always visible
            continue
        angles.append(math.degrees(math.atan2(y - ly, x - lx)))
```

> **[VISUAL: add chunk 2, highlight it.]** Sort, then the wraparound copy.

```python
    angles.sort()
    angles += [a + 360 for a in angles]    # unwrap the circle onto a line
```

> **[VISUAL: add chunk 3.]** The window. `left` chases `right`; shrink while the arc is too wide.

```python
    best = 0
    left = 0
    for right in range(len(angles)):
        while angles[right] - angles[left] > angle + 1e-9:
            left += 1
        best = max(best, right - left + 1)
```

> **[VISUAL: add chunk 4, highlight the return.]** Add back the on-you points at the very end.

```python
    return best + same
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Walk the *why*.

> `atan2(y - ly, x - lx)` — this is the one function that gives a correct angle in **all four quadrants**, sign and all. Plain `atan` can't; it'd collapse opposite directions. `math.degrees` just matches the units of `angle`.

> `same += 1` and `continue` — an on-you point has no direction, so it can't go in the angle list at all. It's always visible, so we bank it and add it once at the end.

> `angles += [a + 360 for a in angles]` — the unwrap. Without it, any wedge crossing the ±180° seam is invisible to a linear window, and you'd fail the wraparound tests.

> **LEARNER:** That `+ 1e-9` on the comparison — why not just `> angle`? Looks like noise.

> **TEACHER:** It's the sneakiest bug in the problem. `atan2` returns **floats**. A point that should sit *exactly* on the wedge edge can come back as `angle` plus a billionth, and a bare `> angle` would wrongly evict it — you'd undercount by one on a boundary test. The epsilon says "this close counts as inside." On a Hard, that one term is the difference between accept and a mystery wrong-answer.

> `right - left + 1` — the window is contiguous by construction, so its size is just the index span. `left` only ever moves forward, so the whole sweep is O(n), not a re-scan.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: number line with the extended angles; a trace table filling row by row.]**

> Run it on our example. Angles `0, 45, 45`, none on you so `same = 0`. Sorted, then plus-360: **`[0, 45, 45, 360, 405, 405]`**. Window width 90.

| `right` | `angles[right]` | shrink while gap > 90 | window | size | `best` |
|---|---|---|---|---|---|
| 0 | 0 | — | `[0]` | 1 | 1 |
| 1 | 45 | 45 ✓ | `[0,45]` | 2 | 2 |
| 2 | 45 | 45 ✓ | `[0,45,45]` | 3 | **3** |
| 3 | 360 | 360>90 → left jumps to 3 | `[360]` | 1 | 3 |
| 4 | 405 | 45 ✓ | `[360,405]` | 2 | 3 |
| 5 | 405 | 45 ✓ | `[360,405,405]` | 3 | 3 |

> `best` locks at **3**, `same` is 0 → **3**. Exactly what we promised in the cold open. Loop closed.

> **[VISUAL: quick second card — angles [−135, 135], angle 90 → extended [−135, 135, 225, 495]; bracket covers 135 and 225 → "2, via wraparound".]**

> And the wraparound proof: two points at −135° and 135°. The window catches `135` and `225` — that `225` is really the −135° point, seen through the seam. Answer two. Drop the angle to 89 and it'd be one. Razor's edge, handled.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two rows — Brute: O(n²). Ours: O(n log n). Note: "sort dominates; sweep is O(n)."]**

> Say it the interview way: *"Brute force is O(n²) — n wedge placements, each scanning n points. Sorting the angles drops it to O(n log n): the sort dominates, and the two-pointer sweep is a single O(n) pass because left never backtracks. Space is O(n) for the angles."*

> That's the sentence that turns a Hard from "I hope" into "I've got it."

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: the O(n) angle array; a "drop the +360 copy?" bubble → a yellow "meh, not worth it".]**

> Can we beat O(n)? **No — and I can say why.** I have to store one angle per point to sort them; that O(n) is the floor, not overhead.

> The only fat is the `+360` copy — it doubles the array. I *could* avoid it by sweeping a single array with modular indexing and a 360 correction when the window laps the end. But that's still O(n), same class, and it swaps a clean loop for a bug-prone wrap condition.

> Say that out loud: *"Space is O(n) and that's optimal — an angle per point is intrinsic. The plus-360 duplicate is a 2× constant; I could remove it with modular indexing but it wouldn't change the order and it invites an off-by-one, so I keep the readable version."* Naming why it can't shrink scores more than silently shrinking it.

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Minimum Number of Arrows to Burst Balloons (LC 452)". A blank editor.]**

> Before the next video, try **Minimum Number of Arrows to Burst Balloons.** Different story, same spine: sort by a coordinate, then sweep a window greedily. It'll tell you whether the "sort, then slide" reflex is really yours yet.

> Don't peek. Wrestle it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three to keep:
> 1. **Points around a center + a fixed angle → convert to angles with `atan2`, sort, slide a window.**
> 2. **Circle wraps → duplicate every angle plus 360** so seam-crossing wedges become normal windows.
> 3. **Floats bite → compare against `angle + epsilon`,** and bank on-you points separately.

> The memory peg — the one line that recalls the whole pattern:

> **[VISUAL: big box → "angle-ize · sort · +360 to unroll · slide."]**

> When a problem puts you at a center with a cone of vision, your hand should already be reaching for `atan2`, a sort, and a sliding window.

> *(GCA reminder — for the interview itself: ask the on-you-points clarifying question first, then narrate brute force → "I'll turn points into angles" → "wait, the circle wraps, I'll add 360" out loud. Google's General Cognitive Ability signal isn't the final code — it's you talking through the path from naive to optimal and catching the wraparound before it bites.)*

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "K Closest Points to Origin" — dots with distance rings around a center.]**

> We ranked points by their *angle* around a center. But what if the question isn't which direction they're in — it's which ones are **nearest**? Suddenly sorting everything is overkill, and a heap does the job in a single pass. Same "points around a center," completely different tool. That's next: K Closest Points to Origin. See you there.
