# Find All Possible Recipes from Given Supplies

> **LeetCode:** 2115. Find All Possible Recipes from Given Supplies · **Difficulty:** 🟡 Medium · **Pattern:** Topological Sort (Kahn's BFS) · **Google frequency:** ⭐ high

---

## Problem

You're given three things. `recipes` — a list of names you can *make*. `ingredients` — a parallel list where `ingredients[i]` is everything you need to make `recipes[i]`. And `supplies` — the raw materials you have on hand, in **unlimited** quantity. An ingredient is either a base supply *or* another recipe you'd have to make first. You can only make a recipe if you can get **every** ingredient it needs. Return all the recipes you can make, in **any** order.

**Example:** `recipes = ["bread"]`, `ingredients = [["yeast","flour"]]`, `supplies = ["yeast","flour","corn"]` → `["bread"]`

*(Bread needs `yeast` and `flour`. Both are in `supplies`, so bread is makeable. `corn` is just an unused supply.)*

A two-level example: `recipes = ["bread","sandwich"]`, `ingredients = [["yeast","flour"],["bread","meat"]]`, `supplies = ["yeast","flour","meat"]` → `["bread","sandwich"]`. Sandwich needs `bread`, which isn't a supply — but bread becomes makeable, and *then* sandwich unlocks. That chaining is the whole problem.

**Constraints that matter:** up to `n = 100` recipes, and the total number of ingredients across all recipes is up to ~10⁴. Names are strings. The catch that decides the approach: recipes can depend on **other recipes**, arbitrarily deep, and those dependencies can even form a **cycle** (recipe A needs B, B needs A). A cycle is unmakeable and must be excluded. So this isn't a simple "check each recipe once" scan — it's a dependency-resolution problem, i.e. a graph.

---

## 🧠 Intuition — how you'd actually arrive at this

- **First instinct:** "For each recipe, check if I can make it — are all its ingredients available?" But an ingredient might be *another recipe* you haven't confirmed yet. So you'd recurse: to know if `sandwich` is makeable, first find out if `bread` is makeable. That's a can-I-make-this(x) function with memoization. It works — but it's the recursive framing, and it's easy to get tangled on cycles (you need an "in progress" marker to avoid infinite loops).
- **Where it hurts:** the recursion is fine, but flip the question around and it gets *cleaner*. Instead of pulling — "what does this recipe need?" — think about pushing: **"I have `flour`. Which recipes does that unlock?"** Every time a supply becomes available, it satisfies one requirement for the recipes that list it. When a recipe's requirements all get satisfied, it's done — and now *it* becomes an available ingredient that can unlock further recipes.
- **The leap:** this is exactly **counting down dependencies**. Give each recipe a counter: how many ingredients it's still waiting on (its **indegree**). Seed a queue with everything already available — the `supplies`. Pop an available item, and for every recipe that needs it, tick its counter down by one. The instant a counter hits zero, that recipe is makeable — record it, and drop it into the queue too, because it's now an ingredient others can use. This is **Kahn's algorithm** — topological sort by BFS.
- **Pattern trigger:** **"things depend on other things, resolve in dependency order, and cycles must be excluded"** → **topological sort**. The tell that it's *Kahn's BFS* specifically rather than DFS: you're processing in waves outward from what's already known, and — beautifully — **cycles fall out for free**. A recipe stuck in a cycle never has its indegree reach zero, so it simply never enters the queue. No special cycle check needed.

---

## ① Brute Force

Repeatedly sweep all recipes; each pass, mark any recipe whose ingredients are all currently available (a supply or an already-made recipe). Keep looping until a full pass makes nothing new.

```python
def find_all_recipes_brute(recipes, ingredients, supplies):
    available = set(supplies)          # what we can currently obtain
    made = []
    changed = True
    while changed:                     # keep sweeping until a pass adds nothing
        changed = False
        for r, need in zip(recipes, ingredients):
            if r in available:
                continue               # already makeable, skip
            if all(item in available for item in need):
                available.add(r)       # unlocked it
                made.append(r)
                changed = True         # something changed → sweep again
    return made
```

**Why it's the natural first attempt:** it mirrors real cooking. Look at everything you have, make whatever you now can, then look again — maybe the thing you just made unlocks something else. Loop until nothing new appears.

**Why it's not enough:** it *works* and it correctly excludes cycles (a cycled recipe never becomes fully available, so it's never added). But it's wasteful. Each outer pass re-scans **every** recipe and re-checks **every** ingredient, even recipes that haven't changed at all. In the worst case — a chain where each pass unlocks just one recipe — you do `O(n)` passes over `O(n)` recipes each re-checking all their ingredients: roughly `O(n × total_ingredients)`. On the recursive/re-scan version this is the "loop until stable" trap. We're re-doing settled work every round.

