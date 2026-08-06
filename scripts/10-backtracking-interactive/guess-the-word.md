# 🎬 Recording Script — Guess the Word
**Pattern: Interactive minimax / information-narrowing search · LeetCode 843 · Hard · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Robot Room Cleaner — the same genre (an API instead of an input), but there we rebuilt a *map*; here we spend *information*.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an editor. A list of 100 six-letter words scrolls past, blurring. Above it, one line: `master.guess(word) → int`. Beside it a counter: `guesses left: 10`. The counter ticks 10, 9, 8… and hits 0 with a red "LOST".]**

> One of these hundred words is the secret. You get **ten guesses**. Guess a word and the machine tells you one thing — how many letters you got in the right position. That's the whole interface.
>
> **[VISUAL: `guesses left: 10` resets, glowing.]**
>
> Ten tries, a hundred words. Most people do the arithmetic, decide it's a ten percent lottery, and start guessing. I ran that strategy two thousand times. It won **nine percent** of the time — the lottery, exactly.
>
> But here's the twist that makes this a Google problem. That number coming back isn't a *score*. It's a **filter** — and a good guess can delete eighty words at once while a bad guess deletes exactly one. By the end of this video you'll know how to tell those two apart *before* you spend one — and why this is the same idea as binary search wearing a very strange hat. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below, a tiny pool of just four words, big monospace:]**

```
words  = [ acckzz , ccbazz , eiowzz , abcbzz ]
secret = ??????
master.guess(w) → # of positions that match exactly   (6 = you win)
```

> The whole problem in one line: **find the secret word within ten calls to `master.guess`.**
>
> Every word is exactly six lowercase letters, and the secret is one of the words in the list — that second fact matters enormously, and we'll lean on it hard. Be careful what the number means, though: it counts **exact positional matches**. Not shared letters. Not anagram overlap. Position by position, same letter, same slot.
>
> **[VISUAL: `eiowzz` above `acckzz`, aligned in a 6-column grid. Columns 1–4 flash red, columns 5 and 6 flash green. A big "2" appears.]**
>
> Guess `eiowzz` when the secret is `acckzz`, and only the trailing `z`, `z` line up. The master says **2**.
>
> Now hold on to something — notice what I *didn't* say. I never said this was slow. At most a hundred words, six letters each: comparing every pair is sixty thousand character checks. Microseconds. **Compute is free in this problem.** The only thing you're short of is guesses.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — feel the waste)*

**[VISUAL: the 100-word pool. Words get crossed out one at a time as a "guesses left" counter drops. After 10, 90 words remain uncrossed. Red "LOST".]**

> Let's do what your brain does first. Guess a word. Not it? Guess the next one.

```python
def findSecretWord_brute(words, master):
    for w in words[:10]:              # ten shots, zero learning
        if master.guess(w) == 6:
            return
```

> Guess one. The master says… `2`. Not it, move on. Guess two — `0`. Not it. Guess three — `3`. Not it.
>
> **[VISUAL: each reply — 2, 0, 3, 1 — appears next to a crossed-out word, then fades to grey and vanishes. They pile up in a bin labelled "information we threw away".]**
>
> Watch what's happening to those numbers. `2`. `0`. `3`. They arrive… and we bin them. The only thing this code ever asks is *"is it six?"*
>
> Ten guesses, ninety words still standing. Simulated over two thousand rounds: **nine point one five percent** — exactly the `10 out of 100` you'd predict, because we're literally playing a lottery. This isn't a speed problem. It's a **learning** problem.

---

