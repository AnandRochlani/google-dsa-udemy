# 🗣️ The 6-Step Framework — Think Out Loud on Any Problem

> The interviewer scores your *process*, not just your final code. Run these six steps out loud, every time. It also buys you thinking time without awkward silence.

---

## The six steps

### 1. Clarify (30–60 s)
Repeat the problem back. Ask the questions that change the solution:
- Input size? (tells you the target complexity — n=10⁵ means no O(n²))
- Sorted? Duplicates? Negatives? Empty input?
- One valid answer or many? Return the value or the index?
- Can I modify the input in place?

> *"So I'm given an array of integers and a target, and I return the indices of the two numbers that add to it. Can I assume exactly one solution? Are the numbers sorted?"*

### 2. Examples (30 s)
Walk one **small** example by hand. Then a **tricky edge** one — empty, single element, all duplicates, negatives.

> *"For [2,7,11,15], target 9 → indices [0,1]. Edge case: what if the array is empty? I'll return an empty result."*

### 3. Brute Force + Complexity (60 s)
State the obvious solution **and its Big-O**. Never skip this — it shows you can always produce *something*, and it sets up the optimization.

> *"Brute force: check every pair with two nested loops. O(n²) time, O(1) space. That'll time out at n=10⁵, so let me improve it."*

### 4. Optimise — Name the Pattern (60 s)
Ask: *"what work am I repeating?"* Name the pattern that removes it.

> *"I'm re-scanning for each element's complement. A hash map remembers what I've seen, so each lookup is O(1). That drops it to O(n)."*

### 5. Code (the bulk of the time)
Narrate as you type. State invariants. Use clear names. Don't go silent.

> *"I'll keep a `seen` map from value → index. For each number, I check if `target - num` is already in the map…"*

### 6. Test & Edge Cases (60 s)
Trace your code on the example from step 2. Then check the edges: empty, one element, no solution, duplicates, overflow.

> *"Trace [2,7,11,15]: at 2, complement 7 not seen, store it. At 7, complement 2 is seen → return [0,1]. Now the empty case returns []. Looks right."*

---

## The three-part solve (inside steps 3–5)

Every problem lesson in this course breaks the solve into three explicit layers. Say all three out loud when you can:

| Layer | What you show | What it proves |
|---|---|---|
| **1. Brute Force** | The obvious solution + its Big-O + why it's too slow | You can always ship *something* and you can measure it |
| **2. Optimised Solution** | The pattern that removes the repeated work | You recognize structure, not just memorize answers |
| **3. Space Optimization** | Cut extra memory if the problem allows (in-place, rolling variables, two pointers instead of a copy) | You think about memory, not just speed — the detail that separates *hire* from *strong hire* |

> Not every problem has a step 3. When it doesn't, **say so**: *"Space is already O(1) here — I'm only using two pointers, nothing that grows with the input."* Naming the absence is as strong as finding the optimization.

---

## The cardinal rules

- **Never jump to the optimal solution silently.** Brute force first, always — even one sentence of it.
- **Never go quiet for more than ~10 seconds.** Narrate your thinking, even the dead ends.
- **Always end with time *and* space complexity**, then ask "can I do better on either?"
- **If you're stuck, go back to step 3.** The brute force always exists, and the optimization usually hides in "what am I repeating?"