**Complexity:** Time `O(n × E)` where `E` is total ingredients (up to `n` sweeps), Space `O(E)`.

---

## ② Optimised Solution

Same idea — resolve in dependency order — but stop re-scanning. Build the graph **once**, then let each satisfied ingredient *push* an update only to the recipes that actually care. This is **Kahn's topological sort (BFS)**.

Two structures:
- `children[item]` — for each ingredient, the list of recipes that need it. (Edge: ingredient → recipe.)
- `indegree[recipe]` — how many ingredients that recipe is still waiting on.

Seed the queue with every supply (all immediately available). Pop, satisfy, decrement, and enqueue any recipe that hits zero.

```python
from collections import defaultdict, deque

def find_all_recipes(recipes, ingredients, supplies):
    # ingredient -> recipes that require it
    children = defaultdict(list)
    indegree = defaultdict(int)

    recipe_set = set(recipes)
    for r, need in zip(recipes, ingredients):
        for item in need:
            children[item].append(r)   # item unlocks recipe r
        indegree[r] = len(need)        # r waits on this many ingredients

    # start from everything we already have
    queue = deque(supplies)
    made = []

    while queue:
        item = queue.popleft()         # this ingredient is now available
        for r in children[item]:       # every recipe that needed it
            indegree[r] -= 1           # one requirement satisfied
            if indegree[r] == 0:       # all requirements met → makeable
                made.append(r)
                queue.append(r)        # r is now an ingredient too
    return made
```

**Walk the example** `recipes = ["bread","sandwich"]`, `ingredients = [["yeast","flour"],["bread","meat"]]`, `supplies = ["yeast","flour","meat"]`:

Build phase — `indegree = {bread: 2, sandwich: 2}`, and `children`:

| ingredient | unlocks |
|---|---|
| `yeast` | `bread` |
| `flour` | `bread` |
| `bread` | `sandwich` |
| `meat` | `sandwich` |

Now Kahn's BFS. Queue starts `[yeast, flour, meat]`:

| Pop | Recipes it unlocks | indegree after | Hit 0? → made & enqueued |
|---|---|---|---|
| `yeast` | `bread` | bread: 2→1 | no |
| `flour` | `bread` | bread: 1→0 | **yes** → `made=[bread]`, queue += `bread` |
| `meat` | `sandwich` | sandwich: 2→1 | no |
| `bread` | `sandwich` | sandwich: 1→0 | **yes** → `made=[bread,sandwich]`, queue += `sandwich` |
| `sandwich` | (nothing) | — | queue empty → done |

Result `["bread","sandwich"]`. ✅ Notice `bread` had to be *made* before it could unlock `sandwich` — the queue handled that ordering automatically.

**Why it's correct:** `indegree[r]` is exactly the number of `r`'s ingredients not yet available. We decrement it precisely once per ingredient, the moment that ingredient becomes available — and an ingredient only enters the queue when it's a genuine supply or a fully-made recipe. So `indegree[r]` reaches 0 **iff** every one of `r`'s ingredients is obtainable, which is the definition of makeable. Cycles are excluded for free: if `a` needs `b` and `b` needs `a`, neither ever loses its last dependency, both indegrees stay ≥ 1, and neither is enqueued or reported. Same for a recipe needing an ingredient that's neither a supply nor makeable — that requirement is never satisfied, so its indegree never bottoms out. Each edge (ingredient→recipe) is processed exactly once.

**Complexity:** Time `O(V + E)` — `V` = supplies + recipes, `E` = total ingredients — so `O(E)` overall. Space `O(V + E)` for the graph and queue.

---

