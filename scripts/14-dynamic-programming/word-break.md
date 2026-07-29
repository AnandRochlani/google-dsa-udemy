# 🎬 Recording Script — Word Break
**Pattern: Dynamic Programming (over string prefixes) · LeetCode 139 · Medium · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** the "define dp[i] over a prefix and look back" idea from LIS; the "already-at-the-floor" space honesty from Coin Change.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides. **TEACHER** carries the thread; **LEARNER** is a sharp peer who speaks 3–5 times only.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: the string `leetcode`. A slicer cuts it: `leet | code`. Both light green against a dictionary panel {leet, code}.]**

> Can you slice a string into a sequence of real dictionary words? `"leetcode"` splits into `"leet"` and `"code"` — both in the dictionary — so yes.
>
> Sounds like simple string chopping. But try every possible set of cut points and you've got an exponential explosion — the same suffixes re-examined a thousand ways. The fix is a DP where the "table" is indexed by **positions in the string**. It's a mental leap from grids and staircases, and once it clicks, a whole class of "can this be segmented / partitioned" problems opens up. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: `s = "leetcode"`, dict `["leet","code"]` → true. Below: `s="catsandog"`, dict `[cats,dog,sand,and,cat]` → false.]**

> One line: **can `s` be broken into a sequence of one or more dictionary words**, each reusable any number of times? True or false.
>
> `"leetcode"` with `{leet, code}` → **true**. A trickier false: `"catsandog"` with `{cats, dog, sand, and, cat}` — you can make `cats`, `and`… but then `og` is left stranded. **False.** That near-miss is exactly what the DP has to catch.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — find the decision)*

**[VISUAL: cursor at the front of "leetcode". It tries prefixes: "l", "le", "lee", "leet" — "leet" flashes green (in dict), then recurse on "code".]**

> The decision: segment from the **front**. Try each prefix as the **first word** — if `s[0:k]` is in the dictionary, then recursively ask: can the *remainder* `s[k:]` also be segmented?
>
> **[VISUAL: boxed — "canBreak(start) = true if some s[start:end] is in dict AND canBreak(end)".]**
>
> "leet" is a word, so peel it off and ask about "code." "code" is a word, and the remainder is empty. Base case: an empty remainder is trivially breakable — `canBreak(len(s)) = True`. So the whole thing works.

---

## 4. THE PAIN POINT + PREDICT — `2:40`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: for `"aaaaab"` with dict {a, aa, aaa}, a recursion tree explodes — many different splits all funnel into the SAME suffix position, highlighted identically.]**

> **TEACHER:** Watch this blow up. Take `"aaaaab"` with dictionary `{a, aa, aaa}`. From the front you can peel "a", or "aa", or "aaa" — and each choice leaves a suffix that *itself* forks the same way. Tons of different cut-combinations all funnel into the **same** suffix positions, recomputed from scratch. Exponential.
>
> **LEARNER:** But the state is really simple here, isn't it? Whether a suffix is breakable depends only on **where it starts** — a single index. It doesn't matter *how* I got there.
>
> **TEACHER:** That's the whole insight, and it's the leap of this lesson. The state is *one number* — a position in the string. There are only `n+1` positions, so there are only `n+1` distinct subproblems, no matter how many paths reach them.
>
> Predict: the state is a single index. **So what does the table look like?** Pause.
>
> *(3-second think timer)*

---

## 5. BUILD THE INTUITION (the aha) — `3:35`
*(elaboration — derive the prefix table)*

**[VISUAL: a boolean array dp[0..8] under the characters of "leetcode". dp[0] = True (green).]**

> **TEACHER:** A 1-D boolean array. Let's define it as `dp[i]` = "can the **first `i` characters**, `s[:i]`, be fully segmented?" Seed `dp[0] = True` — the empty prefix is trivially segmentable.
>
> Now fill left to right. `dp[i]` is True if there's some split point `j` where two things hold: `dp[j]` is already True (the front part segments) **and** `s[j:i]` is a dictionary word (the piece from `j` to `i` is one valid word).
>
> **[VISUAL: dp fills. dp[4] turns green because dp[0]=True and s[0:4]="leet" is a word. dp[8] turns green because dp[4]=True and s[4:8]="code" is a word.]**
>
> `dp[4]` goes True: `dp[0]` is True and `"leet"` is a word. Then `dp[8]` goes True: `dp[4]` is True and `"code"` is a word. Answer is `dp[8]` — **true**.

---

## 6. THE KEY MOVE (signaling) — `4:45`
*(one crisp, repeatable sentence)*

**[VISUAL: boxed — "dp[i] = OR over j < i of ( dp[j] AND s[j:i] in dict ). Answer = dp[n]."]**

> The line: **a prefix is breakable if some earlier breakable point is followed by a single dictionary word reaching here.** Combine an already-solved front with one valid word on the end.
>
> And a free but crucial detail: dump the dictionary into a **set** first, so each "is this a word?" check is O(1). A list would make it linear and quietly wreck your complexity.

---

## 7. CODE IT — LIVE & CHUNKED — `5:20`
*(cognitive load — build in pieces)*

**[VISUAL: editor. Type chunk 1.]**

> Set the dictionary up for fast lookups, seed the array.

```python
def word_break(s, wordDict):
    words = set(wordDict)              # O(1) membership
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True                       # empty prefix is segmentable
```

> **[VISUAL: add chunk 2, highlight.]** For each end position, look back for a valid split.

