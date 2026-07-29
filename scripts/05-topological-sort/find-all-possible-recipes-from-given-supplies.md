# 🎬 Recording Script — Find All Possible Recipes from Given Supplies
**Pattern: Topological Sort (Kahn's BFS) · LeetCode 2115 · Medium · Target length ~12 min**
**Audience:** college students + working IT professionals prepping for Google.
**Prereq callback:** Course Schedule — indegree + a queue. Same engine, new coat of paint.

> Format: **[VISUAL: …]** = what's on screen. **>** = spoken narration (read every one out loud). Beat timings are guides.

---

## 1. COLD OPEN / HOOK — `0:00`
*(curiosity gap + emotion — open the loop)*

**[VISUAL: a kitchen-whiteboard sketch. "sandwich" needs "bread" + "meat". "bread" needs "yeast" + "flour". An arrow from sandwich points at bread with a red "?" — is bread even makeable?]**

> You're at the Google onsite. The interviewer says: *"Here's a list of recipes, what each one needs, and what's in your pantry. Tell me everything you can cook."*
>
> Easy, right? Check each recipe, see if you have the ingredients. So you write that loop… and then you hit `sandwich`. It needs `bread`. But `bread` isn't in your pantry — it's *another recipe*. Can you even make it yet? You don't know until you check bread. And bread might need something that's *also* a recipe.
>
> Here's the trap that sinks people: they write a loop that scans over and over until nothing changes. It passes. But there's a clean, single-pass way to do this — and it's a pattern Google asks constantly, just wearing a disguise. By the end, you'll see the disguise fall off. Let's go.

---

## 2. WHAT WE'RE SOLVING (made concrete) — `0:35`
*(concrete before abstract)*

**[VISUAL: one sentence up top. Below, three tidy boxes:]**

```
recipes     = ["bread", "sandwich"]
ingredients = [["yeast","flour"], ["bread","meat"]]
supplies    = ["yeast", "flour", "meat"]
```

> The whole problem in one line: **return every recipe you can make, where an ingredient is either a raw supply you have — unlimited — or another recipe you'd have to make first.**
>
> Tiny example. Two recipes. `bread` needs `yeast` and `flour`. `sandwich` needs `bread` and `meat`. Your pantry has `yeast`, `flour`, `meat`.
>
> Hold the answer in your head before we start: it's **both** — `["bread","sandwich"]`. The interesting bit is *why* sandwich works when bread isn't even in the pantry.

---

## 3. DRY-RUN THE OBVIOUS IDEA (by hand) — `1:10`
*(worked example — let them feel the waste)*

**[VISUAL: the two recipes as rows. A "passes" counter, top-right, at 0. We sweep top-to-bottom, re-scanning each pass.]**

> Let's do what your brain does first: keep sweeping the list, and each pass, make whatever you now can. Loop until a full pass makes nothing new.
>
> **Pass 1.** Check `bread` — needs `yeast`, `flour`. Both in the pantry. ✅ Make it. Now check `sandwich` — needs `bread`, `meat`. We *just* made bread this pass… but did our check see it? Messy. Say it didn't yet. Sandwich waits.
>
> **[VISUAL: pass counter ticks to 1. bread turns green. sandwich still grey.]**
>
> **Pass 2.** Re-scan *everything again*. `bread` — already made, skip. `sandwich` — now `bread` is available. ✅ Make it.
>
> **[VISUAL: pass counter ticks to 2. We re-scanned bread for nothing.]**
>
> **Pass 3.** Sweep again just to confirm nothing new. Nothing. Stop.
>
> Three full passes for two recipes. Notice pass 2 re-checked bread even though bread never changed. On a long dependency chain, you'd do a pass *per link* — re-scanning settled recipes every single time.

---

## 4. THE PAIN POINT + PREDICT — `2:25`
*(close loop #1 + generation effect — first pause)*

**[VISUAL: freeze. Spotlight bread being re-checked in pass 2 with a grey "already done" stamp. A 4-second 🤔 timer.]**

> **TEACHER:** So where's the waste? We keep re-scanning recipes that are already settled, just to find the *one* that newly unlocked. We're pulling — asking each recipe "are you ready yet?" — over and over.
>
> **LEARNER:** But isn't that unavoidable? Sandwich genuinely *can't* be checked until bread is done. The dependency forces the order.
>
> **TEACHER:** The dependency forces the order — true. But what if bread could **tell** sandwich the moment it's ready, instead of sandwich asking again and again? Flip the direction. Pause the video: instead of each recipe *pulling* its ingredients, what if every finished ingredient *pushed* an update to whoever's waiting on it? What would each recipe need to keep track of?
>
> *(pause)*

---

## 5. BUILD THE INTUITION (the aha) — `3:05`
*(elaboration + analogy — derive it, don't hand it over)*

**[VISUAL: build a graph live. Nodes: yeast, flour, meat, bread, sandwich. Draw arrows ingredient → recipe. Each recipe gets a little counter badge.]**

> **TEACHER:** Here's the flip. Draw an arrow from each **ingredient** to the **recipe** that needs it. `yeast → bread`. `flour → bread`. `bread → sandwich`. `meat → sandwich`.
>
> Now give every recipe a counter: **how many ingredients am I still waiting on?** That's its **indegree**. `bread` waits on 2. `sandwich` waits on 2.
>
> **[VISUAL: bread badge "2", sandwich badge "2".]**
>
> Now the magic. Take everything you already have — the supplies — and let each one "arrive." When `yeast` arrives, it satisfies one of bread's requirements. Tick bread down to 1. When `flour` arrives, tick bread to **0**. Zero means every ingredient is here — **bread is makeable.** And the second bread is made, *it* arrives too, and ticks sandwich down.
>
> **[VISUAL: yeast lands → bread 2→1. flour lands → bread 1→0, bread flashes "MADE". bread now itself lands → sandwich 2→1. meat lands → sandwich 1→0 "MADE".]**
>
> **LEARNER:** Wait — what if bread needs sandwich and sandwich needs bread? A cycle. Doesn't that break this, or loop forever?
>
> **TEACHER:** Beautiful worry — and here's the gift. If bread and sandwich need each other, neither ever loses its **last** dependency. Both counters get stuck at 1, forever above zero. So neither ever gets made, neither ever enters our queue — they just fall out silently. **We never even write a cycle check.** The counter reaching zero *is* the proof it's makeable, and a cycle can't fake that.

---

## 6. THE KEY MOVE (signaling) — `4:35`
*(one crisp, repeatable sentence)*

**[VISUAL: a single boxed line: "indegree = ingredients still waiting on → 0 means MAKE it → it becomes a new supply."]**

> Burn this one line in: **give each recipe a countdown of ingredients it's waiting on; every supply that arrives ticks its recipes down; when a recipe hits zero, make it — and it becomes a supply for the next.**
>
> That's Kahn's algorithm. Topological sort by BFS. And here's the disguise falling off — this is the *exact* engine from **Course Schedule**. Same indegree, same queue. Recipes are just courses wearing an apron.

---

## 7. CODE IT — LIVE & CHUNKED — `5:15`
*(cognitive load — build in pieces)*

**[VISUAL: empty editor. Type chunk 1 only.]**

> Let's build it. First, two structures. `children` — for each ingredient, who needs it. And `indegree` — each recipe's countdown.

```python
from collections import defaultdict, deque

def find_all_recipes(recipes, ingredients, supplies):
    children = defaultdict(list)      # ingredient -> recipes that need it
    indegree = defaultdict(int)       # recipe -> how many ingredients it waits on
```

> **[VISUAL: add chunk 2, highlight it.]** Build the graph in one pass over the recipes. Each ingredient points at this recipe; the recipe's countdown is just how many ingredients it lists.

```python
    for r, need in zip(recipes, ingredients):
        for item in need:
            children[item].append(r)  # item unlocks recipe r
        indegree[r] = len(need)       # r waits on this many
```

> **[VISUAL: add chunk 3.]** Seed the queue with everything we already have — the supplies. They're the free arrivals.

```python
    queue = deque(supplies)
    made = []
```

> **[VISUAL: add chunk 4, highlight the `indegree[r] == 0` line.]** The BFS. Pop an available item, tick down every recipe waiting on it, and when one hits zero — make it, and push it back in, because now it's an ingredient too.

```python
    while queue:
        item = queue.popleft()
        for r in children[item]:      # everyone waiting on this item
            indegree[r] -= 1          # one requirement satisfied
            if indegree[r] == 0:      # all met → makeable
                made.append(r)
                queue.append(r)       # r is now a supply for others
    return made
```

---

## 8. EXPLAIN THE CODE (the WHY) — `6:55`
*(elaboration — why each line exists)*

**[VISUAL: the full function; spotlight each line as it's named.]**

> Let's walk *why*, not just what.
>
> `children[item].append(r)` — this is the **flip**. We store, per ingredient, who's waiting. That's what lets a finished ingredient *push* instead of everyone *pulling*.
>
> `indegree[r] = len(need)` — the countdown starts at exactly the number of ingredients. Not "how many are missing" — *all* of them, because at the start nothing's been delivered.
>
> `queue = deque(supplies)` — we seed with supplies because they're available at time zero, for free. They're the spark that starts the chain.
>
> **LEARNER:** Quick objection — why push `r` back into the *same* queue after making it? Feels like mixing supplies and recipes in one bucket.
>
> **TEACHER:** That's the whole trick, and it's on purpose. Once bread is made, bread *is* an ingredient — indistinguishable from a supply as far as sandwich cares. Same bucket is correct: "things now available." That one `queue.append(r)` is what chains bread → sandwich without any extra passes.
>
> `if indegree[r] == 0` — strictly zero, checked right after decrementing. Not "≤ 0", not re-scanned later — the moment it lands on zero we act, exactly once per recipe. And anything stuck in a cycle never reaches this line. No cycle check needed — the zero test already excludes them.

---

## 9. DRY-RUN THE CODE — `8:05`
*(worked example — prove it, close the loop)*

**[VISUAL: the graph with countdown badges; a trace table filling row by row. Queue shown as a strip.]**

> Let's run the real code. Queue starts `[yeast, flour, meat]`, countdowns `bread:2, sandwich:2`.

| Pop | Unlocks (children) | Countdown after | Hit 0? → made + enqueued |
|---|---|---|---|
| `yeast` | bread | bread 2→1 | no |
| `flour` | bread | bread 1→**0** | **yes** → made=[bread], queue += bread |
| `meat` | sandwich | sandwich 2→1 | no |
| `bread` | sandwich | sandwich 1→**0** | **yes** → made=[bread,sandwich], queue += sandwich |
| `sandwich` | — | — | queue empty → done |

> Watch row four: we only reached sandwich's zero *because* bread got popped as an ingredient. The queue chained it for us — no second pass, no re-scan. Answer `["bread","sandwich"]`, exactly the two we promised. Loop closed.

---

## 10. COMPLEXITY, OUT LOUD — `9:05`
*(transfer to interview)*

**[VISUAL: two rows — Brute: O(n · E), re-scans every pass. Ours: O(V + E), each edge touched once. V = supplies + recipes, E = total ingredients.]**

> **TEACHER:** Say it the way you'd say it in the room: *"I build the graph in one pass — that's O(E) over the total ingredients. Then Kahn's BFS pops each available item once and walks each edge once. So it's O(V + E) time — V is supplies plus recipes, E is total ingredients. The brute force was O(n · E) because it re-scanned every recipe every pass; here each edge is touched exactly once."*
>
> That contrast — naming *why* yours is faster — is the sentence that scores.

---

## 11. CAN WE USE LESS MEMORY? (space) — `9:45`
*(depth + honesty)*

**[VISUAL: the adjacency graph; a "shrink it?" thought bubble → red ✗.]**

> Can we cut the O(V + E) memory? **No — and I can say exactly why.** The graph *is* the input re-expressed. To answer the question at all, I have to look at every ingredient of every recipe at least once — that's E, and storing who-needs-what is the same E. The countdown map is one number per recipe, and the queue holds each item at most once. Nothing rolls up or collapses, because dependencies point every direction — one ingredient can feed many recipes.
>
> Say it out loud: *"Space is O(V + E), and that's the floor — it's the dependency graph itself, not overhead I chose."* Naming why it can't shrink beats staying silent.

---

## 12. YOUR TURN (active recall) — `10:20`
*(retrieval practice)*

**[VISUAL: "Your turn → Course Schedule II (LC 210)". A blank editor.]**

> Before the next video, do **Course Schedule II**. Same indegree, same queue — but this time you *return the order* you finished things in, and if there's a cycle you return empty. It's this exact skeleton. If you can write recipes, you can write that. Wrestle with it ten minutes before peeking — that struggle is what makes it stick.

---

## 13. LOCK IT IN — `10:50`
*(retrieval + memory peg)*

**[VISUAL: 3 bullets, then one big boxed line.]**

> Three things to keep:
> 1. **"Depends on other things + exclude cycles" → topological sort.** Recipes needing recipes is the tell.
> 2. **indegree = countdown of what you're waiting on.** Seed the queue with what's free; a zero means "make it and it becomes free too."
> 3. **Cycles need no special check** — a cycled node never hits zero, so it excludes itself.
>
> And the memory peg:
>
> **[VISUAL: big box → "count down the dependencies; zero means go."]**
>
> When something can only happen after other things happen — and loops must be thrown out — your hand should already be reaching for indegree and a queue.
>
> *(GCA reminder — for the interview itself: ask up front "can a recipe depend on another recipe, and can those cycle?" That one clarifying question proves you saw why it's a graph, not a scan. Then narrate the flip from pulling to pushing before you write a line. Google's General Cognitive Ability signal isn't the code — it's you thinking out loud from naive to clean.)*

---

## 14. CLIFFHANGER — `11:20`
*(open loop to next lesson)*

**[VISUAL: a new title blurred in: "Alien Dictionary" — a list of alien words, with a red "?" over the letter order.]**

> Here, the graph was handed to us — recipes and ingredients, edges obvious. But what if the dependencies are *hidden*? Next up: **Alien Dictionary.** You're given words in a mystery alphabet's sorted order, and you have to **deduce** the letter ordering — build the graph yourself from the clues, *then* topo sort it. Same engine, but first you have to find the edges. That's where this gets really Google. See you there.

---

## Appendix — Java version (drop-in for Java tracks)

```java
public List<String> findAllRecipes(String[] recipes, List<List<String>> ingredients, String[] supplies) {
    Map<String, List<String>> children = new HashMap<>();   // ingredient -> recipes needing it
    Map<String, Integer> indegree = new HashMap<>();         // recipe -> countdown

    for (int i = 0; i < recipes.length; i++) {
        String r = recipes[i];
        List<String> need = ingredients.get(i);
        indegree.put(r, need.size());
        for (String item : need) {
            children.computeIfAbsent(item, k -> new ArrayList<>()).add(r);
        }
    }

    Queue<String> queue = new ArrayDeque<>(Arrays.asList(supplies));
    List<String> made = new ArrayList<>();

    while (!queue.isEmpty()) {
        String item = queue.poll();
        for (String r : children.getOrDefault(item, Collections.emptyList())) {
            indegree.put(r, indegree.get(r) - 1);
            if (indegree.get(r) == 0) {
                made.add(r);
                queue.add(r);       // r is now available as an ingredient
            }
        }
    }
    return made;
}
```
