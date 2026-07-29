# 🎬 Recording Script — Valid Parentheses
**Pattern: Stacks · LeetCode 20 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Core idea thread:** *the most-recent-unmatched thing lives on top of a stack.*

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an editor. The string `"([)]"` glows in the middle. A cursor blinks. A green "valid?" question mark pulses beside it.]**

> Google phone screen, minute three. *"Given a string of brackets, tell me if it's valid."*
>
> Easy, right? You think: count the open ones, count the close ones, make sure they match. You type it. And then the interviewer drops this on you — `"([)]"`.
>
> **[VISUAL: highlight — one `(`, one `)`, one `[`, one `]`. Counts all equal 1.]**
>
> Every count is equal. One of each. And it's *invalid*. Your counting idea just died on screen. By the end of this video you'll know the one data structure that makes this trivial — and *why* it's the answer, not just that it is. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one plain sentence up top. Below it two strings: `"([{}])"` in green, `"([)]"` in red.]**

> Here's the whole problem in one line: **a string is valid if every bracket closes with the same type, in the right order.**
>
> Right order means the *most recently opened* bracket is the *first one closed*. Look at the green one — `([{}])`. You open round, square, curly… then close curly, square, round. Perfect nesting. Valid.
>
> The red one — `([)]` — you open round, then square, then try to close round. But square was opened *after* round, so square is still hanging open. You can't reach past it. Invalid.
>
> Hold onto that phrase: **most recently opened, first to close.** That's the entire lesson.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — let them feel the waste)*

**[VISUAL: the string `"([{}])"`. A brute-force idea appears: "find any adjacent matched pair, delete it, repeat."]**

> Okay, counting is out. What's the next honest instinct? Cancel matched pairs. Find an adjacent `()` or `[]` or `{}`, erase it, and repeat until nothing changes.
>
> **[VISUAL: `([{}])` → erase `{}` → `([])` → erase `[]` → `()` → erase `()` → `""`.]**
>
> Watch it collapse. `([{}])` — the `{}` in the middle is a matched pair, wipe it. Now `([])`. The `[]` is adjacent, wipe it. Now `()`. Wipe it. Empty string. Valid!
>
> **[VISUAL: a "re-scans" counter ticking up: 1, 2, 3… as the string is rebuilt each pass.]**
>
> It works. But feel the waste — every single erase rebuilds the *whole* string and re-scans from the start. Deep nesting like `(((…)))` means a pass per layer, each pass walking the whole thing. That's O(n²), and it's fiddly with string slicing.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the collapsing string. Highlight that we keep re-scanning from the left. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** So where's the waste? Every erase, we throw away everything we learned and re-scan the whole string looking for the next matched pair.
>
> **LEARNER:** Wait — but when I erase `{}`, doesn't the answer for *that* part just… disappear? What is there even to remember?
>
> **TEACHER:** That's exactly the instinct to break. Something *is* worth remembering. Pause the video and think: as I read left to right, when a closing bracket shows up, **which single opening bracket is it allowed to close?** Not "which one exists" — which *one specific* one?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:10`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: a vertical column of tiles labeled "STACK", empty, sitting to the right. Bottom is the floor; new tiles land on top.]**

> Here's the answer to that question. A closing bracket can only ever close the **most recently opened** bracket that's still unmatched. Nothing else.
>
> Think of a stack of plates. You add plates to the top; you take from the top. The last plate you set down is the first one you pick up. That's called **Last-In-First-Out** — LIFO — and it's the whole shape of this problem.
>
> **[VISUAL: read `([{}])` left to right. Each opener drops a tile onto the column: `(` lands, `[` on top of it, `{` on top of that. Column grows up.]**
>
> Walk it. See `(` — it's open and unmatched, so drop it on the stack. See `[` — drop it on top. See `{` — drop it on top. The column is growing. The tile on **top** is always the most-recent thing still waiting to be closed.
>
> **[VISUAL: now `}` arrives. It "reaches" for the top tile `{`. Match! The `{` tile lifts off. Column shrinks.]**
>
> Now `}` shows up. Look only at the top — it's `{`. Same type! They cancel. Pop the `{` off; the column shrinks. Then `]` comes — top is now `[`, match, pop. Then `)` — top is `(`, match, pop. Column empty. Valid.
>
> No re-scanning. Each bracket is touched once. The stack *remembers* the unmatched openers for us, newest on top.

---

## 6. THE KEY MOVE (signaling) — `4:30`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "Push openers. On a closer, the top MUST be its match — pop it. End empty = valid."]**

> Burn this in: **push every opener; when a closer arrives, the top of the stack must be its matching opener — pop it; if it isn't, fail; and the stack must end empty.**
>
> That one sentence is the whole algorithm. Everything else is typing.

---

## 7. CODE IT — LIVE & CHUNKED — `5:05`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, a map from each closer to its opener, and an empty stack.

```python
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}   # closer -> its opener
    stack = []
```

> **[VISUAL: add chunk 2, highlight it. The stack column appears on the right.]** Now walk the string. If the character is a closer — it's a key in our map — we check the top.

```python
    for ch in s:
        if ch in pairs:                       # ch is a closing bracket
            top = stack.pop() if stack else "#"
            if pairs[ch] != top:
                return False
```

> **[VISUAL: add chunk 3.]** Otherwise it's an opener — just drop it on the stack.