## 4. THE PAIN POINT + PREDICT — `2:20`
*(close loop #1 + generation effect — pause #1)*

**[VISUAL: freeze. Two words stacked and aligned, `eiowzz` over `acckzz`, with the big "2" between them. A 5-second "🤔 your turn" timer.]**

> **TEACHER:** So let's actually look at that discarded number. I guessed `eiowzz`, and the master said **2**. In plain English the master just told me: *"the secret word shares exactly two positions with `eiowzz`."*
>
> **LEARNER:** Right, but that's a fact about the *secret*, and I don't know the secret. How does knowing something about a word I can't see help me?
>
> **TEACHER:** That is the exact right question, and it's the whole first half of this lesson. Here's the nudge: **I can't test that fact against the secret — but I can test it against every word in my list.** Pause the video. If the secret shares exactly two positions with `eiowzz`, what does that let me say about a word in my list that shares *four* positions with `eiowzz`?
>
> **[VISUAL: the word list, with `eiowzz` circled. Beside three other words, their scores against it: 2, 4, 2. The "4" pulses.]**
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the four-word pool. `eiowzz` circled as the guess. Each other word gets a score badge. Words whose badge ≠ 2 slide off screen into a bin labelled "provably not the secret".]**

> **TEACHER:** Here's the move. The secret scores `2` against `eiowzz`. A word that scores `4` against `eiowzz` therefore **cannot be the secret** — provably, with certainty. Not "unlikely." **Impossible.** So one guess doesn't test one word. It **sorts the entire list into buckets** by score, and the reply tells you which bucket the secret is hiding in. Keep that bucket, delete everything else.
>
> **[VISUAL: the pool fans into 7 labelled bins, 0 through 6. The reply "2" lights bin 2 green; the rest go red and vanish.]**
>
> And it's airtight. `match` counts equal positions, so `match(guess, secret)` and `match(secret, guess)` are the same number — the secret **always** survives its own filter. You can never accidentally delete the answer. That one idea takes us from nine percent to about **ninety-four percent**. Enormous. And still not enough — because look at what I just did.
>
> **[VISUAL: a six-word pool as a matrix of pairwise scores. The `eiowzz` row is highlighted — it reads 2, 2, 2, 2, 2.]**
>
> **TEACHER:** I picked `eiowzz` arbitrarily. Its row scores **2 against every other word in the pool.** The master says "2" and every word lands in the same bucket. Nothing gets deleted except the guess itself — one of my ten lives, for one word.
>
> **LEARNER:** But the pool *does* still shrink by one every time. Ten guesses, ten words gone. Isn't that just slow, rather than broken?
>
> **TEACHER:** That's the tempting wrong idea, and it's worth killing properly. Shrinking by one is **arithmetic**. You need shrinking by a **factor**. A hundred minus ten is ninety — you lose. A hundred *divided* by three, six times over, is one — you win. Same ten guesses, completely different math.
>
> **[VISUAL: two shrinking bars race. "minus one" barely moves; "divide by three" collapses to nothing.]**
>
> **TEACHER:** So — pause number two, the real one. Compare the row for `eiowzz`, all 2s, with the row for `acckzz`, which reads 3, 4, 2, 5, 4. **Which is the better guess, and — say it precisely — what quantity are you actually comparing?**
>
> **[VISUAL: the two rows side by side. Blank space labelled "what makes a probe good?" A 6-second timer.]**
>
> *(pause)*

---

## 6. THE KEY MOVE (signaling) — `4:40`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "bucket the pool by score against w · worst case = biggest bucket · guess the w whose biggest bucket is smallest."]**

> Here it is. Before you spend a guess on a word `w`, **imagine** guessing it. The reply drops you into exactly one bucket — and that bucket *becomes your entire new pool*. You don't get to choose which. So assume the worst: the **biggest** bucket. **The worst case of guessing `w` is the size of `w`'s largest bucket.** Pick the `w` whose largest bucket is smallest.
>
> **[VISUAL: `eiowzz` → one bucket of 5, red. `acckzz` → buckets of 1, 1, 2, 1, green.]**
>
> That's **minimax** — minimise the maximum. Burn this line in: **choose the probe that leaves the fewest survivors in the unluckiest case.**
>
> And you already know this idea. **Binary search.** Why the midpoint? Not tradition — the midpoint is the split whose *larger half* is smallest. Same rule. Wordle, Mastermind, twenty questions, medical triage: whenever you can only probe, you pick the probe that best splits the world.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it in four small pieces. First, the helper the whole problem runs on — how many positions match.

