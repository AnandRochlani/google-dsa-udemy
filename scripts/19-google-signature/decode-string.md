# 🎬 Recording Script — Decode String
**Pattern: Stack · LeetCode 394 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the "match innermost first" instinct from Valid Parentheses.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a code editor. A single encoded string sits center screen: `3[a2[c]]`. A blinking cursor. Below it, an empty output box labeled "= ?"]**

> Google phone screen. The interviewer types eight characters: `3[a2[c]]` — and says *"decode it."*
>
> Your brain goes: easy, `3[...]` means repeat three times. Then you see the `2[c]` hiding *inside*, and suddenly you're not sure what to multiply, or when. You start expanding the outer three… and lose track of the inner part.
>
> Here's the thing — there's one data structure that makes this click instantly, and it's probably the single most-tested idea in a Google interview. By the end you'll see the whole trick *and* why it works. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, two tiny examples stacked: `2[ab]` and `3[a2[c]]`.]**

> The whole problem in one line: **`k[stuff]` means repeat `stuff` k times — and the brackets can nest.**
>
> Start dead simple. `2[ab]` — that's just `ab` twice: `abab`. No nesting, no drama.
>
> Now the spicy one: `3[a2[c]]`. There's a bracket *inside* a bracket. Hold this exact string in your head — we're going to solve it by hand before we write a line of code.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: `3[a2[c]]` with a single left-to-right marker. As it hits `3[`, it tries to write `a` three times and stalls — a red "??" pops over the unfinished inner `2[c]`.]**

> Let's do what your brain does first: read left to right and expand as you go.
>
> Marker hits `3`, then `[`. Okay — repeat what's inside three times. So I start copying… `a`… and then — wait. What's after `a`? Another number, `2`, another bracket. The inside *isn't finished yet.* I can't repeat by three, because I don't even know what "the inside" fully is.
>
> **[VISUAL: the marker bounces back and forth between the outer `3` and the inner `2`, a tangle of arrows building up.]**
>
> So I try to remember "hold the 3 for later," dive in, do the `2[c]`… and now I'm juggling two counts in my head at once. With one more level of nesting, I've dropped one. This is exactly where people freeze in the interview.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Highlight the two live counts — outer `3` and inner `2` — both glowing, with a "don't forget me!" tag. A 4-second "🤔 your turn" timer appears.]**

> **TEACHER:** So what's the actual pain? It's this: when I open a new bracket, I have to **pause** whatever I was doing — remember the string I'd built and the count I owed — go finish the inside, then come back and pick up exactly where I left off.
>
> **LEARNER:** Right, but I could just use recursion for that, no? Function calls itself on the inside and returns.
>
> **TEACHER:** You absolutely could — good instinct, and it works. But pause the video and think about *what recursion is actually giving you here.* What's the one word that describes "pause the current thing, go finish the newest thing, then resume the paused one"? That word is the whole answer.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a stack of physical trays slides in. Each time a `[` appears, a tray labeled "(string-so-far, count)" drops onto the pile. Each `]` lifts the top tray off.]**

> **TEACHER:** The word is **last-in, first-out.** The bracket I opened *most recently* is the one I have to close *first.* That's a **stack.** Recursion was just hiding a stack inside the call stack — let's make it visible and control it ourselves.
>
> **LEARNER:** Wait — why not first-in-first-out, a queue? The `3` came first, shouldn't it resolve first?
>
> **TEACHER:** Great question, and it's the crux. The `3` came first but it *finishes last* — you can't triple the outside until the inside is fully built. Innermost closes first. That's the definition of a stack, not a queue.
>
> Think of it like nested boxes. To wrap the big box, you first have to close the small box inside it. You open big, open small, close small, *then* close big. Last opened, first closed.
>
> **[VISUAL: two hands. Open big box → open small box → close small → close big, in that order, matched to the trays.]**
>
> So here's the plan: keep a running `current` string and a running `num`. Every time I open a bracket, I **push** the pair `(current, num)` onto the stack and start fresh inside. Every time I close one, I **pop** and stitch: `previous + count × current`.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "On `[` push (current, num) & reset · on `]` pop and do prev + k × current."]**

> Burn this one line in: **on open-bracket, push what you've built and the count, then reset. On close-bracket, pop and repeat.**
>
> That's the entire algorithm. Push context going in, pop-and-stitch coming out. Everything else is just building up a number or appending a letter.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it in small pieces. First, our three pieces of state: the stack, the current string, the running number.

```python
def decode_string(s):
    stack = []          # holds (previous_string, repeat_count)
    current = ""
    num = 0
```

> **[VISUAL: add chunk 2, highlight it.]** Now walk the string. If it's a digit, build the number — and note `num * 10` so `12[a]` works, not just single digits.

```python
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
```

> **[VISUAL: add chunk 3.]** Open bracket — the key move going in. Save context, then reset to start fresh inside.

```python
        elif c == '[':
            stack.append((current, num))
            current = ""
            num = 0
```

> **[VISUAL: add chunk 4, highlight the stitch line.]** Close bracket — pop the context back and glue the inside in, repeated `k` times.