```python
        else:                                 # ch is an opening bracket
            stack.append(ch)
    return not stack                          # valid only if nothing left open
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk the *why*.
>
> `pairs` maps closer to opener, so when I see `)` I instantly know I need a `(` on top. One lookup, both checks — right type *and* right order — in a single move.
>
> `stack.append(ch)` for openers — that's "the newest unmatched thing goes on top."
>
> The closer branch is the heart. `stack.pop()` grabs the most recent opener. If it's the matching one, great, it's consumed. If not, `return False` — fail fast.
>
> **LEARNER:** Hold on — that `stack.pop() if stack else "#"`. Why the `"#"`? Why not just check if the stack is empty?
>
> **TEACHER:** Sharp. If a closer shows up and the stack is *empty* — like the string `")("` — there's no opener to match, so it's already invalid. The `"#"` is a sentinel: a fake top that can never equal any real opener, so the very next line fails cleanly. It saves us writing a separate empty-check. Same effect, one line.
>
> And `return not stack` — if anything's *left* on the stack, some opener never got closed, like `"((("`. Only an empty stack means everything matched.

---

## 9. DRY-RUN THE CODE — `7:00`
*(worked example — prove it, close the loop)*

**[VISUAL: string `"([{}])"`; the stack column on the right growing and shrinking; a trace table filling row by row.]**

> Let's run the real code on `([{}])`. Watch the column.

| char | action | stack (bottom→top) |
|---|---|---|
| `(` | opener → push | `(` |
| `[` | opener → push | `( [` |
| `{` | opener → push | `( [ {` |
| `}` | closer → pop `{`, matches ✅ | `( [` |
| `]` | closer → pop `[`, matches ✅ | `(` |
| `)` | closer → pop `(`, matches ✅ | *(empty)* |

> Stack empty at the end → **`true`**. And the red case `([)]`? At the `)`, the top is `[` — `pairs[")"]` wants `(`, but top is `[`. Mismatch → **`false`** instantly. Loop closed: the counting trap from the cold open is dead, and we see exactly why.

---

## 10. COMPLEXITY, OUT LOUD — `7:45`
*(transfer to interview)*

**[VISUAL: two rows — Brute (repeated replace): O(n²). Ours (stack): O(n) time, O(n) space.]**

> Say it the way you'd say it in the room: *"The repeated-erase brute force is O(n squared) because each pass rebuilds the string. The stack does one pass — every character is pushed and popped at most once — so it's O(n) time, and O(n) space for the stack."*
>
> That contrast, brute to stack, is exactly what an interviewer wants to hear.

---

## 11. CAN WE USE LESS MEMORY? (space) — `8:10`
*(depth + honesty)*

**[VISUAL: a string of all openers `"((((("`; every tile stacks up, column tall.]**

> Can we beat O(n) space? Honestly, no — and knowing *why* is a strong-hire detail.
>
> Picture `"((((("` — all openers. You genuinely have to remember every one until its closer shows up. There's no shortcut.
>
> **LEARNER:** But couldn't I just use a *counter* instead of a stack — plus one for open, minus one for close?
>
> **TEACHER:** You could — *if there were only one bracket type.* With just `(` and `)`, a counter is O(1) and perfect. But the moment you have three types, a counter can't tell a `[` from a `{`. You need the stack to remember *which kind* is open. So: *"one type, O(1) counter; three types, O(n) stack, and it's unavoidable."*

---

## 12. YOUR TURN (active recall) — `8:35`
*(retrieval practice)*

**[VISUAL: "Your turn → Remove All Adjacent Duplicates in String (LC 1047)". A blank editor.]**

> Before the next video, try **Remove All Adjacent Duplicates in String**, LC 1047. Same move: walk the string, and when the current character matches the top of the stack, pop instead of push. It's this exact "cancel with the top" idea in a new outfit.
>
> Don't peek at the solution. Wrestle with it for ten minutes — that struggle is what turns "I watched it" into "I own it."

---

## 13. LOCK IT IN — `8:55`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things to keep:
> 1. **Counting fails because order matters** — `")("` proves it.
> 2. **A closer can only close the most-recent opener** — that's LIFO, that's a stack.
> 3. **End empty or it's invalid.** Leftover openers = unclosed.
>
> And the peg — when you hear *"match things in nested order,"* your hand should already be reaching for a stack: **the most-recent-unmatched thing lives on top.**

---

## 14. CLIFFHANGER — `9:15`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Min Stack". A stack with a mysterious second column labeled "min?"]**

> So a stack answers "what's on top" in O(1). But what if the interviewer says: *"give me the smallest element in the stack — also in O(1), at any moment, no scanning"*? A plain stack can't do that. The fix is a beautiful little trick where a *second* stack shadows the first. That's next: Min Stack. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public boolean isValid(String s) {
    Deque<Character> stack = new ArrayDeque<>();   // ArrayDeque as a stack
    for (char c : s.toCharArray()) {
        if (c == '(') stack.push(')');
        else if (c == '[') stack.push(']');
        else if (c == '{') stack.push('}');
        // for a closer: it must equal what we expect on top
        else if (stack.isEmpty() || stack.pop() != c) return false;
    }
    return stack.isEmpty();
}
```

*(Neat trick: push the **expected closer** when you see an opener, so the closing check is a single equality.)*