```python
def match(a, b):
    """How many positions hold the same letter?"""
    return sum(x == y for x, y in zip(a, b))
```

> **[VISUAL: add chunk 2, highlight it.]** Now the scoring function — the one that decides which probe to spend. Bucket the pool by score against `w`, and report the biggest bucket.

```python
def findSecretWord(words, master):
    candidates = words

    def worst_case_size(w):
        buckets = [0] * 7
        for v in candidates:
            buckets[match(w, v)] += 1
        return max(buckets[:6])       # bucket 6 is w itself — that reply means we won
```

> **[VISUAL: add chunk 3. The `min(...)` line highlighted first, then the last line highlighted separately.]** And the main loop — ten rounds. Pick the best probe, spend it, and if we didn't win, run the filter that does the actual deleting.

```python
    for _ in range(10):
        guess = min(candidates, key=worst_case_size)
        k = master.guess(guess)
        if k == 6:
            return                    # solved
        candidates = [w for w in candidates if match(w, guess) == k]
```

> That's the entire solution. Nine lines of logic.

---

## 8. EXPLAIN THE CODE (the WHY) — `7:05`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not what. `min(candidates, key=worst_case_size)` — this is the entire Hard part. Delete it, guess `candidates[0]` instead, and the code still runs and still returns right answers — it just drops from ninety-nine percent to ninety-four. It's the difference between filtering well and **probing** well.
>
> **LEARNER:** Hold on — `max(buckets[:6])`. Why cut off bucket six? That looks like an off-by-one waiting to happen.
>
> **TEACHER:** Great catch, and it's deliberate. Bucket six holds words scoring a perfect six against `w` — and since the words are distinct, that's `w` and only `w`. But if the master ever *replies* six, we've **won** and returned. Including it would penalise a good guess for the crime of possibly being correct. We minimise the worst case among the replies that leave us still playing.
>
> `for w in candidates` inside `worst_case_size` — we score every candidate against every candidate. That's `N²`, and I want you **comfortable** with that: sixty thousand comparisons a round, six hundred thousand across all ten, microseconds. **We are deliberately spending free compute to save a scarce guess** — naming that trade out loud is a strong signal by itself.
>
> `candidates = [w for w in candidates if match(w, guess) == k]` — the filter. Two properties carry the whole proof. The secret **always** passes, because `k` *is* the secret's score against the guess. And the guess itself **always** fails whenever `k < 6`, because a word scores six against itself. So the pool provably shrinks every round and can never lose the answer.

---

## 9. DRY-RUN THE CODE — `8:25`
*(worked example — prove it, close the loop)*

**[VISUAL: a six-word pool. Beside each word, its scores against the other five, then those scores collapsing into buckets.]**

> Let's run the real code on six words. For each word, here are its scores against the other five — and that list of scores **is** the partition it would produce:

| Guess | Scores vs. the other five | Buckets (score → count) | Worst case |
|---|---|---|---|
| `ccbazz` | 3, 2, 2, 2, 5 | 2→3, 3→1, 5→1 | 3 |
| **`acckzz`** | 3, 4, 2, 5, 4 | 2→1, 3→1, 4→2, 5→1 | **2** ✅ |
| `abcbzz` | 2, 4, 2, 5, 2 | 2→3, 4→1, 5→1 | 3 |
| `eiowzz` | 2, 2, 2, 2, 2 | 2→**5** | **5** ❌ |
| `abckzz` | 2, 5, 5, 2, 3 | 2→2, 3→1, 5→2 | 2 |
| `ccbkzz` | 5, 4, 2, 2, 3 | 2→2, 3→1, 4→1, 5→1 | 2 |

> There it is in one table. `eiowzz` scores 2 against everything — one bucket of five, the worst possible probe. `acckzz` splits the pool four ways, so **no reply can leave more than two candidates alive.** The code picks `acckzz`.
>
> **[VISUAL: trace table filling row by row; the pool visibly shrinking beside it.]**