```python
        elif c == ']':
            prev, k = stack.pop()
            current = prev + k * current
        else:
            current += c        # ordinary letter
    return current
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `num = num * 10 + int(c)` — this isn't just "read a digit." Multiplying by ten shifts the old digits left so multi-digit counts like `100[a]` work. Drop the `*10` and `12` becomes a `1` then a `2`. Broken.
>
> `stack.append((current, num))` on `[` — this is the *pause* we struggled with by hand. We freeze exactly two things: the string built *before* this bracket, and how many times this new scope repeats. The machine remembers so we don't have to.
>
> `current = ""` right after — we start the inside with a blank slate. The old string is safe on the stack.
>
> `current = prev + k * current` on `]` — this is the whole payoff. `current` is now the fully-decoded inside. Multiply it by `k`, glue it *after* the `prev` we saved, and that becomes our new running string. Innermost resolved, back to the outer scope.
>
> **LEARNER:** Quick one — why `prev + k * current` and not `k * current + prev`? Does the order matter?
>
> **TEACHER:** It really does. `prev` is everything that came *before* the bracket — it has to stay on the left. In `a2[c]`, when we close, `prev` is `"a"` and `k*current` is `"cc"`. We want `acc`, not `cca`. Left-to-right order of the original string has to survive.

---

## 9. DRY-RUN THE CODE — `8:20`
*(worked example — prove it, close the loop)*

**[VISUAL: `3[a2[c]]` up top, a trace table filling row by row, the stack drawn as a growing/shrinking pile beside it.]**

> Let's run the actual code on `3[a2[c]]` and watch it land.

| char | num | current | stack | note |
|---|---|---|---|---|
| `3` | 3 | `""` | `[]` | build count |
| `[` | 0 | `""` | `[("", 3)]` | push, reset |
| `a` | 0 | `"a"` | `[("", 3)]` | append letter |
| `2` | 2 | `"a"` | `[("", 3)]` | build count |
| `[` | 0 | `""` | `[("", 3), ("a", 2)]` | push, reset |
| `c` | 0 | `"c"` | `[("", 3), ("a", 2)]` | append letter |
| `]` | 0 | `"acc"` | `[("", 3)]` | pop `("a",2)` → `"a" + 2·"c"` |
| `]` | 0 | `"accaccacc"` | `[]` | pop `("", 3)` → `"" + 3·"acc"` |

> Output: `accaccacc`. The inner `2[c]` became `cc`, that made `acc`, and the outer `3` tripled it. Exactly the string we were staring at in the cold open. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:20`
*(transfer to interview)*

**[VISUAL: two lines — Time: O(output length). Space: O(output length). A tiny note: input `10[10[10[a]]]` → 1000 chars.]**

> **TEACHER:** Say it the way you'd say it in the room: *"I touch each input character once, but the work is really proportional to the size of the decoded output — because I'm building every one of those characters. So time is O(output length). Space is O(output length) too, for the string I'm constructing plus the stack."*
>
> And flag the sneaky part out loud: the output can be *way* bigger than the input. `10[10[10[a]]]` is twelve characters in, a thousand `a`s out. That's the thing they want to hear you notice.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:55`
*(depth + honesty)*

**[VISUAL: the phrase "O(output) is INHERENT, not waste" boxed. Beside it: recursion (call stack, depth) vs explicit stack (heap, depth), a small scale balancing them.]**

> Here's the honest answer, and it's a strong one: **we can't beat O(output length) space — and that's not a flaw.** The problem *asks* us to return the whole decoded string. We have to build it. That memory is inherent to the task, not something we wasted. Naming that out loud is a senior move.
>
> The real choice is *which* stack. The recursive version uses the **call stack**, and its depth is the nesting depth — deeply nested input like `1[1[1[...]]]` can overflow it. Our explicit stack lives on the heap, same depth, no recursion-limit risk, and the LIFO intent is right there in the code.
>
> Say it in the room: *"The output space is unavoidable — I have to build the decoded string. Beyond that I'd choose the iterative stack over recursion so deep nesting can't blow the call stack."*
>
> **[GCA reminder — Google's Communication & Analysis:** Google literally scores *how you reason out loud*, not just whether the code runs. Saying "this space is inherent because the problem demands the full output" and "I'd pick iteration to avoid stack overflow" is exactly the kind of tradeoff narration that earns the checkmark. Think in a whisper — say it at full volume.**]**

---

## 12. YOUR TURN (active recall) — `10:25`
*(retrieval practice)*

**[VISUAL: "Your turn → Basic Calculator II (LC 227)". A blank editor.]**

> Before the next video, try **Basic Calculator II**. Same family — you keep a running value and a stack, and you resolve pieces in the right order. Different surface, same "stack to handle nested/pending work" instinct.
>
> Don't peek at the solution. Wrestle with it for ten minutes. That struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `10:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Nested / bracketed → innermost first → stack.** Last opened, first closed.
> 2. **Push context on `[`, pop-and-stitch on `]`.** `prev + k × current`, order matters.
> 3. **O(output) space is inherent** — you're required to build the decoded string; that's not waste.
>
> And the memory peg — when you see **brackets inside brackets**, your hand should already be reaching for a stack: **push going in, pop coming out.**

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: a new problem title blurred in: "Basic Calculator" with `2*(3+(4*5))` faintly visible.]**

> A stack just untangled nested repetition. But what happens when the nested thing isn't repetition — it's *arithmetic*, with `+`, `−`, `×`, and parentheses that change the order of operations? Same stack instinct, but now you're juggling operators and precedence. That's next: turning a stack into a calculator. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public String decodeString(String s) {
    Deque<String> strStack = new ArrayDeque<>();
    Deque<Integer> numStack = new ArrayDeque<>();
    StringBuilder current = new StringBuilder();
    int num = 0;
    for (char c : s.toCharArray()) {
        if (Character.isDigit(c)) {
            num = num * 10 + (c - '0');
        } else if (c == '[') {
            numStack.push(num);
            strStack.push(current.toString());
            current = new StringBuilder();
            num = 0;
        } else if (c == ']') {
            int k = numStack.pop();
            StringBuilder decoded = new StringBuilder(strStack.pop());
            for (int i = 0; i < k; i++) decoded.append(current);
            current = decoded;
        } else {
            current.append(c);
        }
    }
    return current.toString();
}
```
