# 🎬 Recording Script — Robot Room Cleaner
**Pattern: Backtracking / Interactive DFS (spiral backtracking) · LeetCode 489 · Hard · Target length ~13 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** flood-fill DFS (Number of Islands) — the same search, but with the grid taken away and the retreat made physical.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: an editor with a function signature and nothing else: `def cleanRoom(robot):`. No grid parameter. No `m`, no `n`. Just `robot`. A blinking cursor. Then four API calls fade in beside it: `move()` `turnLeft()` `turnRight()` `clean()`.]**

> Google onsite. The interviewer says: *"You're programming a robot vacuum. It's standing somewhere in a room, facing up. Clean every reachable cell."*
>
> You reach for your grid-DFS reflex — then you look at the function signature. **There is no grid.**
>
> **[VISUAL: zoom on the signature. A red circle around the empty parameter list where `grid` should be.]**
>
> No grid. No starting coordinates. No dimensions. You can't index anything, because there's nothing to index. Four calls, that's your entire world: move forward, turn left, turn right, clean.
>
> That silence is where candidates freeze — not because DFS is hard, but because **the two things DFS quietly depends on have both been taken away**, and most people never noticed they were depending on them. By the end of this video you'll know exactly what those two things are, and the five-call maneuver that gets one of them back. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:40`
*(concrete before abstract)*

**[VISUAL: one plain sentence on top. Below it, a tiny 2×3 room, robot icon on `S` with a small arrow pointing up:]**

```
A B C
S ▓ D
```

> The whole problem in one line: **clean every open cell the robot can reach — using only `move()`, `turnLeft()`, `turnRight()`, and `clean()`.**
>
> Here's our tiny room. `S` is where the robot starts, facing up. `▓` is blocked. Five open cells — `S`, `A`, `B`, `C`, `D` — so the target is five `clean()` calls, one each. Now look at `D`, bottom right. It's *right next to* the start, one step as the crow flies — but there's a wall between them. To reach it the robot goes **up** to `A`, **across the top** through `B` and `C`, then **down** the far side. The neighbor you can see is not the neighbor you can reach.
>
> **[VISUAL: a dotted path S → A → B → C → D drawn around the blocked cell.]**
>
> Two rules that matter. `move()` returns `true` if the robot actually stepped, `false` if a wall stopped it — and on `false` **the robot doesn't budge**. And your function returns nothing. Nobody grades your output. They grade which cells got cleaned.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:20`
*(worked example — feel the waste)*

**[VISUAL: the tiny room. The robot bounces around under a "random wander" label. A `clean()` counter climbs to 9, 14, 22… while a "distinct cells cleaned" counter sticks at 4. Cell `D` stays grey.]**

> Let's do what a cheap real vacuum does — what your brain reaches for when there's no grid. **Wander.** Clean where you are, try to move forward, and if you're blocked, turn a random amount and try again.

```python
import random

def clean_room_random(robot):
    while True:                      # when do we stop? exactly.
        robot.clean()
        if not robot.move():
            for _ in range(random.randint(1, 3)):
                robot.turnRight()
```

> Watch it run. Clean `S`. Move up — lands on `A`. Clean `A`. Move up — wall, turn, turn. Move — back down onto `S`. Clean `S` **again**.
>
> **[VISUAL: the `clean()` counter ticks past 20. `S` and `A` glow bright from repeated cleaning. `D` stays grey. Then a spotlight lands on `while True:` with a red question mark over it.]**
>
> Twenty calls in, it's polished `S` and `A` to a mirror shine and never once found its way around to `D`. But here's what should really bother you — look at the `while True`. **When does this loop stop?** It doesn't. It *can't*. The robot has no way to tell "I've cleaned everything reachable" apart from "I'm re-cleaning the same hallway for the fortieth time." From the inside, those feel identical.

---

