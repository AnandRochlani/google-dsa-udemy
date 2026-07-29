# 🎬 Recording Script — Flood Fill
**Pattern: Graphs (flood fill) · LeetCode 733 · Easy · Target length ~9 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Number of Islands — we ran flood fill *many* times to count. Today: the single, pure fill.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a paint program. A cursor clicks the paint-bucket tool on a shape, and it floods with color instantly.]**

> You've used this a thousand times. Paint program, paint-bucket tool, click a region — the whole connected patch changes color at once. That's *this* problem. Google literally asks you to implement the paint bucket.
>
> It looks trivial. Recolor the pixel, recolor its neighbors, done. And it *is* — except for one line that, if you forget it, sends your code into an infinite loop that never returns. Let me show you the whole thing, and that one deadly line.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:30`
*(concrete before abstract)*

**[VISUAL: a 3×3 grid of colors, a marker on cell (1,1):]**

```
1 1 1
1 1 0
1 0 1     start = (1,1), new color = 2
```

> The problem in one line: **start at one pixel, and recolor every pixel connected to it that shares its original color.** Connected means up, down, left, right.
>
> Here the start pixel `(1,1)` is color `1`. So every `1` you can walk to — through 1s only — becomes `2`. Watch that lonely `1` in the bottom-right corner. It's diagonal from the rest, so it's *not* connected. Bet it survives. Hold that thought.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:15`
*(worked example)*

**[VISUAL: from (1,1), color spreads outward one cell at a time, matching-color cells lighting up.]**

> Let's do it by hand. Stand on `(1,1)`, color `1`. Repaint it to `2`. Now look at its neighbors: is each one still the *original* color, `1`? If yes, walk there and repeat.
>
> Up is `(0,1)` — a `1`. Repaint, spread. Left is `(1,0)` — a `1`. Repaint, spread. Right is `(1,2)` — a `0`. Not our color. Stop. Down is `(2,1)` — a `0`. Stop.
>
> **[VISUAL: the connected blob of 1s turns to 2s; the two 0s and the corner 1 stay put.]**
>
> Keep spreading from each new cell and the whole connected clump of 1s flips to 2. That "recolor, then spread to same-colored neighbors" is flood fill — the exact engine from Number of Islands, just run **once** from **one** seed.

---

## 4. THE PAIN POINT + PREDICT — `2:30`
*(generation effect — first pause)*

**[VISUAL: the case start-color = 2, new-color = 2. A cell recolors to 2… and is still 2… neighbors re-qualify… a loop arrow spins. A 4-second "🤔 your turn" timer.]**

> **TEACHER:** Now the trap. In Number of Islands we sank land to `'#'` so we'd never revisit. Here, recoloring *is* our visited marker — once a pixel is the new color, it no longer matches the original, so we won't come back. Clean.
>
> **LEARNER:** But wait — what if the new color is the *same* as the original color? Then recoloring changes nothing, the pixel still matches, and the neighbors keep re-qualifying forever.
>
> **TEACHER:** That is *exactly* the bug, and it's the whole reason this "easy" problem trips people. Pause and predict: **what's the one-line guard that saves you?** Three seconds.
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration — grid as graph, recolor = visited)*

**[VISUAL: the grid morphs to nodes; same-color cells linked by edges. The region to fill = one connected component highlighted.]**

> **TEACHER:** Same reframe as always: **the grid is a graph.** Each pixel a node, edges to same-colored neighbors. The pixels you must recolor are exactly the **connected component** containing your start pixel.
>
> The elegant part: recoloring a pixel simultaneously *marks it visited*, because it stops matching the original color. No separate visited set needed.
>
> But that elegance is precisely what breaks when new color equals original. Recolor to the same value, and "have I visited this?" is answered by "is it a different color?" — which is never true. So we guard it up front: **if the new color already equals the start color, there's nothing to do — return immediately.**
>
> **[VISUAL: a single guard line drops in at the top: `if start == color: return image`. A little shield icon.]**
>
> One line. That's the difference between "correct" and "times out forever."

---

## 6. THE KEY MOVE (signaling) — `4:10`
*(one crisp, repeatable line)*

**[VISUAL: boxed line: "Guard equal color → then DFS/BFS, recoloring as your visited mark."]**

> The key move: **guard the equal-color no-op, then flood-fill the component, using the recolor itself as your visited marker.**

---

## 7. CODE IT — LIVE & CHUNKED — `4:40`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1.]**

> Setup and the all-important guard first.

```python
def flood_fill(image, sr, sc, color):
    start = image[sr][sc]
    if start == color:            # the guard — no-op, and prevents the infinite loop
        return image
    rows, cols = len(image), len(image[0])
```

> **[VISUAL: add chunk 2, highlight.]** Now the flood fill itself.

```python
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if image[r][c] != start:  # off-region or already recolored → stop
            return
        image[r][c] = color       # recolor = mark visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
```