| Round | Pool | Guess (worst case) | Master says | Survivors |
|---|---|---|---|---|
| 1 | all 6 | `acckzz` (2) | `4` | `abcbzz`, `ccbkzz` |
| 2 | 2 | `abcbzz` (1) | `2` | `ccbkzz` |
| 3 | 1 | `ccbkzz` (0) | `6` | 🎉 won |

> Six words, **three** guesses, seven to spare. And at a hundred words, here's the measured median trajectory — minimax against the arbitrary pick:

```
round:      0     1     2     3     4    5    6    7
minimax:  100 →  67 →  22 →  10 →   4 →  2 →  1 →  done
arbitrary:100 →  77 →  54 →  16 →   9 →  5 →  3 →  3   ← stalls
```

> Look at that bottom row. It **stalls at three** and runs out of clock. That's the loop we opened at the start: the bad strategy isn't slower — it stops making progress.

---

## 10. COMPLEXITY, OUT LOUD — `9:35`
*(transfer to interview)*

**[VISUAL: three rows — Blind: O(1) guesses, ~9% win. Filter only: O(R·N·L), ~94%. Minimax: O(R·N²·L), ~99.7%. A note: "60,000 comparisons per round — microseconds."]**

> Say it the way you'd say it in the room: *"Each round I score every candidate against every candidate — that's O(N² · L), and with at most ten rounds it's O(10 · N² · L). Concretely, a hundred words times a hundred words times six letters is sixty thousand comparisons a round, six hundred thousand total — microseconds. Space is O(N) for the candidate pool."* Then add the sentence that shows you understand what problem you're actually in: *"I'm deliberately trading compute for guesses. Compute is free at N = 100; the ten-guess budget is the real constraint."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `10:15`
*(depth + honesty — and one important correction)*

**[VISUAL: the candidate list; a "shrink it?" bubble; then the list relabelled "everything I currently know".]**

> Can we shrink the space? The pool is `O(N)` — and it isn't overhead, it's **my entire knowledge state**: the set of worlds still consistent with every answer I've received. Forget part of it and I either delete the true secret, or keep words I've already disproved and waste guesses on them. One real refinement: stop allocating a fresh list each round and **filter in place**, compacting survivors to the front. Same `O(N)`, but `O(1)` auxiliary.
>
> **LEARNER:** Okay — so with minimax, am I *guaranteed* to win in ten?
>
> **TEACHER:** No. And say that out loud in the interview, because it's the strongest thing you can say. Minimax minimises the worst case **per probe**; it doesn't prove ten probes are enough. I ran it two thousand times: **99.7%**. Not a hundred.
>
> **[VISUAL: a pool where every pair of words scores 0 against every other. Each guess kills exactly one word.]**
>
> **TEACHER:** The killer case is a pool where every pair shares **zero** positions. Every guess returns zero and kills exactly one word. No strategy on Earth wins that — there's simply no information in the pool to extract. Minimax is the right greedy, not a proof. *"This is the best probe I can choose, not a guarantee"* is a senior-engineer sentence.
>
> One pragmatic footnote: a cheaper `O(N·L)` heuristic — score words by how **common their letters are** at each position, guess the most typical — measured **99.8%** in the same test. Same instinct: a guess made of rare letters comes back zero and teaches you nothing. Lead with minimax because it has a *reason*; mention the heuristic because it shows range.

---

## 12. YOUR TURN (active recall) — `10:55`
*(retrieval practice)*

**[VISUAL: "Your turn → Leftmost Column with at Least a One (LC 1428)". A blank editor with `BinaryMatrix.get(row, col)` floating above it.]**