## 4. THE PAIN POINT + PREDICT — `2:35`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze on the wandering robot. Two labels appear side by side: "❌ no memory of where I've been" and "❌ no free way to retreat". A 5-second "🤔 your turn" timer.]**

> **TEACHER:** So name the two missing pieces, precisely. First: **there's no memory.** In Number of Islands you write `visited[r][c] = True` — but there is no `r`, no `c`, and no array to write into. Second, and this is the sneaky one: **there's no free retreat.** In normal DFS, when a branch dead-ends, you `return` and you're magically back at the parent cell. Here the robot is *physically standing* in the dead end. The stack frame pops in your head; the machine doesn't move an inch.
>
> **LEARNER:** Okay, but hold on — why DFS at all? Number of Islands works fine with BFS. Why not just push cells into a queue and process the frontier?
>
> **TEACHER:** That's the exact right question, and the answer is why this problem is Hard. A BFS queue hops: pops a cell on the north wall, then one on the south wall, then back north. A **stack frame can teleport. A robot cannot.** Every BFS pop would mean physically driving across everything you've already explored — each algorithm "step" becomes an `O(cells)` road trip. DFS is the right shape for one very specific reason: **its retreat is local.** Undoing one level of recursion is exactly one step backwards. One step.
>
> So — pause the video. You have no coordinates, and you have no free undo. **What would you invent to fix the first one?** You're allowed to make something up. Think before I answer. *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:25`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: the room, but the labels A/B/C/D fade out. The robot's cell gets stamped `(0, 0)` in a bright colour. A blank notepad icon appears beside the room, titled "MY map".]**

> **TEACHER:** Here's the aha, and it's genuinely a *creative* move, not a technique you look up. **You don't have coordinates. So invent them.**
>
> Nobody said they have to be *real*. Declare, by fiat, that wherever the robot is standing right now is `(0, 0)`, and that "up" means row minus one. That's legal. Those numbers live only in your head and in your `visited` set — which is fine, because **nothing else ever needs them.**
>
> **[VISUAL: coordinates stamp onto the room one at a time as narrated: S = (0,0), A = (-1,0), B = (-1,1), C = (-1,2), D = (0,2), blocked = (0,1). Then a notepad fills with the growing set {(0,0), (-1,0), (-1,1), …} while the actual room dims to near-black.]**
>
> Every time `move()` returns `true`, you update your position on your own notepad. `S` is `(0,0)`. Step up: `(-1, 0)` — that's `A`. Step right: `(-1, 1)` — `B`. Then `(-1, 2)` is `C`, and down from there is `(0, 2)` — `D`. The blocked cell would have been `(0, 1)`. Negative rows, and that's fine — it's *your* system.
>
> **LEARNER:** But I still don't know where the walls are, or how big the room is. Doesn't my made-up map end up wrong?
>
> **TEACHER:** It never needs to be *complete* — only **consistent**. I'm not mapping the room; I'm recording the cells I've personally stood on. The hidden grid can be a hundred by two hundred, any shape — I don't care, because I never ask it a question. I only ask my own set: *"have I stood here before?"* It's dead reckoning in a cave: you can't see the cave, but count your paces and turns honestly and you always know where you are relative to the entrance. That's enough to never walk the same tunnel twice.
>
> Problem one, solved. Now the retreat — and that's the move that separates the people who pass from the people who don't.

---