```python
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break                  # one valid split is enough
    return dp[n]
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:20`
*(elaboration — why each line exists)*

**[VISUAL: the two-pointer sweep i and j over the string; spotlight the substring s[j:i].]**

> The *why*:
>
> `words = set(...)` — the O(1) lookup that keeps the whole thing efficient.
>
> `dp[0] = True` — the anchor. Every valid segmentation ultimately chains back to "the empty prefix works."
>
> `for j in range(i)` — the split point. `dp[j]` asks "is the front breakable?" and `s[j:i]` is the candidate last word.
>
> `break` — the instant *one* valid split is found, `dp[i]` is settled True; no need to check other split points.
>
> **LEARNER:** Objection — why iterate `i` **outer**, `j` **inner**? My gut wanted to recurse forward from the start, not build up prefixes.
>
> **TEACHER:** Because bottom-up needs every subproblem `dp[j]` *finished* before the cell that uses it. `dp[i]` reads `dp[j]` for all `j < i`, so if `i` grows on the outside, every `dp[j]` it needs is already computed. Recursing forward works too — that's the top-down memoized version — but the table form demands "small prefixes first," and that's why `i` is the outer loop. It's the same "solve dependencies first" rule behind every bottom-up DP.

---

## 9. DRY-RUN THE CODE — `7:40`
*(worked example — prove it, close the loop)*

**[VISUAL: the boolean array filling under "leetcode".]**

> Run `"leetcode"`, dict `{leet, code}`:

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| prefix | "" | l | le | lee | leet | leetc | leetco | leetcod | leetcode |
| dp[i] | T | F | F | F | **T** | F | F | F | **T** |

> `dp[4]` flips True at `"leet"` (front `dp[0]` True). Then `dp[8]` flips True at `"code"` (front `dp[4]` True). `dp[8]` is the answer — **true**. And for `"catsandog"`, `dp[9]` would stay False because "og" is never a word. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `8:30`
*(transfer to interview)*

**[VISUAL: rows — Brute: O(2ⁿ). DP: O(n²·L) time, O(n) space.]**

> To the interviewer: *"Naive recursion re-explores the same suffixes exponentially. The DP has n positions, each scanning up to n split points, and each substring check costs up to L — so O(n² · L) time, O(n) space for the boolean array plus the word set."*
>
> Naming the `L` — the substring-build-and-lookup cost — shows you're not hand-waving the hidden work inside `s[j:i]`.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:00`
*(depth + honesty — the strong beat)*

**[VISUAL: dp array with an arrow from dp[i] reaching ALL the way back to dp[0] — a word can be arbitrarily long. No fixed window.]**

> The honest space beat — same shape as Coin Change, and saying it well is the skill. Can we roll this into O(1) like the staircase? No. `dp[i]` can depend on **any** earlier `dp[j]`, because a dictionary word can be as long as the entire string — the reach isn't a fixed window. So `O(n)` is the **floor**.
>
> *"Space is O(n) and that's the floor — a word can span from any earlier boundary all the way to here, so dp[i] may reference any previous entry. No constant-size rolling window applies."*
>
> What you *can* trim is **time**: only look back as far as the **longest dictionary word**, since no valid last word can be longer than that.

```python
def word_break(s, wordDict):
    words = set(wordDict)
    max_len = max((len(w) for w in words), default=0)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(max(0, i - max_len), i):   # only look back one max-word
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[n]
```

> Same O(n) space, but the inner loop is now bounded by the longest word instead of the whole prefix. Say it: *"Space is fixed at O(n); I optimize time by bounding the look-back to the max word length."*

---

## 12. YOUR TURN (active recall) — `10:15`
*(retrieval practice)*

**[VISUAL: "Your turn → Palindrome Partitioning II (LC 132)". A string split into palindromes.]**

> Before the next video: **Palindrome Partitioning II** — minimum cuts to split a string so every piece is a palindrome. It's *this exact split-point DP*, but the predicate changes from "is it a dictionary word?" to "is `s[j:i]` a palindrome?", and instead of true/false you minimize the number of cuts. Same skeleton, new test and a min. Try wiring it up.

---

## 13. LOCK IT IN — `10:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three takeaways:
> 1. **State = a single position in the string.** `dp[i]` = "is `s[:i]` segmentable?"
> 2. **Split-point recurrence:** breakable front (`dp[j]`) + one valid word (`s[j:i]`). Dictionary in a **set**.
> 3. **Space floor is O(n)** — words can reach any earlier boundary; optimize *time* by bounding the look-back.
>
> Memory peg — *"can this string be chopped into valid pieces?"* → **prefix DP: an old True plus one good word reaching here.**

---

## 14. CLIFFHANGER — `11:25`
*(open loop to next lesson)*

**[VISUAL: blurred title — "Best Time to Buy and Sell Stock". A price chart with buy/sell markers.]**

> We've filled tables of counts, booleans, and minimums. Our last DP flips the framing entirely: instead of an array of subproblems, you track *what state you're in* on each day — holding a stock or not — and the whole "table" shrinks to a couple of variables. That's the state-machine DP behind buying and selling stock. A perfect finale. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public boolean wordBreak(String s, List<String> wordDict) {
    Set<String> words = new HashSet<>(wordDict);
    int n = s.length();
    boolean[] dp = new boolean[n + 1];
    dp[0] = true;
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < i; j++) {
            if (dp[j] && words.contains(s.substring(j, i))) {
                dp[i] = true;
                break;
            }
        }
    }
    return dp[n];
}
```
