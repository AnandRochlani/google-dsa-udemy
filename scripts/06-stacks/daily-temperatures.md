# 🎬 Recording Script — Daily Temperatures
**Pattern: Stacks (Monotonic) · LeetCode 739 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the monotonic stack from Next Greater Element — same engine, new payload.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an editor. A row of temperatures `[73, 74, 75, 71, 69, 72, 76, 73]` with day numbers 0–7 beneath. A red "TLE — test 37/47" banner slides in.]**

> Google question: *"For each day, how many days until it gets warmer?"*
>
> You write the obvious loop — for each day, scan forward until it's warmer, count the days. It passes the example. You submit… Time Limit Exceeded.
>
> **[VISUAL: n = 100,000 flashes; the double loop lights up as ~10 billion.]**
>
> A hundred thousand days, a nested scan — ten billion operations. Dead. The fix is the *same monotonic stack* from last lesson — but with one change that trips up almost everyone: what you store on the stack. Get it wrong and your distances are garbage. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: the 8 temperatures with day indices. Answer slots below, all `?`.]**

> The problem in one line: **for each day, the number of days you wait until a warmer temperature** — `0` if it never gets warmer.
>
> Tiny example: `[73, 74, 75, 71, 69, 72, 76, 73]`. Day 0 is 73; day 1 is 74, warmer — wait `1`. Day 2 is 75; the next warmer day is day 6 at 76 — that's `6 − 2 = 4` days. Day 6 is 76 — nothing after is warmer — `0`.
>
> **[VISUAL: answer fills: `[1, 1, 4, 2, 1, 1, 0, 0]`.]**
>
> The answer is `[1, 1, 4, 2, 1, 1, 0, 0]`. Notice day 2's answer — `4` — is a *distance*, `6 − 2`. That word, distance, is the whole game today.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: the temps; from each day, an arrow scans forward.]**