## 6. THE KEY MOVE (signaling) — `4:50`
*(signaling + chunking — the sentence they'll remember)*

**[VISUAL: a single boxed line, big: "The recursion returns for free. The robot has to DRIVE BACK."]**

> Here's the key move, and it's a **physical undo**. When a recursive call finishes, the robot is sitting in the child cell while your parent frame thinks it's at the parent cell. Those two facts disagree — and if you let them disagree for even one step, every coordinate after that is a lie. So you write the undo by hand: **turn right, turn right, move, turn right, turn right.** Five calls.
>
> **[VISUAL: animate the five calls on a single cell, slow. Robot faces up ↑. Turn right → faces right →. Turn right → faces down ↓. `move()` — the robot slides back one cell. Turn right → faces left ←. Turn right → faces up ↑ again. A green "✓ position restored, heading restored" stamp lands.]**
>
> Watch it carefully — this is the exact thing candidates fumble at the whiteboard. Turn right, turn right: 180 degrees, facing back the way you came. `move()`: one step home — and that move **cannot fail**, because you drove through that cell thirty seconds ago. It's open by construction. Then turn right twice more — another 180 — and you're facing your original direction.
>
> **Position restored. Heading restored.** Not just position. Skip that second pair of turns and the robot ends up backwards, and every direction you compute from then on is rotated 180 degrees. Silently, invisibly wrong.
>
> **[VISUAL: side-by-side — "with the second 180°: ✓ facing up" vs "without: ✗ facing down, all future moves inverted".]**
>
> Say it out loud once: **every recursive return gets a real-world return.** And one polish makes the code beautiful. Try the four directions in **clockwise order starting from wherever you're currently facing** — up, right, down, left, wrapping around. Why clockwise? Because then "advance to the next candidate" is literally **one `turnRight()`**. No angle arithmetic, no turning left three times. The loop and the hardware agree.

---

## 7. CODE IT — LIVE & CHUNKED — `6:00`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, the direction table — and the order is load-bearing.

```python
def cleanRoom(robot):
    # clockwise order — up, right, down, left — so that turnRight()
    # advances to the next candidate direction with zero bookkeeping
    DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    visited = set()
```

> Up, right, down, left — indices `0` through `3`, clockwise, the same way `turnRight()` goes. And `visited` is the map, in *our* coordinates.
>
> **[VISUAL: add chunk 2, highlight it. The five-call animation replays small in the corner.]** Now the physical undo, as its own named function — naming it shows the interviewer you know it's a distinct idea.

```python
    def go_back():
        # physical undo: 180° turn, one step back, 180° turn again
        robot.turnRight(); robot.turnRight()   # face the way we came
        robot.move()                           # guaranteed open — we just came from there
        robot.turnRight(); robot.turnRight()   # restore the original heading
```

> **[VISUAL: add chunk 3, highlight the signature line.]** Now the DFS. Read the signature as a **contract** — the robot is *physically* at `(row, col)`, *physically* facing `d`.

```python
    def dfs(row, col, d):                      # robot is AT (row, col), FACING d
        visited.add((row, col))
        robot.clean()
```

> **[VISUAL: add chunk 4 — the loop — one line at a time.]** And the loop over the four headings, starting from the one we're already facing.

```python
        for i in range(4):
            nd = (d + i) % 4                   # current heading after i right turns
            nr, nc = row + DIRS[nd][0], col + DIRS[nd][1]
            if (nr, nc) not in visited and robot.move():
                dfs(nr, nc, nd)
                go_back()                      # child left us where it started; undo one step
            robot.turnRight()                  # rotate to the next heading — even after a failed move
        # four right turns total → we exit facing d, exactly as we entered
```

> **[VISUAL: add chunk 5.]** And kick it off — the start is the origin, "facing up" is direction zero. Fifteen lines. That's the whole Hard.

```python
    dfs(0, 0, 0)                               # the start is our origin; facing up = 0
```

---

## 8. EXPLAIN THE CODE (the WHY) — `7:40`
*(elaboration — why each line exists)*

**[VISUAL: the full function on screen; spotlight each line as it's named.]**

> Let's walk *why*, not just what — every line here is defending an invariant.
>
> `nd = (d + i) % 4` — `d` is the heading we walked in with; `i` counts the `turnRight()`s we've done in this loop. So `nd` is **the direction the robot is physically facing right now**. The variable and the hardware are the same fact. That's the whole design.
>
> **LEARNER:** Wait — `(nr, nc) not in visited and robot.move()`. Those are in one `if`. Does the order actually matter, or is that just style?
>
> **TEACHER:** It matters enormously — my favourite line in the solution. Python short-circuits `and`: if the left side is false, **the right side never runs.** So if the neighbour is already visited, `robot.move()` is *never called* and the robot doesn't budge. Flip them and you'd physically step into an already-cleaned cell, then have to notice and back out — extra travel, and a much easier place to lose track of yourself. The free check goes first. Say it out loud in the room: *"visited first, so a known cell costs zero physical moves."*
>
> `robot.turnRight()` **outside** the `if` — the line people delete by accident. It runs whether the move succeeded, failed, or was skipped. Four iterations, four right turns, net **360 degrees**. So `dfs` exits facing exactly the direction it entered facing.
>
> **[VISUAL: a circle diagram — four quarter-turn arcs closing into a full circle, labelled "net 360° → exits facing d".]**
>
> Not a cute detail — it's what makes `go_back()` correct one level up. The parent calls `go_back()` right after the child returns, and `go_back` assumes the robot is facing the direction it originally moved in. It only *is* facing that way because the child's loop closed its full circle. **The invariant in the child is what makes the parent's undo legal.**
>
> **LEARNER:** Then here's my real objection. I've got a `visited` set — the DFS already knows every cell it's been to. Why do I need `go_back()` at all? Just let the recursion unwind and let `visited` stop me repeating myself.
>
> **TEACHER:** That's the single most tempting wrong idea in this problem, and it comes from conflating two things. `visited` is the **algorithm's memory** — it stops you *logically* re-exploring. `go_back()` is about the robot's **body** — it puts the machine where the algorithm believes it is. Drop `go_back` and `visited` is still perfectly populated; it's just describing a robot that isn't there. Your parent frame computes `(row-1, col)` for "up," but the robot is physically three cells away in a dead end, so "up" from *its* position is a completely different cell. The set stays clean while the map becomes fiction. **Memory doesn't move hardware.**
>
> Last two. `robot.clean()` right after `visited.add(...)` — clean on entry, exactly once per cell, because the `visited` check upstream guarantees we only enter a cell once. And `dfs(0, 0, 0)` — origin and heading declared by fiat. Nothing verifies these. Nothing needs to.

---

## 9. DRY-RUN THE CODE — `9:00`
*(worked example — prove it, close the loop)*

**[VISUAL: the tiny room with our invented coordinates stamped on. A trace table fills row by row; the robot icon moves and rotates in sync; cells turn green as they're cleaned.]**

> Let's run the actual code on the actual room. `S` is `(0,0)`, up is row minus one.

```
A B C          A=(-1,0)  B=(-1,1)  C=(-1,2)
S ▓ D          S=(0,0)   ▓=(0,1)   D=(0,2)
```

| Robot at | Tries heading | Result |
|---|---|---|
| `S (0,0)` facing up | up | `move()` ✓ → recurse into `A`, clean it |
| `A (-1,0)` | up | wall — `move()` ✗, `turnRight` |
| `A` | right | ✓ → clean `B (-1,1)` |
| `B` | right | ✓ → clean `C (-1,2)` |
| `C` | right | wall ✗ → turn; **down** ✓ → clean `D (0,2)` |
| `D` | down ✗ wall · left ✗ blocked `(0,1)` · up — `C` visited, skip · right ✗ wall | dead end — all four headings exhausted |
| `D → C` | — | **`go_back()`**: turnRight ×2 (now facing up), `move()` (back on `C`), turnRight ×2 (facing down again — exactly the heading `C`'s loop expects) |
| `C → B → A → S` | — | each frame finishes its remaining headings (everything is visited or wall) and unwinds the same way; `S` checks right/down/left, all blocked or walls |

> **[VISUAL: freeze on the `D → C` row. Replay the five-call undo in slow motion beside the table.]**
>
> Stop on that `go_back()` row — that's the moment everything either holds together or falls apart. The robot is at `D`. It *arrived* heading down; it tried down, left, up, right, one `turnRight()` after each — four turns, a full 360 — so it leaves the loop heading **down**, exactly as it arrived. Now `go_back()`: turn right twice → facing **up**. `move()` → it slides back onto `C`. Turn right twice → facing **down** again.
>
> And **down** is precisely the heading `C`'s loop was in the middle of. `C`'s frame resumes as if nothing happened — does its `turnRight()`, moves to the next candidate, and never knows its child went on an adventure.
>
> **[VISUAL: all five cells green. Counter: "clean() calls: 5 · cells: 5 · re-cleans: 0".]**
>
> Five cells. Five `clean()` calls. Every cell entered **exactly once** — against a wanderer that cleaned `S` twenty times and never found `D` at all. Loop closed. One more pause-and-predict: **what breaks if you delete the second pair of `turnRight()` calls from `go_back()`?** Don't guess vaguely — trace one step. Pause here.
>
> *(pause)* Answer: the robot arrives back on `C` facing **up** instead of down. `C`'s loop then does its `turnRight()` believing it's rotating from down to left — when it's actually rotating from up to right. Every coordinate `C` computes after that is off by 180 degrees, and `visited` fills with cells the robot was never standing on. Nothing crashes. It just silently cleans the wrong room.

---

## 10. COMPLEXITY, OUT LOUD — `10:20`
*(transfer to interview)*

**[VISUAL: two rows — Random wander: "Time: unbounded — no termination guarantee · Space O(1)". Ours: "Time O(N) · Space O(N)". A note: "N = reachable open cells".]**

> **TEACHER:** Say it the way you'd say it in the room. Let `N` be the number of open cells reachable from the start.
>
> *"Each cell is entered exactly once — the visited check guarantees that. Inside a cell I do at most four move attempts and four turns, and each edge I actually traverse costs one extra `go_back`, which is five constant API calls. So everything per cell is `O(1)`, and total time is `O(N)`. Space is `O(N)` for the visited set, plus `O(N)` recursion depth in the worst case — a snake-shaped room where the reachable region is one long corridor and the stack goes as deep as there are cells."*
>
> And the room is capped at a hundred by two hundred — twenty thousand cells, max. Size was never the enemy here. **Blindness was.**

---

## 11. CAN WE USE LESS MEMORY? — `10:55`
*(depth + honesty — naming the absence is a skill)*

**[VISUAL: the `visited` set on one side, the invisible room on the other, an equals sign between them. Then a red ✗ over a "shrink it?" thought bubble.]**

> Normally this is where we shave the space down. Not here — and *why* not is the heart of the problem.

```python
# No space-optimised variant exists: visited IS the self-built map, and
# remembering where you've been is the entire difference between this
# solution and the never-terminating random walk.
```

> **The `visited` set isn't overhead. It's the map the robot was never given.** A blind robot with less than `O(N)` memory can't, in general, tell a cell it has cleaned from one it hasn't. Forget a cell and you either re-clean it forever or you can't prove you're finished. That's not a performance regression — **that's the random wanderer's disease coming back.** Memory *is* the termination condition.
>
> The recursion stack is forced too. It isn't bookkeeping; it's the **physical breadcrumb trail** back to unexplored territory. Convert it to an explicit stack if you like — it holds the same `O(N)` path in the worst case, because the path is real. Say it out loud in the interview: *"Space is O(N) and that's the floor — the robot is blind, so the visited set is the map I'm building myself. Drop any part of it and I lose termination, which is precisely what's wrong with the naive wanderer."* Being able to say *why nothing can be optimised* is a stronger signal than silence.

---

## 12. YOUR TURN (active recall) — `11:30`
*(retrieval practice)*

**[VISUAL: "Your turn → Unique Paths III (LC 980)". A blank editor.]**

> Before the next video, try **Unique Paths III**. You walk over every open cell exactly once and count the ways. Same skeleton — DFS with an explicit **undo after the recursive call** — but here the undo is *virtual*: you unmark the cell instead of driving a robot back.
>
> Do them back to back and the contrast teaches you something no single problem can: **backtracking is always "do, recurse, undo."** The only question is whether the undo costs a variable assignment or a physical move. And if today felt steep, do **Number of Islands** first — it's this exact search with the blindfold off.

---

## 13. LOCK IT IN — `12:00`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **No coordinates? Invent them.** Call the start `(0, 0)`, track your own position on every successful `move()`, and put `visited` in *your* relative system. The hidden grid never has to exist.
> 2. **Every recursive return needs a physical return.** `turnRight ×2 · move · turnRight ×2` restores **position and heading**. Both. Always.
> 3. **Clockwise directions from your current heading** means "next candidate" is a single `turnRight()`, and four iterations close a perfect 360 — so every frame exits facing exactly the way it entered. That invariant is the entire correctness proof.
>
> And the memory peg — the one line that recalls the whole pattern:
>
> **[VISUAL: big box → "When you're blind, build your own map."]**
>
> Whenever a problem hands you an *API* instead of an *input* — `move()`, `guess()`, `query()` — your reflex is: pick an origin, keep your own bookkeeping in relative terms, and mirror every logical retreat with a real one.
>
> *(GCA reminder — for the interview itself: before you write a line, ask the API questions out loud. "The robot starts on an open cell facing up, moves are 4-directional, and `move()` returns false and stays put when blocked — right?" Nailing the interaction contract before touching the keyboard is exactly what the interactive genre is testing. Then narrate the two losses — no coordinates, no free undo — and solve them one at a time. Google's General Cognitive Ability signal isn't the fifteen lines. It's you noticing what was taken away.)*

---

## 14. CLIFFHANGER — `12:35`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Guess the Word" — a list of six-letter words, and a single API call floating above them: `master.guess(word) → int`. No grid. No robot. Nothing but a number coming back.]**

> Here's the thing about today. We were blind — but the world was still a **grid**. Cells, neighbours, four directions. Once we invented coordinates, all our old grid instincts came flooding back.
>
> The next problem takes even that away. **Guess the Word.** A list of words, and one API: you guess a word, and it tells you how many letters you got in the right position. No map to build, no neighbours, no geometry at all. And you only get **ten guesses**.
>
> So what do you even *track*, when there's nothing to draw? A completely different currency — not position, but **information**. Every guess has to eliminate as many candidates as possible, and choosing *which* word to burn a guess on becomes the entire problem.
>
> Same genre, same instinct — an API instead of an input — but the map you build is made of something you can't see at all. That's next. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
class Solution {
    // clockwise: up, right, down, left — matches turnRight()
    private static final int[][] DIRS = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
    private final Set<String> visited = new HashSet<>();
    private Robot robot;

    public void cleanRoom(Robot robot) {
        this.robot = robot;
        dfs(0, 0, 0);                          // start = origin, facing up = 0
    }

    private void dfs(int row, int col, int d) {
        visited.add(row + "," + col);
        robot.clean();
        for (int i = 0; i < 4; i++) {
            int nd = (d + i) % 4;
            int nr = row + DIRS[nd][0];
            int nc = col + DIRS[nd][1];
            if (!visited.contains(nr + "," + nc) && robot.move()) {
                dfs(nr, nc, nd);
                goBack();                       // restore position AND heading
            }
            robot.turnRight();                  // next heading, even after a failed move
        }
        // net four right turns: we exit facing d, as we entered
    }

    private void goBack() {
        robot.turnRight();
        robot.turnRight();
        robot.move();                           // step back — guaranteed open
        robot.turnRight();
        robot.turnRight();
    }
}
```