> **[VISUAL: add chunk 3.]** Kick it off from the seed and return.

```python
    dfs(sr, sc)
    return image
```

---

## 8. EXPLAIN THE CODE (the WHY) — `5:45`
*(elaboration — why each line exists)*

**[VISUAL: full function; spotlight lines.]**

> The `start = image[sr][sc]` grab has to happen *before* any recoloring — it's the color we're chasing. Read it after you start painting and you've lost your reference.
>
> The guard `if start == color` — that's the star of the show. Skip it and the `color == start` test case spins forever.
>
> Inside `dfs`, the check `image[r][c] != start` does triple duty: it stops at pixels of a different color, at pixels already recolored, and — combined with the bounds check — at the edges of the image.
>
> `image[r][c] = color` recolors *and* marks visited in one stroke, because the pixel now fails the `== start` test next time.
>
> **LEARNER:** Quick one — why 4 recursive calls and not 8? Couldn't diagonal pixels be part of the region?
>
> **TEACHER:** Only if the problem says so — and this one says 4-directional. Diagonal connectivity is a *different* problem. Match the neighbor set to the spec exactly; adding diagonals here would over-fill and fail tests.

---

## 9. DRY-RUN THE CODE — `6:45`
*(worked example — prove it)*

**[VISUAL: the 3×3 grid, cells flipping to 2 as visited.]**

> Run it. `start = 1`, `color = 2` — guard passes, they differ.

| at cell | value vs start(1) | action |
|---|---|---|
| (1,1) | 1 | → 2, recurse |
| (0,1) | 1 | → 2, recurse |
| (0,0),(0,2) | 1 | → 2 |
| (1,0) | 1 | → 2 → down to (2,0) |
| (2,0) | 1 | → 2 ; its neighbor (2,1)=0 stop |
| (1,2),(2,1) | 0 | skip |

> Result:
> ```
> 2 2 2
> 2 2 0
> 2 0 1
> ```
> The bottom-right `1` — never reached, not connected. Just like we predicted at the start. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `7:30`
*(transfer to interview)*

**[VISUAL: Time O(rows × cols) · Space O(rows × cols) stack.]**

> Out loud: *"Each pixel is touched at most once — recoloring marks it visited — so O(rows times cols) time. Space is the recursion stack, worst case the whole image is one region, so O(rows times cols)."*

---

## 11. CAN WE USE LESS MEMORY? (space) — `7:55`
*(depth + honesty)*

**[VISUAL: "in place — no visited set" checkmark; "or restore / copy if mutation not allowed".]**

> We're already in place — the recolor *is* the visited marker, so zero extra bookkeeping. The only unavoidable memory is the traversal frontier: the DFS stack, or a BFS queue if you'd rather dodge recursion depth. Same big-O.
>
> If the interviewer says "don't mutate my image," you'd copy it or track a separate visited set — O(rows times cols) extra. But for this problem, in-place *is* the expected answer.

---

## 12. YOUR TURN (active recall) — `8:20`
*(retrieval practice)*

**[VISUAL: "Your turn → Number of Closed Islands (LC 1254)". Blank editor.]**

> Your turn: **Number of Closed Islands.** It's flood fill with a clever setup — first flood every island that touches the border to erase it, *then* count what's left. Same engine, sneakier framing.

---

## 13. LOCK IT IN — `8:45`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big line.]**

> Three things:
> 1. **Flood fill = one traversal from one seed**, recoloring the connected component.
> 2. **The recolor is your visited marker** — no separate set needed.
> 3. **Guard equal colors first** — the one line that stops the infinite loop.
>
> Memory peg: **"same color in, same color out? Bail before you paint."** That guard line is the whole difference on this problem.

---

## 14. CLIFFHANGER — `9:05`
*(open loop to next lesson)*

**[VISUAL: a grid of oranges — some green, some brown — with a ticking clock. Title blurred: "Rotting Oranges (LC 994)".]**

> So far our floods just *fill* — they don't care about distance or time. But what if the question is *"how many minutes until the whole grid is infected,"* and the rot spreads from **many** sources at once? Flood fill can't answer "how far" or "how fast." For that we need its sharper cousin — BFS, and a twist called *multi-source*. That's next. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public int[][] floodFill(int[][] image, int sr, int sc, int color) {
    int start = image[sr][sc];
    if (start == color) return image;      // guard against infinite loop
    dfs(image, sr, sc, start, color);
    return image;
}

private void dfs(int[][] image, int r, int c, int start, int color) {
    if (r < 0 || r >= image.length || c < 0 || c >= image[0].length || image[r][c] != start)
        return;
    image[r][c] = color;
    dfs(image, r + 1, c, start, color);
    dfs(image, r - 1, c, start, color);
    dfs(image, r, c + 1, start, color);
    dfs(image, r, c - 1, start, color);
}
```