> Brute force by hand: from each day, walk forward to the first warmer day, count the steps.
>
> Day 0, 73 — day 1 is 74, warmer, one step. Day 2, 75 — day 3 is 71 nope, day 4 is 69 nope, day 5 is 72 nope, day 6 is 76 yes — four steps.
>
> **[VISUAL: a cold stretch `[100, 99, 98, 97, …]`; every day's arrow runs to the very end.]**
>
> Now the killer case — a long cooling stretch. Every day scans almost the *entire* rest of the array and finds nothing. Each of those is a full O(n) walk. Over n days → O(n²). At 100k, that's your TLE. We keep re-walking the same future over and over.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the cold stretch, arrows overlapping. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** The waste is the re-walking — every day re-scans a future that barely changes.
>
> **LEARNER:** This feels *just* like Next Greater Element — a warmer day is a "greater element." So same monotonic stack, right? Just push the temperatures?
>
> **TEACHER:** You've nailed the pattern — it *is* the same stack. But there's a catch that'll bite you. Last time we wanted the greater *value*. Here we want a *distance* — how many days. Pause and think: **if I only store the temperatures on the stack, can I compute a distance when I pop? What do I actually need to remember instead?**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a stack column labeled "days still waiting for warmth". Sweep the temps; tiles show the DAY INDEX, temp in small text.]**

> Here's the fix. Same monotonic stack — remember, a *monotonic stack* keeps its values sorted, only ever increasing or only ever decreasing bottom to top. We keep a stack of days still **waiting for a warmer day**, decreasing in temperature.
>
> But we store the **day index**, not the temperature. Why? Because the answer is a distance, and a distance is `today − that day`. You can't subtract temperatures to get days. You need to remember *which day* each waiter was.
>
> **[VISUAL: sweep. i=0 (73) push index 0. i=1 (74): 74 > temp at top (73) → the tile for day 0 lights up, answer[0] = 1 − 0 = 1, pop. Push 1.]**
>
> Day 0, 73 — push index 0. Day 1, 74 — look at the top: it's day 0, temp 73. Is today warmer? Yes. So today *resolves* day 0. The wait is `1 − 0 = 1` — subtract the indices. Record it, pop, push day 1.
>
> **[VISUAL: i=3 (71) and i=4 (69) both just push — colder than top. Column: indices [2,3,4], temps 75,71,69 decreasing.]**
>
> Days 3 and 4 are colder than the top, so they just get in line. Column now holds days 2, 3, 4 — temps 75, 71, 69, decreasing top-down.
>
> **[VISUAL: i=5 (72): warmer than day 4 (69) → answer[4]=5−4=1, pop; warmer than day 3 (71) → answer[3]=5−3=2, pop; NOT warmer than day 2 (75) → stop. Push 5.]**
>
> Day 5, 72 — it's warmer than day 4 (69): resolve, `5 − 4 = 1`, pop. Still warmer than day 3 (71): resolve, `5 − 3 = 2`, pop. But day 2 is 75, *not* colder than 72 — stop. Push day 5. One warm day cleared a whole run of colder waiters — that's the monotonic magic, now paying out in distances.

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Decreasing stack of INDICES. Warmer day pops colder waiters; wait = i − popped index."]**

> Burn this in: **keep a decreasing stack of day indices; when today is warmer than the top, it resolves that day — the wait is today's index minus that day's index.**
>
> The one-word upgrade from last lesson: store **indices**, not values, whenever the answer is a *distance*.

---

## 7. CODE IT — LIVE & CHUNKED — `5:10`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. Answer array of zeros, and the stack of indices.

```python
def daily_temperatures(temperatures):
    n = len(temperatures)
    answer = [0] * n
    stack = []                       # indices, temps decreasing bottom -> top
```

> **[VISUAL: add chunk 2, highlight it. Stack column on the right, tiles = indices.]** The sweep. Today resolves every colder waiting day on top.

```python
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev = stack.pop()
            answer[prev] = i - prev  # distance in days
        stack.append(i)
    return answer
```

> That's the whole thing. Days left on the stack at the end keep their `0` — they never warmed up, and we pre-filled zeros for exactly that.

---

## 8. EXPLAIN THE CODE (the WHY) — `6:10`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as named.]**

> Let's walk the *why*.
>
> `answer = [0] * n` — the default is `0`, so any day that never finds warmth needs no special handling. Free.
>
> `temperatures[stack[-1]] < temp` — the stack holds indices, so to compare temperatures we look them *up* in the array. That's the price of storing indices, and it's cheap.
>
> `answer[prev] = i - prev` — this is why we stored indices. The wait is the gap between today and the resolved day. With only temperatures on the stack, this line is impossible.
>
> The `while` clears a whole run of colder days in one arrival. `stack.append(i)` puts today in line as the newest waiter.
>
> **LEARNER:** Why `<` and not `<=`? If today ties the top day's temperature, does it matter?
>
> **TEACHER:** It matters, and `<` is correct. "Warmer" means *strictly* greater. If today only *ties* the top day, it is not warmer — that day is still waiting for a genuinely hotter day. So we must *not* pop on a tie. `<` leaves tied days on the stack; `<=` would wrongly resolve them with a distance to a day that isn't actually warmer. Small symbol, wrong answer.

---

## 9. DRY-RUN THE CODE — `7:20`
*(worked example — prove it, close the loop)*

**[VISUAL: the 8 temps; stack column of indices growing/shrinking; trace table filling.]**

> Let's run the real code. Stack holds indices; temps shown for clarity.

| i | temp | pops → assign | stack (indices) | answer so far |
|---|---|---|---|---|
| 0 | 73 | — | `[0]` | `[0,0,0,0,0,0,0,0]` |
| 1 | 74 | pop 0 → `ans[0]=1` | `[1]` | `[1,0,…]` |
| 2 | 75 | pop 1 → `ans[1]=1` | `[2]` | `[1,1,…]` |
| 3 | 71 | — | `[2,3]` | unchanged |
| 4 | 69 | — | `[2,3,4]` | unchanged |
| 5 | 72 | pop 4 →`ans[4]=1`, pop 3 →`ans[3]=2` | `[2,5]` | `[1,1,0,2,1,0,0,0]` |
| 6 | 76 | pop 5 →`ans[5]=1`, pop 2 →`ans[2]=4` | `[6]` | `[1,1,4,2,1,1,0,0]` |
| 7 | 73 | — | `[6,7]` | unchanged |

> Leftover indices 6 and 7 never resolved → stay `0`. Final `[1, 1, 4, 2, 1, 1, 0, 0]` — exactly what we predicted. And there's day 2's `4`, the distance `6 − 2`, straight out of the index subtraction. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:15`
*(transfer to interview)*

**[VISUAL: two rows — Brute: O(n²). Ours: O(n) time, O(n) space.]**

> Say it in the room: *"Brute force scans forward from each day — O(n²), which times out at 100k on a decreasing array. The monotonic stack does one pass: each index is pushed once and popped at most once, so total pushes plus pops is at most 2n — O(n) time. Space is O(n) for the stack, worst case a strictly decreasing array puts every index on it at once."*
>
> "Each index pushed once, popped once" — that's the amortized argument that turns a nested-looking `while` into linear time. Interviewers want to hear it.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:55`
*(depth + honesty)*

**[VISUAL: the temps range badge "30–100, only 71 values"; a right-to-left scan with a single `hottest` scalar.]**

> The stack is O(n) and, for the *general* problem, inherent — a strictly decreasing array leaves every day unresolved until the end. But this problem has a gift: **temperatures are bounded, 30 to 100, only 71 distinct values.** That opens an O(1)-extra-space variant.

```python
def daily_temperatures_bounded(temperatures):
    n = len(temperatures)
    answer = [0] * n
    hottest = 0
    for i in range(n - 1, -1, -1):
        if temperatures[i] >= hottest:
            hottest = temperatures[i]
            continue                 # nothing to the right is warmer
        days = 1
        while temperatures[i + days] <= temperatures[i]:
            days += answer[i + days] # JUMP using already-computed answers
        answer[i] = days
    return answer
```

> **LEARNER:** Hang on — that inner `while` looks like another nested loop. How is this not O(n²) again?
>
> **TEACHER:** Because of the jump. `days += answer[i + days]` doesn't step one day at a time — it *leaps* over an entire run that we've already proven can't help, reusing an answer we filled in earlier. Scanning right-to-left, those answers already exist. Combined with the tiny value range, the total work stays O(n) — and the only real extra memory is the single `hottest` scalar. O(1) extra space beyond the output.
>
> Honest verdict for the room: *"The plain stack is O(n) and perfectly acceptable — it's what I'd write first. But since temperatures span only 71 values, I can scan right-to-left and jump using computed answers for O(1) extra space."*

---

## 12. YOUR TURN (active recall) — `10:00`
*(retrieval practice)*

**[VISUAL: "Your turn → Online Stock Span (LC 901)". A streaming price feed.]**

> Before the next video, try **Online Stock Span**, LC 901. Same monotonic stack — but counting *backwards*: how many consecutive prior days were less-than-or-equal to today. It flips the direction and streams the input. See if the pattern transfers.
>
> Ten minutes of real struggle before the solution. That's the rep that counts.

---

## 13. LOCK IT IN — `10:25`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Distance answer → store indices**, not values. Subtract indices for the gap.
> 2. **Same monotonic stack**: a warmer day **pops every colder waiter** — one arrival, a whole run cleared.
> 3. **`<` vs `<=` is not cosmetic** — "strictly warmer" means don't pop on a tie.
>
> And the peg: **we pop while the new element beats the top** — and when the question asks *how far*, the stack holds *where*, not *what*.

---

## 14. CLIFFHANGER — `10:50`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Largest Rectangle in Histogram". Bars of a histogram; a rectangle stretching across several.]**

> We've used the stack to look *one* direction — the next greater. But the boss-level problem needs *both* directions at once: for each bar, how far left AND how far right can it stretch before hitting something shorter? One monotonic stack, and the answer falls out the moment you pop. That's the hard one: Largest Rectangle in Histogram. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int[] dailyTemperatures(int[] temperatures) {
    int n = temperatures.length;
    int[] answer = new int[n];
    Deque<Integer> stack = new ArrayDeque<>();     // indices, temps decreasing

    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && temperatures[stack.peek()] < temperatures[i]) {
            int prev = stack.pop();
            answer[prev] = i - prev;
        }
        stack.push(i);
    }
    return answer;    // unresolved indices already 0
}
```