> Before the next video, try **Leftmost Column with at Least a One**. Another interactive: a hidden binary matrix, every row sorted, one API — `get(row, col)` — and a budget of a thousand calls. Same reflex, different costume. Ask the question from today: **what does one probe eliminate, and which probe eliminates the most?** You'll find each call kills an entire row or an entire column, and the whole solution is a staircase walk from one corner.
>
> And if today felt steep, warm up on **Guess Number Higher or Lower** — LC 374. It's this exact lesson with everything stripped away: the reply partitions the space, and the midpoint is minimax. Ten minutes of wrestling beats an hour of watching.

---

## 13. LOCK IT IN — `11:25`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **The reply is a filter, not a score.** If the secret scores `k` against your guess, every word scoring anything else is **provably** eliminated — and the secret always survives, because `match` is symmetric.
> 2. **Choose the probe before you spend it.** Bucket the pool by score against `w`; the worst case is `w`'s biggest bucket. Pick the word whose biggest bucket is smallest.
> 3. **Shrink by a factor, not by one.** A hundred minus ten is ninety and you lose. A hundred divided by three, six times, is one and you win.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "When you can only probe, pick the probe with the smallest worst case."]**
>
> That's binary search's midpoint. That's Wordle. That's Mastermind. Whenever a problem gives you a hard budget of questions, stop asking *"what should I guess?"* and start asking *"which question splits the world most evenly?"*
>
> *(GCA reminder — for the interview itself: open by naming the constraint inversion out loud. "N is only 100, so compute is free; the ten guesses are the scarce resource." Then walk the two leaps in order — the reply is a filter, then the probe is a choice — and finish by volunteering that minimax is a greedy, not a guarantee. Google's General Cognitive Ability signal isn't the nine lines of code. It's you identifying which resource is actually scarce, and admitting the limits of your own strategy.)*

---

## 14. CLIFFHANGER — `12:10`
*(open loop to next lesson)*

**[VISUAL: the interactive section closes with a checkmark. A new title blurs in: "Maximum Number of Visible Points" — a scatter of points on a plane, and a viewing cone sweeping around a fixed observer.]**

> That closes the interactive section. Two problems, one instinct: an API instead of an input. Robot Room Cleaner made us build a **map** we couldn't see; Guess the Word made us spend **information** we couldn't see. Different currencies, same reflex — you get a probe, so make the probe count. Next section, everything flips. You get the **entire input**, all of it, right there in the parameter list. No hidden anything. And it's still hard — because the data is a cloud of points on a plane, and the question is: standing at one spot, rotating your head, **how many can you see at once?**
>
> **[VISUAL: the cone rotates; points light up and go dark. The angle numbers wrap past 360 and glitch.]**
>
> Suddenly the trouble isn't blindness — it's **geometry**. Angles that wrap around at 360 and break your sorting. Points sitting exactly on top of you that belong to no angle at all. A sliding window that has to run around a circle instead of along a line. That's **Maximum Number of Visible Points**, and it opens Section 11. Full information, and you'll still have to earn it. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class Solution {
    public void findSecretWord(String[] words, Master master) {
        List<String> candidates = new ArrayList<>(Arrays.asList(words));
        for (int round = 0; round < 10 && !candidates.isEmpty(); round++) {
            String guess = pickMinimax(candidates);
            int k = master.guess(guess);
            if (k == 6) return;                          // solved

            List<String> next = new ArrayList<>();
            for (String w : candidates)
                if (match(w, guess) == k) next.add(w);   // keep only consistent words
            candidates = next;
        }
    }

    /** Choose the word whose largest same-score bucket is smallest. */
    private String pickMinimax(List<String> candidates) {
        String best = candidates.get(0);
        int bestWorst = Integer.MAX_VALUE;
        for (String w : candidates) {
            int[] buckets = new int[7];
            for (String v : candidates) buckets[match(w, v)]++;
            int worst = 0;
            for (int k = 0; k < 6; k++) worst = Math.max(worst, buckets[k]);
            if (worst < bestWorst) { bestWorst = worst; best = w; }
        }
        return best;
    }

    private int match(String a, String b) {
        int c = 0;
        for (int i = 0; i < 6; i++) if (a.charAt(i) == b.charAt(i)) c++;
        return c;
    }
}
```