## ③ Space Optimization

**Already optimal — and here's the honest why.** The graph *is* the input, re-expressed. You must record, for every ingredient, which recipes depend on it — that's `O(E)` edges, and `E` is the size of `ingredients` itself. You can't answer the question without at least reading every (recipe, ingredient) pair once, and Kahn's stores each such pair as one adjacency entry. The `indegree` map is `O(n)` (one counter per recipe) and the queue holds at most `V` items over its lifetime. There's no rolling-window or in-place trick, because the dependencies point every which way — a recipe can be needed by many others and can itself need many — so nothing collapses to `O(1)`.

```python
# No lighter variant exists: the adjacency graph is O(E), and E is the input size.
# indegree is O(n), the queue is bounded by O(V). Reading every ingredient once
# is unavoidable, so O(V + E) is the floor, not overhead we chose.
```

**Complexity:** Time `O(V + E)`, Space `O(V + E)` (input-bound; nothing extra to shave).

> Say it out loud: *"Space is O(V + E), but that's the dependency graph — I have to look at every ingredient at least once to answer the question, so this is the floor, not waste."*

---

## Java (for Java interviewers)

```java
public List<String> findAllRecipes(String[] recipes, List<List<String>> ingredients, String[] supplies) {
    // ingredient -> recipes that require it
    Map<String, List<String>> children = new HashMap<>();
    Map<String, Integer> indegree = new HashMap<>();

    for (int i = 0; i < recipes.length; i++) {
        String r = recipes[i];
        List<String> need = ingredients.get(i);
        indegree.put(r, need.size());               // r waits on this many ingredients
        for (String item : need) {
            children.computeIfAbsent(item, k -> new ArrayList<>()).add(r);
        }
    }

    // seed the queue with everything we already have
    Queue<String> queue = new ArrayDeque<>(Arrays.asList(supplies));
    List<String> made = new ArrayList<>();

    while (!queue.isEmpty()) {
        String item = queue.poll();                 // now available
        for (String r : children.getOrDefault(item, Collections.emptyList())) {
            indegree.put(r, indegree.get(r) - 1);   // one requirement satisfied
            if (indegree.get(r) == 0) {             // all met → makeable
                made.add(r);
                queue.add(r);                       // r is now an ingredient too
            }
        }
    }
    return made;
}
```

---

## Complexity Summary

| Approach | Time | Space |
|---|---|---|
| Brute force (loop until stable) | O(n · E) | O(E) |
| Optimised (Kahn's topo BFS) | O(V + E) | O(V + E) |
| Space-optimised | — (none exists) | O(V + E), input-bound |

*(V = supplies + recipes, E = total ingredients across all recipes.)*

---

## Say it out loud (interview narration)

> *"Recipes can depend on other recipes, arbitrarily deep, and those dependencies can even cycle — so this is dependency resolution, which means a graph and a topological sort. I'll build edges ingredient → recipe, and give each recipe an indegree: how many ingredients it's still waiting on. Then Kahn's BFS: seed a queue with all the supplies since those are free, pop an item, and for every recipe that needed it, decrement its indegree. When one hits zero, it's makeable — I record it and push it back into the queue, because now it's an ingredient other recipes can use. The elegant part is cycles need no special handling: a recipe stuck in a cycle never loses its last dependency, so its indegree never reaches zero and it's naturally excluded. Time and space are O(V + E) — I have to read every ingredient once, so that's the floor."*

Before you code, ask the clarifying question that shows you spotted the trap: *"Can a recipe depend on another recipe, and can those dependencies form a cycle?"* Asking that up front is exactly the General Cognitive Ability signal Google rewards — it proves you saw why this is a graph and not a one-pass scan.

## Related / follow-ups
- **Course Schedule (LC 207)** — the canonical cycle-detection topo sort: *can* you finish all courses (is the graph a DAG)?
- **Course Schedule II (LC 210)** — same, but return a valid ordering — Kahn's BFS output order directly.
- **Alien Dictionary (LC 269)** — build the dependency graph from clues first, then topo sort — the harder Google favorite.
- **Parallel Courses (LC 1136)** — topo sort with *levels* (min semesters) — Kahn's BFS processed wave by wave.
